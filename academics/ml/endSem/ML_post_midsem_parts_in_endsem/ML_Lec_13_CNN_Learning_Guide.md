# CNN Layers, Regularization, Parameters and Transfer Learning — Learning Guide

Source: `ML_Lec_13_CNN.pptx`, Slides 1–50. Every number recomputed.
**📘 Beyond the slides** = gap filled from outside the slides. **✏️ Slide discrepancy** = a slide is wrong or unclear.

## Contents

1. [What a CNN is](#1-what-a-cnn-is)
2. [The convolutional layer](#2-the-convolutional-layer)
3. [The pooling layer](#3-the-pooling-layer)
4. [Fully connected and output layers](#4-fully-connected-and-output-layers)
5. [Dropout](#5-dropout)
6. [Batch normalization](#6-batch-normalization)
7. [Counting parameters in a CNN](#7-counting-parameters-in-a-cnn)
8. [The AlexNet table and its mistakes](#8-the-alexnet-table-and-its-mistakes)
9. [A CNN as a feedforward network](#9-a-cnn-as-a-feedforward-network)
10. [Transfer learning](#10-transfer-learning)

---

## 1. What a CNN is

**The idea.** We want a network that looks at an image and says what is in it. A **CNN** (convolutional neural network) first finds small patterns, then builds bigger patterns from them, and at the end makes a decision.

**Definition (Slides 1, 3).**

- A network architecture for deep learning that **learns directly from data**.
- A class of deep learning models designed for **structured grid data**, such as images.
- Very useful for finding patterns in images to recognize objects; also effective for **non-image data** such as audio, time series and signal data.
- Its layered architecture learns **hierarchical features** automatically (simple features first, complex ones built on top), which makes it ideal for computer vision.

**The five layers (Slide 1)**, in order: (1) input, (2) convolutional, (3) pooling, (4) fully connected, (5) output.

**Input layer (Slide 4).** A multi-dimensional array representing an image: height × width × channels. A colour image has three channels: red, green, blue (RGB).

**Applications (Slide 2).** Image classification, object detection, image segmentation, facial recognition, medical image analysis.

![Fig 1 – The architecture of a CNN (media/image1.png)](extracted_ML_Lec_13_CNN/media/image1.png)
*Figure: Slide 3. A 28×28×1 input passes through two convolution + max-pooling pairs, is flattened, then goes through fc_3 (n3 units, ReLU) and fc_4 (with dropout) to ten outputs, 0 to 9.*

**Checking the figure's sizes.** A 5×5 kernel with valid padding (no padding) and stride 1 removes 4 from each side; a 2×2 max pool halves each side. n1 and n2 are the filter counts.

| Layer | Calculation | Output |
| :--- | :--- | :--- |
| Input | given | 28×28×1 |
| Conv_1, 5×5, valid | $28 - 5 + 1 = 24$ | 24×24×n1 |
| Max-pool, 2×2 | $24 / 2 = 12$ | 12×12×n1 |
| Conv_2, 5×5, valid | $12 - 5 + 1 = 8$ | 8×8×n2 |
| Max-pool, 2×2 | $8 / 2 = 4$ | 4×4×n2, then flattened |

---

## 2. The convolutional layer

**The idea.** This is where the CNN finds patterns. It slides a small grid of numbers (a filter) over the image; at each place it outputs one number, which is large where the pattern is present.

**Two tasks (Slide 4).**

1. **Convolution operation:** the core building block of CNNs. **Filters** (also called **kernels**) slide over the input and compute a **dot product** at each position; the results form **feature maps**.
2. **Activation function:** a non-linear function, often **ReLU** (Rectified Linear Unit: keep positives, turn negatives into 0), applied to introduce non-linearity.

In a CNN the kernel is nothing but a filter used to extract features from the image (Slide 5).

![Fig 2 – One step of a convolution: image patch times kernel gives one output value (media/image2.png)](extracted_ML_Lec_13_CNN/media/image2.png)
*Figure: Slide 5. The 3×3 kernel sits on the top-left 3×3 patch (the **local receptive field**) of the 6×6 input; the result, 31, is the first output value.*

**Checking the 31.** Multiply each patch number by the kernel number in the same place, then add.

```math
\text{patch} = \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{bmatrix}, \qquad \text{kernel} = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}
```

Only places where the patch has a 1 count: $1 + 3 + 5 + 6 + 7 + 9 = 31$. The output is 4×4, because a 3×3 kernel fits in $6 - 3 + 1 = 4$ positions along each side.

**Why the convolutional layer is useful (Slides 6–8).**

1. **Feature extraction.** *Local patterns:* learned filters detect edges, textures and shapes. *Hierarchical features:* deeper layers capture more complex features, from simple edges to abstract shapes and objects.
2. **Parameter sharing.** The same filter is applied across the whole input, so features do not depend on location. Far fewer parameters than a fully connected layer: more efficient, easier to train.
3. **Translation invariance.** Because filters cover the whole input, the CNN recognizes an object wherever it is in the image.
4. **Dimensionality reduction.** Stride and padding can keep or reduce the spatial size, and feature maps summarize the important information, so later layers work on a more compact representation.
5. **Non-linearity.** An activation (commonly ReLU) after the convolution lets the network learn more complex patterns and relationships.
6. **Preprocessing of input** (*normalizing features*): convolutional layers help preprocess the data so useful representations are easier to learn.

---

## 3. The pooling layer

**Purpose (Slide 9).** Reduce the spatial size of the feature maps, which cuts the parameters and computation later in the network. It looks at a small window and keeps one number for it.

**Types (Slides 9, 11).**

| Type | Keeps | Notes |
| :--- | :--- | :--- |
| **Max pooling** | the maximum in each window | retains the most prominent features; good for edges and textures |
| **Average pooling** | the average in each window | smoother map; can be less sensitive to noise; used to retain more contextual information |
| **Global average pooling** | the average of the **entire** map | one output per feature map; used in the final layers, before the output layer; effective for classification |
| **Global max pooling** | the maximum of the **entire** map | one output per map, keeping the most significant feature; before the output layer when spatial resolution matters less |

**Pooling parameters (Slide 12).** Max and average pooling generally reduce spatial resolution; by how much depends on: (1) **window size** (e.g. 2×2, 3×3); (2) **stride**, the pixels moved per step (larger stride → smaller output); (3) **padding**, extra pixels around the map; pooling typically uses none, but some architectures do.

**Trade-offs (Slide 13).** Some architectures skip pooling and use **convolutions with stride > 1** to downsample while learning features. Pooling can **lose spatial information**, critical for tasks like image segmentation. The choice of pooling depends on the task.

![Fig 3 – Max pooling and average pooling with a 2x2 window and stride 2 (media/image3.png)](extracted_ML_Lec_13_CNN/media/image3.png)
*Figure: Slide 10.*

**Slide 10 by hand.** This 4×4 map, with a 2×2 window and stride 2, splits into four non-overlapping blocks:

```math
\begin{bmatrix} 8 & 7 & 5 & 3 \\ 12 & 9 & 5 & 7 \\ 13 & 2 & 10 & 3 \\ 9 & 4 & 5 & 14 \end{bmatrix}
```


| Block | Values | Max | Average |
| :--- | :--- | :---: | :--- |
| Top-left | 8, 7, 12, 9 | 12 | $36 / 4 = 9$ |
| Top-right | 5, 3, 5, 7 | 7 | $20 / 4 = 5$ |
| Bottom-left | 13, 2, 9, 4 | 13 | $28 / 4 = 7$ |
| Bottom-right | 10, 3, 5, 14 | 14 | $32 / 4 = 8$ |

Both match the figure; 4×4 became 2×2. Pooling only picks or averages, so it has **no parameters** to learn (Slides 26, 34).

---

## 4. Fully connected and output layers

**The idea.** Convolution and pooling find features but give no answer. The last layers combine all the features and decide.

**Fully connected layers (Slide 14).** After several conv and pooling layers, the pooled maps are **flattened** into a single long continuous linear vector. **Fully connected (FC)** layers, where each neuron connects to every neuron of the previous layer, then do the high-level reasoning.

**Output layer (Slide 14).** **Softmax** for classification (one probability per class); **linear** activation for regression (a plain number).

The flattened length is width × height × depth of the last maps: in Fig 1, $4 \times 4 \times n_2$; in section 7's example, $5 \times 5 \times 16 = 400$ inputs to the first FC layer.

---

## 5. Dropout

**The problem.** A network can memorize its training data: good on that data, bad on new data. This is **overfitting**; techniques against it are called **regularization**.

**What dropout does (Slide 15).** It randomly sets a **fraction of units to zero during training**. It acts as a **mask** that cancels some neurons' contribution to the next layer and leaves all others unchanged.

![Fig 4 – The same network without dropout and with dropout on the hidden layer (media/image4.png)](extracted_ML_Lec_13_CNN/media/image4.png)
*Figure: Slide 15. Two of the four hidden neurons are crossed out, so their connections are gone for this step: a rate of $2/4 = 50$%.*

**How it helps (Slides 16–17).**

1. **Prevents overfitting:** the model cannot depend too much on certain neurons or patterns, so it generalizes better.
2. **Encourages redundancy:** different neurons drop each iteration, so learned representations spread across many neurons; this improves robustness.
3. **Effective ensemble:** each mini-batch trains a different sub-network, in effect an **ensemble** of models. At **inference** (using the trained model) all neurons are used, which can improve performance.
4. **Stochasticity:** the randomness can help escape local minima and lead to better optimization.

**In practice (Slide 17).** In CNNs, dropout typically goes **after activation functions and before pooling**. The **dropout rate** is commonly **20–50%**; adjusting it balances training speed against generalization. *E.g.* rate 20% on 100 units: about 20 units are zeroed each step, a different 20 each time.

---

## 6. Batch normalization

**The problem.** During training every layer's weights keep changing, so the inputs reaching later layers keep changing their range. Each layer must keep re-adjusting; training is slow and unstable. **Batch normalization (BN)** normalizes each layer's inputs to improve stability and speed up training (Slide 18).

**Why BN helps (Slides 18–19).**

1. **Reduces internal covariate shift**, the change in the distribution of a layer's inputs during training. With normalized inputs the layers see the same distribution, so training is more stable and faster.
2. **Faster convergence:** a stable process allows **larger learning rates**, so less training time.
3. **Improved gradient flow:** normalized inputs give a smoother loss function and keep gradients from becoming too small (**vanishing**) or too large (**exploding**).
4. **Regularization effect:** normalizing over mini-batches adds noise, which regularizes and reduces the need for dropout.

![Batch normalization in four steps](figures/cnn/l13_04_batchnorm.jpg)
*Figure: BN on one mini-batch: take the inputs, compute mean and variance, normalize, then scale and shift (illustration).*

**How BN works (Slides 20–21).** A **mini-batch** is the small group of samples processed together in one step.

1. **Normalize** with the mini-batch's mean and variance:

```math
\mu_B = \frac{1}{m} \sum_{i=1}^{m} x_i, \qquad \sigma_B^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_B)^2, \qquad \hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}
```

Subtract the mean, divide by the spread; the values then have mean 0 and variance about 1. $m$ is the batch size; $\epsilon$ is a tiny constant that stops division by zero.

2. **Scale and shift** with learnable $\gamma$ (scale) and $\beta$ (shift), so the model can recover the original distribution if needed:

```math
y_i = \gamma \hat{x}_i + \beta
```

3. **At inference** the mean and variance come from **running averages**, not batch statistics.

![Fig 5 – The normalization step of batch normalization (media/image5.png)](extracted_ML_Lec_13_CNN/media/image5.png)

![Fig 6 – Scaling and shifting, and what happens during inference (media/image6.png)](extracted_ML_Lec_13_CNN/media/image6.png)
*Figure: Slides 20–21.*

**By hand.** Batch 2, 4, 6, 8 (ignore $\epsilon$): $\mu_B = 20/4 = 5$; $\sigma_B^2 = (9 + 1 + 1 + 9)/4 = 5$; $\hat{x} = (-1.342, -0.447, 0.447, 1.342)$, e.g. $(2 - 5)/\sqrt{5} = -1.342$. With $\gamma = 2$, $\beta = 1$: $y_1 = 2 \times (-1.342) + 1 = -1.683$.

**Where BN goes (Slide 21).** After the conv layer and **before** the activation (e.g. ReLU), or **after** the activation. Either way it speeds convergence while keeping or improving performance.

**Training vs inference (Slides 22–23).** Training uses mini-batch statistics, helping the model adapt to changing input distributions. Inference uses **running averages** (statistics accumulated during training), because:

1. **Consistency:** inference often feeds one sample or small batches; running averages make normalization the same for any batch size.
2. **Stability:** batch statistics at inference could fluctuate a lot with small batches, giving inconsistent results.

**Running averages (Slide 24).** After each mini-batch during training:

```math
\text{running\_mean} = \alpha \cdot \text{running\_mean} + (1 - \alpha) \cdot \mu_B, \qquad \text{running\_variance} = \alpha \cdot \text{running\_variance} + (1 - \alpha) \cdot \sigma_B^2
```

Keep most of the old value, mix in a little of the new batch. $\alpha$ is a hyperparameter, often about 0.9; near 1 means slow updates. *E.g.* running mean 4.0, $\mu_B = 5$: $0.9 \times 4.0 + 0.1 \times 5 = 4.1$, a small step towards the new mean.

**Parameters (Slide 35):** $2 \times C$ for $C$ channels (one $\gamma$ and one $\beta$ each); BN on 16 channels has 32.

---

## 7. Counting parameters in a CNN

A **parameter** is a number the network learns: a weight or a bias. The count tells you how big the model is.

**Formulas (Slides 33–35).**

| Layer | Parameters | In words |
| :--- | :--- | :--- |
| Convolutional | $(K_w \times K_h \times C_{in} + 1) \times C_{out}$ | weights in one filter, +1 bias, × number of filters |
| Fully connected | $(N_{in} + 1) \times N_{out}$ | each output neuron: one weight per input, +1 bias |
| Pooling | 0 | nothing to learn |
| Batch norm | $2 \times C$ | scale and shift per channel |

$K_w$, $K_h$: filter width and height; $C_{in}$: input channels (depth); $C_{out}$: number of filters. Slides 25–30 write the conv formula as $K \times (F \times F \times D + 1)$: $K$ kernels of size $F$, input depth $D$. Same formula.

![Fig 7 – The example network of Slides 25–30 (media/image7.png)](extracted_ML_Lec_13_CNN/media/image7.png)
*Figure: Input 32, Conv 1 (28), Pool (14), Conv 2 (10), Pool 2 (5), FC 120, FC 84, Output 10.*

**The example network (Slides 25–30).** Settings from Slide 25: conv layers $S = 1$, $F = 5$, $P = 0$; pools $S = 2$, $F = 2$, $P = 0$.

| Layer (slide) | Output | Calculation | Parameters |
| :--- | :--- | :--- | ---: |
| Input | 32×32×1 | — | 0 |
| Conv-1, $K = 6$ (26) | $32 - 5 + 1 = 28$ → 28×28×6 | one kernel $5 \times 5 \times 1 + 1 = 26$; × 6 | 156 |
| Pool 1 | $28/2 = 14$ → 14×14×6 | — | 0 |
| Conv-2, $K = 16$ (27) | $14 - 5 + 1 = 10$ → 10×10×16 | $D = 6$ (6 maps from Conv-1): $5 \times 5 \times 6 + 1 = 151$; × 16 | 2,416 |
| Pool 2 | $10/2 = 5$ → 5×5×16 | — | 0 |
| 1st FC (28) | 120 | input $5 \times 5 \times 16 = 400$: $(400 + 1) \times 120$ | 48,120 |
| 2nd FC (29) | 84 | $(120 + 1) \times 84$ | 10,164 |
| Output (30) | 10 | $(84 + 1) \times 10$ | 850 |
| **Total** | | | **61,706** |

All match the slides. Notice where the weights are: both conv layers together have $156 + 2416 = 2572$; the 1st FC layer alone has 48,120. Parameter sharing keeps conv layers small.

---

## 8. The AlexNet table and its mistakes

**Kinds of CNN (Slide 31).** **Classic:** LeNet, AlexNet, which laid the groundwork. **Modern:** VGG, ResNet, Inception, with **skip connections** (paths that carry data past one or more layers), deeper networks and varying kernel sizes.

**The AlexNet layers (Slides 32, 36).** Slide 36 says "By default, assume pad=0 and stride=1. There are mistakes in the table. Correct it."

| No. | Layer | Kernel / window | Filters / nodes | Stride | Pad |
| :--- | :--- | :--- | :--- | :---: | :---: |
| 0 | Image | — | 3 × 224 × 224 | — | — |
| 1 | Conv-1 | 11 × 11 | 96 | 4 | 0 |
| 2 | MaxPool-1 | 3 × 3 | — | 2 | 0 |
| 3 | Conv-2 | 5 × 5 | 256 | 1 | 2 |
| 4 | MaxPool-2 | 3 × 3 | — | 2 | 0 |
| 5–7 | Conv-3, 4, 5 | 3 × 3 | 384, 384, 256 | 1 | 1 |
| 8 | MaxPool-3 | 3 × 3 | — | 2 | 0 |
| 9–11 | FC-1, 2, 3 | — | 4096, 4096, 1000 | — | — |

![Fig 8 – The AlexNet layers as given on Slides 32 and 36 (media/image19.png)](extracted_ML_Lec_13_CNN/media/image19.png)

**How to check it.** For each layer, (1) the size with $W_2 = (W_1 - F + 2P)/S + 1$, rounding down ($W_1$ input size, $F$ kernel, $P$ pad, $S$ stride); (2) the parameters with section 7's formulas.

**Step 1: parameters** (these depend only on kernel sizes and depths, not image size):

| Layer | Calculation | Weights | Biases | Parameters |
| :--- | :--- | ---: | ---: | ---: |
| Conv-1 | $(11 \times 11 \times 3 + 1) \times 96$ | 34,848 | 96 | 34,944 |
| Conv-2 | $(5 \times 5 \times 96 + 1) \times 256$ | 614,400 | 256 | 614,656 |
| Conv-3 | $(3 \times 3 \times 256 + 1) \times 384$ | 884,736 | 384 | 885,120 |
| Conv-4 | $(3 \times 3 \times 384 + 1) \times 384$ | 1,327,104 | 384 | 1,327,488 |
| Conv-5 | $(3 \times 3 \times 384 + 1) \times 256$ | 884,736 | 256 | 884,992 |
| FC-1 | $(6 \times 6 \times 256 + 1) \times 4096$ | 37,748,736 | 4,096 | 37,752,832 |
| FC-2 | $(4096 + 1) \times 4096$ | 16,777,216 | 4,096 | 16,781,312 |
| FC-3 | $(4096 + 1) \times 1000$ | 4,096,000 | 1,000 | 4,097,000 |
| **Total** | | | | **62,378,344** |

All match Slide 36, which uses Indian commas (6,23,78,344 = 62,378,344). Pooling, input and output rows have 0. FC-1 assumes a 6×6×256 input (9216 values).

**Step 2: sizes from a 224 input.**

| Layer | Calculation | Correct | Slide 36 says |
| :--- | :--- | :--- | :--- |
| Conv-1 | $(224 - 11)/4 + 1 = 54.25$ → 54 | 54×54×96 | 54×54×96 |
| MaxPool-1 | $(54 - 3)/2 + 1 = 26.5$ → 26 | 26×26×96 | 26×26×96 |
| Conv-2 | $(26 - 5 + 4)/1 + 1 = 26$ | 26×26×256 | 26×26×256 |
| MaxPool-2 | $(26 - 3)/2 + 1 = 12.5$ → 12 | 12×12×256 | **13**×13×256 |
| Conv-3, 4, 5 | $(12 - 3 + 2)/1 + 1 = 12$ | 12×12×(384, 384, 256) | **13**×13 |
| MaxPool-3 | $(12 - 3)/2 + 1 = 5.5$ → 5 | 5×5×256 | **6**×6×256 |

> ✏️ **The mistakes (Slide 36).** With a 224 input, the five sizes from MaxPool-2 to MaxPool-3 are wrong: 13 and 6 cannot follow from 26. FC-1's input is then $5 \times 5 \times 256 = 6400$, so FC-1 has $(6400 + 1) \times 4096 = 26{,}218{,}496$ parameters and the total becomes $62{,}378{,}344 - 37{,}752{,}832 + 26{,}218{,}496 = 50{,}844{,}008$.

**Step 3: the other correction, a 227 input** (as in Lecture 12). No division needs rounding:

| Layer | Calculation | Size |
| :--- | :--- | :--- |
| Conv-1 | $(227 - 11)/4 + 1 = 55$ | 55×55×96 |
| MaxPool-1 | $(55 - 3)/2 + 1 = 27$ | 27×27×96 |
| Conv-2 | $(27 - 5 + 4)/1 + 1 = 27$ | 27×27×256 |
| MaxPool-2 | $(27 - 3)/2 + 1 = 13$ | 13×13×256 |
| Conv-3, 4, 5 | $(13 - 3 + 2)/1 + 1 = 13$ | 13×13×384, 13×13×384, 13×13×256 |
| MaxPool-3 | $(13 - 3)/2 + 1 = 6$ | 6×6×256 |

These are exactly Slide 32's sizes, and they give the 6×6×256 that Slide 36's FC-1 count uses.

![Slide 36: input 224 vs 227](figures/cnn/l13_07_slide36_paths.jpg)
*Figure: From 224 the formula gives 12 after the second pool, not 13; from 227 it gives 13 and matches the table (illustration).*

![AlexNet feature-map sizes](figures/cnn/l13_06_alexnet.jpg)
*Figure: The sizes for a 227 input, from 227×227×3 down to the 1000 outputs (illustration).*

**Summary.** Slide 36's header says 224, but its sizes 13 and 6 need 227; it mixes the two.

| Input | Sizes (Conv-1 … MaxPool-3) | FC-1 parameters | Total |
| :--- | :--- | ---: | ---: |
| 224 | 54, 26, 26, 12, 12, 12, 12, 5 | 26,218,496 | 50,844,008 |
| 227 | 55, 27, 27, 13, 13, 13, 13, 6 | 37,752,832 | 62,378,344 |

Either way the FC layers hold most of the weights: with 227, $37{,}752{,}832 + 16{,}781{,}312 + 4{,}097{,}000 = 58{,}631{,}144$ of 62,378,344; the five conv layers hold only 3,747,200.

---

## 9. A CNN as a feedforward network

**The question (Slide 37).** Slide 37 shows a **fully connected** network and asks: how do we make it a CNN? Input: a 3×3 grid b, c, d, e, f, g, h, i, j (9 neurons). Kernel: 2×2 with weights w, x, y, z. Next layer: 4 neurons l, m, n, o; in the fully connected version every input connects to every one of them.

**The answer (Slides 38–42).**

1. A CNN can be implemented as a **feedforward neural network**.
2. Only a few weights are active (drawn in colour).
3. The rest are **zero** (drawn in grey).
4. So we can train a CNN with **backpropagation**, thinking of it as a feedforward network with **sparse connections**.

**Which connections are active.** The kernel on the top-left 2×2 block covers b, c, e, f and gives l, so l connects only to those four; the other five inputs have weight 0 for l. Sliding one step at a time:

| Output | Kernel covers | Value |
| :--- | :--- | :--- |
| l | b, c, e, f | $wb + xc + ye + zf$ |
| m | c, d, f, g | $wc + xd + yf + zg$ |
| n | e, f, h, i | $we + xf + yh + zi$ |
| o | f, g, i, j | $wf + xg + yi + zj$ |

Each colour in the slides is one kernel weight; the same w, x, y, z serve every output: **parameter sharing** (section 2).

![Fig 9 – A CNN drawn as a feedforward network with sparse connections (media/image28.png)](extracted_ML_Lec_13_CNN/media/image28.png)
*Figure: Slide 42. Coloured arrows are active weights; grey ones are zero.*

**Counting.** Fully connected: $9 \times 4 = 36$ weights, all different. CNN: each output uses 4 inputs, so $4 \times 4 = 16$ active, $36 - 16 = 20$ zero, and only **4** distinct values to learn. The output is 2×2 because a 2×2 kernel fits $3 - 2 + 1 = 2$ positions per side.

---

## 10. Transfer learning

**The problem.** Training a big CNN from scratch needs lots of data and time; often we have little data. **Transfer learning** reuses a model already trained on another task, so we do not start from zero.

**Definition (Slide 43).** A model developed for one task is reused as the **starting point** for a model on a second task; knowledge from the first task improves performance on the new one. Very valuable when data is limited. Using **pre-trained models** reuses learned features, which reduces training time and improves performance.

**Key concepts (Slides 44–45).**

1. **Pre-trained models:** typically trained on large datasets (like **ImageNet** for image classification); their learned features help in many tasks.
2. **Fine-tuning:** retrain some or all layers on your dataset, adjusting the weights to suit the new task and improve accuracy.
3. **Feature extraction:** use the pre-trained model as a **fixed** feature extractor: remove the last few layers and feed the remaining layers' output to a new model. Useful with limited data; no additional training of the pre-trained part.

| | Feature extraction | Fine-tuning |
| :--- | :--- | :--- |
| What is trained | only the new model after the kept layers | some or all pre-trained layers |
| Pre-trained weights | fixed | adjusted to the new task |
| Good when | data is limited | higher accuracy is needed |
| Risk | features may not fit a very different task | overfitting on a small dataset |

**Steps (Slide 46).** (1) **Select** a pre-trained model trained on a similar task or dataset. (2) **Modify the architecture:** adapt the output layer to the new number of classes. (3) **Fine-tune:** retrain the whole model or specific layers. (4) **Train** the modified model on the new dataset. (5) **Evaluate and optimize.**

*Step 2 in numbers:* AlexNet's FC-3 (section 8) has 1000 outputs; for a 10-class task it becomes 10 outputs, going from $(4096 + 1) \times 1000 = 4{,}097{,}000$ to $(4096 + 1) \times 10 = 40{,}970$ parameters.

**Benefits (Slide 47).** **Reduced training time** (the weights start close to optimal); **improved performance**, especially on small datasets; **less data required**, since the model already learned from a large dataset.

**Challenges (Slide 48).** **Domain shift:** if the new task is too different, transferred features may not help. **Overfitting:** fine-tuning on a small dataset can learn noise instead of general patterns. Overall it makes many ML tasks more efficient, most of all with limited data.

**Applications (Slide 49).** Image classification (adapting VGG, ResNet, Inception); NLP with **BERT** (Bidirectional Encoder Representations from Transformer) or **GPT** (Generative Pre-trained Transformer) for sentiment analysis or summarization; medical imaging (general-image models helping detect diseases in scans).
