"""Causal multi-head self-attention in plain NumPy (GPT-style), with sanity checks."""
import numpy as np

def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)          # numerical stability
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

class MultiHeadSelfAttention:
    def __init__(self, d_model, n_heads, seed=0):
        assert d_model % n_heads == 0
        rng = np.random.default_rng(seed)
        self.h, self.d_k = n_heads, d_model // n_heads
        s = 1 / np.sqrt(d_model)
        self.W_Q = rng.normal(0, s, (d_model, d_model))  # all heads' W_Q stacked together
        self.W_K = rng.normal(0, s, (d_model, d_model))
        self.W_V = rng.normal(0, s, (d_model, d_model))  # all heads' "value-down"
        self.W_O = rng.normal(0, s, (d_model, d_model))  # "value-up" of all heads = output matrix

    def split(self, x):                                   # (n, d_model) -> (heads, n, d_k)
        n = x.shape[0]
        return x.reshape(n, self.h, self.d_k).transpose(1, 0, 2)

    def __call__(self, E):
        n = E.shape[0]
        Q, K, V = self.split(E @ self.W_Q.T), self.split(E @ self.W_K.T), self.split(E @ self.W_V.T)
        scores = Q @ K.transpose(0, 2, 1) / np.sqrt(self.d_k)       # (heads, n, n)
        future = np.triu(np.ones((n, n), dtype=bool), k=1)          # True above the diagonal
        scores = np.where(future, -1e9, scores)                     # mask BEFORE softmax
        A = softmax(scores, axis=-1)                                # each row sums to 1
        out = A @ V                                                 # weighted sum of values
        out = out.transpose(1, 0, 2).reshape(n, -1)                 # concatenate heads
        delta_E = out @ self.W_O.T                                  # project back up
        return E + delta_E, A                                       # residual: E + ΔE

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    n_tokens, d_model, n_heads = 6, 64, 8
    E = rng.normal(size=(n_tokens, d_model))
    attn = MultiHeadSelfAttention(d_model, n_heads)
    E_new, A = attn(E)
    print("output shape:", E_new.shape, "  attention shape:", A.shape)
    print("rows sum to 1:", np.allclose(A.sum(-1), 1))
    print("no looking ahead (upper triangle ~0):", np.abs(np.triu(A, 1)).max() < 1e-12)
    # Causality check: changing the LAST token must not change any earlier output
    E2 = E.copy(); E2[-1] += 10.0
    E2_new, _ = attn(E2)
    print("earlier tokens unaffected by a future change:", np.allclose(E_new[:-1], E2_new[:-1]))
    print("head 0 attention pattern:\n", np.round(A[0], 2))
