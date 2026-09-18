"""Multi-head Latent Attention (MLA) vs standard multi-head attention, in NumPy.

Shows three things:
  1. MLA caches one small latent per token instead of full keys/values for every head.
  2. The 'absorb the up-projection' identity holds exactly (without RoPE).
  3. How many numbers each scheme stores per token.
"""
import numpy as np

rng = np.random.default_rng(0)
d_model, n_heads, d_head, d_latent, n_tokens = 256, 8, 32, 48, 10

def softmax(x):
    x = x - x.max(-1, keepdims=True); e = np.exp(x); return e / e.sum(-1, keepdims=True)

X = rng.normal(size=(n_tokens, d_model))                       # token representations entering the layer

# ---------------- MLA parameters
W_DKV = rng.normal(0, 0.1, (d_latent, d_model))                # shared down-projection  x -> latent c
W_UK = rng.normal(0, 0.1, (n_heads, d_head, d_latent))         # per-head key up-projection   c -> k
W_UV = rng.normal(0, 0.1, (n_heads, d_head, d_latent))         # per-head value up-projection c -> v
W_Q = rng.normal(0, 0.1, (n_heads, d_head, d_model))           # per-head query projection

# ---------------- generation loop: cache ONLY the latent c
latent_cache = []
outputs_naive, outputs_absorbed = [], []
for t in range(n_tokens):
    x = X[t]
    latent_cache.append(W_DKV @ x)                             # the only thing we store
    C = np.stack(latent_cache)                                 # (t+1, d_latent)

    heads_naive, heads_absorbed = [], []
    for h in range(n_heads):
        q = W_Q[h] @ x
        # (a) naive: decompress keys and values for every cached token, then attend
        K = C @ W_UK[h].T; V = C @ W_UV[h].T
        a = softmax(K @ q / np.sqrt(d_head))
        heads_naive.append(a @ V)
        # (b) absorbed: q·(W_UK c) = (W_UKᵀ q)·c  and  Σ a_j W_UV c_j = W_UV (Σ a_j c_j)
        q_latent = W_UK[h].T @ q                               # query moved into latent space
        a2 = softmax(C @ q_latent / np.sqrt(d_head))
        heads_absorbed.append(W_UV[h] @ (a2 @ C))
    outputs_naive.append(np.concatenate(heads_naive))
    outputs_absorbed.append(np.concatenate(heads_absorbed))

print("absorbed version identical to naive version:",
      np.allclose(outputs_naive, outputs_absorbed))

# ---------------- what gets cached per token, per layer
mha = 2 * n_heads * d_head
gqa = 2 * (n_heads // 4) * d_head
mqa = 2 * d_head
mla = d_latent
print(f"numbers cached per token  MHA={mha}  GQA(4)={gqa}  MQA={mqa}  MLA={mla}")

# ---------------- the real DeepSeek-V3/R1 numbers
L, H, dh, latent, rope, fp16 = 61, 128, 128, 512, 64, 2
mha_b = 2 * H * dh * L * fp16
mla_b = (latent + rope) * L * fp16
print(f"DeepSeek-R1: MHA {mha_b/1e6:.2f} MB/token, MLA {mla_b/1e3:.1f} KB/token, ratio {mha_b/mla_b:.1f}x")
print(f"100K-token context: MHA {mha_b*1e5/1e9:.0f} GB, MLA {mla_b*1e5/1e9:.1f} GB")
