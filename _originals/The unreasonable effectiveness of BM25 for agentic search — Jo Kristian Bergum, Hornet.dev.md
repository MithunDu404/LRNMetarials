# The Unreasonable Effectiveness of BM25 for Agentic Search

## Speaker and Context

Jo Kristian Bergum, CEO of Vespa/Hornet.dev (referred to in the talk as "Hornet"), has worked on search and retrieval problems for over 20 years. His company builds retrieval infrastructure specifically for agents. The talk's core argument is that BM25 — a roughly 30-year-old lexical scoring function — is making a strong comeback in the era of agentic search, not because the algorithm changed, but because the *user* of search has changed.

## Defining Agentic Search

Bergum defines agentic search as **search that happens inside an agent loop**. An agent is trying to accomplish some task (writing code, doing deep research, etc.), and to do that task successfully it has an information need that must be satisfied along the way.

Building a good agentic search system requires three components:

1. **A capable model** — one that can use tools and formulate queries well.
2. **A harness** — the way the retrieval/search functions are exposed to the model. This could be classic tool calling, or what Bergum calls "code mode" (referencing another speaker, Edo, who demonstrated exposing retrieval infrastructure this way at the same event).
3. **A retrieval engine** — something that can perform search efficiently, potentially over billion-scale document sets.

## What BM25 Actually Is

BM25 stands for **Best Match 25**. The name comes from the fact that researchers ran many different scoring experiments, and experiment number 25 was the one that performed best — hence the name stuck.

Mechanically, BM25 is a **scoring function**: given a query and a document, it computes a score from the interaction between query terms and document terms, and that score is used as a proxy for how relevant the document is to the query.

The naive way to use it is to score every document in the corpus against the query and pick the top K. Decades of information retrieval research (30-40 years) have gone into accelerating this top-K retrieval process without changing the underlying scoring function itself. Bergum notes that BM25 the *formula* hasn't changed — what has changed is the environment it's being used in.

## Why BM25 Is Resurging: The New, More Powerful User

The key insight of the talk is that BM25 hasn't gotten better — the *user issuing the queries* has. That user is now often an LLM rather than a human, and LLMs bring:

- **General knowledge**: LLMs know about entities, companies, dates, and other real-world facts. This implicit parametric knowledge lets them formulate much better search queries than a typical human would.
- **Speed and volume**: an LLM can issue far more queries, far faster, than a human typing at a keyboard.

Historically, BM25 was treated purely as a **baseline** — every information retrieval paper would report a BM25 score, then show that some fancier neural or embedding-based method beat it. Evaluation used to mean: a human looks at "10 blue links," scans them, and some metric is computed from that. Bergum argues this style of evaluation is becoming less relevant, because an agent doesn't behave like a human doing a single-shot query — it can reformulate, expand, and issue many queries in a trajectory.

## BrowseComp-Plus: A Benchmark Case Study

Bergum highlights **BrowseComp-Plus**, a deep research benchmark published the prior year, as one of his favorite benchmarks.

- It contains almost exactly 830 questions.
- The questions are riddle-like — Bergum compares them to pub quiz questions — and are fairly long.
- The corpus is small by web standards: about 100,000–105,000 web documents.
- The harness is deliberately simple: the model is given one tool, `search`, which takes a query string and returns snippets.
- Each question has a golden reference answer, so end-to-end accuracy (does the full model+harness+retriever loop produce the correct answer?) can be measured directly.

### Why Retrieval Still Matters: The Floppy Disk Analogy

Bergum draws an analogy between context windows and floppy disks (a nostalgic reference to installing games from floppies in the 1980s). A single floppy disk held about 1.4 megabytes. He estimates that current models start degrading in quality somewhere around 350,000 tokens of context — in his framing, that's "one floppy disk" worth of usable context.

This is why retrieval matters: you need a mechanism to fetch only the relevant information and place it into that limited "floppy disk" of context. BrowseComp-Plus demonstrates this concretely: it shows how retrieval quality directly affects end-to-end task accuracy.

**The experiment**: 
- If you artificially stuff the *correct evidence documents* directly into the model's context window (bypassing retrieval entirely), accuracy on these riddle-like questions is very high — even for a model like GPT-4. This shows that **reasoning is not the bottleneck**; given the right evidence, the model can answer correctly.
- But if you instead give the model a search tool and make it retrieve the evidence itself, accuracy drops substantially. The result now depends on the harness — specifically, on the model's ability to formulate good queries *and* on the quality of the retriever behind the tool.

Bergum draws a broader conclusion from this: even if models eventually become perfect or AGI-level and stop making mistakes, they will still be bounded by a context window roughly the size of a floppy disk. So retrieval remains relevant regardless of how capable the underlying model becomes, because something still has to decide what gets loaded into that limited window.

### Search Trajectories

Within BrowseComp-Plus, answering one riddle-like question becomes a **search trajectory**: the model issues a query, gets a response, reads it, reformulates the query, and repeats — continuing until either it fills up the context window or it finds the answer, whichever happens first.

Bergum and his team studied these trajectories to see how GPT-5 formulates queries, and wrote up findings in a blog post on hornet.dev.

### Comparing LLM Queries to Human Queries (AOL Query Log)

To contextualize how LLMs search differently from humans, Bergum references the **AOL query log** — a large sample of real user search queries that AOL accidentally published publicly. Human queries in that log (and in more recent logs Bergum has seen) are typically short, just a few terms.

GPT-5, by contrast, behaves like a much more powerful searcher:
- It can write long, elaborate queries in one shot.
- It uses search syntax and operators it has learned from web search conventions — e.g., the `site:` operator, exact phrase matching, and similar constructs.

This constitutes a genuinely new kind of query workload compared to what BM25 systems were historically tuned against.

### The Parameter Pitfall: "Which BM25 Do You Mean?"

BM25 has two key hyperparameters that control aspects of its scoring behavior. Because BM25 is usually treated as a throwaway baseline, papers (including the original BrowseComp-Plus paper) often don't tune it carefully. Bergum notes that when you look at the BrowseComp-Plus paper's own BM25 baseline, it performs terribly compared to fancier techniques like embedding models — which seems to support the "BM25 is obsolete" narrative.

However, more recent research shows that the hyperparameters used in that paper's BM25 baseline were poorly suited to the long documents in the benchmark. Once tuned properly, BM25's relative standing improves dramatically. This is the basis for Bergum's recurring rhetorical question: **"Which BM25 do you mean?"** — implementation and parameter choices matter enormously, and a poorly configured BM25 is not representative of what a properly configured one can do.

## Why BM25 Is Well-Suited to This New, More Powerful User

Bergum lists three reasons BM25 pairs well with LLM-driven search:

1. **Exact matching is still valuable.** LLMs know precise entities — names, zip codes, SKUs, etc. These are hard to represent well with an embedding model, which compresses all tokens into a fixed-size vector over a fixed vocabulary, potentially losing exactness. BM25's literal term matching handles this naturally.
2. **It's cheap.** This is especially true compared to embedding-based retrieval, where some embedding models have billions of parameters (he mentions models around 8 billion parameters) and require standing up dedicated inference infrastructure just to encode text. BM25 has no such inference cost.
3. **Tooling is mature and results are explainable.** The ecosystem around BM25 is well developed and readily available. Just as importantly, because BM25 matches on literal terms and phrases, it's easy for the model to *inspect* why a particular query returned particular results — which helps the model reformulate queries intelligently in the next step of its trajectory.

## Combining BM25 with Grep-Like Tools: Dynamic Workspace Expansion

Bergum highlights a recent paper from Jimmy Lin's group at the University of Waterloo — a group he praises for its strong work in both classical information retrieval and agentic search — titled **"Scaling Direct Corpus Interaction via Dynamic Workspace Expansion."**

### The Scenario

Imagine building web-search infrastructure for agents (something multiple companies, including ones Bergum's team works with, are actively doing). At web scale you may have billions of documents — far too many to fit in any context window, so retrieval (with BM25 as a strong baseline) is necessary just to narrow things down.

### The Idea: A Workspace as a Filesystem

The output of retrieval can be thought of as a **search engine results page (SERP) for agents**. Instead of just returning snippets directly into the prompt, you place the retrieved documents into a **workspace organized as a file system**.

This unlocks the same "progressive disclosure" pattern used elsewhere in agent tooling (skills, etc.):
- The model is first shown lightweight information — a document's title plus a small snippet.
- If the model decides it needs more, it can choose to read further into that specific document.
- To do this "reading more," the model uses the same primitive tools it's already very good at using as a coding agent — things like `grep`, `ripgrep`, `sed`, `bash`, and general filesystem navigation. Bergum notes that everyone in the audience, as users of coding agents, has already seen these tools used this way to manage context.

### Why This Combination Is Powerful

This approach combines two previously separate infrastructure worlds: sandbox/virtual-filesystem infrastructure and retrieval infrastructure. Bergum finds this exciting because it lets an agentic search system exploit both retrieval algorithms *and* filesystem-navigation tools at once.

He also frames this as a deliberate **hack that rides the grain of what current frontier models are already optimized for**. Every frontier LLM lab is currently investing heavily in making their models better at coding, bash usage, and tool use. By building your agentic search system on top of that same trajectory (files, grep, bash), your retrieval system automatically gets better every time model vendors improve these core coding/tool-use capabilities — you're borrowing from a capability curve that's already being pushed hard for other reasons. He speculates that eventually, if/when AGI arrives, agents might just use a browser directly instead — but for now, this filesystem-plus-retrieval hybrid is a very effective way to build agentic search infrastructure.

## Evaluation Is Changing Too

Traditional information retrieval evaluation assumed a single query producing a single ranked list, scored with a metric like NDCG (normalized discounted cumulative gain), and then compared across systems. Bergum argues this framework is largely obsolete for agentic search: because the new "user" (the agent) can reformulate queries, issue many of them, and expand searches dynamically, judging quality by a single query's ranked list no longer captures what matters.

Instead, evaluation should focus on **whether the model can successfully perform the end task it was set** — for example, in question-answering, whether it gets the final answer right, rather than whether any single intermediate ranked list looks good by classical metrics.

## Hornet's Bet: Efficient BM25 Infrastructure

Hornet is explicitly betting on BM25 as one of its core retrieval primitives, and the company has set out to build the best and most efficient implementation of BM25 available, precisely because Bergum sees it as such a strong fundamental primitive for this new agentic search era.

He shows a benchmark chart comparing several anonymized search engines against Hornet, all running on the same hardware, indexing 100 million web documents on a single node. Hornet's implementation shows substantially better performance (lower latency, i.e., the y-axis, which he corrects himself on mid-talk — initially saying QPS, then clarifying it's actually latency) than the competing engines at the same throughput. For companies building web-search infrastructure for agents at scale, this kind of efficiency gain translates directly into significant infrastructure cost savings.

## Four Takeaways

1. **There's a new, more powerful user.** It types faster, reads faster, reformulates queries fluidly, and carries a large amount of general/world knowledge — and this combination makes even simple tools like grep and BM25 more effective than they were when the primary user was a human.
2. **"Which BM25 do you mean?"** Implementations differ meaningfully in performance and in the hyperparameters used, and those differences can dramatically swing benchmark outcomes (as seen with BrowseComp-Plus's originally mistuned baseline). Don't treat "BM25" as a single monolithic, already-understood quantity.
3. **BM25 is effective for agentic search primarily because it's explainable to the model** — the model can see literal term/phrase matches and understand why a result came back, which helps it decide how to reformulate its next query.
4. **BM25 pairs naturally with grep-like tools.** Since grep is also fundamentally about literal matching, combining BM25-based retrieval with filesystem/grep-style tools produces a strong, coherent agentic search/retrieval paradigm.

---

Source: [The unreasonable effectiveness of BM25 for agentic search — Jo Kristian Bergum, Hornet.dev](https://youtu.be/fZH97QHHYjY?si=3euDuUZAzRYEq6eJ) — AI Engineer
