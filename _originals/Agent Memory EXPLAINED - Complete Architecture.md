# Agent Memory Explained — Complete Architecture

## What Long-Term Memory Is (and Isn't)

The starting point is a basic fact about LLMs: they are stateless. When you send a prompt, the model processes it and returns a completion, but it retains nothing afterward. If you send a second prompt, it has no recollection of the first exchange unless you explicitly include that history again.

This is why **conversational memory** exists. It is handled by the agent scaffold/harness, not by long-term memory systems. The mechanism is simple: every time you send a message, the harness appends your message and the LLM's response to a running history it keeps in its own state. When you send the next message, that new message is added to the same history, and the *entire* history is sent back to the LLM again. This is how an agent appears to "remember" things said earlier in the same conversation — because the whole conversation is being resent each time.

The catch is that conversational memory is scoped to a single conversation. If you start a brand-new conversation, none of what was discussed in the old one carries over, because it lives in a different context.

**Long-term memory** solves this by introducing a separate service that stores information across *every* conversation, not just the current one. On each turn, the agent checks this long-term memory store to recall relevant facts about the user or about itself, and those facts are independent of — and persist beyond — the conversational history.

Some architectural principles for long-term memory:
- It must be **external** to the conversation/session store — not saved in the same place as session data — so that it persists across sessions.
- Because it can be centered on the user rather than on a single agent, the **same memory store can be shared across multiple different agents/assistants** (e.g., one person's preferences and current projects could be shared between ChatGPT, Claude, Pi, etc., rather than being duplicated per assistant).
- Ideally, the agent should have tools to explicitly explore its own memory, and/or ingestion and retrieval should happen automatically on every turn or at least after every conversation.

The rest of the lesson explores these ideas concretely through **Mem0**, a popular existing long-term memory implementation.

## Mem0's Storage Architecture

Mem0 relies on three separate stores.

### 1. Main Memory Store (Vector Store)

This holds the actual memories themselves — short sentences or paragraphs such as "the user prefers vegan restaurants" — along with metadata attached to each memory:

- **Date created/updated** — when the memory was made or last modified.
- **Owner** — whether the memory belongs to the user or to the agent (e.g., a fact about the user's preferences vs. something the agent learned about a procedure or about current events).
- **Hash of the memory** — used specifically for deduplication.
- **Lemmatized version of the memory text** — used for keyword search later in retrieval.
- **Expiration date**.
- **Attribution** — which agent created the memory, relevant when multiple agents share the same memory store.

This store is a vector database, so the memory content itself is embedded for semantic search.

### 2. Entity Store (Entity Memory)

Mem0 extracts named entities — places, proper names, people, etc. — from the memories in the main store and stores them in a *second* vector database. In this store, each point/entry is an entity rather than a full memory, and each entity's metadata links it to the one or more main memories that mention it.

Example: if a memory says "my favorite neighborhood in Paris is Marais," the entities extracted are "Marais" and "Paris." Later, if a query is about Paris, the entity store surfaces the "Paris" entity, which is linked back to that memory — helping retrieval find it even by entity association rather than pure semantic similarity.

### 3. SQLite Database

This serves two purposes:
- **Logging/history** — it tracks the history of all changes made to the vector stores.
- **Short-term rolling buffer** — it keeps the **10 most recent messages** sent into the ingestion pipeline. This recent context is important for the LLM extraction step to resolve ambiguous references (pronouns) in new messages — for example, if a new message says "it is great" or "he's really good at this," the extractor needs the last few messages to know what "it" or "he" refers to.

## Ingestion: How New Memories Get Created

Ingestion runs after every agent turn: once the agent finishes producing a response, the messages from that turn are sent into the ingestion pipeline.

There are **three ways** messages can become memories:

1. **Procedural memory** — summarizes the process or sequence of actions/tool calls the agent took, so that in the future the exact procedure can be retrieved and reproduced. Useful for remembering *how* something was done, including which tools were called and what results came back. The speaker notes this approach isn't heavily used anymore, since you can often just extract things directly from a conversation transcript with better results.
2. **`infer = false`** — the input messages are embedded and inserted directly into the database as-is, with no transformation.
3. **`infer = true`** — this triggers the more sophisticated **LLM-based extraction pipeline**, which is the focus of the lesson.

### The LLM Extraction Pipeline (infer = true)

When `infer` is set to true, incoming messages go through the following steps:

**Step 1 — Load recent context.** Because extraction is performed by an LLM that must output a structured JSON of memories, the LLM needs a carefully constructed prompt containing several pieces of context, not just the raw messages:

- **Role**: the LLM is framed as a "memory extractor."
- **User summary**: a summary of who the user is.
- **The input messages** themselves (the new turn being processed).
- **Recent memories**: memories that were recently saved to the database.
- **Relevant memories**: found by flattening the new messages into a single string, embedding that string, and searching the main vector database for related existing memories — these are appended to the context too.
- **Last 10 messages**: pulled from the SQLite rolling buffer, used to disambiguate pronouns and references in the new messages (as discussed above).
- **Conversation date and current date**.

**Step 2 — LLM produces structured output.** Given all that context, the LLM outputs a JSON structure representing the extracted memory. Example: from a conversation, it might extract "the user prefers vegan restaurants" as a memory.

**Step 3 — Save into the main memory store.** The new memory gets:
- A creation/update date.
- An owner tag (user vs. agent).
- A hash, checked against existing hashes for **deduplication**. The speaker notes this is a fairly weak deduplication method, since exact-hash matching only catches memories that are worded identically — near-duplicates with different phrasing won't be caught.
- A lemmatized version of the text, stored for future keyword search.

The message is also logged into the SQLite database to update the rolling 10-message buffer.

**On model choice**: the LLM extraction step can be handled by a small model since extraction is a relatively simple task. Mem0 reportedly uses GPT-5 mini by default, but the speaker emphasizes this can be swapped for a small open-source model and run locally for free.

## Retrieval: How Relevant Memories Are Found

Retrieval means finding memories relevant to whatever is currently being discussed, and it happens in two scenarios:

1. **Explicit retrieval** — exposed to the agent as a tool (e.g., a "search memory database" tool) that the agent can invoke with a query whenever it decides it needs to look something up.
2. **Automatic retrieval** — triggered on every agent turn automatically: the system finds relevant memories for the incoming message and appends them to the LLM's context before generating a response, without the agent needing to explicitly ask.

Both paths use the **same retrieval pipeline** underneath.

### Retrieval Inputs

- **Query** — typically the user's message itself. The speaker notes this is a good point to insert *query rewriting* (using a small LLM to reformulate the query for better retrieval), but Mem0 does not do this by default — it would need to be implemented on the harness side.
- **Top K** — how many memories should ultimately be returned (e.g., top 10).
- **Threshold** — a minimum score a memory needs to be included in results.
- **Identity** — whose memory is being searched: the user's, the agent's, or the specific run's. This matters because agent-owned memories (things it learned about the world, procedures) are conceptually different from user-owned memories (preferences, past experiences).

### Retrieval Steps

**Step 1 — Embed the query**, using the same embedding model that was used to build the vector database in the first place.

**Step 2 — Semantic vector search (nearest neighbors)** against the main vector store. This is where Top K comes in, but not directly: rather than fetching exactly K results, the search retrieves a **larger candidate pool** to allow for reranking, since reranking works better over a bigger pool. The pool size is computed as `max(top_k × 4, 60)` — so if Top K is 10, the initial vector search actually returns 60 candidate memories. Crucially, the two reranking steps that follow can only *reorder/reweight* this pool — they cannot introduce new memories that weren't in the original 60.

**Step 3 — Keyword matching score.** The query is lemmatized (and recall that every stored memory already has its lemmatized form saved in metadata from ingestion). The lemmatized query is compared against the lemmatized memories using **BM25** to measure word overlap, producing a score normalized to a **0–1** range.

**Step 4 — Entity boost.** Entities are extracted from the query, and the entity database is searched for matches. Each matched entity is linked to one or more memories (as established in the entity store design). Only the memories that are both (a) linked to a matched entity and (b) already present in the initial 60-candidate pool receive this boost — this produces a score in the **0–5** range roughly translating to up to 0.5 on the same normalized scale used elsewhere.

The scoring logic here has a deliberate intuition: **the fewer memories an entity is linked to, the higher the boost score for those memories.** If "Paris" is linked to a thousand memories, matching that entity isn't very informative — it doesn't narrow things down much, so the score contribution is low. But if "Paris" is linked to only two memories, matching that entity strongly suggests those two memories are what's being asked about, so they get a much higher boost score (closer to the 0.5 ceiling).

### Combining Scores

Each candidate memory in the pool ends up with three separate scores:
- Vector similarity score: range 0–1
- Keyword (BM25) matching score: range 0–1
- Entity boost score: range 0–0.5

These three are **summed** (max possible total = 2.5) and then **divided by 2.5** to normalize back into a 0–1 final score. Memories are ranked by this combined score, and the actual **Top K** are selected and returned to the agent or user.

The overall takeaway on retrieval is that it's meaningfully more complex than ingestion, blending pure semantic similarity with keyword overlap and an entity-linkage signal that rewards specificity.

## Recommendations for Building This Yourself Locally

For anyone wanting to replicate this system entirely with open-source, locally-run models (e.g., browsing Hugging Face models):

- **Extraction model**: since extraction is a relatively simple structured task, a small model suffices — in the range of roughly **1B to 12B parameters**. The speaker advises not going below 1B unless the model is fine-tuned specifically for this task to preserve accuracy. Example candidates mentioned: Llama models, Qwen (specifically suggesting something like **Qwen3 8B** as a good balance).
- **Embedding models**: filter Hugging Face by "feature extraction" to find embedding models. The speaker recommends checking a reputable embedding benchmark/leaderboard to compare models — including benchmarks broken out by use case, such as multilingual, English-only, or domain-specific benchmarks (the example given is a medical-domain embedding benchmark).
- **Fine-tuning**: for long-term, serious local deployments, the speaker recommends fine-tuning your own small models for both extraction and embeddings, since this improves performance specifically for the memory-extraction task and makes running everything locally more viable.

Mem0 by default uses closed/hosted models (e.g., GPT-5 mini for extraction), but every component — extraction LLM and embedding model — can be swapped for open-source equivalents and run entirely on local hardware.

---

Source: [Agent Memory EXPLAINED - Complete Architecture](https://youtu.be/aYfZN8t6AQs?si=bPe1Ajxv2XXRtMYF) — Hugging Face
