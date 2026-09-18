# How DeepSeek Rewrote the Transformer: Multi-Head Latent Attention

## Background: DeepSeek and R1

In January 2025, the Chinese company DeepSeek released R1, a language model highly competitive with leading American models but requiring only a fraction of the compute. Unlike most American labs, DeepSeek publicly released the R1 model weights, inference code, and detailed technical reports — publishing roughly one report per month throughout 2024, each documenting innovations that eventually culminated in R1.

One of these innovations, introduced in June 2024, is called **multi-head latent attention (MLA)**. Unlike many DeepSeek improvements that live at the margins of the system, MLA modifies the core Transformer architecture itself — the compute structure shared by virtually all large language models. MLA shrinks a major memory bottleneck called the **key-value (KV) cache** by a factor of 57, which lets DeepSeek's model generate text more than six times faster than a traditional Transformer implementation.

## How Standard Attention Works

### Tokens and the autoregressive process

Language models generate text one fragment (**token**) at a time. Because generation is autoregressive, each new token is a function of every token that came before it. The mechanism that handles interactions between tokens is called **attention**.

### Attention patterns and heads

Attention works by computing matrices called **attention patterns**. For example, feeding GPT-2 Small the text "the American flag is red white and" produces 144 attention patterns — because GPT-2 Small has 12 attention heads per layer and 12 layers (12 × 12 = 144). DeepSeek R1, by contrast, has 128 attention heads per layer and 61 layers, producing 7,808 total attention patterns.

In both models, each attention pattern is a square matrix whose size equals the number of input tokens. Since "the American flag is red white and" tokenizes into 9 tokens, every attention pattern for this example is a 9×9 matrix.

Attention patterns move information between token positions in the model's **residual stream**. Two concrete illustrations from GPT-2 Small on this example:
- In layer 3, one attention pattern shows a high value mapping from "American" to "flag" — this head is likely applying the modifier "American" to the noun "flag," fusing them into a single "American flag" concept.
- In layer 11, another attention pattern shows high values mapping "flag," "red," and "white" to the final token "and" — this head is pulling together the relevant context needed to predict the correct next token, which is "blue." GPT-2 Small does in fact predict "blue" correctly here.

### Computing an attention pattern step by step

Attention starts from an input matrix $X$, which can be the input to any layer. $X$ has one row per input token and a number of columns equal to the model's **embedding dimension** — the length of the vector representing each token. GPT-2 Small uses an embedding dimension of 768; DeepSeek R1 uses 7168.

To build one attention pattern:

1. **Queries and keys.** Multiply $X$ by two separate learned weight matrices, $W_Q$ and $W_K$. In GPT-2, these are each $768 \times 64$, producing a query matrix $Q$ and a key matrix $K$, each $9 \times 64$. Each row of $Q$ is a "query," each row of $K$ is a "key."

   The intuition: attention searches for pairs of tokens whose queries and keys are similar, so the model can learn relationships between tokens. For instance, the token "flag" might produce a query that asks "what words modify me?", while "American" might produce a key in certain heads that signals "I am a modifier." A matching modifier-query and modifier-key pair should produce similar query and key vectors.

2. **Dot products.** Similarity between keys and queries is measured via dot product — high dot products indicate similar vectors. All pairwise dot products between the 9 queries and 9 keys are computed at once by transposing $K$ and multiplying by $Q$, giving a $9 \times 9$ matrix where each entry is the dot product of one query/key pair.

3. **Masking.** The upper-right portion of this matrix is zeroed out. This matters mainly during training, preventing the model from "cheating" at next-token prediction by peeking at future tokens.

4. **Normalization.** The result is divided by the square root of the embedding dimension, then passed through a softmax so each row sums to 1. This final normalized matrix is the attention pattern.

### Using the attention pattern: values

Once the attention pattern is computed, it needs to actually move information. This requires a **value matrix** $V$, computed by multiplying $X$ by a third learned weight matrix $W_V$ — the same kind of operation used for $Q$ and $K$, just with different learned weights.

The attention pattern matrix is then multiplied by $V$, producing a weighted sum of the values according to the attention pattern. Conceptually, this step processes the input through a kind of neural network whose weights are themselves determined dynamically by the data (the attention pattern), rather than being fixed.

### Multiple heads and the output projection

Each attention block contains multiple heads. Every head performs the identical sequence of computations above, but with its own distinct learned weights, yielding its own queries, keys, attention pattern, and values. This lets different heads specialize — for example, one head might search for adjectives, another might search for repeated instances of the same token.

To produce the attention block's final output, the results from all heads are stacked together and multiplied by one more learned weight matrix, $W_O$, giving the final output matrix of the block.

## The Quadratic Compute Problem

Because each attention pattern's height and width equal the number of input tokens, the number of entries in the pattern scales as the **square** of the input length. This becomes a serious computational problem at scale: models like ChatGPT now support context lengths over 100,000 tokens — roughly the length of the first Harry Potter book. Computing the attention pattern for such an input is like laying the entire book out as both a row and a column and computing the dot product for every possible pair of tokens across the whole text.

## KV Caching: The Existing Shortcut

Fortunately, there's a major computational shortcut available because generation happens one token at a time and attention patterns don't change much between steps.

### Worked example

Continuing the "American flag" example: suppose the model generates "blue" as the next token, extending the input to "the American flag is red white and blue" — 10 tokens. This new 10-token sequence is fed back into the model to predict the 11th token.

Recomputing $Q$, $K$, and $V$ for this 10-token input gives $10 \times 64$ matrices. But since the weight matrices ($W_Q$, $W_K$, $W_V$) apply the exact same transformation to each token independently, the **first nine rows** of $Q$, $K$, and $V$ are identical to what was computed on the previous (9-token) pass — only the new tenth row is actually new.

When transposing $K$ and multiplying by $Q$ to get the new $10\times10$ attention pattern: since the first nine rows of $Q$ and first nine columns of $K^T$ are unchanged, the entire upper-left $9\times9$ block of the new attention pattern is also unchanged. Combined with the fact that the upper-right of the pattern gets masked out anyway, this means **only the new bottom row** of the attention pattern actually needs to be computed.

That bottom row comes from multiplying the *final row* of $Q$ (the one new query) by *every column* of $K^T$ (all the keys, old and new). So computing it requires:
- The full set of keys (all 10 rows of $K$)
- Only the new, final row of $Q$

Since 9 of the 10 rows of $K$ were already computed on the prior forward pass, it's far cheaper to **store (cache) those keys in memory** and reuse them rather than recompute them. The same logic applies to $V$: the full $V$ matrix is needed to compute outputs, but only its last row is new, so the rest can be cached. Note that queries do **not** need to be cached — only the new row of $Q$ is ever needed to extend the attention pattern.

### Why this matters

This technique — **KV caching** — is core infrastructure for large language models. It converts the attention block's compute from scaling quadratically with input length to scaling **linearly**.

### The cost: memory

This speed gain isn't free: it requires storing keys and values for the entire session history, across every attention head and every layer, in memory. Given a model with:
- $L$ layers
- $N_H$ attention heads per layer
- $D_H$ dimension per key/value matrix
- $n$ input tokens

the KV cache must store $2 \times n \times D_H \times N_H \times L$ numbers (the factor of 2 accounts for storing both keys and values).

Using float16 numbers, DeepSeek R1's architecture, and a context length of 100,000 tokens, this works out to **4 megabytes of KV cache per token** — meaning generating each new token requires reading **400 gigabytes** of memory. This is the bottleneck MLA is designed to attack.

## Existing Solutions Before MLA

### Multi-query attention

One existing fix is to **share a single key and value matrix across all attention heads** in a layer, instead of giving each head its own. This shrinks the KV cache by a factor equal to the number of heads per layer — 128× for DeepSeek R1's architecture. However, forcing every head to share identical keys and values reduces how much heads can specialize, which hurts model performance.

### Grouped query attention

A gentler version of this idea: instead of one shared key/value matrix for *all* heads, organize heads into **groups**, where heads within a group share keys and values. Meta's Llama 3 models use grouped query attention with groups of 8 heads, reducing KV cache size by a factor of 8. This still reduces cache size, but still costs some performance relative to full multi-head attention with independent keys/values per head.

## DeepSeek's Solution: Multi-Head Latent Attention

### The key insight

DeepSeek's approach reduces KV cache size by a factor of **57** while actually **improving** performance — a result that seems to beat the apparent trade-off between cache size and model quality. The key idea borrows a very common machine learning concept: a **latent space**. The question DeepSeek asked was: what if the model could learn to *efficiently compress* its own keys and values, rather than simply forcing heads to share them outright?

### Architecture of MLA

MLA inserts an extra step between each attention head's input and its key/value matrices:

1. The input is projected into a **compressed latent space** — a lower-dimensional representation. Like multi-query attention, this latent space is **shared across all heads** in the block.
2. Unlike multi-query attention (where heads then use the *exact same* keys and values), in MLA the shared latent representation is projected back **up** into full keys and values using two more learned weight matrices, $W_{UK}$ and $W_{UV}$ — and critically, these up-projection weights are **unique to each head**.

This gives MLA more representational flexibility than either multi-query or grouped-query attention: heads share a compressed common representation, but each head can still decode its own distinct keys and values from it.

### Avoiding extra inference compute: absorbing the weights

At first glance, this looks like it trades memory savings for extra compute — introducing new matrix multiplications (the up-projections) undoes the point of KV caching, which was to reduce the heavy compute burden of attention.

DeepSeek's resolution, per their technical report, uses a clever piece of linear algebra: because $W_{UK}$ and $W_{UV}$ are fixed after training, they can be **algebraically absorbed** into other computations:
- The $W_{UK}$ weights can be folded into the **query computation**.
- The $W_{UV}$ weights can be folded into the **final output computation**.

Since these are static weight matrices, the "absorbed" combined weights only need to be computed once (not per inference call), so there's no extra runtime compute cost. In practice, when a new token arrives, the model simultaneously computes its query vector *and* the query's projection into the latent cache space in a single step, and then computes the attention pattern directly against the cached latent key/value matrix.

### Result: cache size becomes independent of head count

With MLA, the KV cache size **no longer depends on the number of attention heads per layer at all** — it only depends on the size of the single shared latent KV matrix. For DeepSeek R1, that shared latent dimension is 576 (as opposed to depending on $N_H \times D_H$ as in standard attention).

### Comparing cache sizes for DeepSeek R1

| Attention type | KV cache per token |
|---|---|
| Standard multi-head attention | 4 megabytes |
| Grouped query attention (group size 8) | 500 kilobytes |
| Multi-head latent attention | 70 kilobytes |

That's a 57× reduction in KV cache size going from standard attention to MLA — achieved not by throwing away information (as multi-query/grouped-query attention effectively do) but by letting the model *learn* an efficient shared compression of key/value information, which each head can then decompress in its own specialized way.

## Significance

The combination of a much smaller KV cache and no added inference-time compute is what lets DeepSeek R1 generate tokens more than six times faster than a standard Transformer, while also improving algorithmic performance rather than sacrificing it. This represents a genuine architectural improvement to the Transformer itself — the model learns how to compress and share key/value information between heads in a more optimal way than prior hand-designed sharing schemes (multi-query or grouped-query attention) achieved.

---

Source: [How DeepSeek Rewrote the Transformer [MLA]](https://youtu.be/0VLAoVGf_74?si=rv4YR-nPW7dnGsE4) — Welch Labs
