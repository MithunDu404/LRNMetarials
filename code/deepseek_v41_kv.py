"""DeepSeek-V4.1-Flash: the KV-cache arithmetic, from the published configuration.

Standard library only.  Every number printed here is either
  (a) taken directly from the DeepSeek-V4.1-Flash technical report, or
  (b) derived from the report's published model configuration (Section 4.2.1).

Where a derived number does not exactly match the paper's headline figure, the
script says so rather than fudging the inputs.  Run:  python code/deepseek_v41_kv.py
"""

# ---------------------------------------------------------------------------
# Published configuration (DeepSeek-V4.1-Flash tech report, Section 4.2.1)
# ---------------------------------------------------------------------------
LAYERS = 40                # total transformer layers
ENC_LAYERS = 20            # causal encoder
DEC_LAYERS = 20            # decoder
SWA_ONLY = 2               # first two layers: sliding-window attention only
WIN = 128                  # SWA window size, in tokens
TOP_K = 512                # main-KV entries selected per query
IDX_BLOCKS = 2048          # hierarchical indexer: blocks kept
IDX_BLOCK_SIZE = 8         # positions per block
CAND_POOL = IDX_BLOCKS * IDX_BLOCK_SIZE     # candidate positions

# Reported headline numbers
GLOBAL_KV_BYTES_V41 = 890  # bytes/token, always resident in HBM
RATIO_VS_V4_FLASH = 4      # "roughly 1/4 of DeepSeek-V4-Flash"
RATIO_VS_V1 = 437          # "approximately 437-fold reduction vs DeepSeek-V1"
PERSIST_RATIO_VS_V4 = 8    # persistent (SSD/host) cache: "roughly 1/8"


def layer_map():
    """Rebuild the per-layer CSA2 mode assignment described in Section 4.2.1.

    Encoder: 2 SWA-only layers, then 18 CSA2 layers (compression rate 2) in
             3 groups of 6 -> [Full, Reuse x5].
    Decoder: 20 CSA2 layers (compression rate 1) in 5 groups of 4.
             Group 1 -> [Full, Reuse x3];  groups 2-5 -> [Reindex, Reuse x3].
    """
    layers = []
    for _ in range(SWA_ONLY):
        layers.append(("encoder", "SWA-only", 0))
    for g in range(3):                                  # 3 groups of 6 = 18
        layers.append(("encoder", "Full", 2))
        layers += [("encoder", "Reuse", 2)] * 5
    for g in range(5):                                  # 5 groups of 4 = 20
        layers.append(("decoder", "Full" if g == 0 else "Reindex", 1))
        layers += [("decoder", "Reuse", 1)] * 3
    assert len(layers) == LAYERS, len(layers)
    return layers


def section(n, title):
    print(f"\n{n}. {title}")
    print("-" * (len(title) + 4))


# ---------------------------------------------------------------------------
print("DeepSeek-V4.1-Flash  |  KV cache arithmetic from the published config")
print("=" * 70)

section(1, "LAYER MAP: who actually stores a KV cache?")
lm = layer_map()
modes = {}
for part, mode, _ in lm:
    modes[mode] = modes.get(mode, 0) + 1
for mode in ("SWA-only", "Full", "Reindex", "Reuse"):
    print(f"   {mode:<10} {modes.get(mode, 0):>3} layers")
csa2 = LAYERS - modes["SWA-only"]
full = modes["Full"]
print(f"   -> of {csa2} CSA2 layers, only {full} compute their own main KV "
      f"({100 * full / csa2:.0f}%); {100 * modes['Reuse'] / csa2:.0f}% are pure Reuse")
print(f"   -> a plain transformer would store {csa2} layers of KV, V4.1 stores {full}: "
      f"{csa2 / full:.1f}x fewer")

section(2, "GLOBAL KV CACHE ACROSS GENERATIONS (reported, Figure 1b)")
v1 = GLOBAL_KV_BYTES_V41 * RATIO_VS_V1
v4f = GLOBAL_KV_BYTES_V41 * RATIO_VS_V4_FLASH
for name, b in (("DeepSeek-V1", v1), ("DeepSeek-V4-Flash", v4f),
                ("DeepSeek-V4.1-Flash", GLOBAL_KV_BYTES_V41)):
    print(f"   {name:<22} {b:>9,.0f} bytes/token")
print(f"   V1 -> V4.1 reduction: {v1 / GLOBAL_KV_BYTES_V41:.0f}x")
print("   (V1 and V4-Flash are back-computed from the paper's stated ratios.)")

section(3, "WHAT 890 BYTES/TOKEN BUYS YOU AT 1M TOKENS")
ctx = 1_000_000
HBM_GB = 192.0            # one large HBM module, for scale
for name, b in (("DeepSeek-V1", v1), ("DeepSeek-V4-Flash", v4f),
                ("DeepSeek-V4.1-Flash", GLOBAL_KV_BYTES_V41)):
    gb = b * ctx / 1e9
    share = 100 * gb / HBM_GB
    concurrent = HBM_GB / gb
    print(f"   {name:<22} {gb:>8.1f} GB   = {share:>6.1f}% of a {HBM_GB:.0f} GB HBM module"
          f"   -> {concurrent:>6.1f} such contexts fit")
print("   -> the global cache must stay in HBM, so this ratio is literally how")
print("      many 1M-token conversations one memory module can serve at once.")

section(4, "THREE MULTIPLICATIVE DIMENSIONS (the paper's own framing)")
print("   Baseline: every layer keeps its own uncompressed BF16 KV entry.")
dims = [
    ("entry size   ", "MLA-style shared latent instead of per-head K,V", None),
    ("precision    ", "FP4 main KV instead of FP8 (V4)", 2.0),
    ("sequence dim ", "encoder compression rate 2 (1 entry per 2 tokens)", 2.0),
    ("layer dim    ", f"only {full} of {csa2} layers keep main KV", csa2 / full),
]
prod = 1.0
for label, how, factor in dims:
    if factor is None:
        print(f"   {label}  {how}")
    else:
        prod *= factor
        print(f"   {label}  {how:<48} x{factor:>5.1f}")
print(f"   product of the three quantified dimensions: {prod:.0f}x")
print("   NOTE: this is not the paper's 4x figure and is not meant to be. The 4x")
print("   compares V4.1-Flash against V4-Flash, which had already paid for the")
print("   entry-size and sequence dimensions. These factors are relative to a")
print("   plain per-layer BF16 cache.")

section(5, "HIERARCHICAL SPARSE INDEXER: positions scored per query")
print(f"   candidate pool = {IDX_BLOCKS} blocks x {IDX_BLOCK_SIZE} positions "
      f"= {CAND_POOL:,} positions")
print(f"   final selection per layer = top-{TOP_K} entries")
print(f"   {'context':>12} {'flat indexer':>14} {'hierarchical':>14} {'saving':>9}")
index_layers = modes["Full"] + modes["Reindex"]   # layers that run an indexer
for n in (4_000, 32_000, 128_000, 1_000_000):
    # every indexing layer scores the whole causally visible range ...
    flat = index_layers * n
    # ... vs: the first Full layer scans everything, the rest scan the pool only
    hier = n + (index_layers - 1) * min(CAND_POOL, n)
    print(f"   {n:>12,} {flat:>14,} {hier:>14,} {flat / hier:>8.1f}x")
print("   -> deeper indexers become O(1) in context length, not O(n).")
print("      The first Full-mode layer still scans the full range: that is the")
print("      residual term that stops decode cost being perfectly flat.")

section(6, "SWA BOUNDED REPLAY: replay cost vs exact reconstruction")
exact_enc = LAYERS * WIN
exact_dec = (DEC_LAYERS) * WIN
print(f"   SWA window = {WIN} tokens, layers = {LAYERS}")
print(f"   exact reconstruction needs L x win  = {exact_enc:,} tokens replayed")
print(f"   bounded replay needs        win     = {WIN:,} tokens replayed")
print(f"   -> {exact_enc / WIN:.0f}x less recomputation, at the cost of an")
print("      approximate (not bit-identical) SWA state")
print(f"   decoder-side exact reconstruction would need (L/2) x win = {exact_dec:,} tokens")

section(7, "WHY RECOMPUTE BEATS FETCHING (order-of-magnitude model)")
# Deliberately crude: we only need the sign of the comparison, not its size.
SSD_LATENCY_US = 100.0        # NVMe read latency, microseconds (typical)
SSD_BW_GBPS = 7.0            # per-drive sequential read, GB/s
GPU_TFLOPS = 1000.0         # BF16-class dense throughput, TFLOP/s (order of magnitude)
HIDDEN = 5120
ACTIVE_PARAMS_PREFILL = 8e9

swa_bytes = WIN * LAYERS * 2 * HIDDEN * 1        # FP8 SWA KV, both K and V
fetch_us = SSD_LATENCY_US + (swa_bytes / (SSD_BW_GBPS * 1e9)) * 1e6
flops = 2 * ACTIVE_PARAMS_PREFILL * WIN          # 2*N*tokens for a forward pass
recompute_us = (flops / (GPU_TFLOPS * 1e12)) * 1e6
print(f"   replaying {WIN} tokens through an 8B-active forward pass:")
print(f"     work        = {flops / 1e12:.2f} TFLOP  ->  ~{recompute_us:.0f} us of GPU time")
print(f"   fetching the same SWA state from SSD:")
print(f"     bytes       = {swa_bytes / 1e6:.1f} MB  ->  ~{fetch_us:.0f} us "
      f"(latency + bandwidth)")
verdict = "recompute" if recompute_us < fetch_us else "fetch"
print(f"   -> cheaper option: {verdict}  "
      f"({max(fetch_us, recompute_us) / min(fetch_us, recompute_us):.1f}x)")
print("   NOTE: an order-of-magnitude argument with assumed hardware constants,")
print("   not a measurement. It shows why the trade-off exists, not its exact size.")
print(f"   NOTE: {recompute_us:.0f} us is milliseconds, not the 'microseconds' the")
print("   video claims. The direction of the trade-off is right; the margin is")
print("   narrower than it was presented, which is why the paper calls this a")
print("   'new storage-computation trade-off' rather than a free win.")

section(8, "PREFILL SAVING FROM THE ENCODER/DECODER SPLIT")
print(f"   {'prompt':>10} {'all 40 layers':>15} {'CED (20 + replay)':>19} {'saving':>9}")
for n in (1_000, 10_000, 100_000, 1_000_000):
    plain = LAYERS * n
    ced = ENC_LAYERS * n + DEC_LAYERS * WIN
    print(f"   {n:>10,} {plain:>15,} {ced:>19,} {100 * (1 - ced / plain):>8.1f}%")
print("   -> layer-tokens of work. The decoder only ever sees the last 128 tokens")
print("      during prefill, so the split saves almost exactly half.")

section(9, "ENGRAM: memory that does not live on the GPU")
ENGRAM_PARAMS = 196e9
ENGRAM_MODULES = 2
HASH_HEADS = 8
NGRAM_ORDERS = (2, 3, 4)
TABLE_ENTRIES = 16e6
print(f"   {ENGRAM_PARAMS / 1e9:.0f}B Engram parameters, split evenly over "
      f"{ENGRAM_MODULES} modules (layers 1 and 14)")
print(f"   n-gram orders {NGRAM_ORDERS}, {HASH_HEADS} hash heads, "
      f"~{TABLE_ENTRIES / 1e6:.0f}M entries per head, FP8")
print(f"   stored in HOST memory: {ENGRAM_PARAMS * 1 / 1e9:.0f} GB at FP8, "
      f"prefetched over RDMA")
print(f"   backbone is {552 / (552 + 196) * 100:.0f}% of the {552 + 196}B total; "
      f"Engram is the other {196 / (552 + 196) * 100:.0f}%")
print("   -> parameters you look facts up in, not parameters you think with.")

print("\n" + "=" * 70)
print("Sources: DeepSeek-V4.1-Flash technical report, Sections 2.1-2.5, 3.2, 4.2.1.")
print("Derived figures are labelled; assumed constants are labelled.")
