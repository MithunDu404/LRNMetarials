# Neural Network 3 — Backpropagation, Learning Rate, Batches and Epochs: Exam Questions and Answers

Companion to [neural_networks_visual_guide.md](../../neural_networks_visual_guide.md), sections 7, 10, 12 and 13 (deck `Neural_Network_3.pptx`). Try each question first, then read the answer.

**Pattern:** Part A = 2-mark questions. Part B = 10-mark questions split (a) + (b), 5 + 5 or 6 + 4.
**Tags:** 🎯 real paper (year, question); ✍️ practice to cover the deck; 📘 beyond the slides. 💡 = memory hook.
This deck is mid-sem material that is also in the end-sem syllabus. "2026 Mid" = this year's mid-sem paper. Backpropagation is the most-asked derivation in this course.

**Symbol key** (this file uses these simple symbols; the last column shows the slides' symbol, so you can recognise it in a question):

| Symbol | Meaning | On the slides |
| :--- | :--- | :--- |
| $x$ | input (layer 0 output, so $a0 = x$) | $X$, $o^0$ |
| $z$ | weighted sum entering a neuron | $\theta$ |
| $a$ | activation: $a = \sigma(z)$ | $o$, $\hat{y}$ |
| $y$ | target | $t$, $y$ |
| $d$ | delta, the neuron's share of the error | $\delta$ |
| $\eta$ | learning rate | $\eta$ |
| $a2_j$ | output of neuron $j$ in layer 2 | $o_j^K$ |
| $a1_i$ | output of neuron $i$ in layer 1 | $o_i^{K-1}$ |
| $z2_j$ | weighted sum entering neuron $j$ of layer 2 | $\theta_j^K$ |
| $W2_{ij}$ | weight from neuron $i$ (layer 1) to neuron $j$ (layer 2) | $W_{ij}^K$ |
| $d2_j$, $d1_i$ | delta of that neuron | $\delta_j^K$, $\delta_i^{K-1}$ |
| $n2$ | number of neurons in layer 2 | $M_K$ |

Layer 2 is the output layer, layer 1 the hidden layer before it, layer 0 the one before that. The bias is a weight on a fixed input of 1, so it follows the same rules. A deeper network repeats the same pattern backwards.

| Topic in the guide | Question |
| :--- | :--- |
| MLFFNN architecture and notation (§7) | B1(a) |
| Single layer: linear vs sigmoid update (§12, Step 1) | A1 |
| Single layer, many outputs (§12, Step 1b) | A1 |
| Why the error must be propagated back (§12) | A2 |
| Learning rate: choosing it (§10) | A3 |
| Batch size, iteration vs epoch, batching strategies (§10) | A4, B3 |
| Output-layer derivation (§12, Step 2) | B2(a) |
| Hidden-layer derivation, order of updates (§12, Step 3) | A5, B2(b) |
| DNN training process (§10, §12) | B1 |
| Worked example (§13) | B4 |

---

## Part A — 2-mark questions

### A1. Write the weight update rule for a single-layer network with (i) a linear activation and (ii) a sigmoid activation. ✍️ [2]

With squared error and one sample (stochastic):

| Activation | Prediction | Update |
| :--- | :--- | :--- |
| Linear $a = z$ | $a = w \cdot x$ | $w \leftarrow w - \eta(a - y)\,x$ |
| Sigmoid $a = \sigma(z)$ | $a = \sigma(w \cdot x)$ | $w \leftarrow w - \eta(a - y)\,a(1 - a)\,x$ |

The only difference is the sigmoid's derivative $a(1 - a)$. The step function is not differentiable, which is why the sigmoid is used. With several outputs, the same rule is applied to every weight: $W_{ij} \leftarrow W_{ij} - \eta(a_j - y_j)\,a_j(1 - a_j)\,x_i$.

> 💡 Sigmoid adds one factor: its own slope.

### A2. Why is the algorithm called "backpropagation"? ✍️ [2]

The error can be computed only at the **output layer**, where the true targets are known. For a hidden neuron, no one tells us what its output should have been, so we cannot define its error directly. Instead, the output error is sent **backwards** through the network with the chain rule, layer by layer, to find each hidden neuron's share of the error ($d$). The weights are then updated with gradient descent.

> 💡 Errors are known only at the end, so they travel backwards.

### A3. How do you choose the learning rate? ✍️ [2]

1. **Trial and error:** start with a medium value like 0.01 or 0.001.
2. **Monitor the loss:** if it fluctuates wildly or rises, **decrease** $\eta$; if it falls very slowly, **increase** it.
3. **Adaptive optimisers** (Adam, RMSprop, AdaGrad) adjust it per parameter during training.
4. **Learning-rate schedules** decay it as training goes on.

> 💡 Loss jumping → smaller η; loss crawling → bigger η.

### A4. Distinguish iteration and epoch. 1,000 samples, batch size 50, 20 epochs: how many weight updates? ✍️ [2]

- **Iteration:** one weight update, using one batch.
- **Epoch:** one full pass over the whole dataset; it contains many iterations.

$$\text{iterations per epoch} = \frac{\text{dataset size}}{\text{batch size}} = \frac{1000}{50} = 20, \qquad 20 \times 20 \text{ epochs} = \mathbf{400} \text{ updates}$$

For SGD (batch size 1) an epoch has 1,000 iterations; for batch GD it has 1.

> 💡 Iteration = one batch; epoch = all batches.

### A5. In backpropagation, why are all deltas ($d$) computed with the old weights before any update? ✍️ [2]

Each $d$ in a layer uses the **next** layer's weights **as they were during the forward pass**. If we updated those weights first, we would be differentiating a different network, and the gradient would be wrong. So: forward pass → compute all $d$ from the output back to the first hidden layer → then update all weights.

> 💡 Measure everything first, then change it.

---

## Part B — 10-mark questions

### B1. 🎯 2026 Mid Q1 + 🎯 2025 End Q4(a)

**(a)** Describe the architecture of a deep neural network (DNN) and explain forward propagation and the loss function. **[5]**
**(b)** Explain how backpropagation, gradient descent and the parameter updates are used to train it. **[5]**
*(The 2026 mid-sem asked this as one 10-mark question; 2025 End asked it for 6.)*

**(a) Answer.**

![MLFFNN architecture](../../nn_guide_images/nn_11_mlffnn_architecture.png)

**Architecture:**

- **Layer 0 (input):** one neuron per feature; passes the input on ($a0 = x$).
- **Layers 1 to K−1 (hidden):** fully connected, each with a non-linear activation (ReLU, sigmoid, tanh). "Deep" = many hidden layers.
- **Layer K (output):** one neuron per class (sigmoid or softmax), or one linear neuron for regression.
- Notation (two-layer form; deeper networks repeat it): $W2_{ij}$ = weight from neuron $i$ in layer 1 to neuron $j$ in layer 2.

**Forward propagation:** each neuron does two tasks:

1. weighted sum of all inputs from the previous layer: $z2_j = \sum_i W2_{ij}\,a1_i$ (bias included);
2. activation: $a2_j = f(z2_j)$.

Layer by layer, from input to output: $x \to a1 \to a2$.

**Loss function:** measures how wrong the prediction is:

- squared error $E = \frac{1}{2}\sum_j(a2_j - y_j)^2$ (or MSE), for regression;
- cross-entropy $C = -\sum_j y_j\log a2_j$, for classification.

**(b) Answer.**

![Backpropagation flow](../../nn_guide_images/nn_23_backpropagation_flow.png)

**Backpropagation:** compute the gradient of the loss with respect to every weight with the chain rule, starting at the output layer.

- Output layer: $d2_j = (a2_j - y_j)\,a2_j(1 - a2_j)$
- Hidden layer: $d1_i = a1_i(1 - a1_i)\sum_j d2_j\,W2_{ij}$ (sum over all neurons it feeds)
- Gradients: $\partial E/\partial W2_{ij} = d2_j\,a1_i$ and $\partial E/\partial W1_{pi} = d1_i\,a0_p$

**Gradient descent / parameter update:**

$$W2_{ij} \leftarrow W2_{ij} - \eta\,d2_j\,a1_i, \qquad W1_{pi} \leftarrow W1_{pi} - \eta\,d1_i\,a0_p$$

weight change = −η × ($d$ of the receiving neuron) × (output of the sending neuron).

**Training loop:**

1. Initialise weights randomly (Xavier/He).
2. For each mini-batch: forward pass → loss → backward pass (all $d$ with the old weights) → update all weights once.
3. One pass over all batches = one epoch; repeat for many epochs until the loss stops falling (check on validation data).

> 💡 Forward, loss, backward, update; repeat.

### B2. 🎯 2024 End Q2(a) + ✍️

**(a)** Derive the weight update rule for a sample input $X = (X_1, \dots, X_n)$ at the **output layer** of a multilayer feed-forward neural network with $(K-1)$ hidden layers, using backpropagation with gradient descent. $M_i$ is the number of neurons in layer $i$, $i = 0, 1, \dots, K$; use the sigmoid activation and squared error. **[6]**
**(b)** Extend the derivation to the weights of the last hidden layer. **[4]**

**(a) Answer.**

Let **layer 2 = output layer $K$** and **layer 1 = layer $K-1$**, so $n2 = M_K$. Output neuron $j$:

$$z2_j = \sum_i W2_{ij}\,a1_i, \qquad a2_j = \sigma(z2_j) = \frac{1}{1 + e^{-z2_j}}$$

Error for the sample, over the $n2$ output neurons:

$$E = \frac{1}{2}\sum_{j=1}^{n2}(a2_j - y_j)^2$$

$E$ depends on $W2_{ij}$ only through $a2_j$, which depends on it through $z2_j$. Chain rule:

$$\frac{\partial E}{\partial W2_{ij}} = \frac{\partial E}{\partial a2_j}\cdot\frac{\partial a2_j}{\partial z2_j}\cdot\frac{\partial z2_j}{\partial W2_{ij}}$$

The three factors:

1. $\dfrac{\partial E}{\partial a2_j} = a2_j - y_j$ (the $\frac{1}{2}$ cancels the 2)
2. $\dfrac{\partial a2_j}{\partial z2_j} = a2_j(1 - a2_j)$ (sigmoid derivative: $\partial a/\partial z = a(1 - a)$)
3. $\dfrac{\partial z2_j}{\partial W2_{ij}} = a1_i$ (only one term of the sum contains $W2_{ij}$)

Define $d2_j = (a2_j - y_j)\,a2_j(1 - a2_j)$. Then:

$$\boxed{W2_{ij} \leftarrow W2_{ij} - \eta\,d2_j\,a1_i}$$

for every $i$ and $j$. If there is no hidden layer, $a1_i$ is simply the raw input $x_i$. In the slides' symbols this is $W_{ij}^K \leftarrow W_{ij}^K - \eta\,\delta_j^K\,o_i^{K-1}$.

**(b) Answer.**

Weight $W1_{pi}$ goes from neuron $p$ (layer 0, i.e. layer $K-2$) to neuron $i$ (layer 1). A hidden neuron has no target, but it affects $E$ through **every** output neuron $j$, so sum over all paths:

$$\frac{\partial E}{\partial W1_{pi}} = \sum_{j=1}^{n2}\underbrace{(a2_j - y_j)\,a2_j(1 - a2_j)}_{d2_j}\cdot\underbrace{W2_{ij}}_{\partial z2_j/\partial a1_i}\cdot\underbrace{a1_i(1 - a1_i)}_{\partial a1_i/\partial z1_i}\cdot\underbrace{a0_p}_{\partial z1_i/\partial W1_{pi}}$$

$$d1_i = a1_i(1 - a1_i)\sum_{j=1}^{n2}d2_j\,W2_{ij}, \qquad W1_{pi} \leftarrow W1_{pi} - \eta\,d1_i\,a0_p$$

The same pattern repeats for every earlier layer: each layer's $d$ is built from the $d$ of the layer after it, working backwards to layer 1.

> 💡 Output $d$ uses the target; hidden $d$ sums the $d$ values above it.

### B3. 🎯 2024 End Q4(b) + ✍️

**(a)** What is meant by batch size in gradient descent? Explain the different batching strategies, with their merits and demerits. How is batch size related to an epoch? **[1 + 4.5 + 1.5 → 6]**
**(b)** How are batches created in each epoch? How does batch size interact with the learning rate? **[4]**

**(a) Answer.**

**Batch size** = the number of training examples used to compute the gradient for **one** weight update.

| Strategy | Batch size | Merits | Demerits |
| :--- | :--- | :--- | :--- |
| Batch GD | all $N$ samples | exact, stable gradient; smooth convergence | slow; whole dataset must fit in memory; can get stuck in local minima |
| Stochastic GD | 1 | fast, frequent updates; little memory; noise can escape local minima | very noisy path; does not use vectorised hardware well |
| Mini-batch GD | between 1 and $N$ (32, 64, 128, 256) | balance of speed and stability; efficient GPU matrix operations; **most used** | batch size is one more hyperparameter to tune |

**Relation to epoch:** one epoch = one pass over all $N$ samples, so

$$\text{iterations per epoch} = N / \text{batch size}$$

Batch GD: 1; SGD: $N$; mini-batch: $N / B$. *E.g.* 1,000 samples, batch 100 → 10 iterations per epoch.

**(b) Answer.**

**Creating batches each epoch:**

1. **Sequential:** split the data in its fixed order (1–100, 101–200, …); no randomness. Simple, but the model can learn the order.
2. **Random (shuffling):** shuffle the whole dataset at the start of every epoch, then split. Batches differ between epochs, which improves generalisation. The usual choice.
3. **Stratified:** each batch keeps the class proportions of the full dataset; important for **imbalanced** data, so rare classes appear in every batch.

**Batch size and learning rate:** a **larger** batch averages more samples, so its gradient is less noisy and it can use a **larger** $\eta$. A **small** batch gives a noisy gradient and needs a **smaller** $\eta$ to stay stable. The batch size is also limited by GPU memory.

> 💡 Shuffle every epoch; big batch, bigger step.

### B4. ✍️ (numerical)

A 2-2-1 network uses sigmoid activations everywhere, squared error and $\eta = 0.5$. Input $x = (0.6, 0.2)$, target $y = 1$. The first column of each weight matrix is the bias:

$$W1 = \begin{bmatrix} 0.1 & 0.5 & -0.4 \\ -0.2 & 0.3 & 0.8 \end{bmatrix}, \qquad W2 = [0.2,\ 0.7,\ -0.5]$$

**(a)** Do the forward pass and compute the error and all the deltas ($d$). **[5]**
**(b)** Update all the weights and check that the error falls. **[5]**

**(a) Answer.**

Hidden layer:

$$z1 = [0.1 + 0.5(0.6) - 0.4(0.2),\ \ -0.2 + 0.3(0.6) + 0.8(0.2)] = [0.32,\ 0.14]$$
$$a1 = [\sigma(0.32),\ \sigma(0.14)] = [0.5793,\ 0.5349]$$

Output:

$$z2 = 0.2 + 0.7(0.5793) - 0.5(0.5349) = 0.3381, \quad a2 = 0.5837, \quad E = \tfrac{1}{2}(0.5837 - 1)^2 = 0.0866$$

Deltas (old weights):

$$d2 = (0.5837 - 1)(0.5837)(0.4163) = -0.10115$$
$$d1_1 = 0.5793(0.4207)(-0.10115)(0.7) = -0.01726$$
$$d1_2 = 0.5349(0.4651)(-0.10115)(-0.5) = +0.01258$$

**(b) Answer.**

Each update is $W \leftarrow W - \eta\,d\,[1, \text{inputs}]$:

$$W2_{new} = [0.2,\ 0.7,\ -0.5] - 0.5(-0.10115)[1,\ 0.5793,\ 0.5349] = [0.2506,\ 0.7293,\ -0.4729]$$

$$W1_{new} = \begin{bmatrix} 0.1 + 0.00863 & 0.5 + 0.00518 & -0.4 + 0.00173 \\ -0.2 - 0.00629 & 0.3 - 0.00377 & 0.8 - 0.00126 \end{bmatrix} = \begin{bmatrix} 0.1086 & 0.5052 & -0.3983 \\ -0.2063 & 0.2962 & 0.7987 \end{bmatrix}$$

**Check:** with the new weights the output rises from 0.5837 to **0.6043** and the error falls from 0.0866 to **0.0783**. ✓

> 💡 Gradient = $d$ × [1, inputs]; negative $d$ raises the weights.
