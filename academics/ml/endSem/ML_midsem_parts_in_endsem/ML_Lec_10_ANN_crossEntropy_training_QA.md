# Lecture 10 — Backpropagation with Cross-Entropy Loss: Exam Questions and Answers

Companion to [activation_crossentropy_backprop_visual_guide.md](../../activation_crossentropy_backprop_visual_guide.md), sections 7–9 (deck `ML_Lec_10_ANN_crossEntropy_training.pptx`). Try each question first, then read the answer.

**Pattern:** Part A = 2-mark questions. Part B = 10-mark questions split (a) + (b), 5 + 5 or 6 + 4.
**Tags:** 🎯 real paper (year, question); ✍️ practice to cover the deck; 📘 beyond the slides. 💡 = memory hook.
This deck is mid-sem material that is also in the end-sem syllabus.

| Topic in the guide | Question |
| :--- | :--- |
| Why squared error learns slowly (§7) | A1, B1(b) |
| Binary cross-entropy from likelihood (§8) | B1(a) |
| Its gradient and update rule (§8) | A4, B1(a) |
| Multi-class cross-entropy and its gradient (§9) | B2(b) |
| Softmax (§9) | A2, A3, B2(a) |

---

## Part A — 2-mark questions

### A1. Why does squared error make a sigmoid network learn slowly? ✍️ [2]

With squared error, the output delta is $\delta = (o - t)\,o(1 - o)$. When the sigmoid output is near 0 or 1, the factor $o(1 - o)$ is near 0, so the update almost vanishes **even when the network is completely wrong**.

| Output $o$ (target 0) | $(o - t)$ | $o(1 - o)$ | $\delta$ |
| :---: | :---: | :---: | :---: |
| 0.5 | 0.5 | 0.25 | 0.125 |
| 0.99 | 0.99 | 0.0099 | 0.0098 |

The most wrong neuron gets a correction about 13× smaller than the half-wrong one.

> 💡 Confidently wrong + flat sigmoid = almost no learning.

### A2. Why does multi-class cross-entropy need softmax outputs instead of independent sigmoids? ✍️ [2]

Cross-entropy treats the outputs as a **probability distribution** over the classes. Softmax makes every output positive and makes them **sum to 1**. Independent sigmoids are each in (0, 1) but need not sum to 1: e.g. scores [2.0, 1.0, 0.1] give sigmoids [0.88, 0.73, 0.52], which sum to 2.14, not a distribution.

> 💡 Probabilities must add to 1; only softmax guarantees it.

### A3. Apply softmax to the scores [2.0, 1.0, 0.1]. ✍️ [2]

$$o_j = \frac{e^{\theta_j}}{\sum_k e^{\theta_k}}$$

- $e^{\theta} = [7.389,\ 2.718,\ 1.105]$, sum = 11.213
- $o = [0.659,\ 0.242,\ 0.099]$, which sums to 1

Class 1 is predicted, with probability 0.659. Exponentiating makes all values positive and exaggerates gaps (a score difference of 1 becomes a ratio of $e \approx 2.72$).

> 💡 Exponentiate, then divide by the total.

### A4. What does the cross-entropy weight update do when a sample is misclassified? ✍️ [2]

$$W \leftarrow W - \eta\,\frac{1}{N}\sum_{X_i} X_i(\hat{y} - y)$$

- Class 1 misclassified ($\hat{y}$ near 0): $(\hat{y} - y) < 0$, so the weight **increases**.
- Class 0 misclassified ($\hat{y}$ near 1): $(\hat{y} - y) > 0$, so the weight **decreases**.

The step is proportional to the error $(\hat{y} - y)$: **the bigger the mistake, the bigger the correction**.

> 💡 Cross-entropy: rate of learning ∝ error.

---

## Part B — 10-mark questions

### B1. 🎯 2024 End Q2(b) + 🎯 2025 Mid Q4(a)

**(a)** What is the cross-entropy loss function? Derive the binary cross-entropy loss from the likelihood and find its gradient for a sigmoid neuron. **[6]**
**(b)** Why is cross-entropy preferred over the sum of squared errors (quadratic loss) for training deep neural networks with backpropagation? **[4]**

**(a) Answer.**

A single sigmoid neuron: $\hat{y} = \sigma(\theta)$, $\theta = W^TX_i$, classes $y \in \{0, 1\}$.

1. **Likelihood:** $\hat{y}$ is the likelihood that $X_i$ is in class 1, and $1 - \hat{y}$ that it is in class 0.
2. **One formula for both cases:** $L = \hat{y}^{\,y}(1 - \hat{y})^{\,1-y}$. If $y = 1$ it gives $\hat{y}$; if $y = 0$ it gives $1 - \hat{y}$.
3. **Log-likelihood** (product → sum): $\log L = y\log\hat{y} + (1 - y)\log(1 - \hat{y})$.
4. **Average and negate** (we maximise likelihood, but minimise loss):

$$C = -\frac{1}{N}\sum_{X_i}\big[y\log\hat{y} + (1 - y)\log(1 - \hat{y})\big]$$

This is the **binary cross-entropy** loss.

**Gradient** by the chain rule:

$$\frac{\partial C}{\partial\hat{y}} = -\frac{1}{N}\sum\left(\frac{y}{\hat{y}} - \frac{1 - y}{1 - \hat{y}}\right) = -\frac{1}{N}\sum\frac{y - \hat{y}}{\hat{y}(1 - \hat{y})}, \qquad \frac{\partial\hat{y}}{\partial\theta} = \hat{y}(1 - \hat{y}), \qquad \frac{\partial\theta}{\partial W} = X_i$$

The $\hat{y}(1 - \hat{y})$ in the denominator **cancels** the sigmoid's slope:

$$\frac{\partial C}{\partial W} = \frac{1}{N}\sum_{X_i}X_i(\hat{y} - y), \qquad W \leftarrow W - \eta\,\frac{1}{N}\sum_{X_i}X_i(\hat{y} - y)$$

**(b) Answer.**

| Loss | Output delta | When very wrong |
| :--- | :--- | :--- |
| Squared error | $(\hat{y} - y)\,\hat{y}(1 - \hat{y})$ | $\hat{y}(1 - \hat{y}) \approx 0$ → learning stalls |
| Cross-entropy | $(\hat{y} - y)$ | large → learns fast |

*Example:* $y = 1$ but $\hat{y} = 0.1$.

- Squared error: $\delta = (0.1 - 1)(0.1)(0.9) = -0.081$.
- Cross-entropy: $\delta = 0.1 - 1 = -0.9$, about **11× larger**.

Reasons it is preferred:

1. **No learning slowdown:** the sigmoid slope cancels, so the update is proportional to the error; confidently wrong outputs get the largest correction.
2. **Probabilistic meaning:** it is the negative log-likelihood, so it fits sigmoid/softmax outputs read as probabilities.
3. **Strong penalty for confident mistakes:** $-\log(0.1) = 2.30$, against $\tfrac{1}{2}(0.9)^2 = 0.405$ for squared error.
4. 📘 For a single sigmoid neuron the loss is convex in the weights, so there are no bad local minima.

In a test with the same bad start, cross-entropy reached 96% accuracy while squared error stayed stuck at 4%.

![Cross-entropy vs squared error](../../lec_guide_images/l07_cross_entropy_vs_squared_error.png)

> 💡 Cross-entropy cancels the sigmoid's slope.

### B2. 🎯 2025 End Q3(b) + ✍️

**(a)** Explain the softmax activation function: its mathematical formulation, working principle and typical applications. **[4]**
**(b)** Write the multi-class cross-entropy loss and derive the weight update rule for the output layer of a multilayer feed-forward network. **[6]**

**(a) Answer.**

$$o_j = \frac{e^{\theta_j}}{\sum_{k=1}^{M_K}e^{\theta_k}}, \quad j = 1, \dots, M_K$$

**Working:**

1. **Exponentiate** each score: all values become positive, and larger scores are exaggerated.
2. **Divide by the total:** the outputs sum to exactly 1.

So $o_j$ is read as $P(X \in \text{class } j)$, and the class with the largest $o_j$ is predicted. *E.g.* [2.0, 1.0, 0.1] → [0.659, 0.242, 0.099].

![Softmax step by step](../../lec_guide_images/l08_softmax_step_by_step.png)

**Applications:** the output layer of multi-class classifiers (digits 0–9, Iris species, ImageNet's 1000 classes), always paired with cross-entropy loss; next-word prediction in language models (RNN/LSTM).

**(b) Answer.**

Target $t_j = 1$ for the true class, 0 otherwise.

For one output node $j$: $-\big[t_j\log o_j^K + (1 - t_j)\log(1 - o_j^K)\big]$.

Over all $M_K$ nodes and all $N$ samples:

$$C = -\frac{1}{N}\sum_X\sum_{j=1}^{M_K}\big[t_j\log o_j^K + (1 - t_j)\log(1 - o_j^K)\big]$$

With $o_j^K = \sigma(\theta_j^K)$ and $\theta_j^K = \sum_i W_{ij}^K o_i^{K-1}$, the chain rule gives:

$$\frac{\partial C}{\partial W_{ij}^K} = -\frac{1}{N}\sum_X\left(\frac{t_j}{o_j^K} - \frac{1 - t_j}{1 - o_j^K}\right)o_j^K(1 - o_j^K)\,o_i^{K-1} = \frac{1}{N}\sum_X(o_j^K - t_j)\,o_i^{K-1}$$

$$\boxed{W_{ij}^K \leftarrow W_{ij}^K - \eta\,\frac{1}{N}\sum_X(o_j^K - t_j)\,o_i^{K-1}}$$

Compared with squared error ($\delta_j = (o_j - t_j)o_j(1 - o_j)$), the delta is simply $\delta_j = o_j - t_j$: **bigger error, bigger step**. (📘 With true softmax outputs and the categorical loss $-\sum_j t_j\log o_j$, the delta is also exactly $o_j - t_j$.)

> 💡 Every cross-entropy delta is just output − target.
