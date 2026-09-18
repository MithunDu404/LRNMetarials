# Attention in Transformers, Step-by-Step

## Recap and Context

The model under study takes in a piece of text and predicts the next word. The input text is broken into **tokens** — usually words or pieces of words, though for simplicity this lesson treats every token as a full word.

The first step of a transformer converts each token into a high-dimensional vector called its **embedding**. The key idea to hold onto is that directions in this high-dimensional embedding space can carry semantic meaning. In the previous chapter, one example showed that a particular direction/step in the space could take you from the embedding of a masculine noun to the embedding of the corresponding feminine noun — that is, direction can encode something like gender. By analogy, many other directions in this space likely encode other aspects of meaning.

The purpose of a transformer is to progressively adjust these embeddings so that they stop representing just an isolated word and instead absorb much richer, contextual meaning. Attention is the mechanism that drives this contextual adjustment, and it commonly trips people up — that's expected, and the goal here is to build intuition before the matrix mechanics.

## Motivating Examples for What Attention Should Do

### The word "mole"
Consider three phrases: "American shrew mole," "one mole of carbon dioxide," and "take a biopsy of the mole." The word "mole" means something different in each. But after the very first step of the transformer (the embedding lookup), the vector for "mole" is identical in all three cases, because that initial embedding is just a context-free lookup table entry. It's only in later steps — via attention — that surrounding words get a chance to feed information into this vector.

The mental picture: there are multiple distinct directions in embedding space corresponding to the different meanings of "mole," and a well-trained attention block computes what needs to be added to the generic embedding to move it toward the direction matching its meaning in context.

### The word "tower"
The embedding of "tower" alone probably points in some generic direction associated with large, tall nouns. If preceded by "Eiffel," you'd want attention to shift that vector toward a much more specific direction — one correlated with "Paris," "France," "steel," and so on. If the phrase were "miniature Eiffel tower," the vector should shift again, this time away from directions associated with large/tall things.

### Beyond single words
More generally, attention allows the model to move information from one embedding to another, even across long distances in the text, and the information transferred can be far richer than a single word's meaning. As an extreme illustration: imagine feeding in most of a mystery novel up to the sentence "Therefore the murderer was ___." For the model to predict the next word accurately, the final embedding in the sequence — which started out simply representing the word "was" — must, after passing through every attention block, encode essentially all contextually relevant information from the entire novel. Recall from the previous chapter that the next-token prediction is computed purely as a function of this final vector in the sequence.

## Working Example: "a fluffy blue creature roamed the verdant forest"

To make the mechanics concrete, imagine the sentence "a fluffy blue creature roamed the verdant forest," and suppose — purely for illustration, not because this is literally what the model learns — that the only kind of updating we care about is adjectives refining the meaning of their corresponding nouns. What follows is a description of a **single attention head**; later we'll see that real attention blocks run many heads in parallel.

Each initial embedding vector encodes both the identity of the word and its position in the sequence (positional encoding is a separate topic not detailed here). These embeddings are denoted $E$.

The goal is a sequence of computations, built mostly out of matrix-vector products with tunable weight matrices, that produces new, refined embeddings — e.g., ones where nouns have absorbed meaning from their adjectives.

### Queries
Picture each noun, like "creature," implicitly asking: "Are there any adjectives sitting in front of me?" This question is encoded as a vector called the **query**. The query lives in a much smaller space than the embedding space — e.g., dimension 128 versus the embedding's larger dimension.

The query is computed by multiplying the embedding by a tunable **query matrix**, $W_Q$:

$$q = W_Q E$$

Applying $W_Q$ to every embedding in the context produces one query vector per token. The entries of $W_Q$ are learned parameters. For the sake of intuition, imagine $W_Q$ learns to map noun embeddings to a direction in query space that effectively represents "looking for preceding adjectives" (what it does to other embeddings is a separate, simultaneous concern encoded in the same matrix).

### Keys
In parallel, a second tunable matrix, the **key matrix** $W_K$, is multiplied by every embedding to produce **key** vectors:

$$k = W_K E$$

Keys live in the same smaller space as queries, and conceptually a key "answers" a query when it closely aligns with it. In the example, $W_K$ would ideally map "fluffy" and "blue" to key vectors that align closely with the query produced by "creature."

### Matching keys to queries: dot products and the attention pattern
To measure how well each key matches each query, take the dot product between every key–query pair. This produces a grid of values — one row/column per token pair — where large positive dot products indicate strong alignment (in ML jargon, the key's word "attends to" the query's word). In the example, the dot products between the keys for "fluffy"/"blue" and the query for "creature" would be large and positive, while the dot product between the key for "the" and the query for "creature" would be small or negative, reflecting irrelevance.

These raw dot products range over all real numbers. To turn each column into a set of weights that behave like a probability distribution (non-negative, summing to 1), a **softmax** is applied to each column independently. After softmax, each column can be read as: "how relevant is the word on the left to the word at the top of this column." This resulting grid is called the **attention pattern**.

### The compact formula
The original paper writes this as:

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Here $Q$ and $K$ denote the full arrays of query and key vectors. The numerator term $QK^T$ compactly represents the grid of all pairwise dot products between keys and queries. Dividing by $\sqrt{d_k}$ (the square root of the key/query space's dimension) is a normalization step included purely for numerical stability during training. The softmax is applied column-by-column, as described above. The $V$ term is addressed in the next section.

### Masking
During training, it's much more efficient to have the model simultaneously predict the next token after *every* subsequence prefix in a passage, not just at the very end. For example, with "a fluffy blue creature roamed...," the model is also implicitly being trained to predict what follows "creature," what follows "the," etc.

This creates a constraint: later tokens must never be allowed to influence earlier tokens in the attention pattern, or they'd leak information about the "answer" the earlier positions are supposed to predict. So all entries in the grid corresponding to a later token affecting an earlier one must be forced to zero.

Simply zeroing them out after the fact would break the column-normalization (columns would no longer sum to 1). Instead, the standard trick is to set those entries to $-\infty$ *before* applying softmax — softmax then naturally maps them to 0, while the rest of the column remains properly normalized. This technique is called **masking**. It's not universal to all forms of attention, but GPT-style models always apply it (even though its necessity is really about training efficiency rather than, say, chatbot inference).

### Why context size is expensive
The attention pattern's size scales with the *square* of the context length (one entry per pair of tokens). This is why context size is such a significant bottleneck for large language models, and why scaling context windows up is nontrivial — it has motivated various more scalable variants of attention in recent research, though this lesson stays with the basics.

### Values: actually moving information between embeddings
Having computed the attention pattern, the model now knows which words are relevant to which. The next step is to actually use that pattern to update embeddings — e.g., to move "creature" in a direction that more specifically encodes "fluffy blue creature."

The straightforward approach (later refined for multi-headed attention) uses a third tunable matrix: the **value matrix**, $W_V$. Multiplying $W_V$ by the embedding of a word (e.g., "fluffy") produces a **value vector**. This value vector lives in the same high-dimensional space as the embeddings, and it represents: "if this word is relevant to some other word, this is what should be added to that other word's embedding to reflect the relevance."

Concretely: multiply $W_V$ by every embedding to get a sequence of value vectors, one per token. Then, for each column of the attention pattern (i.e., for each token being updated), rescale each value vector by that column's corresponding attention weight, and sum the rescaled value vectors together. In the "creature" column, this means the value vectors for "fluffy" and "blue" get large weights and contribute substantially, while irrelevant words' value vectors are scaled to nearly zero.

The resulting sum for a given column is denoted $\Delta E$ — the change to be added to that token's original embedding. Adding $\Delta E$ to the original embedding produces a new, more contextually rich vector (ideally encoding something like "fluffy blue creature" for the "creature" position). This same procedure — weighted sum of value vectors, added to the original embedding — happens for every column/token position simultaneously, producing a full sequence of refined embeddings. This entire process, parameterized by $W_Q$, $W_K$, and $W_V$, is **one head of attention**.

## Parameter Counting (Using GPT-3 as the Running Example)

- $W_Q$ and $W_K$ each have 12,288 columns (matching the embedding dimension) and 128 rows (matching the key/query space dimension) — about 1.5 million parameters each.
- If $W_V$ were a full square matrix mapping the 12,288-dimensional embedding space to itself (as the naive description above would imply), it would need roughly 150 million parameters — vastly more than $W_Q$ or $W_K$.

In practice, it's far more parameter-efficient (and especially relevant once many heads run in parallel) to make the value map's parameter count match that of the key/query maps. This is achieved by **factoring the value map into two smaller matrices**:

- A **value-down matrix** (not standard terminology, used here for clarity) that maps the large embedding space down to the smaller key/query-sized space.
- A **value-up matrix** (also non-standard terminology) that maps back up from that smaller space to the full embedding space, producing the actual vectors added to update embeddings.

Conceptually, the overall value map is still a single linear transformation from embedding space to embedding space (e.g., mapping "blue" to a "blueness" direction added to nouns) — it's just implemented as a composition of two low-rank matrices instead of one full-rank matrix. In linear algebra terms, this constrains the value map to be a **low-rank transformation**. All four matrices ($W_Q$, $W_K$, value-down, value-up) end up the same size, giving roughly **6.3 million parameters per attention head**.

*Note on standard terminology:* what's called the "value matrix" for a given head in most papers/implementations actually refers only to the value-down projection. The value-up matrices across all heads in a multi-headed block are conventionally stapled together into one large matrix called the **output matrix** of the multi-headed attention block. This detail matters for reading papers/code but is a secondary technicality.

## Self-Attention vs. Cross-Attention

Everything described so far is technically **self-attention**, to distinguish it from **cross-attention**, which appears in models that process two distinct data streams — e.g., translating text from one language to another, or transcribing audio speech into text. Cross-attention looks almost identical, except the key and query maps act on two different datasets (e.g., keys from one language, queries from another), so the attention pattern captures correspondence between the two. Cross-attention also typically has no masking, since there's no notion of "later tokens" leaking information within a single sequence. This lesson stays focused on self-attention, which is what GPT-style models use.

## Multi-Headed Attention

A single head captures one specific type of contextual relationship (in the example: adjectives modifying nouns). But there are countless other kinds of contextual influence:

- "They crashed the ___" before "car" affects the implied shape/condition of the car.
- The word "wizard" appearing anywhere in a passage alongside "Harry" suggests "Harry Potter."
- If instead "Queen," "Sussex," and "William" appear in the passage, "Harry" should instead be updated toward the prince.

Each such pattern would require its own distinct key, query, and value matrices to capture its particular attention pattern and its particular update behavior. In practice, the actual learned behavior of these matrices is difficult to interpret — they're simply tuned to whatever minimizes the model's prediction loss.

A full attention block therefore runs many heads in parallel — this is **multi-headed attention**. GPT-3 uses **96 attention heads per block**. Each head has its own independent $W_Q$, $W_K$, and pair of value matrices, producing 96 distinct attention patterns and 96 distinct sequences of value vectors. For each token position, all 96 heads propose their own change to that embedding; these 96 proposed changes are summed together, and the sum is added to the original embedding. This combined sum is what a multi-headed attention block outputs for a single position. Running many heads in parallel gives the model the capacity to learn many distinct ways that context can alter meaning simultaneously.

With 96 heads, each containing four matrices of the size described above, a single block of multi-headed attention totals **around 600 million parameters**.

## Zooming Out: Attention Within the Full Network

Data flowing through a transformer doesn't pass through just one attention block. It also passes through **multi-layer perceptron (MLP)** blocks (covered in a later chapter), and the whole combination of attention + MLP is repeated across **many layers**. This means each embedding gets repeated opportunities to absorb context, with the nuance of the surrounding embeddings themselves growing richer at every layer. The hope is that, deep enough into the network, the model can encode increasingly abstract properties beyond grammar and word-level descriptors — things like sentiment, tone, whether the text is a poem, or relevant underlying facts.

GPT-3 has **96 layers**, so the attention parameter count of roughly 58 million per block... wait — multiplying the ~600 million per block by 96 layers gives a total of **just under 58 billion parameters devoted to attention** across the whole network. That is a large number, but it's only about a third of GPT-3's total 175 billion parameters — meaning the majority of parameters actually live in the MLP blocks between attention layers, not in attention itself, despite attention getting most of the conceptual spotlight.

## Why Attention Succeeded: Parallelizability

A major part of the attention mechanism's practical success is not tied to any one specific behavior it enables, but to the fact that its computations are **highly parallelizable** — they can be run as a large number of simultaneous operations on GPUs. Given that scale has repeatedly produced large qualitative jumps in deep learning model performance, architectures that scale efficiently in this way have a substantial practical advantage, which helps explain why attention-based transformers became so dominant.

---

Source: [Attention in transformers, step-by-step | Deep Learning Chapter 6](https://youtu.be/eMlx5fFNoYc?si=K4rmmpydkNhrEvX_) — 3Blue1Brown
