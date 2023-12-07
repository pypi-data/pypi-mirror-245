from math import ceil, log2

import torch
from torch import nn, Tensor, einsum
from torch.nn import Module, ModuleList
import torch.nn.functional as F
from torch.cuda.amp import autocast

from torchtyping import TensorType

from beartype import beartype
from beartype.typing import Tuple, Callable, Optional

from einops import rearrange, repeat, reduce, pack, unpack
from einops.layers.torch import Rearrange

from x_transformers import Decoder
from x_transformers.attend import Attend
from x_transformers.autoregressive_wrapper import (
    eval_decorator,
    top_k,
    top_p,
)

from vector_quantize_pytorch import (
    ResidualVQ,
    ResidualLFQ
)

from ema_pytorch import EMA

from torch_geometric.nn.conv import SAGEConv

from tqdm import tqdm

# helper functions

def exists(v):
    return v is not None

def default(v, d):
    return v if exists(v) else d

def divisible_by(num, den):
    return (num % den) == 0

def l1norm(t):
    return F.normalize(t, dim = -1, p = 1)

# tensor helper functions

@beartype
def discretize_coors(
    t: Tensor,
    *,
    continuous_range: Tuple[float, float],
    num_discrete: int = 128
) -> Tensor:
    lo, hi = continuous_range
    assert hi > lo

    t = (t - lo) / (hi - lo)
    t *= num_discrete
    t -= 0.5

    return t.round().long().clamp(min = 0, max = num_discrete - 1)

@beartype
def undiscretize_coors(
    t: Tensor,
    *,
    continuous_range = Tuple[float, float],
    num_discrete: int = 128
) -> Tensor:
    lo, hi = continuous_range
    assert hi > lo

    t = t.float()

    t += 0.5
    t /= num_discrete
    return t * (hi - lo) + lo

@beartype
def gaussian_blur_1d(
    t: Tensor,
    *,
    sigma: float = 1.
) -> Tensor:

    _, channels, _, device = *t.shape, t.device

    width = int(ceil(sigma * 5))
    width += (width + 1) % 2
    half_width = width // 2

    distance = torch.arange(-half_width, half_width + 1, dtype = torch.float, device = device)

    gaussian = torch.exp(-(distance ** 2) / (2 * sigma ** 2))
    gaussian = l1norm(gaussian)

    kernel = repeat(gaussian, 'n -> c 1 n', c = channels)
    return F.conv1d(t, kernel, padding = half_width, groups = channels)

@beartype
def scatter_mean(
    tgt: Tensor,
    indices: Tensor,
    src = Tensor,
    *,
    dim: int = -1,
    eps: float = 1e-5
):
    num = tgt.scatter_add(dim, indices, src)
    den = torch.zeros_like(tgt).scatter_add(dim, indices, torch.ones_like(src))
    return num / den.clamp(min = eps)

# resnet block

class Block(Module):
    def __init__(self, dim, groups = 8):
        super().__init__()
        self.proj = nn.Conv1d(dim, dim, 3, padding = 1)
        self.norm = nn.GroupNorm(groups, dim)
        self.act = nn.SiLU()

    def forward(self, x, mask = None):
        if exists(mask):
            x = x.masked_fill(~mask, 0.)

        x = self.proj(x)

        if exists(mask):
            x = x.masked_fill(~mask, 0.)

        x = self.norm(x)
        x = self.act(x)
        return x

class ResnetBlock(Module):
    def __init__(
        self,
        dim,
        *,
        groups = 8
    ):
        super().__init__()
        self.block1 = Block(dim, groups = groups)
        self.block2 = Block(dim, groups = groups)

    def forward(
        self,
        x,
        mask = None
    ):
        h = self.block1(x, mask = mask)
        h = self.block2(h, mask = mask)
        return h + x

# main classes

class MeshAutoencoder(Module):
    @beartype
    def __init__(
        self,
        dim,
        num_discrete_coors = 128,
        coor_continuous_range: Tuple[float, float] = (-1., 1.),
        dim_coor_embed = 64,
        encoder_depth = 2,
        decoder_depth = 2,
        dim_codebook = 192,
        num_quantizers = 2,           # or 'D' in the paper
        codebook_size = 16384,        # they use 16k, shared codebook between layers
        use_residual_lfq = True,      # whether to use the latest lookup-free quantization
        rq_kwargs: dict = dict(),
        commit_loss_weight = 0.1,
        bin_smooth_blur_sigma = 0.4,  # they blur the one hot discretized coordinate positions
        pad_id = -1
    ):
        super().__init__()

        self.num_discrete_coors = num_discrete_coors
        self.coor_continuous_range = coor_continuous_range

        self.coor_embed = nn.Embedding(num_discrete_coors, dim_coor_embed)
        self.project_in = nn.Linear(dim_coor_embed * 9, dim)

        self.encoders = ModuleList([])

        for _ in range(encoder_depth):
            sage_conv = SAGEConv(dim, dim)

            self.encoders.append(sage_conv)

        self.codebook_size = codebook_size
        self.num_quantizers = num_quantizers

        self.project_dim_codebook = nn.Linear(dim, dim_codebook * 3)

        if use_residual_lfq:
            assert log2(codebook_size).is_integer()

            self.quantizer = ResidualLFQ(
                dim = dim_codebook,
                num_quantizers = num_quantizers,
                codebook_size = codebook_size,
                commitment_loss_weight = 1.,
                **rq_kwargs
            )
        else:
            self.quantizer = ResidualVQ(
                dim = dim_codebook,
                num_quantizers = num_quantizers,
                codebook_size = codebook_size,
                shared_codebook = True,
                commitment_weight = 1.,
                **rq_kwargs
            )

        self.pad_id = pad_id # for variable lengthed faces, padding quantized ids will be set to this value

        self.project_codebook_out = nn.Linear(dim_codebook * 3, dim)

        self.decoders = ModuleList([])

        for _ in range(decoder_depth):
            resnet_block = ResnetBlock(dim)
            self.decoders.append(resnet_block)

        self.to_coor_logits = nn.Sequential(
            nn.Linear(dim, num_discrete_coors * 9),
            Rearrange('... (v c) -> ... v c', v = 9)
        )

        # loss related

        self.commit_loss_weight = commit_loss_weight
        self.bin_smooth_blur_sigma = bin_smooth_blur_sigma

    @beartype
    def encode(
        self,
        *,
        vertices:         TensorType['b', 'nv', 3, int],
        faces:            TensorType['b', 'nf', 3, int],
        face_edges:       TensorType['b', 2, 'e', int],
        face_edges_mask:  TensorType['b', 'e', bool],
        return_face_coordinates = False
    ):
        """
        einops:
        b - batch
        nf - number of faces
        nv - number of vertices (3)
        c - coordinates (3)
        d - embed dim
        """

        batch, num_vertices, num_coors, device = *vertices.shape, vertices.device
        _, num_faces, _ = faces.shape

        faces_vertices = repeat(faces, 'b nf nv -> b nf nv c', c = num_coors)
        vertices = repeat(vertices, 'b nv c -> b nf nv c', nf = num_faces)

        face_coords = vertices.gather(-2, faces_vertices)
        face_coords = rearrange(face_coords, 'b nf nv c -> b nf (nv c)') # 9 coordinates per face

        face_embed = self.coor_embed(face_coords)
        face_embed = rearrange(face_embed, 'b nf c d -> b nf (c d)')

        face_embed = self.project_in(face_embed)

        face_embed = rearrange(face_embed, 'b nf d -> (b nf) d')

        # handle variable lengths by creating a padding node
        # padding for edges will refer to this node

        pad_node_id = face_embed.shape[0]
        face_embed = F.pad(face_embed, (0, 0, 0, 1), value = 0.)

        batch_arange = torch.arange(batch, device = device)
        batch_offset = batch_arange * num_faces
        batch_offset = rearrange(batch_offset, 'b -> b 1 1')

        face_edges = face_edges + batch_offset

        face_edges = face_edges.masked_fill(~face_edges_mask, pad_node_id)
        face_edges = rearrange(face_edges, 'b ij e -> ij (b e)')

        for conv in self.encoders:
            face_embed = conv(face_embed, face_edges)

        face_embed = face_embed[:-1] # remove padding node
        face_embed = rearrange(face_embed, '(b nf) d -> b nf d', b = batch)

        if not return_face_coordinates:
            return face_embed

        return face_embed, face_coords

    @beartype
    def quantize(
        self,
        *,
        faces: TensorType['b', 'nf', 3, int],
        face_mask: TensorType['b', 'n', bool],
        face_embed: TensorType['b', 'nf', 'd', float],
        pad_id = None
    ):
        pad_id = default(pad_id, self.pad_id)
        batch, num_faces, device = *faces.shape[:2], faces.device

        max_vertex_index = faces.amax()
        num_vertices = int(max_vertex_index.item() + 1)

        face_embed = self.project_dim_codebook(face_embed)
        face_embed = rearrange(face_embed, 'b nf (nv d) -> b nf nv d', nv = 3)

        vertex_dim = face_embed.shape[-1]
        faces_with_dim = repeat(faces, 'b nf nv -> b nf nv d', d = vertex_dim)

        vertices = torch.zeros((batch, num_vertices, vertex_dim), device = device)

        # create pad vertex, due to variable lengthed faces

        pad_vertex_id = num_vertices
        vertices = F.pad(vertices, (0, 0, 0, 1), value = 0.)

        faces = faces.masked_fill(~rearrange(face_mask, 'b n -> b n 1'), pad_vertex_id)

        # prepare for scatter mean

        faces_with_dim = rearrange(faces_with_dim, 'b ... d -> b (...) d')
        face_embed = rearrange(face_embed, 'b ... d -> b (...) d')

        # scatter mean

        averaged_vertices = scatter_mean(vertices, faces_with_dim, face_embed, dim = -2)

        # residual VQ

        quantized, codes, commit_loss = self.quantizer(averaged_vertices)

        # gather quantized vertexes back to faces for decoding
        # now the faces have quantized vertices

        face_embed_output = quantized.gather(-2, faces_with_dim)
        face_embed_output = rearrange(face_embed_output, 'b (nf nv) d -> b nf (nv d)', nv = 3)

        face_embed_output = self.project_codebook_out(face_embed_output)

        # vertex codes also need to be gathered to be organized by face sequence
        # for autoregressive learning

        faces_with_quantized_dim = repeat(faces, 'b nf nv -> b (nf nv) q', q = self.num_quantizers)
        codes_output = codes.gather(-2, faces_with_quantized_dim)

        # make sure codes being outputted have this padding

        face_mask = repeat(face_mask, 'b nf -> b (nf nv) 1', nv = 3)
        codes_output = codes_output.masked_fill(~face_mask, self.pad_id)

        # output quantized, codes, as well as commitment loss

        return face_embed_output, codes_output, commit_loss

    @beartype
    def decode(
        self,
        quantized: TensorType['b', 'n', 'd', float],
        face_mask:  TensorType['b', 'n', bool]
    ):
        quantized = rearrange(quantized, 'b n d -> b d n')
        face_mask = rearrange(face_mask, 'b n -> b 1 n')

        x = quantized

        for resnet_block in self.decoders:
            x = resnet_block(x, mask = face_mask)

        return rearrange(x, 'b d n -> b n d')

    @beartype
    @torch.no_grad()
    def decode_from_codes_to_faces(
        self,
        codes: Tensor,
        face_mask: Optional[TensorType['b', 'n', bool]] = None,
        return_discrete_codes = False
    ):
        codes = rearrange(codes, 'b ... -> b (...)')

        if not exists(face_mask):
            face_mask = reduce(codes != self.pad_id, 'b (nf nv q) -> b nf', 'all', nv = 3, q = self.num_quantizers)

        # handle different code shapes

        codes = rearrange(codes, 'b (n q) -> b n q', q = self.num_quantizers)

        # decode

        quantized = self.quantizer.get_output_from_indices(codes)
        quantized = rearrange(quantized, 'b (nf nv) d -> b nf (nv d)', nv = 3)

        face_embed_output = self.project_codebook_out(quantized)

        decoded = self.decode(
            face_embed_output,
            face_mask = face_mask
        )

        pred_face_coords = self.to_coor_logits(decoded)
        pred_face_coords = pred_face_coords.argmax(dim = -1)

        pred_face_coords = rearrange(pred_face_coords, '... (v c) -> ... v c', v = 3)

        # back to continuous space

        continuous_coors = undiscretize_coors(
            pred_face_coords,
            num_discrete = self.num_discrete_coors,
            continuous_range = self.coor_continuous_range
        )

        if not return_discrete_codes:
            return continuous_coors

        return continuous_coors, pred_face_coords

    @torch.no_grad()
    def tokenize(self, *args, **kwargs):
        assert 'return_codes' not in kwargs
        self.eval()
        return self.forward(*args, return_codes = True, **kwargs)

    @beartype
    def forward(
        self,
        *,
        vertices: TensorType['b', 'nv', 3, float],
        faces: TensorType['b', 'nf', 3, int],
        face_edges: TensorType['b', 2, 'ij', int],
        face_len: TensorType['b', int],
        face_edges_len: TensorType['b', int],
        return_codes = False,
        return_loss_breakdown = False
    ):
        num_faces, num_face_edges, device = faces.shape[1], face_edges.shape[-1], faces.device

        face_mask = torch.arange(num_faces, device = device) < rearrange(face_len, 'b -> b 1')
        face_edges_mask = torch.arange(num_face_edges, device = device) < rearrange(face_edges_len, 'b -> b 1')

        discretized_vertices = discretize_coors(
            vertices,
            num_discrete = self.num_discrete_coors,
            continuous_range = self.coor_continuous_range,
        )

        encoded, face_coordinates = self.encode(
            vertices = discretized_vertices,
            faces = faces,
            face_edges = face_edges,
            face_edges_mask = face_edges_mask,
            return_face_coordinates = True
        )

        quantized, codes, commit_loss = self.quantize(
            face_embed = encoded,
            faces = faces,
            face_mask = face_mask
        )

        if return_codes:
            return codes

        decode = self.decode(
            quantized,
            face_mask = face_mask
        )

        pred_face_coords = self.to_coor_logits(decode)

        # prepare for recon loss

        pred_face_coords = rearrange(pred_face_coords, 'b ... c -> b c (...)')
        face_coordinates = rearrange(face_coordinates, 'b ... -> b 1 (...)')

        # reconstruction loss on discretized coordinates on each face
        # they also smooth (blur) the one hot positions, localized label smoothing basically

        with autocast(enabled = False):
            pred_log_prob = pred_face_coords.log_softmax(dim = 1)

            target_one_hot = torch.zeros_like(pred_log_prob).scatter(1, face_coordinates, 1.)

            if self.bin_smooth_blur_sigma >= 0.:
                target_one_hot = gaussian_blur_1d(target_one_hot, sigma = self.bin_smooth_blur_sigma)

            # cross entropy with localized smoothing

            recon_loss = (-target_one_hot * pred_log_prob).sum(dim = 1).mean()

        # calculate total loss

        total_loss = recon_loss + \
                     commit_loss.sum() * self.commit_loss_weight

        if not return_loss_breakdown:
            return total_loss

        loss_breakdown = (recon_loss, commit_loss)

        return recon_loss, loss_breakdown

class MeshTransformer(Module):
    @beartype
    def __init__(
        self,
        autoencoder: MeshAutoencoder,
        *,
        dim = 512,
        max_seq_len = 8192,
        attn_num_tokens = 128 ** 2,
        attn_depth = 12,
        attn_dim_head = 64,
        attn_heads = 16,
        attn_kwargs: dict = dict(
            ff_glu = True,
            num_mem_kv = 4
        ),
        pad_id = -1
    ):
        super().__init__()

        self.autoencoder = autoencoder
        self.codebook_size = autoencoder.codebook_size
        self.num_quantizers = autoencoder.num_quantizers

        self.sos_token = nn.Parameter(torch.randn(dim))
        self.eos_token_id = self.codebook_size

        # they use axial positional embeddings

        assert divisible_by(max_seq_len, 3 * self.num_quantizers) # 3 vertices per face, with D codes per vertex

        self.token_embed = nn.Embedding(self.codebook_size + 1, dim)

        self.quantize_level_embed = nn.Parameter(torch.randn(self.num_quantizers, dim))
        self.vertex_embed = nn.Parameter(torch.randn(3, dim))

        self.abs_pos_emb = nn.Embedding(max_seq_len, dim)

        self.max_seq_len = max_seq_len

        # main autoregressive attention network

        self.decoder = Decoder(
            dim = dim,
            depth = attn_depth,
            dim_head = attn_dim_head,
            heads = attn_heads,
            **attn_kwargs
        )

        self.to_logits = nn.Linear(dim, self.codebook_size + 1)

        self.pad_id = pad_id

    @property
    def device(self):
        return next(self.parameters()).device

    @eval_decorator
    @torch.no_grad()
    @beartype
    def generate(
        self,
        prompt: Optional[Tensor] = None,
        batch_size: Optional[int] = None,
        filter_logits_fn: Callable = top_k,
        filter_kwargs: dict = dict(),
        temperature = 1.,
        return_codes = False
    ):
        if exists(prompt):
            assert not exists(batch_size)

            prompt = rearrange(prompt, 'b ... -> b (...)')
            assert prompt.shape[-1] <= self.max_seq_len

            batch_size = prompt.shape[0]

        batch_size = default(batch_size, 1)

        codes = default(prompt, torch.empty((batch_size, 0), dtype = torch.long, device = self.device))

        curr_length = codes.shape[-1]

        for i in tqdm(range(curr_length, self.max_seq_len)):
            can_eos = divisible_by(i + 1, self.num_quantizers * 3)  # only allow for eos to be decoded at the end of each face, defined as 3 vertices with D residusl VQ codes

            logits = self.forward(codes, return_loss = False, append_eos = False)
            logits = logits[:, -1]

            if not can_eos:
                logits[:, -1] = -torch.finfo(logits.dtype).max

            filtered_logits = filter_logits_fn(logits, **filter_kwargs)
            probs = F.softmax(filtered_logits / temperature, dim = -1)

            sample = torch.multinomial(probs, 1)
            codes, _ = pack([codes, sample], 'b *')

        if return_codes:
            codes = codes[:, 1:] # remove sos
            codes = rearrange(codes, 'b (n q) -> b n q', q = self.num_quantizers)
            return codes

        self.autoencoder.eval()
        return self.autoencoder.decode_from_codes_to_faces(codes)

    def forward_from_raw_face_data(
        self,
        *,
        vertices:       TensorType['b', 'nv', 3, int],
        faces:          TensorType['b', 'nf', 3, int],
        face_edges:     TensorType['b', 2, 'e', int],
        face_len:       TensorType['b', int],
        face_edges_len: TensorType['b', int],
        **kwargs
    ):
        codes = self.autoencoder.tokenize(
            vertices = vertices,
            faces = faces,
            face_edges = face_edges,
            face_len = face_len,
            face_edges_len = face_edges_len
        )

        return self.forward(codes, **kwargs)

    def forward(
        self,
        codes = None,
        return_loss = True,
        append_eos = False,
        code_lens: Optional[Tensor] = None  # needed for inserting eos automatically for variable lengthed meshes
    ):
        if codes.ndim > 2:
            codes = rearrange(codes, 'b ... -> b (...)')

        # get some variable

        batch, seq_len, device = *codes.shape, codes.device

        assert seq_len <= self.max_seq_len, f'received codes of length {seq_len} but needs to be less than or equal to set max_seq_len {self.max_seq_len}'

        # auto append eos token

        if append_eos:
            code_lens = default(code_lens, torch.full((batch, 1), seq_len, device = device))
            codes = F.pad(codes, (0, 1), value = 0)

            batch_arange = torch.arange(batch, device = device)
            batch_arange = rearrange(batch_arange, '... -> ... 1')

            codes[batch_arange, code_lens] = self.eos_token_id

        # if returning loss, save the labels for cross entropy

        if return_loss:
            assert seq_len > 0
            codes, labels = codes[:, :-1], codes

        # token embed (each residual VQ id)

        codes = codes.masked_fill(codes == self.pad_id, 0)
        codes = self.token_embed(codes)

        # codebook embed + absolute positions

        seq_arange = torch.arange(codes.shape[-2], device = device)

        codes = codes + self.abs_pos_emb(seq_arange)

        # embedding for quantizer level

        code_len = codes.shape[1]

        level_embed = repeat(self.quantize_level_embed, 'q d -> (r q) d', r = ceil(code_len / self.num_quantizers))
        codes = codes + level_embed[:code_len]

        # embedding for each vertex

        vertex_embed = repeat(self.vertex_embed, 'nv d -> (r nv q) d', r = ceil(code_len / (3 * self.num_quantizers)), q = self.num_quantizers)
        codes = codes + vertex_embed[:code_len]

        # auto prepend sos token

        sos = repeat(self.sos_token, 'd -> b d', b = batch)
        codes, _ = pack([sos, codes], 'b * d')

        # attention

        attended = self.decoder(codes)

        # logits

        logits = self.to_logits(attended)

        if not return_loss:
            return logits

        # loss

        ce_loss = F.cross_entropy(
            rearrange(logits, 'b n c -> b c n'),
            labels,
            ignore_index = self.pad_id
        )

        return ce_loss
