"""Demos for 'AI Engineering 9 - Customising Models' (target/ai/).
1. LoRA trainable-parameter counts for an 8B-class transformer.
2. The DPO loss on toy log-probabilities.
3. GRPO's group-relative advantages.
numpy only.  Run:  py -3.12 code/ai_lora_dpo_grpo.py
"""
import numpy as np

# ---------------------------------------------------------------- 1. LoRA parameter counts
def lora_params(shapes, r):
    return sum(r * (d_in + d_out) for d_in, d_out in shapes)

def demo_lora():
    d, kv, ff, layers = 4096, 1024, 14336, 32          # Llama-3-8B-like shapes (assumed)
    per_layer = [(d, d), (d, kv), (d, kv), (d, d),     # q, k, v, o projections
                 (d, ff), (d, ff), (ff, d)]           # gate, up, down (MLP)
    full_linear = layers * sum(a * b for a, b in per_layer)
    for r in (8, 16, 64):
        n = layers * lora_params(per_layer, r)
        print(f"rank {r:>2}: {n/1e6:6.1f}M trainable params = {n / 8.03e9:.2%} of an 8.03B model "
              f"({n / full_linear:.2%} of its linear-layer weights)")
    print(f"full fine-tune memory, ~16 bytes/param (weights+grads+Adam states): {8.03e9 * 16 / 1e9:.0f} GB")

# ---------------------------------------------------------------- 2. DPO loss
def dpo_loss(pol_chosen, ref_chosen, pol_rejected, ref_rejected, beta=0.1):
    margin = (pol_chosen - ref_chosen) - (pol_rejected - ref_rejected)
    return -np.log(1 / (1 + np.exp(-beta * margin))), margin

def demo_dpo():
    for label, args in [("start (policy = reference)", (-14.0, -14.0, -13.0, -13.0)),
                        ("after some training", (-12.0, -14.0, -15.0, -13.0)),
                        ("wrong direction", (-16.0, -14.0, -11.0, -13.0))]:
        loss, m = dpo_loss(*args)
        print(f"{label:28s} margin {m:+5.1f} -> loss {loss:.3f}")

# ---------------------------------------------------------------- 3. GRPO advantages
def grpo_advantages(rewards):
    r = np.asarray(rewards, float); s = r.std()
    return np.zeros_like(r) if s == 0 else (r - r.mean()) / s

def demo_grpo():
    for rewards in ([1, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]):
        print(f"rewards {rewards} -> advantages {np.round(grpo_advantages(rewards), 2).tolist()}")

if __name__ == "__main__":
    for d in (demo_lora, demo_dpo, demo_grpo):
        print(f"--- {d.__name__}"); d()
