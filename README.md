# Learnmat — Study Guides

Thirteen notes taken from YouTube talks, rewritten as self-contained study guides: every one has diagrams and plots, worked examples with real numbers, the engineering impact, runnable code, a self-quiz and a glossary.

**Almost every plot is computed, not drawn.** Simulations, benchmarks and formulas are run by the scripts in `figures/`, so the numbers on the charts are real. Anything illustrative (a toy model, an assumed cost) says so on the figure itself, and anything quoted from a talk is labelled "as reported".

**Written for a first reading, not a second one.** Every guide opens with **§0.1 "First, in completely plain words"** — the whole topic in ordinary language with an everyday analogy, before any jargon or notation appears. Equations are followed by a "how to read that out loud" line. Nothing is assumed except what the guide's §0 says is assumed.

**Every guide was re-verified on 18 September 2026**, and each one carries a `Facts re-checked` line at the top saying what changed since its source video. Where a field moved, the guide has a dedicated update section rather than a silent edit — see the table below.

---

## The guides

### Machine learning

| Guide | What you'll get out of it |
|---|---|
| [**Backpropagation from scratch**](Backpropagation%20-%20How%20Neural%20Networks%20Learn.md) | Derivatives → gradients → the chain rule → the backward pass, with a worked computational graph and a 60-line autograd engine you can run. Why one gradient costs ~3 forward passes no matter how many parameters you have. |
| [**Predictive coding: how the brain may learn instead**](Predictive%20Coding%20-%20How%20the%20Brain%20May%20Learn%20Instead.md) | Predictive coding as an energy-based model: local Hebbian rules, relaxation, clamping. The sequel to the backprop guide. |
| [**Attention in transformers**](Attention%20in%20Transformers%20-%20Queries%20Keys%20and%20Values.md) | Q/K/V built up from "what am I looking for?", attention patterns computed by a real head, why √d_k matters, masking, multi-head, and the quadratic cost of long context. |
| [**How DeepSeek rewrote the transformer (MLA)**](Multi-head%20Latent%20Attention%20-%20Shrinking%20the%20KV%20Cache.md) | The KV cache, why generation is memory-bound, and how MLA cuts the cache 57× by caching a learned latent instead of keys and values. Includes the RoPE catch the video skips. |
| [**DeepSeek-V4.1-Flash: pushing KV cache compression**](DeepSeek%20V4.1%20Flash%20-%20Extreme%20KV%20Cache%20Compression.md) | The sequel to the MLA note, worked through from the technical report. Half the model skips reading the prompt; only 4 of 38 layers keep a cache; short-term memory is deleted and recomputed because that's cheaper than fetching it. |

### AI engineering

| Guide | What you'll get out of it |
|---|---|
| [**Why the harness matters more than the model**](Agent%20Harnesses%20-%20Why%20the%20Scaffold%20Beats%20the%20Model.md) | Everything between the model and the world: context compilation, tools, memory hierarchy (L1/L2/L3), sub-agents, and harnesses that learn. With a working minimal harness. |
| [**Graph engineering for agents**](Graph%20Engineering%20-%20Agent%20Workflows%20as%20DAGs.md) | Jobs, arrows, state; cutting fake arrows for parallelism; the split→work→check→merge diamond; stop rules and human gates. With a real parallel graph runner. |
| [**Agent memory (Mem0 architecture)**](Agent%20Memory%20-%20Long-Term%20Memory%20with%20Mem0.md) | Why LLMs are stateless, what long-term memory actually stores, and a hybrid retrieval pipeline (vector + BM25 + entity boost) you can run and inspect. |
| [**BM25 for agentic search**](BM25%20-%20Keyword%20Search%20for%20AI%20Agents.md) | The BM25 formula explained piece by piece, why a smarter querier revives an old algorithm, and how parameter choices swing recall from 24% to 98%. |

### Backend and systems

| Guide | What you'll get out of it |
|---|---|
| [**System design explained**](System%20Design%20-%20APIs%20Databases%20Caching%20CDNs%20and%20Scaling.md) | One server → load balancers → replicas → cache → CDN, plus APIs, protocols, auth and security. 16 figures, including a load-balancer queueing simulation and consistent hashing measured. |
| [**8 API laws**](REST%20API%20Design%20-%20The%208%20Laws.md) | Resources vs actions, method semantics, status codes, one error shape, pagination, versioning. Includes a working API in pure Python that follows all eight. |
| [**1 million requests per second**](Scaling%20to%201%20Million%20Requests%20per%20Second.md) | The four walls: bandwidth, CPU per request, concurrency and memory. Why a query rewrite beat every hardware upgrade. |
| [**8 years of platform engineering (Atlassian)**](Platform%20Engineering%20-%20Lessons%20from%208%20Years%20at%20Atlassian.md) | Async provisioning, control plane vs data plane, immutable infrastructure, centralizing auth/rate limits at the edge — and why maintenance is the hard part. |

---

## What changed since the source videos (verified 18 September 2026)

The AI guides age fastest. These are the substantive updates, each written up inside the relevant guide rather than quietly patched in:

| Guide | What moved | Where |
|---|---|---|
| **DeepSeek MLA** | Biggest change of the set. DeepSeek-V3.2 (2025) added *sparse* attention on top of MLA; **DeepSeek-V4 (April 2026) replaced MLA altogether** with a compressed + sparse hybrid, and V4.1-Flash added a third compression dimension. MLA lives on in Kimi K2 and GLM-5.x | §7.5, and [its own guide](DeepSeek%20V4.1%20Flash%20-%20Extreme%20KV%20Cache%20Compression.md) |
| **Why the harness matters** | Nearly everything the talk claimed is now published and checkable: Prime Agent open-sourced with a paper, OpenJarvis shipped from Stanford, and the ARC Prize leaderboard now reports **the same model under two harnesses** — a gap of up to 80 points | §6.6.1, §7 |
| **BM25** | The talk's thesis was tested properly and held: tuned BM25 + a strong model reached **83.1%** on BrowseComp-Plus, beating dense-retriever agents. Includes the tuned parameter values | §5.3 |
| **Attention** | FlashAttention-4 (2026); the learned-sparse-attention family that made 1M-token context affordable; current GQA/MLA adoption | §9 |
| **Predictive coding** | "PC can't train deep networks" is now **out of date** — 128-layer and 1,000-layer results have since been published | §11.5 |
| **Agent memory** | Confirmed against Mem0's current algorithm, including why it only ever *adds* memories and what that means for stale facts | §4.4 |
| **8 API laws** | `Deprecation` is now **RFC 9745**; `Idempotency-Key` is **still not an RFC**, contrary to what the earlier version implied | §4.3, §8 |
| **System design** | **OWASP Top 10:2025** is the current edition (two new categories); PostgreSQL 18 shifts a few database defaults | §3.3, §12.1 |
| **1M requests/s** | UUIDv7 is standardized and now built into PostgreSQL 18 | §6.5 |
| **Graph engineering** | How much orchestration to hard-code, now that models plan well themselves | §9.1 |
| **Atlassian platform engineering** | Open Service Broker's Kubernetes home was retired; Operators and Crossplane are the modern equivalents of the same pattern | §3.1 |
| **Backpropagation** | Nothing. It's a 1970 algorithm that still works exactly as described — §10.6 says what moved *around* it | §10.6 |

---

## Suggested reading orders

**Understanding modern AI:** Backprop → Predictive coding → Attention → MLA → **V4.1-Flash** → Harness → Graph engineering → Agent memory → BM25

**Just the efficiency story (how LLMs got cheap to serve):** Attention §9 → MLA → V4.1-Flash. Three guides, one continuous argument, ending at 890 bytes per token.

**Becoming a better backend engineer:** System design → 8 API laws → 1M requests/s → Atlassian platform engineering

**Just curious:** read **§0.1** of any guide — that's the plain-language version of the whole topic, and it takes about two minutes — then look at the figures. Each guide also opens with a "how to use this" table for 10 minutes / 1 hour / a weekend.

---

## Repository layout

Every guide is named after **what it teaches**, not after the video it came from. The video title is always in the guide's `Source:` line, and the untouched original note is in `_originals/` under the video's own name.

```
*.md                     the thirteen study guides
figures/<topic>/         PNGs + the make_figs.py script that generates them
figures/_style.py        shared plotting style and drawing helpers
code/                    runnable examples referenced by the guides
_originals/              the original notes (video titles), plus source papers
```

Guide ↔ figure folder ↔ code file:

| Guide | Figures | Code |
|---|---|---|
| Backpropagation | `figures/backprop/` | `code/backprop_micrograd.py` |
| Predictive Coding | `figures/predictive_coding/` | *(in the guide)* |
| Attention in Transformers | `figures/attention/` | `code/attention_numpy.py` |
| Multi-head Latent Attention | `figures/deepseek_mla/` | `code/mla_numpy.py` |
| DeepSeek V4.1 Flash | `figures/deepseek_v41/` | `code/deepseek_v41_kv.py` |
| Agent Harnesses | `figures/agent_harness/` | `code/minimal_harness.py` |
| Graph Engineering | `figures/graph_engineering/` | `code/graph_runner.py` |
| Agent Memory | `figures/agent_memory/` | `code/agent_memory_mini.py` |
| BM25 | `figures/bm25/` | `code/bm25_search.py` |
| System Design | `figures/system_design/` | `code/system_design_demos.py` |
| REST API Design | `figures/api_design/` | `code/rest_api_server.py` |
| Scaling to 1M req/s | `figures/million_rps/` | `code/million_rps_math.py` |
| Platform Engineering | `figures/platform_engineering/` | `code/platform_patterns.py` |

### Regenerating the figures

Needs Python with `numpy`, `matplotlib` and `scipy`:

```bash
python figures/backprop/make_figs.py
```

Each topic folder has its own script; running it rewrites that topic's PNGs. The one exception is the predictive-coding script, which takes its output directory as an argument:

```bash
python figures/predictive_coding/make_figs.py figures/predictive_coding
```

### Running the code examples

Every example runs offline with no API keys. The two ML ones need `numpy`; the rest use only the standard library.

```bash
python code/backprop_micrograd.py      # autograd engine + gradient descent
python code/attention_numpy.py         # causal multi-head self-attention with checks
python code/mla_numpy.py               # MLA, and proof the "absorption" identity holds
python code/deepseek_v41_kv.py         # V4.1-Flash KV budgets, rebuilt from the published config
python code/bm25_search.py             # BM25 index, scoring, and hybrid fusion
python code/agent_memory_mini.py       # mini long-term memory with hybrid retrieval
python code/minimal_harness.py         # agent loop: tools, sub-agents, compaction, limits
python code/graph_runner.py            # parallel job graph with stop rules and a human gate
python code/rest_api_server.py         # REST API following the 8 laws (+ self-test)
python code/platform_patterns.py       # async broker, config validation, token bucket
python code/system_design_demos.py     # SQL injection, JWT, consistent hashing, LRU cache
python code/million_rps_math.py              # the arithmetic behind 1M requests/second
```

---

## A note on accuracy

Where a source made a factual slip, the guide **fixes it and says so** — for example the GPT-3 attention parameter count, the bit/byte mix-up in the 1M req/s notes, CORS being described as a CSRF defence, and Route 53's latency-based routing. Where a claim couldn't be verified (recent benchmark results, product names from auto-transcripts), it's marked "as reported" rather than presented as fact.

Three rules are applied consistently, so you can always tell what kind of statement you're reading:

- **Verified** claims name a primary source and a date (a paper, an RFC, an official leaderboard, a release).
- **"As reported"** means it came from the talk and could not be independently confirmed. Don't quote these without checking.
- **Figures** state their own status on the image: computed, measured, simulated, or an explicitly-labelled toy model with assumed inputs.

Where a source's claim has since become *false* rather than merely dated — the two clearest cases are "DeepSeek uses MLA" and "predictive coding can't go deep" — the guide says so in its own section rather than deleting the original claim, because knowing what changed is usually more instructive than the corrected fact on its own.
