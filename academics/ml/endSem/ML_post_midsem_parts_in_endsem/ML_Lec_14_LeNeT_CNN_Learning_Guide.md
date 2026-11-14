# LeNet-5 — Learning Guide

Source: `ML_Lec_14_LeNeT_CNN.pptx`, Slides 1–14. Every number recomputed.
**📘 Beyond the slides** = gap filled from outside the slides. **✏️ Slide discrepancy** = a slide is wrong or unclear.

## Contents

1. [What LeNet is](#1-what-lenet-is)
2. [The layers of LeNet5](#2-the-layers-of-lenet5)
3. [Key characteristics and impact](#3-key-characteristics-and-impact)

---

## 1. What LeNet is

**The problem.** People write digits in many styles, and computers had to read them, for example the amounts on bank cheques. Hand-written rules for every style do not work. **LeNet** solved this with a small CNN that learns from examples.

**Popular CNN models (Slide 1).** LeNet, AlexNet, GoogleNet, VGG, ResNet, DenseNet, ResNeXt, EfficientNet. LeNet is the first.

**Facts (Slide 2).**

- One of the **pioneering CNN architectures**, developed by **Yann LeCun** and colleagues in the **late 1980s and early 1990s**.
- Designed mainly for **handwritten digit recognition**, specifically the **MNIST** dataset (images of handwritten digits).
- Used by **many banks** to read handwritten numbers on cheques.
- Test error rate as low as **0.95%**, i.e. accuracy $100 - 0.95 = 99.05$%, "more than 99%".

**Versions (Slide 5).** There are many versions of LeNet; this lecture studies **LeNet5**.

![Fig 1 – The LeNet5 CNN (media/image1.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image1.png)
*Figure: Slide 5. INPUT 32×32, C1 (6 maps of 28×28), S2 (6 of 14×14), C3 (16 of 10×10), S4 (16 of 5×5), C5 (120), F6 (84), OUTPUT (10).*

---

## 2. The layers of LeNet5

**The idea.** LeNet5 turns a digit image into one of ten answers in small steps: convolutions find patterns, pooling shrinks the maps, fully connected layers decide. To understand it, follow the size of the data through each layer.

**Names.** **C** = convolutional layer, **S** = subsampling (another name for pooling), **F** = fully connected; the number is the layer's position.

**Input (Slide 3).** Typically a **32×32 grayscale** image. MNIST images are 28×28, so they are often **zero-padded** (a border of zeros added) to 32×32: $28 + 2 + 2 = 32$.

![Zero-padding 28x28 MNIST to 32x32](figures/cnn/l14_02_zero_padding.jpg)
*Figure: 2 pixels of zeros on every side turn a 28×28 digit into 32×32 (illustration).*

**C1, convolutional layer 1 (Slides 3, 6).** **6 filters of 5×5** give **6 feature maps of 28×28**: the 32×32 image becomes 28×28, and 6 kernels give depth 6. Activation: typically **sigmoid** or **tanh** (smooth functions that squash a number into a fixed range).

![Fig 2 – C1: a 5x5 convolution turns the 32x32x1 input into 28x28x6 (media/image2.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image2.png)

**S2, pooling layer 1 (Slides 3, 7).** **Average pooling** (each 2×2 block replaced by its average), **2×2 filter, stride 2**: size halved, 28×28 → **14×14**.

![Fig 3 – S2: pooling reduces 28x28x6 to 14x14x6 (media/image3.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image3.png)

**C3, convolutional layer 2 (Slides 3, 8).** **16 filters of 5×5**, default **pad = 0, stride = 1**: **16 maps of 10×10**, i.e. 10×10×16.

![Fig 4 – C3: the second convolution turns 14x14x6 into 10x10x16 (media/image4.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image4.png)

**S4, pooling layer 2 (Slides 4, 9).** Like S2: average pooling, 2×2, stride 2: 10×10×16 → **5×5×16**. This is then **flattened** (all values written in one long row) into a vector of **400** values.

![Fig 5 – S4: pooling reduces 10x10x16 to 5x5x16 (media/image5.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image5.png)

**Three fully connected layers (Slides 4, 10)** for classification:

1. **C5:** takes the flattened S4 output and connects to **120** neurons (1st FC layer).
2. **F6:** connects to **84** neurons (2nd FC layer).
3. **Output:** **10** neurons, one per digit class 0–9 (3rd FC layer).

![Fig 6 – The full LeNet5 with the three fully connected layers (media/image6.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image6.png)

> ✏️ **Slide discrepancy (Slide 10).** The figure labels the 120-node layer "C3 layer 120". It should read **C5**; C3 is the second convolutional layer (16 maps of 10×10, Slides 3–5).

![LeNet-5 dataflow](figures/cnn/l13_05_lenet5.jpg)
*Figure: The whole path (illustration). "6@28×28" means 6 feature maps of 28×28.*

**The sizes, calculated.** For a convolution with pad 0 and stride 1 (Slide 6): output = input − filter + 1, because the filter cannot hang over the edge. The general formula, with $W_1$ input size, $F$ filter, $P$ pad, $S$ stride, counts the positions where the filter fits:

```math
W_2 = \frac{W_1 - F + 2P}{S} + 1
```

The depth of a conv output is its number of filters; pooling halves width and height and keeps the depth.

| Layer | Calculation | Output |
| :--- | :--- | :--- |
| Input | $28 + 2 + 2$ | 32×32×1 |
| C1 | $(32 - 5 + 0)/1 + 1 = 28$, 6 filters | 28×28×6 |
| S2 | $(28 - 2 + 0)/2 + 1 = 14$ | 14×14×6 |
| C3 | $(14 - 5 + 0)/1 + 1 = 10$, 16 filters | 10×10×16 |
| S4 | $(10 - 2 + 0)/2 + 1 = 5$ | 5×5×16 |
| Flatten | $5 \times 5 \times 16$ | 400 |
| C5, F6, Output | fully connected | 120, 84, 10 |

Slide 6 prints the C1 line as $(32 - 5 + 1) \times (32 - 5 + 1) \times 6 = 28 \times 28 \times 6$.

**Summary table (Slide 11).**

| Layer | Also called (Slides 3–5) | Filters | Filter size | Stride | Feature map | Activation |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| Input | — | — | — | — | 32×32×1 | — |
| Conv 1 | C1 | 6 | 5×5 | 1 | 28×28×6 | tanh |
| Pooling 1 | S2 | — | 2×2 | 2 | 14×14×6 | — |
| Conv 2 | C3 | 16 | 5×5 | 1 | 10×10×16 | tanh |
| Pooling 2 | S4 | — | 2×2 | 2 | 5×5×16 | — |
| Fully Connected 1 | C5 | — | — | — | 120 | tanh |
| Fully Connected 2 | F6 | — | — | — | 84 | tanh |
| Fully Connected 3 | Output | — | — | — | 10 | **Softmax** (one probability per digit) |

![Fig 7 – Summary of the LeNet5 architecture (media/image7.png)](extracted_ML_Lec_14_LeNeT_CNN/media/image7.png)
*Figure: Slide 11.*

> 📘 **Beyond the slides.** Lecture 13 (Slides 25–30) counts this same network's parameters: 156 (C1) + 2,416 (C3) + 48,120 (C5) + 10,164 (F6) + 850 (output) = **61,706**.

---

## 3. Key characteristics and impact

**Key characteristics (Slide 12).**

| Choice | LeNet | Later architectures |
| :--- | :--- | :--- |
| Activation | sigmoid or tanh | modern adaptations often use **ReLU** |
| Pooling | **average** pooling, common at the time | **max** pooling (keep the largest value) became more popular |
| Training | one of the **first** networks trained with **backpropagation** (adjusting each weight to reduce the error) | standard everywhere |

*Average vs max on one block* 1, 3, 5, 7: average $(1 + 3 + 5 + 7)/4 = 4$; max 7.

**Impact and applications (Slide 13).** (i) **Legacy:** laid the groundwork for more complex CNNs and influenced later computer vision. (ii) **Use cases:** beyond digits, variations were adapted for many image classification tasks.

**Summary (Slide 13).** LeNet introduced key deep learning concepts: **convolutional layers**, **pooling** and **end-to-end training** (the whole network trained together, input to output). It remains a foundational model in neural networks and computer vision.
