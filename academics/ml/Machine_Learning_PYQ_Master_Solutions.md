# Machine Learning (CS 4102) — Previous Year Questions (PYQ) Master Solutions

> **Academic Context:** B.Tech CST / CS / IT ($7^{\text{th}}$ Semester) Examination | **Subject:** Machine Learning (`CS 4102`) | **Institution:** IIEST Shibpur  
> **Source Mode:** **Strict Notes-Bound Mode** (Strictly grounded in authorized course reference notes: [[ml_foundations_regression_classification_visual_guide|Foundations of ML, Regression & Classification]], [[activation_crossentropy_backprop_visual_guide|Non-linearity, Activations, Cross-Entropy & Backprop]], and [[neural_networks_visual_guide|Neural Networks Guide]])  
> **Verification Status:** All mathematical formulations and numerical problems independently audited and calculated via Python scratch engine; all figures programmatically generated at 300 DPI (zero ASCII / zero raw Mermaid).

---

## Contents

- [Multi-Year Frequency & Recurrence Matrix](#multi-year-frequency--recurrence-matrix)
- [Comprehensive Question Audit Matrix](#comprehensive-question-audit-matrix)
- [2025 Mid-Semester Examination Solutions](#2025-mid-semester-examination-solutions)
- [2025 End-Semester Examination Solutions](#2025-end-semester-examination-solutions)
- [2024 Mid-Semester Examination Solutions](#2024-mid-semester-examination-solutions)
- [2024 Final-Semester Examination Solutions](#2024-final-semester-examination-solutions)
- [2023 Mid-Semester Examination Solutions](#2023-mid-semester-examination-solutions)
- [2023 End-Semester Examination Solutions](#2023-end-semester-examination-solutions)
- [Comprehensive Quick-Recall Formula Sheet](#comprehensive-quick-recall-formula-sheet)
- [Viva Voce & Oral Defense Preparation](#viva-voce--oral-defense-preparation)
- [Unanswered / Uncovered Questions (Not in Reference Notes)](#unanswered--uncovered-questions-not-in-reference-notes)

---

## Multi-Year Frequency & Recurrence Matrix

Analysis of examination recurrence across 2023, 2024, and 2025 for topics covered in authorized reference notes:

| Core Topic / Concept | Recurrence Rate | Exam Sessions Appeared | Typical Marks | Exam Hall Yield Level |
|:---|:---:|:---|:---:|:---:|
| **Why Linear Regression Fails for Classification & Why MSE Fails for Logistic** | ★★★★★ (100% in Endsems) | 2025 Mid (Q2a), 2023 Mid (Q3a), 2023 End (Q1a, Q2c) | 3M – 5M | **High-Yield Theory Guaranteed** |
| **Logic Gates Implementation (AND, OR, XOR) & Non-linear Mapping** | ★★★★☆ (80%) | 2025 Mid (Q3a), 2024 Mid (Q3b) | 3M | **High-Yield Visual Architecture** |
| **Activation Functions Comparison (Sigmoid vs Tanh vs ReLU vs Leaky ReLU)** | ★★★★★ (100%) | 2025 Mid (Q3b), 2025 End (Q3a), 2024 Final (Q3b), 2023 End (Q3a) | 3M – 6M | **Guaranteed Core Derivation** |
| **Backpropagation Output Layer Derivation & Delta Rule** | ★★★★☆ (80%) | 2024 Final (Q2a), 2025 End (Q4a) | 6M – 7M | **High-Yield Long Derivation** |
| **Cross-Entropy vs Sum of Squared Errors (SSE / Quadratic Loss)** | ★★★★☆ (80%) | 2025 Mid (Q4a), 2024 Final (Q2b) | 3M – 5.5M | **High-Yield Calculus Proof** |
| **Batching Strategies in Gradient Descent (Batch vs SGD vs Mini-Batch) & Epochs** | ★★★★☆ (80%) | 2025 Mid (Q4b), 2024 Final (Q4b) | 3M – 7M | **High-Yield Comparative Table** |
| **Multiclass Classification Strategies (One-vs-All vs One-vs-One & Softmax)** | ★★★★☆ (80%) | 2025 End (Q3b), 2023 Mid (Q3b), 2023 End (Q1b) | 3M – 5M | **Guaranteed Analytical Question** |
| **Single Neuron Forward Pass Numerical & Sigmoid Evaluation** | ★★★☆☆ (60%) | 2023 Mid (Q4a), 2023 End (Q4a) | 3M | **Guaranteed Full-Marks Numerical** |
| **Perceptron Learning Algorithm & Novikoff Convergence Proof** | ★★★☆☆ (60%) | 2024 Mid (Q3c) | 5M | **High-Value Rigorous Proof** |
| **Ordinary Least Squares (Simple & Multiple Linear Regression Normal Equations)** | ★★★☆☆ (60%) | 2024 Mid (Q1a), 2024 Final (Q1a) | 4M – 5.5M | **High-Value Calculus Derivation** |
| **Regularization in Logistic Regression (L1 Lasso vs L2 Ridge)** | ★★★★☆ (80%) | 2025 Mid (Q2c), 2025 End (Q2b), 2024 Mid (Q2c) | 3M – 4M | **High Probability Theory** |

---

## Comprehensive Question Audit Matrix

| Exam Session | Q# | Topic / Concept Prompt | Marks | Tier | Status in Guide | Authorized Study Guide Reference | Programmatic Figure / Verification |
|:---|:---:|:---|:---:|:---:|:---:|:---|:---|
| **2025 Mid** | Q1(i) | MCQ: Main goal of regression analysis | 1M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Section 2.1]] | Analytical deduction |
| **2025 Mid** | Q1(ii) | MCQ: Non-linear activation function identification | 1M | VSA | **Answered** | [[activation_crossentropy_backprop_visual_guide#3-threshold-function|Sections 3–6]] | Analytical deduction |
| **2025 Mid** | Q1(iii) | MCQ: Predictive modeling definition in ML | 1M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#1-what-is-machine-learning-the-core-paradigm|Section 1]] | Mitchell Operational Definition |
| **2025 Mid** | Q1(iv) | MCQ: Supervised learning algorithm selection | 1M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Section 2.1]] | Analytical deduction |
| **2025 Mid** | Q1(v) | MCQ: Main purpose of unsupervised learning | 1M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Section 2.2]] | Analytical deduction |
| **2025 Mid** | Q1(vi) | MCQ: Unsupervised dimensionality reduction algorithm | 1M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Section 2.2]] | Analytical deduction |
| **2025 Mid** | Q2(a) | Differentiate linear regression and logistic regression | 2M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Section 15]] | 7-Point Comparative Matrix |
| **2025 Mid** | Q2(b) | Performance evaluation of logistic regression | 3M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Section 10]] & [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Section 15]] | Metric formulations |
| **2025 Mid** | Q2(c) | Role of regularization in logistic regression | 3M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Section 11]] | Geometry & sparsity formulation |
| **2025 Mid** | Q3(a) | Neural structures for AND, OR, and XOR gates | 3M | SA | **Answered** | [[neural_networks_visual_guide#3-logic-gates-with-one-neuron|Section 3]] & [[neural_networks_visual_guide#6-xor-needs-a-hidden-layer|Section 6]] | `pyq_images/pyq_fig01_logic_gates_and_xor.png` |
| **2025 Mid** | Q3(b) | Compare Sigmoid, Tanh, and ReLU activations | 3M | SA | **Answered** | [[activation_crossentropy_backprop_visual_guide#6-tanh-function|Section 6.1]] & [[neural_networks_visual_guide#8-activation-functions|Section 8]] | `pyq_images/pyq_fig02_activations_and_gradients.png` |
| **2025 Mid** | Q3(c) | Vanishing gradient problem & ReLU / Leaky ReLU remedy | 2M | VSA | **Answered** | [[neural_networks_visual_guide#11-problems-minima-saddles-vanishing-and-exploding-gradients|Section 11]] & [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Section 5]] | `pyq_images/pyq_fig02_activations_and_gradients.png` |
| **2025 Mid** | Q4(a) | Cross-Entropy vs SSE in deep neural networks | 3M | SA | **Answered** | [[activation_crossentropy_backprop_visual_guide#7-why-squared-error-learns-slowly|Section 7]] & [[activation_crossentropy_backprop_visual_guide#8-binary-cross-entropy-and-its-gradient|Section 8]] | Mathematical gradient comparison |
| **2025 Mid** | Q4(b) | Difference between SGD, Batch GD, and Mini-Batch GD | 3M | SA | **Answered** | [[neural_networks_visual_guide#10-learning-rate-batches-and-epochs|Section 10]] & [[ml_foundations_regression_classification_visual_guide#14-optimization-solvers-in-logistic-regression|Section 14]] | Comparative Table + Examples |
| **2025 Mid** | Q4(c) | Working principle & advantages of Batch Normalization | 2M | VSA | **Answered** | [[neural_networks_visual_guide#11-problems-minima-saddles-vanishing-and-exploding-gradients|Section 11]] & [[neural_networks_visual_guide#15-viva-questions|Viva Q16]] | Architectural placement formula |
| **2025 End** | Q1(a) | Differentiate supervised and unsupervised learning | 2M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Section 2]] | Comparative Matrix |
| **2025 End** | Q1(b) | Underfitting definition | 2M | VSA | **Answered** | [[neural_networks_visual_guide#2-mcculloch-pitts-neuron-and-the-perceptron|Section 2]] & [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Section 11]] | Bias-Variance definition |
| **2025 End** | Q1(c) | Differentiate classification and regression | 2M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Section 2.1]] | Mathematical target types |
| **2025 End** | Q1(d) | Confusion matrix definition | 2M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Section 15]] | 2x2 Contingency Table |
| **2025 End** | Q1(e) | Hyperparameter definition | 2M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Section 11]] & [[neural_networks_visual_guide#10-learning-rate-batches-and-epochs|Section 10]] | Parameter vs Hyperparameter distinction |
| **2025 End** | Q2(a) | Bias, Variance & Bias-Variance Tradeoff | 3M | SA | **Answered** | [[neural_networks_visual_guide#2-mcculloch-pitts-neuron-and-the-perceptron|Section 2]] & [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Section 11]] | Mathematical decomposition |
| **2025 End** | Q2(b) | L1 Lasso vs L2 Ridge regularization & weight effects | 4M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Section 11]] | Sparsity vs Shrinkage table |
| **2025 End** | Q3(a) | Graphs, formulas & comparison of ReLU, Sigmoid, Tanh | 6M | LA | **Answered** | [[activation_crossentropy_backprop_visual_guide#4-sigmoid-function|Sections 4–6]] & [[neural_networks_visual_guide#8-activation-functions|Section 8]] | `pyq_images/pyq_fig02_activations_and_gradients.png` |
| **2025 End** | Q3(b) | Softmax activation formulation, principle & applications | 4M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#12-multiclass-classification-one-vs-rest-vs-multinomial-softmax|Section 12.2]] & [[activation_crossentropy_backprop_visual_guide#9-multi-class-cross-entropy-and-softmax|Section 9]] | Multi-class probability derivation |
| **2025 End** | Q4(a) | DNN Architecture, Forward Pass & Backpropagation | 6M | LA | **Answered** | [[neural_networks_visual_guide#7-multilayer-feed-forward-networks|Section 7]] & [[neural_networks_visual_guide#12-backpropagation-derivation|Section 12]] | `pyq_images/pyq_fig03_backprop_output_layer.png` |
| **2024 Mid** | Q1(a) | Least Squares derivation for Simple Linear Regression | 4M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#4-simple-linear-regression-slr--the-least-squares-derivation|Section 4]] | Calculus partial derivative proof |
| **2024 Mid** | Q2(c) | Two regularization techniques in logistic regression | 4M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Section 11]] | L1 vs L2 penalty formulas |
| **2024 Mid** | Q3(a) | Biological vs Artificial Neuron correspondence | 2M | VSA | **Answered** | [[neural_networks_visual_guide#1-from-brain-to-artificial-neuron|Section 1]] | Biological mapping table |
| **2024 Mid** | Q3(b) | XOR gate neural network & non-linear mapping | 3M | SA | **Answered** | [[neural_networks_visual_guide#6-xor-needs-a-hidden-layer|Section 6]] & [[activation_crossentropy_backprop_visual_guide#2-non-linear-mapping-the-circle-example|Section 2]] | `pyq_images/pyq_fig01_logic_gates_and_xor.png` |
| **2024 Mid** | Q3(c) | Perceptron learning algorithm & Convergence proof | 5M | LA | **Answered** | [[neural_networks_visual_guide#4-perceptron-learning-algorithm|Section 4]] & [[neural_networks_visual_guide#5-convergence-proof|Section 5]] | `pyq_images/pyq_fig04_perceptron_convergence.png` |
| **2024 Final** | Q1(a) | Matrix form of Multiple Linear Regression & Normal Equations | 5.5M | LA | **Answered** | [[ml_foundations_regression_classification_visual_guide#6-multiple-linear-regression-mlr--normal-equations-in-matrix-form|Section 6]] | `pyq_images/pyq_fig05_mlr_projection_geometry.png` |
| **2024 Final** | Q2(a) | Weight update rule derivation for output layer of DNN | 7M | LA | **Answered** | [[neural_networks_visual_guide#12-backpropagation-derivation|Section 12 (Step 1 & 2)]] | `pyq_images/pyq_fig03_backprop_output_layer.png` |
| **2024 Final** | Q2(b) | Cross-entropy vs quadratic loss in backpropagation | 5.5M | LA | **Answered** | [[activation_crossentropy_backprop_visual_guide#7-why-squared-error-learns-slowly|Section 7]] & [[activation_crossentropy_backprop_visual_guide#8-binary-cross-entropy-and-its-gradient|Section 8]] | Analytical gradient cancellation |
| **2024 Final** | Q3(a) | Vanishing & exploding gradients: effects & solutions | 6.5M | LA | **Answered** | [[neural_networks_visual_guide#11-problems-minima-saddles-vanishing-and-exploding-gradients|Section 11]] | `pyq_images/pyq_fig02_activations_and_gradients.png` |
| **2024 Final** | Q3(b) | ReLU properties, limitations & Leaky ReLU solution | 6M | LA | **Answered** | [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Section 5]] & [[neural_networks_visual_guide#8-activation-functions|Section 8]] | `pyq_images/pyq_fig02_activations_and_gradients.png` |
| **2024 Final** | Q4(b) | Batch size, batching strategies, and relation to epoch | 7M | LA | **Answered** | [[neural_networks_visual_guide#10-learning-rate-batches-and-epochs|Section 10]] & [[ml_foundations_regression_classification_visual_guide#14-optimization-solvers-in-logistic-regression|Section 14]] | Comprehensive Comparison Table |
| **2023 Mid** | Q1(a) | Gradient descent derivation for polynomial regression hypothesis | 7M | LA | **Answered** | [[ml_foundations_regression_classification_visual_guide#4-simple-linear-regression-slr--the-least-squares-derivation|Section 4]] & [[neural_networks_visual_guide#9-gradient-descent-and-the-delta-rule|Section 9]] | Full step-by-step calculus derivation |
| **2023 Mid** | Q3(a) | Why linear regression fails for classification & MSE fails for logistic | 5M | LA | **Answered** | [[ml_foundations_regression_classification_visual_guide#8-why-linear-regression-fails-for-classification|Section 8]] & [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Section 10.1]] | Analytical non-convexity proof |
| **2023 Mid** | Q3(b) | Multiclass classification via One-vs-All and One-vs-One | 5M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#12-multiclass-classification-one-vs-rest-vs-multinomial-softmax|Section 12.1]] | $c$ vs $c(c-1)/2$ classifier counts |
| **2023 Mid** | Q4(a) | Numerical: Output of 3-input neuron with bias and sigmoid | 3M | SA | **Answered** | [[neural_networks_visual_guide#1-from-brain-to-artificial-neuron|Section 1]] & [[activation_crossentropy_backprop_visual_guide#4-sigmoid-function|Section 4]] | Audited: $z=0.45, \sigma(z)=0.6106$ |
| **2023 Mid** | Q4(b) | Log-likelihood derivation for biased coin toss parameter $p$ | 7M | LA | **Answered** | [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Section 10.2]] | Analytical Bernoulli derivation |
| **2023 End** | Q1(a) | Why linear regression fails for classification & MSE fails for logistic | 3M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#8-why-linear-regression-fails-for-classification|Section 8]] & [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Section 10.1]] | Concise 3M dual rationale |
| **2023 End** | Q1(b) | One-vs-All vs One-vs-One multiclass classification | 3M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#12-multiclass-classification-one-vs-rest-vs-multinomial-softmax|Section 12.1]] | Classifier complexity analysis |
| **2023 End** | Q1(c) | Numerical: Precision, Recall, TPR, F1 from 5-prediction table | 4M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Section 15]] | Audited: Prec=0.50, Rec=1.00, F1=0.6667 |
| **2023 End** | Q2(c) | Why linear regression fails for classification & MSE fails for logistic | 2M | VSA | **Answered** | [[ml_foundations_regression_classification_visual_guide#8-why-linear-regression-fails-for-classification|Section 8]] & [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Section 10.1]] | Crisp recap |
| **2023 End** | Q2(d) | Differences between Feed-Forward Network and Recurrent Network | 2M | VSA | **Answered** | [[neural_networks_visual_guide#7-multilayer-feed-forward-networks|Section 7]] (Line 302) | Structural loop & temporal table |
| **2023 End** | Q3(a) | Significance of ReLU activation function in CNNs | 4M | SA | **Answered** | [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Section 5]] & [[neural_networks_visual_guide#8-activation-functions|Section 8]] | Sparsity & gradient flow proof |
| **2023 End** | Q4(a) | Numerical: Output of 3-input neuron with bias and sigmoid | 3M | SA | **Answered** | [[neural_networks_visual_guide#1-from-brain-to-artificial-neuron|Section 1]] & [[activation_crossentropy_backprop_visual_guide#4-sigmoid-function|Section 4]] | Audited: $z=0.45, \sigma(z)=0.6106$ |
| **2023 End** | Q4(b) | Log-likelihood and SGD algorithm for biased coin toss | 3M | SA | **Answered** | [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Section 10.2]] & [[neural_networks_visual_guide#9-gradient-descent-and-the-delta-rule|Section 9]] | Step-by-step SGD update rule |
| **All Other** | Various | KNN, Decision Trees, Naive Bayes, SVM QP/KKT, AlexNet, VGG16, Autoencoders, RNN/LSTM/GRU | Various | — | **Unanswered** | *Out of reference notes* | Placed in [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes) |

---
## 2025 Mid-Semester Examination Solutions

> [!tip] 🎯 Exam Hall Selection Advisory
> **Status:** Compulsory Paper — **Attempt All Questions**.  
> **Total Marks:** 30 | **Time:** 2 Hours  
> **Scoring Strategy:** All 4 questions are 100% grounded in authorized course materials. Allocate ~15 mins for Q1 (MCQs), ~30 mins for Q2 (Regression & LogReg), ~35 mins for Q3 (Activations & Logic Gates), and ~40 mins for Q4 (Losses & Optimizers).

---

### Question 1: Multiple Choice Questions [6 Marks]

> 1. Pick the most appropriate option. **[6]**
>    - **(i)** Which of the following is the main goal of regression analysis?  
>      (a) To classify data into categories  
>      (b) To cluster similar data points  
>      (c) To predict a continuous outcome variable  
>      (d) To reduce the dimensionality of data  
>    - **(ii)** Which of the following is a non-linear activation function?  
>      (a) Sigmoid  
>      (b) ReLU  
>      (c) Tanh  
>      (d) All of the above  
>    - **(iii)** Predictive modeling in machine learning refers to:  
>      (a) Describing historical data patterns only  
>      (b) Estimating future outcomes based on patterns in data  
>      (c) Reducing dataset size  
>      (d) Clustering unlabeled data  
>    - **(iv)** Which of the following is a supervised learning algorithm?  
>      (a) K-Means Clustering  
>      (b) Principal Component Analysis  
>      (c) Decision Tree  
>      (d) Apriori Algorithm  
>    - **(v)** The main purpose of unsupervised learning is:  
>      (a) Predicting continuous values  
>      (b) Predicting categorical labels  
>      (c) Finding hidden structures and patterns in data  
>      (d) Optimizing gradient descent  
>    - **(vi)** Which algorithm is used for dimensionality reduction in unsupervised learning?  
>      (a) PCA  
>      (b) Decision Tree  
>      (c) Naive Bayes  
>      (d) Logistic Regression  

#### Tier 1 Model Answers & Rigorous Rationales

- **(i) Answer: (c) To predict a continuous outcome variable**  
  *First-Principles Rationale:* In supervised learning taxonomy, regression maps input vectors $\mathbf{x} \in \mathbb{R}^d$ to a continuous metric target $y \in \mathbb{R}$ (e.g., house price, temperature). Option (a) defines classification ($y \in \{0, 1\}$ or discrete classes), (b) defines clustering, and (d) defines dimensionality reduction.  
  *Reference:* [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Foundations Guide §2.1]]

- **(ii) Answer: (d) All of the above**  
  *First-Principles Rationale:* Sigmoid ($\sigma(z) = \frac{1}{1 + e^{-z}}$), Tanh ($\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$), and ReLU ($f(z) = \max(0, z)$) are all non-linear activation functions. Non-linearity is essential to allow multi-layer neural networks to approximate non-linear functions (Universal Approximation Theorem); a composition of strictly linear functions collapses to a single linear layer: $\mathbf{W}_2(\mathbf{W}_1\mathbf{x}) = (\mathbf{W}_2\mathbf{W}_1)\mathbf{x} = \mathbf{W}'\mathbf{x}$.  
  *Reference:* [[activation_crossentropy_backprop_visual_guide#3-threshold-function|Activations Guide §3–6]] and [[neural_networks_visual_guide#8-activation-functions|Neural Networks Guide §8]]

- **(iii) Answer: (b) Estimating future outcomes based on patterns in data**  
  *First-Principles Rationale:* Predictive modeling constructs a mathematical mapping $\hat{y} = f(\mathbf{x}; \boldsymbol{\theta})$ trained on historical empirical observations to generalize and make predictions on unseen future instances. Option (a) describes descriptive analytics, (c) describes compression, and (d) describes clustering.  
  *Reference:* [[ml_foundations_regression_classification_visual_guide#1-what-is-machine-learning-the-core-paradigm|Foundations Guide §1]]

- **(iv) Answer: (c) Decision Tree**  
  *First-Principles Rationale:* A Decision Tree trains on labeled tuples $\{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^m$ to predict continuous or discrete targets by recursively partitioning the feature space. K-Means and PCA are unsupervised algorithms (no ground-truth labels), while Apriori is an association rule mining algorithm.  
  *Reference:* [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Foundations Guide §2.1]]

- **(v) Answer: (c) Finding hidden structures and patterns in data**  
  *First-Principles Rationale:* Unsupervised learning operates on unlabeled data $\{\mathbf{x}^{(i)}\}_{i=1}^m$ to discover intrinsic underlying geometry, probability densities, or grouping structures (e.g., clusters, manifold projections) without external supervision or ground-truth error signals.  
  *Reference:* [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Foundations Guide §2.2]]

- **(vi) Answer: (a) PCA (Principal Component Analysis)**  
  *First-Principles Rationale:* PCA is an unsupervised linear transformation that projects high-dimensional data onto orthogonal axes of maximal variance (eigenvectors of the sample covariance matrix $\mathbf{\Sigma} = \frac{1}{m}\mathbf{X}^T\mathbf{X}$), reducing dimensionality while minimizing reconstruction error. Decision Tree, Naive Bayes, and Logistic Regression are supervised models.  
  *Reference:* [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Foundations Guide §2.2]]

---

### Question 2(a): Linear vs Logistic Regression [2 Marks]

> **(a)** Differentiate between linear regression and logistic regression. **[2]**

#### Tier 1 Model Answer

Linear regression predicts a continuous real-valued quantity by modeling a linear conditional expectation $\mathbb{E}[Y|\mathbf{X}=\mathbf{x}] = \mathbf{w}^T \mathbf{x} + b$, whereas logistic regression models the posterior probability of a discrete categorical class label $P(Y=1|\mathbf{X}=\mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) \in (0, 1)$ via the non-linear logistic sigmoid link function.

| Comparative Dimension | Linear Regression | Logistic Regression |
|:---|:---|:---|
| **Target Variable ($y$)** | Continuous metric: $y \in \mathbb{R}$ | Discrete categorical / binary: $y \in \{0, 1\}$ |
| **Hypothesis Function** | $h_{\mathbf{w}}(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b \in (-\infty, +\infty)$ | $h_{\mathbf{w}}(\mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}} \in (0, 1)$ |
| **Loss Function** | Mean Squared Error (MSE / OLS): $\frac{1}{2m}\sum (y - \hat{y})^2$ | Binary Cross-Entropy (Log-Loss): $-\frac{1}{m}\sum [y\ln\hat{y} + (1-y)\ln(1-\hat{y})]$ |
| **Optimization Method** | Closed-form Normal Equations or Gradient Descent | Numerical Optimization only (Gradient Descent, L-BFGS, Newton-Raphson) |

*Reference:* [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Foundations Guide §15]]

---

### Question 2(b): Performance Evaluation of Logistic Regression [3 Marks]

> **(b)** How do you evaluate the performance of a logistic regression model? **[3]**

#### Tier 2 Model Answer

A logistic regression model outputs continuous class probabilities $\hat{p} = \sigma(\mathbf{w}^T \mathbf{x} + b) \in (0, 1)$, which are then thresholded (typically at $\tau = 0.5$) to generate discrete class labels $\hat{y} \in \{0, 1\}$. Its performance is comprehensively evaluated across both **probabilistic loss** and **decision-boundary classification metrics**:

1. **Log-Loss / Binary Cross-Entropy (Probabilistic Calibration Metric):**  
   Evaluates how well-calibrated the predicted probabilities are against true binary labels:
   $$\mathcal{L}_{\text{BCE}}(\mathbf{w}) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln \hat{p}^{(i)} + (1 - y^{(i)}) \ln (1 - \hat{p}^{(i)}) \right]$$
   Penalizes confident wrong predictions with infinite asymptotic loss ($\lim_{\hat{p}\to 0} \ln \hat{p} = -\infty$).

2. **Confusion Matrix Contingency Metrics (Threshold-Dependent at $\tau$):**  
   From counts of True Positives ($\text{TP}$), False Positives ($\text{FP}$), True Negatives ($\text{TN}$), and False Negatives ($\text{FN}$):
   - **Classification Accuracy:** $\frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$ (Misleading under severe class imbalance).
   - **Precision (Positive Predictive Value):** $\frac{\text{TP}}{\text{TP} + \text{FP}}$ (Measures exactness; critical when False Positives are costly, e.g., spam filtering).
   - **Recall / Sensitivity / TPR:** $\frac{\text{TP}}{\text{TP} + \text{FN}}$ (Measures completeness; critical when False Negatives are fatal, e.g., tumor detection).
   - **$\text{F}_1$-Score:** The harmonic mean balancing precision and recall:
     $$\text{F}_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}}$$

3. **Threshold-Independent Metrics (ROC-AUC & PR-AUC):**  
   - **Receiver Operating Characteristic (ROC) Curve:** Plots $\text{TPR}$ (Sensitivity) vs $\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$ across all thresholds $\tau \in [0, 1]$.
   - **Area Under Curve ($\text{AUC-ROC}$):** Measures the ranking capability—the probability that the model ranks a randomly chosen positive instance higher than a randomly chosen negative instance.

*Reference:* [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Foundations Guide §10]] and [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Foundations Guide §15]]

---

### Question 2(c): Role of Regularization in Logistic Regression [3 Marks]

> **(c)** Explain the role of regularization in logistic regression. **[3]**

#### Tier 2 Model Answer

Regularization modifies the logistic regression training objective by appending a penalty term $\Omega(\mathbf{w})$ that constrains the magnitude of the parameter weights:
$$J_{\text{reg}}(\mathbf{w}) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln \sigma(\mathbf{w}^T \mathbf{x}^{(i)}) + (1 - y^{(i)}) \ln (1 - \sigma(\mathbf{w}^T \mathbf{x}^{(i)})) \right] + \lambda \, \Omega(\mathbf{w})$$

Its critical roles in logistic regression are:

1. **Preventing Catastrophic Overfitting on Linearly Separable Data:**  
   If the training data is perfectly linearly separable, unregularized maximum likelihood estimation causes the weights to diverge to infinity ($\|\mathbf{w}\| \to \infty$). Because $\lim_{z \to \infty} \sigma(z) = 1$ and $\lim_{z \to -\infty} \sigma(z) = 0$, the optimization pushes $\|\mathbf{w}\|$ infinitely large to force empirical cross-entropy loss to absolute zero. This creates an infinitely steep step-function decision boundary with zero margin, destroying generalization. Regularization penalizes large weight magnitudes, guaranteeing a finite, unique global optimum.

2. **Taming Multicollinearity:**  
   When features are highly correlated, the Hessian matrix of log-loss becomes ill-conditioned (nearly singular), causing unstable gradient updates and massive parameter variance. Regularization stabilizes numerical optimization by conditioning the curvature.

3. **Structural Induction via $L_1$ vs $L_2$ Penalties:**
   - **$L_2$ Regularization (Ridge / Weight Decay, $\Omega(\mathbf{w}) = \frac{1}{2}\|\mathbf{w}\|_2^2 = \frac{1}{2}\sum_{j=1}^n w_j^2$):** Shrinks weights smoothly toward zero, distributing predictive burden evenly across collinear features.
   - **$L_1$ Regularization (Lasso, $\Omega(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_{j=1}^n |w_j|$):** Possesses sharp non-differentiable corners at coordinate axes; under gradient updates, it drives non-informative feature weights strictly to zero ($w_j = 0$), performing automated feature selection and yielding sparse models.

*Reference:* [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]]

---

### Question 3(a): Neural Structures for AND, OR, and XOR Gates [3 Marks]

> 3. **(a)** Draw the neural network structures that implement (i) a 2-input AND gate and (ii) a 2-input OR gate. How do these structures differ from the one required to implement a 2-input XOR gate? **[3]**

#### Tier 2 Model Answer

![Logic Gates and XOR Architectures](pyq_images/pyq_fig01_logic_gates_and_xor.png)

##### 1. Neural Structures for Linearly Separable Gates (Single Perceptron)
Both 2-input AND and OR gates are **linearly separable** truth tables. A single artificial neuron (McCulloch-Pitts / Perceptron) with inputs $x_1, x_2 \in \{0, 1\}$, weights $w_1, w_2$, bias $b$, and Heaviside step activation $\phi(z) = \mathbb{I}(z \ge 0)$ computes:
$$y = \phi(w_1 x_1 + w_2 x_2 + b)$$

- **(i) 2-Input AND Gate:**  
  Requires $y=1$ only when $x_1=1$ and $x_2=1$.  
  Parameters: $w_1 = 1.0, \; w_2 = 1.0, \; b = -1.5$ (Decision boundary: $x_1 + x_2 - 1.5 = 0$).  
  - $(0, 0) \to 0 + 0 - 1.5 = -1.5 < 0 \implies y = 0$  
  - $(1, 0) \to 1 + 0 - 1.5 = -0.5 < 0 \implies y = 0$  
  - $(0, 1) \to 0 + 1 - 1.5 = -0.5 < 0 \implies y = 0$  
  - $(1, 1) \to 1 + 1 - 1.5 = +0.5 \ge 0 \implies y = 1$ ✓

- **(ii) 2-Input OR Gate:**  
  Requires $y=1$ if either $x_1=1$ or $x_2=1$.  
  Parameters: $w_1 = 1.0, \; w_2 = 1.0, \; b = -0.5$ (Decision boundary: $x_1 + x_2 - 0.5 = 0$).  
  - $(0, 0) \to 0 + 0 - 0.5 = -0.5 < 0 \implies y = 0$  
  - $(1, 0) \to 1 + 0 - 0.5 = +0.5 \ge 0 \implies y = 1$  
  - $(0, 1) \to 0 + 1 - 0.5 = +0.5 \ge 0 \implies y = 1$  
  - $(1, 1) \to 1 + 1 - 0.5 = +1.5 \ge 0 \implies y = 1$ ✓

##### 2. Structural Difference for the 2-Input XOR Gate
The XOR truth table output is $y=1$ for $\{(1, 0), (0, 1)\}$ and $y=0$ for $\{(0, 0), (1, 1)\}$. In 2D Euclidean space, the positive and negative exemplars form alternating diagonal pairs. No single straight line $w_1 x_1 + w_2 x_2 + b = 0$ can separate them (Minsky & Papert, 1969).

- **Architectural Requirement:** XOR **cannot** be solved by a single-layer perceptron. It requires a **Multi-Layer Perceptron (MLP)** with at least **one hidden layer containing at least 2 hidden neurons** (or a combination of intermediate logic gates: $\text{XOR}(x_1, x_2) = (x_1 \lor x_2) \land \neg(x_1 \land x_2)$):
  1. **Hidden Neuron $h_1$ (OR gate):** Computes $z_1 = \phi(x_1 + x_2 - 0.5)$.
  2. **Hidden Neuron $h_2$ (NAND gate):** Computes $z_2 = \phi(-x_1 - x_2 + 1.5)$.
  3. **Output Neuron $y$ (AND gate):** Computes $y = \phi(z_1 + z_2 - 1.5)$.
- **Mechanism:** The hidden layer performs a **non-linear coordinate transformation** mapping the input space into a hidden representation space $(h_1, h_2)$ where the classes become linearly separable.

*Reference:* [[neural_networks_visual_guide#3-logic-gates-with-one-neuron|Neural Networks Guide §3]] and [[neural_networks_visual_guide#6-xor-needs-a-hidden-layer|Neural Networks Guide §6]]

---

### Question 3(b): Comparison of Sigmoid, Tanh, and ReLU [3 Marks]

> **(b)** Compare sigmoid, tanh, and ReLU activation functions in terms of range, gradient behavior, and advantages/disadvantages. **[3]**

#### Tier 2 Model Answer

![Activation Functions and Derivatives](pyq_images/pyq_fig02_activations_and_gradients.png)

| Characteristic | Sigmoid ($\sigma(z)$) | Hyperbolic Tangent ($\tanh(z)$) | Rectified Linear Unit ($\text{ReLU}(z)$) |
|:---|:---|:---|:---|
| **Mathematical Formula** | $\sigma(z) = \frac{1}{1 + e^{-z}}$ | $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ | $f(z) = \max(0, z)$ |
| **Output Range** | $(0, 1)$ | $(-1, 1)$ | $[0, +\infty)$ |
| **First Derivative** | $\sigma'(z) = \sigma(z)(1 - \sigma(z))$ | $\tanh'(z) = 1 - \tanh^2(z)$ | $f'(z) = \begin{cases} 1 & z > 0 \\ 0 & z < 0 \end{cases}$ (undefined at $0$) |
| **Maximum Gradient** | **$0.25$** (at $z = 0$) | **$1.0$** (at $z = 0$) | **$1.0$** (constant for all $z > 0$) |
| **Zero-Centered?** | ❌ No (Outputs strictly $> 0$) | ✅ Yes (Mean output near $0$) | ❌ No (Outputs $\ge 0$) |
| **Gradient Behavior & Issues** | Severe **Vanishing Gradients**: for $|z| > 4$, $\sigma'(z) \approx 0$. Gradient chaining shrinks exponentially: $\prod_{l=1}^L \sigma' \le (0.25)^L$. | Vanishing gradients in saturation wings ($|z| > 2.5$), but stronger gradient flow near origin than sigmoid ($\max = 1.0$). | **No vanishing gradient** in the positive regime ($z > 0$, derivative is identity $1$). Suffers from **Dying ReLU** for $z < 0$. |
| **Computational Cost** | High (Exponential function $e^{-z}$ and division) | High (Two exponential evaluations) | **Extremely Low** (Simple CPU/GPU branch / threshold at 0) |
| **Primary Use Cases** | Output layer for binary classification | Hidden layers in shallow networks or RNN state transitions | Standard default activation for hidden layers in modern deep feedforward and CNN models |

*Reference:* [[activation_crossentropy_backprop_visual_guide#6-tanh-function|Activations Guide §6.1]] and [[neural_networks_visual_guide#8-activation-functions|Neural Networks Guide §8]]

---

### Question 3(c): Vanishing Gradient Problem & Remedies [2 Marks]

> **(c)** Explain the vanishing gradient problem. How do ReLU and its variant, such as Leaky ReLU, help to overcome it? **[2]**

#### Tier 1 Model Answer

1. **The Vanishing Gradient Problem:**  
   During backpropagation through an $L$-layer network, the error gradient with respect to early layer weights involves repeated matrix products of activation derivatives via the chain rule:
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{w}_1} \propto \prod_{l=2}^L \mathbf{W}_l^T \cdot \text{diag}(\sigma'(z_l))$$
   For saturating activations like Sigmoid ($\sigma'(z) \le 0.25$) and Tanh ($\tanh'(z) \le 1.0$), multiplying these fractional values causes the backpropagated gradient to decay exponentially toward zero as $L$ increases ($\le 0.25^L \to 0$). Consequently, early hidden layers stop learning, leaving the network underfitted.

2. **How ReLU and Leaky ReLU Overcome It:**  
   - **ReLU ($f(z) = \max(0, z)$):** For any positive pre-activation ($z > 0$), the derivative is exactly constant: $f'(z) = 1$. The gradient propagates backward without any multiplicative attenuation factor, eliminating vanishing gradients along active paths.  
   - **Leaky ReLU ($f(z) = \max(\alpha z, z)$ with $\alpha \approx 0.01$):** Provides a small non-zero slope for negative inputs ($f'(z) = \alpha$ for $z < 0$). This ensures a continuous gradient flow even when neurons are inactive, preventing the "Dying ReLU" problem where neurons become permanently deactivated.

*Reference:* [[neural_networks_visual_guide#11-problems-minima-saddles-vanishing-and-exploding-gradients|Neural Networks Guide §11]] and [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Activations Guide §5]]

---

### Question 4(a): Cross-Entropy vs SSE in Deep Networks [3 Marks]

> 4. **(a)** Why is Cross-Entropy loss function preferred over Sum of Square Error (SSE) loss function for training deep neural networks? **[3]**

#### Tier 2 Model Answer

When training neural networks equipped with sigmoid (or softmax) output activations, Cross-Entropy (CE) loss is vastly superior to Sum of Squared Errors (SSE) because **Cross-Entropy analytically cancels the vanishing derivative of the sigmoid function**, whereas SSE induces severe learning stalls.

##### 1. Mathematical Proof of Derivative Cancellation
Let the output neuron compute $a = \sigma(z) = \frac{1}{1 + e^{-z}}$, with ground truth $y \in \{0, 1\}$. Note that $\frac{\partial a}{\partial z} = a(1 - a)$.

- **Case A: Sum of Squared Errors (SSE):**  
  Loss: $\mathcal{L}_{\text{SSE}} = \frac{1}{2}(y - a)^2$.  
  By chain rule:
  $$\frac{\partial \mathcal{L}_{\text{SSE}}}{\partial z} = \frac{\partial \mathcal{L}_{\text{SSE}}}{\partial a} \cdot \frac{\partial a}{\partial z} = -(y - a) \cdot \sigma'(z) = -(y - a) \cdot a(1 - a)$$
  *The Failure Mode:* If the model makes an extremely confident wrong prediction (e.g., $y=1$, but $z = -10 \implies a = \sigma(-10) \approx 0.00004$):  
  The error is maximal ($y - a \approx 1$), but the gradient is:
  $$\frac{\partial \mathcal{L}_{\text{SSE}}}{\partial z} \approx -1 \cdot (0.00004)(0.99996) \approx -0.00004 \approx 0$$
  The gradient vanishes into the saturation wings of the sigmoid. The weight update $\Delta w = -\eta \frac{\partial \mathcal{L}}{\partial z} x \approx 0$ halts, freezing the network in a wrong state.

- **Case B: Binary Cross-Entropy (BCE):**  
  Loss: $\mathcal{L}_{\text{BCE}} = -[y \ln a + (1 - y) \ln (1 - a)]$.  
  By chain rule:
  $$\frac{\partial \mathcal{L}_{\text{BCE}}}{\partial a} = -\left[ \frac{y}{a} - \frac{1-y}{1-a} \right] = -\frac{y(1-a) - a(1-y)}{a(1-a)} = \frac{a - y}{a(1-a)}$$
  Multiplying by $\frac{\partial a}{\partial z} = a(1 - a)$:
  $$\frac{\partial \mathcal{L}_{\text{BCE}}}{\partial z} = \frac{\partial \mathcal{L}_{\text{BCE}}}{\partial a} \cdot \frac{\partial a}{\partial z} = \frac{a - y}{a(1-a)} \cdot a(1 - a) = a - y$$
  *The Direct Linear Error Signal:* The saturating term $a(1-a)$ cancels out perfectly. The backpropagated error gradient $\frac{\partial \mathcal{L}_{\text{BCE}}}{\partial z} = a - y$ is directly proportional to the prediction error. If $y=1$ and $a \approx 0$, the gradient magnitude is $|a - y| \approx 1$ (maximum gradient), driving rapid weight corrections with zero saturation stall.

*Reference:* [[activation_crossentropy_backprop_visual_guide#7-why-squared-error-learns-slowly|Activations Guide §7]] and [[activation_crossentropy_backprop_visual_guide#8-binary-cross-entropy-and-its-gradient|Activations Guide §8]]

---

### Question 4(b): SGD vs Batch GD vs Mini-Batch GD [3 Marks]

> **(b)** Explain the difference between stochastic gradient descent, batch gradient descent, and mini-batch gradient descent with examples. **[3]**

#### Tier 2 Model Answer

The three variants of Gradient Descent differ in the number of training samples $B$ utilized to compute the gradient of the empirical loss $\nabla_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta})$ before performing a single parameter update:

| Property | Batch Gradient Descent (BGD) | Stochastic Gradient Descent (SGD) | Mini-Batch Gradient Descent (MBGD) |
|:---|:---|:---|:---|
| **Batch Size ($B$)** | Entire dataset ($B = m$) | Exactly one sample ($B = 1$) | Subset of size $B$ (typically $32, 64, 128$) |
| **Parameter Update Rule** | $\boldsymbol{\theta} := \boldsymbol{\theta} - \eta \frac{1}{m}\sum_{i=1}^m \nabla \mathcal{L}_i(\boldsymbol{\theta})$ | $\boldsymbol{\theta} := \boldsymbol{\theta} - \eta \nabla \mathcal{L}_i(\boldsymbol{\theta})$ | $\boldsymbol{\theta} := \boldsymbol{\theta} - \eta \frac{1}{B}\sum_{k=1}^B \nabla \mathcal{L}_{i_k}(\boldsymbol{\theta})$ |
| **Trajectory in Loss Landscape** | Perfectly smooth, monotonic descent directly toward local/global minimum | Highly noisy, jagged, erratic oscillations | Smooth descent with mild stochastic fluctuations |
| **Escaping Saddle Points / Local Minima** | Prone to getting stuck in saddle points or sharp local minima | High gradient variance easily knocks parameters out of shallow local minima | Balances noise and stability; escapes bad minima while converging reliably |
| **Computational Efficiency** | Slow per update; cannot fit massive datasets in GPU VRAM | Computationally fast per step, but inefficient vectorization on SIMD/GPU hardware | Highly optimized for parallel matrix multiplication on modern GPUs |

##### Concrete Numerical Example
Consider a dataset containing $m = 10,000$ images:
- **Batch GD:** Processes all $10,000$ images simultaneously through forward and backward passes to execute **$1$ single weight update** per epoch.
- **SGD:** Picks $1$ image at a time, computes its single loss gradient, and executes **$10,000$ separate weight updates** per epoch.
- **Mini-Batch GD ($B = 64$):** Partitions the $10,000$ images into $\lceil 10,000 / 64 \rceil = 157$ mini-batches. It processes $64$ images in parallel on GPU tensor cores, executing **$157$ stable weight updates** per epoch. This is the de facto industry standard for deep neural network training.

*Reference:* [[neural_networks_visual_guide#10-learning-rate-batches-and-epochs|Neural Networks Guide §10]] and [[ml_foundations_regression_classification_visual_guide#14-optimization-solvers-in-logistic-regression|Foundations Guide §14]]

---

### Question 4(c): Batch Normalization [2 Marks]

> **(c)** Explain the working principle of batch normalization and its advantages in deep neural networks. **[2]**

#### Tier 1 Model Answer

1. **Working Principle:**  
   Batch Normalization (Ioffe & Szegedy, 2015) is inserted between the linear affine layer ($\mathbf{z} = \mathbf{W}\mathbf{x} + \mathbf{b}$) and the non-linear activation function ($\mathbf{a} = \phi(\text{BN}(\mathbf{z}))$). For a mini-batch $\mathcal{B} = \{z_1, \dots, z_B\}$ of pre-activations, it standardizes each feature dimension across the batch and restores network expressive capacity via learned scale ($\gamma$) and shift ($\beta$) parameters:
   $$\mu_{\mathcal{B}} = \frac{1}{B}\sum_{i=1}^B z_i, \quad \sigma_{\mathcal{B}}^2 = \frac{1}{B}\sum_{i=1}^B (z_i - \mu_{\mathcal{B}})^2$$
   $$\hat{z}_i = \frac{z_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}, \quad y_i = \gamma \hat{z}_i + \beta$$
   where $\epsilon > 0$ ensures numerical stability, and $\gamma, \beta$ are learned via backpropagation.

2. **Key Advantages in Deep Networks:**  
   - **Eliminates Internal Covariate Shift:** Keeps the distribution of layer inputs stable during training as upstream weights evolve.
   - **Accelerates Convergence:** Prevents activations from entering saturation wings of functions (like Sigmoid/Tanh), allowing much higher learning rates ($\eta$) without divergence.
   - **Acts as a Mild Regularizer:** Mini-batch sampling noise in $\mu_{\mathcal{B}}$ and $\sigma_{\mathcal{B}}$ introduces stochastic noise during training, reducing dependence on Dropout.

*Reference:* [[neural_networks_visual_guide#11-problems-minima-saddles-vanishing-and-exploding-gradients|Neural Networks Guide §11]] and [[neural_networks_visual_guide#15-viva-questions|Neural Networks Guide Viva Q16]]

---
## 2025 End-Semester Examination Solutions

> [!tip] 🎯 Exam Hall Selection Advisory
> **Status:** Compulsory Q1 (10 Marks) + Attempt any FOUR from Q2–Q7 (10 Marks each).  
> **Total Marks:** 50 | **Time:** 3 Hours  
> **Reference-Grounded Strategy:**
> 1. **Question 1 [10 Marks]:** Mandatory compulsory question. All 5 sub-parts (a–e) are 100% grounded in [[ml_foundations_regression_classification_visual_guide|Foundations Guide]].
> 2. **Question 3 [10 Marks]:** **Highest-Yield Choice!** Covers activations: Q3(a) [6M] comparing ReLU, Sigmoid, Tanh + Q3(b) [4M] Softmax derivation. Fully grounded in [[activation_crossentropy_backprop_visual_guide|Activations Guide]] and [[neural_networks_visual_guide|Neural Networks Guide]].
> 3. **Question 2 [Partially Grounded - 7 Marks]:** Q2(a) [3M] Bias-Variance Tradeoff + Q2(b) [4M] L1 Lasso vs L2 Ridge. *(Note: Q2(c) Early Stopping is placed in the [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*
> 4. **Question 4 [Partially Grounded - 6 Marks]:** Q4(a) [6M] DNN Architecture, Forward Pass & Backpropagation. Fully grounded in [[neural_networks_visual_guide|Neural Networks Guide]]. *(Note: Q4(b) Sentence Semantics is placed in the [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*
> 5. **Questions 5, 6, 7:** Cover VGG16, Autoencoders, and RNN/GRU architectures. Outside the 3 reference guides and deferred to the [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes).

---

### Question 1: Fundamental Concepts (Compulsory) [10 Marks]

#### Question 1(a): Supervised vs Unsupervised Learning [2 Marks]

> 1. **(a)** Differentiate between supervised and unsupervised learning. **[2]**

##### Tier 1 Model Answer

Supervised learning trains a parameterized model on labeled data $\{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^m$ to learn a mapping $f: \mathcal{X} \to \mathcal{Y}$ that minimizes prediction loss against ground-truth targets. In contrast, unsupervised learning processes unlabeled instances $\{\mathbf{x}^{(i)}\}_{i=1}^m$ to discover latent patterns, density distributions, or low-dimensional manifolds without external supervisory feedback.

| Attribute | Supervised Learning | Unsupervised Learning |
|:---|:---|:---|
| **Data Nature** | Feature-label pairs $(\mathbf{x}, y)$ | Feature vectors $\mathbf{x}$ only (no target labels $y$) |
| **Objective / Feedback** | Minimize error/loss against ground-truth ($y - \hat{y}$) | Maximize internal consistency, cluster separation, or variance |
| **Typical Tasks** | Classification, Metric Regression | Clustering (K-Means), Dimensionality Reduction (PCA) |
| **Mathematical Goal** | Model conditional distribution $P(Y|\mathbf{X})$ | Model joint/data distribution $P(\mathbf{X})$ or manifold geometry |

*Reference:* [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Foundations Guide §2]]

---

#### Question 1(b): Underfitting [2 Marks]

> **(b)** What is underfitting? **[2]**

##### Tier 1 Model Answer

Underfitting occurs when a machine learning model possesses **insufficient hypothesis complexity (excessive structural bias)** to capture the underlying deterministic trend of the data distribution.  

- **Mathematical Symptoms:** Characterized by **high training error** and **high validation/test error** simultaneously ($J_{\text{train}}(\boldsymbol{\theta}) \gg 0$ and $J_{\text{val}}(\boldsymbol{\theta}) \gg 0$).
- **Root Causes:** Using an overly restrictive model class (e.g., fitting a linear hypothesis $\hat{y} = w_1 x + w_0$ to a quadratic/sinusoidal phenomenon), over-regularizing (excessively high $\lambda$), or prematurely terminating training before convergence.

*Reference:* [[neural_networks_visual_guide#2-mcculloch-pitts-neuron-and-the-perceptron|Neural Networks Guide §2]] and [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]]

---

#### Question 1(c): Classification vs Regression [2 Marks]

> **(c)** Differentiate between classification and regression. **[2]**

##### Tier 1 Model Answer

In supervised learning, classification and regression are distinguished by the topological nature of the target output space $\mathcal{Y}$:

| Aspect | Classification | Regression |
|:---|:---|:---|
| **Target Output Space** | Discrete qualitative categorical: $\mathcal{Y} \in \{0, 1\}$ or $\{C_1, \dots, C_K\}$ | Continuous quantitative metric: $\mathcal{Y} \in \mathbb{R}$ |
| **Decision Surface** | Partitions input space $\mathcal{X}$ into distinct decision regions separated by decision boundaries | Fits a continuous hypersurface (line, plane, hyper-manifold) through the data points |
| **Standard Metrics** | Accuracy, Precision, Recall, $\text{F}_1$-score, ROC-AUC, Log-Loss | Mean Squared Error (MSE), Root MSE (RMSE), Mean Absolute Error (MAE), $R^2$ |
| **Canonical Example** | Predicting whether a patient has diabetes ($1$) or not ($0$) | Predicting blood glucose concentration level ($\text{mg/dL}$) |

*Reference:* [[ml_foundations_regression_classification_visual_guide#2-the-taxonomy-of-learning-supervised-unsupervised-semi-supervised-and-rl|Foundations Guide §2.1]]

---

#### Question 1(d): Confusion Matrix [2 Marks]

> **(d)** What is a confusion matrix? **[2]**

##### Tier 1 Model Answer

A confusion matrix is a structured $K \times K$ contingency table that comprehensively quantifies the performance of a supervised classification model by tabulating predicted class labels against true ground-truth labels across the test set.

For a binary classification task ($K=2$ with Positive $P$ and Negative $N$ classes):

| | **Predicted Class: Positive ($\hat{y} = 1$)** | **Predicted Class: Negative ($\hat{y} = 0$)** |
|:---|:---:|:---:|
| **Actual Class: Positive ($y = 1$)** | **True Positive ($\text{TP}$)** | **False Negative ($\text{FN}$)** (Type II Error) |
| **Actual Class: Negative ($y = 0$)** | **False Positive ($\text{FP}$)** (Type I Error) | **True Negative ($\text{TN}$)** |

- **Significance:** Exposes asymmetric classification errors (distinguishing between Type I and Type II errors) that standard scalar accuracy masks under class imbalance.

*Reference:* [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Foundations Guide §15]]

---

#### Question 1(e): Hyperparameter [2 Marks]

> **(e)** What is a hyperparameter? **[2]**

##### Tier 1 Model Answer

A hyperparameter is an external configuration variable whose value is set **prior to initiating the learning algorithm** and remains fixed during training, governing the learning process and model capacity.

- **Fundamental Distinction from Model Parameters:**
  - **Parameters ($\mathbf{w}, \mathbf{b}$):** Internal weights learned directly from data by optimizing the loss function via gradient descent or analytical normal equations.
  - **Hyperparameters ($\eta, \lambda, B, K$):** Tuned externally via validation set performance or grid/random search (e.g., learning rate $\eta$, regularization strength $\lambda$, mini-batch size $B$, number of hidden layers, or polynomial degree $d$).

*Reference:* [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]] and [[neural_networks_visual_guide#10-learning-rate-batches-and-epochs|Neural Networks Guide §10]]

---

### Question 2: Bias-Variance & Regularization [7 Marks Covered]

#### Question 2(a): Bias, Variance & Bias-Variance Tradeoff [3 Marks]

> 2. **(a)** Define the terms bias and variance in a model. Explain the bias–variance tradeoff. **[3]**

##### Tier 2 Model Answer

##### 1. Formal Definitions
For a true generating process $y = f(\mathbf{x}) + \epsilon$ with zero-mean noise $\mathbb{E}[\epsilon]=0$ and variance $\sigma_\epsilon^2$:
- **Bias:** The expected difference between the learning algorithm's average prediction over all possible training sets and the true target function:
  $$\text{Bias}[\hat{f}(\mathbf{x})] = \mathbb{E}_{\mathcal{D}}[\hat{f}(\mathbf{x})] - f(\mathbf{x})$$
  High bias indicates overly rigid assumptions (underfitting), failing to capture the underlying function.
- **Variance:** The variability of the model's prediction for a given test point across different randomly sampled training sets $\mathcal{D}$:
  $$\text{Variance}[\hat{f}(\mathbf{x})] = \mathbb{E}_{\mathcal{D}}\left[ \left(\hat{f}(\mathbf{x}) - \mathbb{E}_{\mathcal{D}}[\hat{f}(\mathbf{x})]\right)^2 \right]$$
  High variance indicates excessive model sensitivity to the specific training data sample (overfitting), memorizing noise.

##### 2. The Bias-Variance Tradeoff
The expected test Mean Squared Error decomposes mathematically into three mutually exclusive terms:
$$\mathbb{E}_{\mathcal{D}}\left[(y - \hat{f}(\mathbf{x}))^2\right] = \underbrace{\left(\text{Bias}[\hat{f}(\mathbf{x})]\right)^2}_{\text{Underfitting}} + \underbrace{\text{Var}[\hat{f}(\mathbf{x})]}_{\text{Overfitting}} + \underbrace{\sigma_\epsilon^2}_{\text{Irreducible Noise}}$$

```
Error
  ^
  |       \                             /  Total Test Error
  |        \                           /
  |         \     Optimum Complexity  /
  |          \          |            /
  |           \         v           /
  |            \       ---         /
  |             \     /   \       /
  |              \---/     \-----/  Variance
  |               \             /
  |  Bias^2        \           /
  |                 \         /
  +---------------------------------------------> Model Complexity
     (Underfitting)                   (Overfitting)
```

As model complexity increases (e.g., adding polynomial features or deep neural layers):
- Bias decreases monotonically as the model fits complex patterns.
- Variance increases monotonically as the model becomes sensitive to sample noise.
The tradeoff dictates identifying the sweet spot of model complexity that minimizes the total generalization error.

*Reference:* [[neural_networks_visual_guide#2-mcculloch-pitts-neuron-and-the-perceptron|Neural Networks Guide §2]] and [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]]

---

#### Question 2(b): L1 Lasso vs L2 Ridge Regularization [4 Marks]

> **(b)** Define L1 regularization (Lasso Regression) and L2 regularization (Ridge Regression). Describe their effects on model weights. **[4]**

##### Tier 2 Model Answer

Regularization penalizes large weight vectors by appending a norm penalty to the empirical loss function $\mathcal{L}_0(\mathbf{w})$:

$$\mathcal{L}_{\text{reg}}(\mathbf{w}) = \mathcal{L}_0(\mathbf{w}) + \lambda \, \Omega(\mathbf{w})$$

##### 1. Mathematical Formulations
- **$L_1$ Regularization (Lasso — Least Absolute Shrinkage and Selection Operator):**  
  Uses the Manhattan ($L_1$) norm penalty:
  $$\Omega_{L_1}(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_{j=1}^n |w_j| \implies \mathcal{L}_{\text{Lasso}}(\mathbf{w}) = \mathcal{L}_0(\mathbf{w}) + \lambda \sum_{j=1}^n |w_j|$$
- **$L_2$ Regularization (Ridge Regression / Weight Decay):**  
  Uses the squared Euclidean ($L_2$) norm penalty:
  $$\Omega_{L_2}(\mathbf{w}) = \frac{1}{2}\|\mathbf{w}\|_2^2 = \frac{1}{2}\sum_{j=1}^n w_j^2 \implies \mathcal{L}_{\text{Ridge}}(\mathbf{w}) = \mathcal{L}_0(\mathbf{w}) + \frac{\lambda}{2} \sum_{j=1}^n w_j^2$$

##### 2. Detailed Effects on Model Weights
| Regularization Type | Geometric Constraint Shape | Derivative of Penalty | Effect on Weights | Feature Selection? |
|:---|:---|:---|:---|:---:|
| **$L_1$ Lasso** | Rhombus / Polytope with sharp corners at axes ($|w_1| + |w_2| \le C$) | $\frac{\partial}{\partial w_j} = \lambda \cdot \text{sgn}(w_j)$ (Constant force) | **Sparsity Induction:** Drives uninformative weights strictly to zero ($w_j = 0$). | **Yes** (Automated feature selection) |
| **$L_2$ Ridge** | Smooth sphere / Circle ($w_1^2 + w_2^2 \le C$) | $\frac{\partial}{\partial w_j} = \lambda w_j$ (Proportional decay) | **Weight Shrinkage:** Shrinks weights smoothly toward zero, but never exactly to zero ($w_j \to 0, w_j \neq 0$). | **No** (Retains all features) |

- **Analytical Gradient Update Comparison:**
  - In Ridge: $w_j := w_j(1 - \eta \lambda) - \eta \frac{\partial \mathcal{L}_0}{\partial w_j}$. The weight is multiplied by a shrinkage factor $(1 - \eta \lambda) < 1$ at every step.
  - In Lasso: $w_j := w_j - \eta \lambda \, \text{sgn}(w_j) - \eta \frac{\partial \mathcal{L}_0}{\partial w_j}$. The weight is decremented by a fixed constant $\eta \lambda$ regardless of its size, truncating small weights to exactly zero.

*Reference:* [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]]

---

### Question 3: Activation Functions & Softmax [10 Marks]

#### Question 3(a): Mathematical Expressions, Graphs & Comparison of ReLU, Sigmoid, and Tanh [6 Marks]

> 3. **(a)** Explain the mathematical expressions and graphs of the ReLU, Sigmoid, and Tanh activation functions, and compare them with one another. **[6]**

##### Tier 3 Model Answer

![Activation Functions Comparison](pyq_images/pyq_fig02_activations_and_gradients.png)

##### 1. Mathematical Formulations & Analytic Derivatives
1. **Sigmoid Activation Function:**
   $$\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{e^z + 1}$$
   - *First Derivative:*  
     $$\sigma'(z) = \frac{d}{dz}(1 + e^{-z})^{-1} = -(1 + e^{-z})^{-2}(-e^{-z}) = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \sigma(z)(1 - \sigma(z))$$
   - *Gradient Peak:* Attains its maximum value $\sigma'(0) = 0.5(1 - 0.5) = 0.25$ at $z=0$. For $|z| \ge 4$, $\sigma'(z) \to 0$.

2. **Hyperbolic Tangent (Tanh) Function:**
   $$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} = 2\sigma(2z) - 1$$
   - *First Derivative:*  
     $$\tanh'(z) = \frac{d}{dz}\left(\frac{\sinh z}{\cosh z}\right) = \frac{\cosh^2 z - \sinh^2 z}{\cosh^2 z} = 1 - \tanh^2(z)$$
   - *Gradient Peak:* Attains its maximum value $\tanh'(0) = 1.0$ at $z=0$. For $|z| \ge 3$, $\tanh'(z) \to 0$.

3. **Rectified Linear Unit (ReLU):**
   $$f(z) = \max(0, z) = \begin{cases} z & \text{if } z > 0 \\ 0 & \text{if } z \le 0 \end{cases}$$
   - *Sub-gradient Derivative:*  
     $$f'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z < 0 \end{cases} \quad (\text{sub-gradient at } z=0 \text{ is } [0, 1])$$

##### 2. Comprehensive Comparative Matrix
| Property | Sigmoid ($\sigma$) | Tanh ($\tanh$) | ReLU ($f$) |
|:---|:---|:---|:---|
| **Domain** | $(-\infty, +\infty)$ | $(-\infty, +\infty)$ | $(-\infty, +\infty)$ |
| **Codomain / Range** | $(0, 1)$ | $(-1, 1)$ | $[0, +\infty)$ |
| **Zero-Centered?** | ❌ No ($>0$, induces zig-zag gradient updates) | ✅ Yes (Mean output centered at 0) | ❌ No (Outputs $\ge 0$) |
| **Max Derivative** | $0.25$ | $1.0$ | $1.0$ (constant for $z > 0$) |
| **Vanishing Gradient** | **Extremely Severe** ($\le 0.25^L \to 0$) | **Severe in saturation wings** ($|z| > 2.5$) | **None** along active paths ($z > 0$) |
| **Pathology** | Saturation at both extremes | Saturation at both extremes | **Dying ReLU** (permanent deactivation when $z \le 0$) |
| **Computation** | Expensive ($e^{-z}$, division) | Expensive ($2e^z$, division) | **Trivial** (`max(0, z)`, threshold branch) |

##### 3. Graph Interpretation & Saturation Dynamics
- As seen in the programmatic figure above, both Sigmoid and Tanh exhibit horizontal asymptotes ("plateaus"). Whenever $|z|$ becomes moderately large, the tangent slope drops to zero. In deep networks, the chain rule multiplies these sub-unitary derivatives across $L$ layers, annihilating gradient flow to early layers.
- ReLU maintains a constant gradient of $1.0$ for all positive pre-activations, allowing gradient signals to flow backwards across dozens of layers unimpeded.

*Reference:* [[activation_crossentropy_backprop_visual_guide#4-sigmoid-function|Activations Guide §4–6]] and [[neural_networks_visual_guide#8-activation-functions|Neural Networks Guide §8]]

---

#### Question 3(b): Softmax Activation Function [4 Marks]

> **(b)** Explain the Softmax activation function in detail, including its mathematical formulation, working principle, and typical applications in neural networks. **[4]**

##### Tier 2 Model Answer

##### 1. Mathematical Formulation
For a multiclass classification problem with $K$ mutually exclusive classes, the Softmax activation takes an unnormalized real-valued logit vector $\mathbf{z} = [z_1, z_2, \dots, z_K]^T \in \mathbb{R}^K$ from the final affine layer and maps it to a normalized probability distribution vector $\mathbf{p} = [p_1, p_2, \dots, p_K]^T \in \mathbb{R}^K$:

$$p_k = \text{Softmax}(\mathbf{z})_k = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}} \quad \text{for } k = 1, 2, \dots, K$$

##### 2. Working Principle & Properties
1. **Strict Probability Axiom Satisfaction:**  
   - Positivity: Because $e^{z_k} > 0$ for all $z_k \in \mathbb{R}$, every output satisfies $p_k \in (0, 1)$.
   - Partition of Unity: The denominator normalizes the vector such that:
     $$\sum_{k=1}^K p_k = \frac{\sum_{k=1}^K e^{z_k}}{\sum_{j=1}^K e^{z_j}} = 1.0$$
2. **Soft Approximation of the Argmax Function:**  
   The exponential operator accentuates the largest logit relative to others while retaining a continuous, differentiable distribution (unlike discrete non-differentiable $\text{argmax}$).
3. **Analytic Gradient with Categorical Cross-Entropy:**  
   When paired with Multiclass Cross-Entropy $\mathcal{L}_{\text{CE}} = -\sum_{k=1}^K y_k \ln p_k$, the derivative with respect to any input logit $z_i$ simplifies to an exceptionally clean linear error signal:
   $$\frac{\partial \mathcal{L}_{\text{CE}}}{\partial z_i} = p_i - y_i$$
   where $y_i \in \{0, 1\}$ is the one-hot encoded ground truth.

##### 3. Typical Applications
- **Output Layer for Multi-Class Classification:** Serving as the final activation layer in networks categorizing inputs into one of $K \ge 3$ discrete classes (e.g., ImageNet 1000-class classification, MNIST 10-digit recognition).
- **Attention Mechanisms (Transformers):** Computing normalized attention weight distributions across keys: $\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$.

*Reference:* [[ml_foundations_regression_classification_visual_guide#12-multiclass-classification-one-vs-rest-vs-multinomial-softmax|Foundations Guide §12.2]] and [[activation_crossentropy_backprop_visual_guide#9-multi-class-cross-entropy-and-softmax|Activations Guide §9]]

---

### Question 4(a): Deep Neural Network Architecture & Backpropagation [6 Marks]

> 4. **(a)** Describe the architecture of a Deep Neural Network (DNN) and explain how forward propagation and backpropagation are used to train it. **[6]**

##### Tier 3 Model Answer

![Backpropagation and Output Layer Error](pyq_images/pyq_fig03_backprop_output_layer.png)

##### 1. Architecture of a Deep Neural Network (DNN)
A Deep Neural Network (DNN) is a directed acyclic computational graph organized into $L$ sequential layers:
- **Input Layer ($l = 0$):** Receives raw feature vector $\mathbf{x} \in \mathbb{R}^{M_0}$.
- **Hidden Layers ($l = 1, 2, \dots, L-1$):** Intermediate representation layers containing $M_l$ neurons. Each layer extracts progressively more abstract latent representations.
- **Output Layer ($l = L$):** Produces the final prediction $\hat{\mathbf{y}} \in \mathbb{R}^{M_L}$.

##### 2. Forward Propagation Mechanism
Information flows strictly forward from input to output. For each layer $l = 1, 2, \dots, L$:
1. **Linear Affine Combination:**  
   $$\mathbf{z}^{[l]} = \mathbf{W}^{[l]} \mathbf{a}^{[l-1]} + \mathbf{b}^{[l]}$$
   where $\mathbf{W}^{[l]} \in \mathbb{R}^{M_l \times M_{l-1}}$ is the weight matrix, $\mathbf{b}^{[l]} \in \mathbb{R}^{M_l}$ is the bias vector, and $\mathbf{a}^{[l-1]}$ is the activation from the previous layer (with $\mathbf{a}^{[0]} = \mathbf{x}$).
2. **Non-linear Activation:**  
   $$\mathbf{a}^{[l]} = \phi^{[l]}(\mathbf{z}^{[l]})$$
   At the output layer, $\hat{\mathbf{y}} = \mathbf{a}^{[L]}$. A scalar loss $\mathcal{L}(\hat{\mathbf{y}}, \mathbf{y})$ is computed against target $\mathbf{y}$.

##### 3. Backpropagation Training Algorithm
Backpropagation executes reverse-mode automatic differentiation using the multivariate chain rule to calculate $\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}}$ and $\frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}}$:

1. **Step 1: Compute Output Layer Error ($\boldsymbol{\delta}^{[L]}$):**  
   Define layer error vector $\boldsymbol{\delta}^{[l]} \equiv \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{[l]}}$. For the output layer:
   $$\boldsymbol{\delta}^{[L]} = \frac{\partial \mathcal{L}}{\partial \mathbf{a}^{[L]}} \odot \phi'(\mathbf{z}^{[L]})$$
   *(Note: For cross-entropy loss with sigmoid/softmax activation, this simplifies directly to $\boldsymbol{\delta}^{[L]} = \mathbf{a}^{[L]} - \mathbf{y}$).*

2. **Step 2: Backward Error Propagation through Hidden Layers ($l = L-1, \dots, 1$):**  
   The error signal propagates backward via transpose weight multiplication:
   $$\boldsymbol{\delta}^{[l]} = \left( (\mathbf{W}^{[l+1]})^T \boldsymbol{\delta}^{[l+1]} \right) \odot \phi'(\mathbf{z}^{[l]})$$
   where $\odot$ denotes the element-wise Hadamard product.

3. **Step 3: Weight and Bias Gradient Evaluation:**  
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}} = \boldsymbol{\delta}^{[l]} (\mathbf{a}^{[l-1]})^T, \quad \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}} = \boldsymbol{\delta}^{[l]}$$

4. **Step 4: Parameter Optimization (Gradient Descent):**  
   Parameters are updated against the gradient with learning rate $\eta$:
   $$\mathbf{W}^{[l]} := \mathbf{W}^{[l]} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}}, \quad \mathbf{b}^{[l]} := \mathbf{b}^{[l]} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}}$$

*Reference:* [[neural_networks_visual_guide#7-multilayer-feed-forward-networks|Neural Networks Guide §7]] and [[neural_networks_visual_guide#12-backpropagation-derivation|Neural Networks Guide §12]]

---
## 2024 Mid-Semester Examination Solutions

> [!tip] 🎯 Exam Hall Selection Advisory
> **Status:** Attempt All Questions (3 Questions $\times$ 10 Marks = 30 Marks).  
> **Total Marks:** 30 | **Time:** 2 Hours  
> **Reference-Grounded Coverage (18 Marks Total):**
> - **Question 1(a) [4 Marks]:** Simple Linear Regression OLS derivation. (Grounded in [[ml_foundations_regression_classification_visual_guide#4-simple-linear-regression-slr--the-least-squares-derivation|Foundations Guide §4]]). *(Note: Q1(b,c) KNN [6M] are outside course guides and deferred to [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*
> - **Question 2(c) [4 Marks]:** L1 & L2 Regularization in Logistic Regression. (Grounded in [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]]). *(Note: Q2(a,b) Decision Trees & Naive Bayes [6M] deferred to [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*
> - **Question 3 [10 Marks Complete!]:** Entire Question 3 is 100% grounded in [[neural_networks_visual_guide|Neural Networks Guide]]:
>   - Q3(a) [2M]: Biological vs Artificial Neuron mapping.
>   - Q3(b) [3M]: XOR Gate neural network & non-linear mapping.
>   - Q3(c) [5M]: Perceptron Learning Algorithm & Novikoff Convergence Proof.

---

### Question 1(a): Ordinary Least Squares Derivation for Simple Linear Regression [4 Marks]

> 1. **(a)** Estimate the Regressor Coefficients of a Simple Linear Regression Model using Least Square Method. **[4]**

#### Tier 2 Model Answer

##### 1. Problem Formulation & Objective Function
In a Simple Linear Regression (SLR) model with a single scalar predictor $x \in \mathbb{R}$ and target $y \in \mathbb{R}$, the hypothesis function is:
$$\hat{y}_i = w_1 x_i + w_0$$
Given a training dataset of $m$ observations $\{(x_i, y_i)\}_{i=1}^m$, the Ordinary Least Squares (OLS) objective minimizes the Residual Sum of Squares (RSS):
$$S(w_0, w_1) = \sum_{i=1}^m e_i^2 = \sum_{i=1}^m (y_i - \hat{y}_i)^2 = \sum_{i=1}^m (y_i - w_0 - w_1 x_i)^2$$

##### 2. Analytical Calculus Derivation via First-Order Necessary Conditions
To find the global minimum, we compute the partial derivatives with respect to $w_0$ and $w_1$ and set them to zero:

- **Step 1: Derivative with respect to intercept $w_0$:**
  $$\frac{\partial S}{\partial w_0} = \sum_{i=1}^m 2(y_i - w_0 - w_1 x_i)(-1) = -2 \sum_{i=1}^m (y_i - w_0 - w_1 x_i) = 0$$
  Dividing by $-2$ and distributing the summation:
  $$\sum_{i=1}^m y_i - m w_0 - w_1 \sum_{i=1}^m x_i = 0 \implies m w_0 = \sum_{i=1}^m y_i - w_1 \sum_{i=1}^m x_i$$
  Dividing through by the sample size $m$, where sample means are $\bar{x} = \frac{1}{m}\sum x_i$ and $\bar{y} = \frac{1}{m}\sum y_i$:
  $$\mathbf{w_0 = \bar{y} - w_1 \bar{x}}$$
  *(Physical Insight: The least squares regression line strictly passes through the centroid of the data $(\bar{x}, \bar{y})$).*

- **Step 2: Derivative with respect to slope $w_1$:**
  $$\frac{\partial S}{\partial w_1} = \sum_{i=1}^m 2(y_i - w_0 - w_1 x_i)(-x_i) = -2 \sum_{i=1}^m x_i (y_i - w_0 - w_1 x_i) = 0$$
  Substituting $w_0 = \bar{y} - w_1 \bar{x}$ into the equation:
  $$\sum_{i=1}^m x_i \Big( y_i - (\bar{y} - w_1 \bar{x}) - w_1 x_i \Big) = 0$$
  $$\sum_{i=1}^m x_i \Big( (y_i - \bar{y}) - w_1 (x_i - \bar{x}) \Big) = 0$$
  $$\sum_{i=1}^m x_i (y_i - \bar{y}) = w_1 \sum_{i=1}^m x_i (x_i - \bar{x})$$

  Using the algebraic centroid identities $\sum_{i=1}^m \bar{x}(y_i - \bar{y}) = 0$ and $\sum_{i=1}^m \bar{x}(x_i - \bar{x}) = 0$, we subtract them from the left and right hand sides respectively:
  $$\sum_{i=1}^m (x_i - \bar{x})(y_i - \bar{y}) = w_1 \sum_{i=1}^m (x_i - \bar{x})^2$$

  Solving explicitly for slope $w_1$:
  $$\mathbf{w_1 = \frac{\sum_{i=1}^m (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^m (x_i - \bar{x})^2} = \frac{\text{Cov}(x, y)}{\text{Var}(x)}}$$

The second-order partial derivative matrix (Hessian) $\mathbf{H} = \begin{bmatrix} 2m & 2\sum x_i \\ 2\sum x_i & 2\sum x_i^2 \end{bmatrix}$ is strictly positive definite (det $\mathbf{H} = 4m\sum (x_i - \bar{x})^2 > 0$), guaranteeing that $(w_0, w_1)$ is a unique global minimum.

*Reference:* [[ml_foundations_regression_classification_visual_guide#4-simple-linear-regression-slr--the-least-squares-derivation|Foundations Guide §4]]

---

### Question 2(c): Regularization Techniques in Logistic Regression [4 Marks]

> **(c)** Explain two popular regularization techniques used to prevent overfitting in logistic regression. **[4]**

#### Tier 2 Model Answer

Overfitting in logistic regression occurs when model weights grow excessively large, fitting empirical sample noise or memorizing separable data points with extreme decision margins ($\|\mathbf{w}\| \to \infty$). Two standard regularization techniques prevent this by appending norm penalties to the binary log-loss:

$$\mathcal{L}_{\text{reg}}(\mathbf{w}) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln \sigma(\mathbf{w}^T\mathbf{x}^{(i)}) + (1 - y^{(i)})\ln(1 - \sigma(\mathbf{w}^T\mathbf{x}^{(i)})) \right] + \lambda \, \Omega(\mathbf{w})$$

##### 1. $L_2$ Regularization (Ridge Logistic Regression)
- **Penalty Formulation:** $\Omega_{L_2}(\mathbf{w}) = \frac{1}{2}\|\mathbf{w}\|_2^2 = \frac{1}{2}\sum_{j=1}^n w_j^2$.
- **Mechanism:** Imposes a quadratic cost on weight magnitudes. Under gradient descent, the parameter update equation becomes:
  $$w_j := w_j - \eta \lambda w_j - \eta \frac{\partial \mathcal{L}_0}{\partial w_j} = w_j(1 - \eta \lambda) - \eta \frac{\partial \mathcal{L}_0}{\partial w_j}$$
  At every iteration, the weight is pre-multiplied by a shrinkage factor $(1 - \eta \lambda) < 1$ (**Weight Decay**).
- **Behavior:** Shrinks all weights smoothly toward zero while keeping them strictly non-zero. It stabilizes numerical convergence and handles collinear features exceptionally well by sharing weights evenly.

##### 2. $L_1$ Regularization (Lasso Logistic Regression)
- **Penalty Formulation:** $\Omega_{L_1}(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_{j=1}^n |w_j|$.
- **Mechanism:** Imposes an absolute magnitude penalty. Because $|w_j|$ has a non-differentiable sharp peak at $w_j = 0$, its sub-gradient is constant:
  $$\frac{\partial}{\partial w_j} \Omega_{L_1} = \text{sgn}(w_j) \implies w_j := w_j - \eta \lambda \, \text{sgn}(w_j) - \eta \frac{\partial \mathcal{L}_0}{\partial w_j}$$
- **Behavior (Sparsity Induction):** Applies a constant subtractive force that drives irrelevant or redundant feature coefficients exactly to zero ($w_j = 0$). This yields a sparse weight vector, performing automated feature selection and producing compact, interpretable models.

> [!caution] Exam Hall Trap Alert
> In Scikit-Learn notation, the objective uses the inverse regularization parameter $C = \frac{1}{\lambda}$. A very large $C$ corresponds to weak regularization (approaching unregularized logistic regression), whereas a small $C$ enforces aggressive regularization. Always state whether $\lambda$ or $C$ is being analyzed.

*Reference:* [[ml_foundations_regression_classification_visual_guide#11-regularization-l1-lasso-l2-ridge-and-the-c-parameter|Foundations Guide §11]]

---

### Question 3(a): Biological vs Artificial Neuron Correspondence [2 Marks]

> 3. **(a)** How do the specific parts of biological neurons correspond to their counterparts in artificial neurons? **[2]**

#### Tier 1 Model Answer

The artificial neuron model (McCulloch & Pitts, 1943; Rosenblatt, 1958) abstracts the biophysical electro-chemical transmission mechanism of biological nerve cells into mathematical operations:

| Biological Neuron Anatomy | Biophysical Function | Artificial Neuron Counterpart | Mathematical Operation / Role |
|:---|:---|:---|:---|
| **Dendrites** | Receptive filaments that receive incoming electro-chemical pulses from upstream neurons | **Input Channels / Features** | Input feature vector $\mathbf{x} = (x_1, x_2, \dots, x_n)$ |
| **Synapses** | Gaps modulating connection strength via neurotransmitter density | **Synaptic Weights** | Scalar weight values $\mathbf{w} = (w_1, w_2, \dots, w_n)$ |
| **Soma (Cell Body)** | Sums incoming dendritic membrane potentials over time and space | **Summation Junction ($\Sigma$) & Bias** | Affine combination: $z = \sum_{j=1}^n w_j x_j + b$ |
| **Axon Hillock / Axon** | Fires an action potential (spike) only if membrane voltage exceeds threshold | **Activation Function ($\phi$)** | Non-linear mapping $\hat{y} = \phi(z)$ (Step, Sigmoid, ReLU) |

*Reference:* [[neural_networks_visual_guide#1-from-brain-to-artificial-neuron|Neural Networks Guide §1]]

---

### Question 3(b): XOR Neural Network & Non-Linear Mapping [3 Marks]

> **(b)** Draw the structure of a neural network that implements an XOR gate and explain how nonlinear mapping is utilized in this implementation. **[3]**

#### Tier 2 Model Answer

![XOR Architecture and Non-linear Mapping](pyq_images/pyq_fig01_logic_gates_and_xor.png)

##### 1. XOR Neural Network Architecture
The XOR function truth table produces $1$ if and only if exactly one input is active: $\{(0, 1) \to 1, (1, 0) \to 1\}$ and $\{(0, 0) \to 0, (1, 1) \to 0\}$. It is implemented using a 2-layer network comprising an input layer, a 2-neuron hidden layer, and 1 output neuron, using step activation $\phi(z) = \mathbb{I}(z \ge 0)$:

- **Hidden Neuron 1 ($h_1$, OR function):**
  $$z_1 = x_1 + x_2 - 0.5, \quad h_1 = \phi(z_1)$$
- **Hidden Neuron 2 ($h_2$, NAND function):**
  $$z_2 = -x_1 - x_2 + 1.5, \quad h_2 = \phi(z_2)$$
- **Output Neuron ($y$, AND function over hidden features):**
  $$z_{\text{out}} = h_1 + h_2 - 1.5, \quad y = \phi(z_{\text{out}})$$

##### 2. How Non-Linear Mapping is Utilized
1. **Input Space Inseparability:** In the original input coordinate system $(x_1, x_2)$, the decision boundary would need to separate $(0, 1)$ and $(1, 0)$ from $(0, 0)$ and $(1, 1)$. These classes are non-linearly separable because their convex hulls intersect.
2. **Feature Space Transformation:** The non-linear hidden layer projects the 2D input vertices into a new hidden representation space $(h_1, h_2)$:
   - $(0, 0) \to (h_1=0, h_2=1)$ [Target $0$]
   - $(0, 1) \to (h_1=1, h_2=1)$ [Target $1$]
   - $(1, 0) \to (h_1=1, h_2=1)$ [Target $1$]
   - $(1, 1) \to (h_1=1, h_2=0)$ [Target $0$]
3. **Linear Separation in Latent Space:** Notice that both positive instances $(0, 1)$ and $(1, 0)$ collapse to the identical point $(1, 1)$ in the hidden feature space! The output neuron now effortlessly draws a single linear line $h_1 + h_2 - 1.5 = 0$ that isolates $(1, 1)$ from $(0, 1)$ and $(1, 0)$.

*Reference:* [[neural_networks_visual_guide#6-xor-needs-a-hidden-layer|Neural Networks Guide §6]] and [[activation_crossentropy_backprop_visual_guide#2-non-linear-mapping-the-circle-example|Activations Guide §2]]

---

### Question 3(c): Perceptron Learning Algorithm & Novikoff Convergence Proof [5 Marks]

> **(c)** Describe the perceptron learning algorithm for binary classification problems and prove its convergence. **[5]**

#### Tier 3 Model Answer

![Perceptron Geometry and Novikoff Proof](pyq_images/pyq_fig04_perceptron_convergence.png)

##### 1. The Perceptron Learning Algorithm (PLA)
For binary classification with training set $\{(\mathbf{x}_i, y_i)\}_{i=1}^m$ where $\mathbf{x}_i \in \mathbb{R}^{d+1}$ (with bias absorbing $x_{i, 0} = 1$) and target labels $y_i \in \{-1, +1\}$:
The perceptron prediction is:
$$\hat{y} = \text{sgn}(\mathbf{w}^T \mathbf{x}_i)$$
An instance is misclassified whenever $y_i (\mathbf{w}^T \mathbf{x}_i) \le 0$.

**Algorithm Steps:**
1. Initialize weight vector $\mathbf{w}_0 = \mathbf{0} \in \mathbb{R}^{d+1}$.
2. Iterate through training instances. If $(\mathbf{x}_i, y_i)$ is misclassified, execute the additive update rule:
   $$\mathbf{w}_{k+1} = \mathbf{w}_k + \eta \, y_i \mathbf{x}_i$$
   *(Without loss of generality, assume learning rate $\eta = 1$).*
3. Repeat until all training examples satisfy $y_i (\mathbf{w}^T \mathbf{x}_i) > 0$.

---

##### 2. Formal Proof of Convergence (Novikoff Theorem, 1962)

###### Assumptions:
1. **Linear Separability:** There exists an optimal unit weight vector $\mathbf{w}^*$ ($\|\mathbf{w}^*\| = 1$) and a positive margin $\gamma > 0$ such that for all $i = 1, \dots, m$:
   $$y_i ((\mathbf{w}^*)^T \mathbf{x}_i) \ge \gamma > 0$$
2. **Bounded Data Hypersphere:** All feature vectors are bounded within a ball of radius $R$:
   $$\|\mathbf{x}_i\| \le R \quad \forall i$$

###### The Convergence Proof:
Let $\mathbf{w}_k$ denote the weight vector after $k$ mistakes, starting from $\mathbf{w}_0 = \mathbf{0}$. Suppose at step $k$, a mistake occurs on $(\mathbf{x}_i, y_i)$, so $\mathbf{w}_{k+1} = \mathbf{w}_k + y_i \mathbf{x}_i$.

- **Step 1: Lower Bounding the Inner Product $(\mathbf{w}^*)^T \mathbf{w}_k$:**
  $$(\mathbf{w}^*)^T \mathbf{w}_{k+1} = (\mathbf{w}^*)^T (\mathbf{w}_k + y_i \mathbf{x}_i) = (\mathbf{w}^*)^T \mathbf{w}_k + y_i (\mathbf{w}^*)^T \mathbf{x}_i$$
  By linear separability, $y_i (\mathbf{w}^*)^T \mathbf{x}_i \ge \gamma$. Therefore:
  $$(\mathbf{w}^*)^T \mathbf{w}_{k+1} \ge (\mathbf{w}^*)^T \mathbf{w}_k + \gamma$$
  Since $\mathbf{w}_0 = \mathbf{0}$, telescoping across $k$ mistake updates yields:
  $$(\mathbf{w}^*)^T \mathbf{w}_k \ge k\gamma \quad \implies \quad ((\mathbf{w}^*)^T \mathbf{w}_k)^2 \ge k^2 \gamma^2 \quad \text{--- (Equation 1)}$$

- **Step 2: Upper Bounding the Squared Norm $\|\mathbf{w}_k\|^2$:**
  $$\|\mathbf{w}_{k+1}\|^2 = \|\mathbf{w}_k + y_i \mathbf{x}_i\|^2 = \|\mathbf{w}_k\|^2 + 2 y_i \mathbf{w}_k^T \mathbf{x}_i + y_i^2 \|\mathbf{x}_i\|^2$$
  Because update $k$ was triggered by a mistake, $y_i \mathbf{w}_k^T \mathbf{x}_i \le 0$. Furthermore, $y_i^2 = 1$ and $\|\mathbf{x}_i\|^2 \le R^2$. Hence:
  $$\|\mathbf{w}_{k+1}\|^2 \le \|\mathbf{w}_k\|^2 + 0 + R^2$$
  Telescoping across $k$ mistake updates from $\|\mathbf{w}_0\|^2 = 0$ yields:
  $$\|\mathbf{w}_k\|^2 \le k R^2 \quad \text{--- (Equation 2)}$$

- **Step 3: Synthesizing Bounds via Cauchy-Schwarz Inequality:**
  By the Cauchy-Schwarz inequality, for any two vectors:
  $$((\mathbf{w}^*)^T \mathbf{w}_k)^2 \le \|\mathbf{w}^*\|^2 \|\mathbf{w}_k\|^2$$
  Since $\|\mathbf{w}^*\| = 1$, substituting Equations (1) and (2):
  $$k^2 \gamma^2 \le ((\mathbf{w}^*)^T \mathbf{w}_k)^2 \le \|\mathbf{w}_k\|^2 \le k R^2$$
  $$k^2 \gamma^2 \le k R^2$$
  Dividing both sides by $k \gamma^2$ ($k > 0, \gamma > 0$):
  $$\mathbf{k \le \left(\frac{R}{\gamma}\right)^2}$$

###### Conclusion:
The total number of mistakes $k$ made by the Perceptron Learning Algorithm is strictly bounded by the finite constant $\left(\frac{R}{\gamma}\right)^2$. Consequently, the algorithm is mathematically guaranteed to terminate in a finite number of iterations and find a separating hyperplane. $\blacksquare$

*Reference:* [[neural_networks_visual_guide#4-perceptron-learning-algorithm|Neural Networks Guide §4]] and [[neural_networks_visual_guide#5-convergence-proof|Neural Networks Guide §5]]

---
## 2024 Final-Semester Examination Solutions

> [!tip] 🎯 Exam Hall Selection Advisory
> **Status:** Attempt any FOUR Questions ($12\frac{1}{2} \text{ Marks} \times 4 = 50 \text{ Marks}$).  
> **Total Marks:** 50 | **Time:** 3 Hours  
> **Optimal Reference-Grounded Strategy (37.5 Marks Grounded!):**
> 1. **Question 2 [12.5 Marks Complete!]:** **Must-Attempt Question!**
>    - Q2(a) [7M]: Derivation of Output Layer Weight Update Rule in DNN under SSE & Sigmoid.
>    - Q2(b) [5.5M]: Cross-Entropy vs Quadratic Loss in backpropagation learning.
> 2. **Question 3 [12.5 Marks Complete!]:** **Must-Attempt Question!**
>    - Q3(a) [6.5M]: Vanishing & Exploding Gradients: mechanisms, symptoms, and mathematical remedies.
>    - Q3(b) [6M]: ReLU properties, limitations (dying ReLU), and Leaky ReLU remedy.
> 3. **Question 1(a) [5.5 Marks]:** Matrix form of Multiple Linear Regression & Normal Equations derivation. *(Q1(b) SVM [7M] deferred to [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*
> 4. **Question 4(b) [7 Marks]:** Batch size, batching strategies (Batch vs SGD vs Mini-Batch), and relation to epoch. *(Q4(a) CNN sparsity [5.5M] deferred to [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*
> *(Questions 5, 6, 7, 8 on CNN architectures, AlexNet, Autoencoders, and LSTM are outside the reference guides and collected in the [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*

---

### Question 1(a): Matrix Form of Multiple Linear Regression & Normal Equations [5.5 Marks]

> 1. **(a)** Give the matrix form of a Multiple Linear Regression Model and estimate the Coefficients of it using the Least Squares Method. **[5.5]**

#### Tier 3 Model Answer

![Multiple Linear Regression Projection Geometry](pyq_images/pyq_fig05_mlr_projection_geometry.png)

##### 1. Matrix Formulation of Multiple Linear Regression (MLR)
Let a training dataset comprise $m$ instances and $n$ explanatory features: $\{(\mathbf{x}_i, y_i)\}_{i=1}^m$.  
In matrix notation:
$$\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$
where:
- $\mathbf{Y} \in \mathbb{R}^{m \times 1}$ is the observed response vector: $\mathbf{Y} = [y_1, y_2, \dots, y_m]^T$.
- $\mathbf{X} \in \mathbb{R}^{m \times (n+1)}$ is the design matrix, with a leading column of ones absorbing the intercept:
  $$\mathbf{X} = \begin{bmatrix} 1 & x_{1, 1} & x_{1, 2} & \dots & x_{1, n} \\ 1 & x_{2, 1} & x_{2, 2} & \dots & x_{2, n} \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & x_{m, 1} & x_{m, 2} & \dots & x_{m, n} \end{bmatrix}$$
- $\boldsymbol{\beta} \in \mathbb{R}^{(n+1) \times 1}$ is the unknown coefficient vector: $\boldsymbol{\beta} = [\beta_0, \beta_1, \dots, \beta_n]^T$.
- $\boldsymbol{\epsilon} \in \mathbb{R}^{m \times 1}$ is the stochastic disturbance vector with $\mathbb{E}[\boldsymbol{\epsilon}] = \mathbf{0}$ and $\text{Cov}(\boldsymbol{\epsilon}) = \sigma^2 \mathbf{I}_m$.

The predicted response vector is $\hat{\mathbf{Y}} = \mathbf{X}\hat{\boldsymbol{\beta}}$, and the residual error vector is:
$$\mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}} = \mathbf{Y} - \mathbf{X}\hat{\boldsymbol{\beta}}$$

##### 2. Estimation of Coefficients via Least Squares Method
The Ordinary Least Squares criterion minimizes the Residual Sum of Squares $S(\boldsymbol{\beta})$:
$$S(\boldsymbol{\beta}) = \|\mathbf{e}\|_2^2 = \mathbf{e}^T \mathbf{e} = (\mathbf{Y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{Y} - \mathbf{X}\boldsymbol{\beta})$$

Expanding the matrix quadratic form using vector transpose properties:
$$S(\boldsymbol{\beta}) = (\mathbf{Y}^T - \boldsymbol{\beta}^T \mathbf{X}^T)(\mathbf{Y} - \mathbf{X}\boldsymbol{\beta}) = \mathbf{Y}^T \mathbf{Y} - \mathbf{Y}^T \mathbf{X}\boldsymbol{\beta} - \boldsymbol{\beta}^T \mathbf{X}^T \mathbf{Y} + \boldsymbol{\beta}^T \mathbf{X}^T \mathbf{X} \boldsymbol{\beta}$$

Since $\mathbf{Y}^T \mathbf{X}\boldsymbol{\beta}$ is a $1 \times 1$ scalar, it equals its own transpose: $\mathbf{Y}^T \mathbf{X}\boldsymbol{\beta} = (\mathbf{Y}^T \mathbf{X}\boldsymbol{\beta})^T = \boldsymbol{\beta}^T \mathbf{X}^T \mathbf{Y}$. Thus:
$$S(\boldsymbol{\beta}) = \mathbf{Y}^T \mathbf{Y} - 2\boldsymbol{\beta}^T \mathbf{X}^T \mathbf{Y} + \boldsymbol{\beta}^T (\mathbf{X}^T \mathbf{X}) \boldsymbol{\beta}$$

Applying matrix calculus derivative rules ($\nabla_{\boldsymbol{\beta}}(\mathbf{a}^T \boldsymbol{\beta}) = \mathbf{a}$ and $\nabla_{\boldsymbol{\beta}}(\boldsymbol{\beta}^T \mathbf{A}\boldsymbol{\beta}) = 2\mathbf{A}\boldsymbol{\beta}$ for symmetric $\mathbf{A}$):
$$\nabla_{\boldsymbol{\beta}} S(\boldsymbol{\beta}) = -2\mathbf{X}^T \mathbf{Y} + 2(\mathbf{X}^T \mathbf{X})\boldsymbol{\beta}$$

Setting the gradient to the zero vector $\mathbf{0}$:
$$-2\mathbf{X}^T \mathbf{Y} + 2(\mathbf{X}^T \mathbf{X})\hat{\boldsymbol{\beta}} = \mathbf{0} \implies (\mathbf{X}^T \mathbf{X})\hat{\boldsymbol{\beta}} = \mathbf{X}^T \mathbf{Y}$$
*(These are the famous **Normal Equations**).*

Assuming $\mathbf{X}$ has full column rank ($n+1$), the Gram matrix $(\mathbf{X}^T \mathbf{X})$ is non-singular and strictly invertible. Pre-multiplying by $(\mathbf{X}^T \mathbf{X})^{-1}$ yields the unique analytical OLS estimator:
$$\mathbf{\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}}$$

##### 3. Geometric Orthogonal Projection Interpretation
As illustrated in the programmatic figure, the column vectors of $\mathbf{X}$ span an $(n+1)$-dimensional subspace $\text{Col}(\mathbf{X}) \subset \mathbb{R}^m$. The vector $\hat{\mathbf{Y}} = \mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \mathbf{Y} = \mathbf{H}\mathbf{Y}$ (where $\mathbf{H}$ is the orthogonal projection "hat" matrix) is the unique orthogonal projection of $\mathbf{Y}$ onto $\text{Col}(\mathbf{X})$, guaranteeing that the residual vector is strictly orthogonal to every feature:
$$\mathbf{X}^T \mathbf{e} = \mathbf{X}^T (\mathbf{Y} - \mathbf{X}\hat{\boldsymbol{\beta}}) = \mathbf{X}^T \mathbf{Y} - (\mathbf{X}^T \mathbf{X})(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \mathbf{Y} = \mathbf{0} \implies \mathbf{e} \perp \text{Col}(\mathbf{X})$$

*Reference:* [[ml_foundations_regression_classification_visual_guide#6-multiple-linear-regression-mlr--normal-equations-in-matrix-form|Foundations Guide §6]]

---

### Question 2(a): Backpropagation Output Layer Weight Update Derivation [7 Marks]

> 2. **(a)** Derive the weight update rule for a sample input $X = (X_1, X_2, \dots, X_n)$ at the output layer of a multi-layer feed forward neural network with $(K-1)$ hidden layers using the backpropagation learning algorithm combined with the gradient descent method. In this context, let $M_i$ denote the number of neurons in the $i$-th layer, where $i = 0, 1, 2, \dots, (K-1), K$. Here, the $K$-th layer is the output layer, and the $0$-th layer represents the input layer. Assume that a sigmoid activation function is used at each layer, and the cost function is the sum of squared errors. Please specify any additional assumptions made in this derivation. **[7]**

#### Tier 3 Model Answer

![Backpropagation Derivation at Output Layer](pyq_images/pyq_fig03_backprop_output_layer.png)

##### 1. Mathematical Notation & Explicit Assumptions
- **Network Architecture:** $K$ functional layers ($K-1$ hidden layers, layer $0$ is the input layer with $M_0 = n$ inputs, layer $K$ is the output layer with $M_K$ neurons).
- **Input Sample:** $\mathbf{X} = (X_1, X_2, \dots, X_n)^T \in \mathbb{R}^{M_0}$.
- **Activations at Layer $(K-1)$:** Let $O_{m, K-1}$ denote the output activation of the $m$-th neuron in the preceding layer $(K-1)$ for $m = 1, 2, \dots, M_{K-1}$.
- **Output Layer $K$:** For the $j$-th neuron in output layer $K$ ($j = 1, 2, \dots, M_K$):
  - Synaptic weights connecting neuron $m$ of layer $(K-1)$ to neuron $j$ of layer $K$: $\theta_{j, m, K}$ (or denoted $w_{jm}^{(K)}$).
  - Bias: $\theta_{j, 0, K}$ associated with fictitious constant activation $O_{0, K-1} = 1$.
  - Linear pre-activation:
    $$I_{j, K} = \sum_{m=0}^{M_{K-1}} \theta_{j, m, K} O_{m, K-1}$$
  - Sigmoid activation function:
    $$O_{j, K} = \sigma(I_{j, K}) = \frac{1}{1 + e^{-I_{j, K}}}$$
- **Cost Function (Sum of Squared Errors for instance $X$):**
  $$E = \frac{1}{2} \sum_{k=1}^{M_K} (y_k - O_{k, K})^2$$
  where $y_k$ is the target value for the $k$-th output unit.
- **Additional Assumptions:**
  1. The learning rate $\eta > 0$ is a constant scalar.
  2. Batch size is $1$ (stochastic online sample update for the single instance $X$).
  3. Activations and weight derivatives are continuous and twice differentiable.

---

##### 2. Step-by-Step Chain Rule Derivation

We seek the gradient of the error $E$ with respect to weight $\theta_{j, m, K}$ connecting neuron $m$ in layer $(K-1)$ to neuron $j$ in output layer $K$:
$$\frac{\partial E}{\partial \theta_{j, m, K}}$$

By the multivariate chain rule:
$$\frac{\partial E}{\partial \theta_{j, m, K}} = \frac{\partial E}{\partial I_{j, K}} \cdot \frac{\partial I_{j, K}}{\partial \theta_{j, m, K}}$$

We break this down into three fundamental factors:

- **Factor 1: Derivative of Loss with respect to Output Activation $O_{j, K}$:**
  $$E = \frac{1}{2} (y_j - O_{j, K})^2 + \frac{1}{2} \sum_{k \neq j} (y_k - O_{k, K})^2$$
  Differentiating with respect to $O_{j, K}$:
  $$\frac{\partial E}{\partial O_{j, K}} = \frac{1}{2} \cdot 2(y_j - O_{j, K})(-1) = -(y_j - O_{j, K})$$

- **Factor 2: Derivative of Output Activation with respect to Net Input $I_{j, K}$:**
  Since $O_{j, K} = \sigma(I_{j, K}) = \frac{1}{1 + e^{-I_{j, K}}}$:
  $$\frac{\partial O_{j, K}}{\partial I_{j, K}} = \frac{d}{d I_{j, K}}\left( \frac{1}{1 + e^{-I_{j, K}}} \right) = \frac{e^{-I_{j, K}}}{(1 + e^{-I_{j, K}})^2} = O_{j, K} (1 - O_{j, K})$$

- **Factor 3: Definition of the Output Layer Error Term $\delta_{j, K}$:**
  By definition of the generalized delta rule:
  $$\delta_{j, K} \equiv -\frac{\partial E}{\partial I_{j, K}} = -\left( \frac{\partial E}{\partial O_{j, K}} \cdot \frac{\partial O_{j, K}}{\partial I_{j, K}} \right)$$
  Substituting Factors 1 and 2:
  $$\delta_{j, K} = -\Big( -(y_j - O_{j, K}) \Big) \cdot O_{j, K}(1 - O_{j, K})$$
  $$\mathbf{\delta_{j, K} = (y_j - O_{j, K}) \cdot O_{j, K}(1 - O_{j, K})}$$

- **Factor 4: Derivative of Net Input with respect to Synaptic Weight $\theta_{j, m, K}$:**
  $$I_{j, K} = \sum_{p=0}^{M_{K-1}} \theta_{j, p, K} O_{p, K-1}$$
  Differentiating with respect to the specific weight $\theta_{j, m, K}$:
  $$\frac{\partial I_{j, K}}{\partial \theta_{j, m, K}} = O_{m, K-1}$$

---

##### 3. Synthesizing the Complete Weight Update Rule
Combining the factors via the chain rule:
$$\frac{\partial E}{\partial \theta_{j, m, K}} = -\delta_{j, K} \cdot O_{m, K-1}$$

Under gradient descent, each weight is updated in the direction opposite to the error gradient:
$$\theta_{j, m, K} := \theta_{j, m, K} - \eta \frac{\partial E}{\partial \theta_{j, m, K}}$$
$$\Delta \theta_{j, m, K} = -\eta \left( -\delta_{j, K} \cdot O_{m, K-1} \right) = \eta \, \delta_{j, K} \, O_{m, K-1}$$

Substituting the explicit formula for $\delta_{j, K}$:
$$\mathbf{\theta_{j, m, K} := \theta_{j, m, K} + \eta \, (y_j - O_{j, K}) \, O_{j, K}(1 - O_{j, K}) \, O_{m, K-1}}$$

For the bias parameter $\theta_{j, 0, K}$, setting the constant activation $O_{0, K-1} = 1$:
$$\mathbf{\theta_{j, 0, K} := \theta_{j, 0, K} + \eta \, (y_j - O_{j, K}) \, O_{j, K}(1 - O_{j, K})}$$

This completes the formal derivation. $\blacksquare$

*Reference:* [[neural_networks_visual_guide#12-backpropagation-derivation|Neural Networks Guide §12 (Step 1 & Step 2)]]

---

### Question 2(b): Cross-Entropy vs Quadratic Loss in Backpropagation [5.5 Marks]

> **(b)** What is the cross-entropy loss function, and how does it outperform the quadratic loss function in backpropagation learning for multilayer feedforward neural networks? **[5.5]**

#### Tier 2 Model Answer

##### 1. Definition of the Cross-Entropy Loss Function
For a multi-layer feedforward neural network performing binary classification on a single sample, let the output activation be $a = \sigma(z) \in (0, 1)$ and the target label be $y \in \{0, 1\}$. The **Binary Cross-Entropy (Log-Loss)** function derived from Bernoulli negative log-likelihood is:
$$C_{\text{CE}} = -[y \ln a + (1 - y) \ln (1 - a)]$$
For multi-class classification with $K$ classes and softmax activation $a_k = \frac{e^{z_k}}{\sum_j e^{z_j}}$:
$$C_{\text{MCE}} = -\sum_{k=1}^K y_k \ln a_k$$

In contrast, the **Quadratic Loss (Sum of Squared Errors)** is:
$$C_{\text{quad}} = \frac{1}{2}(y - a)^2$$

##### 2. Why Cross-Entropy Dramatically Outperforms Quadratic Loss
The superiority lies in the behavior of the weight update gradient when a neuron makes a **severe mistake**.

###### A. Analysis under Quadratic Loss:
Differentiating quadratic loss with respect to weight $w$:
$$\frac{\partial C_{\text{quad}}}{\partial w} = \frac{\partial C}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial w} = -(y - a) \cdot \sigma'(z) \cdot x = -(y - a) \cdot a(1 - a) \cdot x$$

Notice the multiplier $\sigma'(z) = a(1 - a)$.  
- Suppose the true label is $y = 1$, but the network is horribly wrong, outputting $a = 0.001$ ($z \approx -6.9$).
- The prediction error is huge: $(y - a) = 0.999 \approx 1$.
- However, the gradient is:
  $$\frac{\partial C_{\text{quad}}}{\partial w} = -0.999 \cdot (0.001)(0.999) \cdot x \approx -0.000998 \cdot x \approx \mathbf{0}$$
- **The Catastrophe (Learning Stall):** Even though the network made a colossal error, the weight gradient is practically zero because the neuron is trapped in the flat saturation wing of the sigmoid! The weight update $\Delta w = -\eta \frac{\partial C}{\partial w} \approx 0$ crawls to an agonizing halt.

###### B. Analysis under Cross-Entropy Loss:
Differentiating cross-entropy loss with respect to activation $a$:
$$\frac{\partial C_{\text{CE}}}{\partial a} = -\frac{y}{a} + \frac{1 - y}{1 - a} = \frac{a - y}{a(1 - a)}$$

Now computing the gradient with respect to weight $w$ via chain rule:
$$\frac{\partial C_{\text{CE}}}{\partial w} = \frac{\partial C_{\text{CE}}}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial w} = \left[ \frac{a - y}{a(1 - a)} \right] \cdot \Big[ a(1 - a) \Big] \cdot x$$

$$\mathbf{\frac{\partial C_{\text{CE}}}{\partial w} = (a - y) \cdot x}$$

##### 3. The Decisive Pedagogical Takeaway
1. **Perfect Analytic Derivative Cancellation:** The saturating term $a(1 - a) = \sigma'(z)$ in the numerator cancels identically with the denominator $a(1 - a)$ introduced by the logarithm derivative.
2. **Proportional Learning Speed:** The rate at which the network learns ($\frac{\partial C}{\partial w}$) is strictly proportional to the raw error $(a - y)$.
   - When the error is massive ($y=1, a=0.001$), $|a - y| \approx 0.999 \approx 1 \implies$ **maximum gradient speed**! The network corrects large errors rapidly.
   - When the error is negligible ($y=1, a=0.999$), $|a - y| \approx 0.001 \implies$ smooth convergence without overshoot.
3. **Loss Surface Convexity:** Paired with linear pre-activations, Cross-Entropy forms a strictly convex loss bowl with no spurious plateau saddle points, whereas Quadratic loss with sigmoid produces a non-convex, rugged landscape ridden with zero-gradient traps.

*Reference:* [[activation_crossentropy_backprop_visual_guide#7-why-squared-error-learns-slowly|Activations Guide §7]] and [[activation_crossentropy_backprop_visual_guide#8-binary-cross-entropy-and-its-gradient|Activations Guide §8]]

---

### Question 3(a): Vanishing & Exploding Gradients [6.5 Marks]

> 3. **(a)** What are vanishing and exploding gradient problems in neural networks? Discuss their effects and outline potential solutions to these problems. **[6.5]**

#### Tier 3 Model Answer

![Vanishing Gradients Mechanism](pyq_images/pyq_fig02_activations_and_gradients.png)

##### 1. Mathematical Mechanism & Causes
Consider backpropagating an error signal $\delta^{[L]}$ from output layer $L$ to layer $l$ in a deep network with activations $\mathbf{a}^{[l]} = \phi(\mathbf{z}^{[l]})$ and weight matrices $\mathbf{W}^{[l]}$:
$$\boldsymbol{\delta}^{[l]} = \left( \prod_{k=l}^{L-1} \mathbf{W}^{[k+1]T} \cdot \text{diag}\Big(\phi'(\mathbf{z}^{[k]})\Big) \right) \boldsymbol{\delta}^{[L]}$$

The magnitude of the backpropagated gradient is governed by the repeated product of two terms: the weight matrices $\mathbf{W}$ and the activation derivatives $\phi'(z)$.

- **The Vanishing Gradient Problem:**  
  Occurs when the spectral radius of the transition operator is strictly less than 1 ($\|\mathbf{W}^T \text{diag}(\phi')\| < 1$).
  - For Sigmoid, $\max \phi'(z) = 0.25$.
  - For Tanh, $\max \phi'(z) = 1.0$, with $\phi'(z) \approx 0$ for $|z| > 2.5$.  
  Multiplying $L$ sub-unitary values causes the error gradient to decay exponentially with depth:
  $$\|\boldsymbol{\delta}^{[1]}\| \le c \cdot (\lambda_{\max})^L \to \mathbf{0} \quad \text{as } L \to \infty$$
  *Effect:* Early hidden layers receive virtually zero gradient. Their weights remain frozen at their random initializations, reducing a deep network to an expensive shallow linear model.

- **The Exploding Gradient Problem:**  
  Occurs when the spectral norm of the weight matrices exceeds 1 ($\|\mathbf{W}\|_2 > 1$) over consecutive layers without saturating derivatives:
  $$\|\boldsymbol{\delta}^{[1]}\| \ge c \cdot (\lambda_{\max})^L \to \boldsymbol{\infty} \quad \text{as } L \to \infty$$
  *Effect:* Gradient vectors take massive updates, causing weights to oscillate wildly, blow up to `NaN` / `Inf`, and lead to numerical catastrophic divergence.

---

##### 2. Comprehensive Comparison Matrix of Solutions
| Pathology | Primary Root Cause | Practical Symptoms | Proven Structural / Algorithmic Solutions |
|:---|:---|:---|:---|
| **Vanishing Gradients** | Saturating activations ($\sigma, \tanh$), inappropriate random weight initialization | Training loss stops decreasing early; deeper layers learn, early layers freeze ($\|\nabla_{\mathbf{W}_1}\| \approx 0$). | 1. **Non-saturating Activations:** Replace Sigmoid/Tanh with **ReLU** or **Leaky ReLU** ($\phi'=1$ for $z>0$).<br>2. **Proper Weight Initialization:** **He (Kaiming) Initialization** ($\text{Var}(W) = \frac{2}{n_{\text{in}}}$) for ReLU; **Xavier/Glorot** ($\text{Var}(W) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$) for Tanh.<br>3. **Batch Normalization:** Restricts pre-activations $z$ to unit variance, preventing saturation.<br>4. **Residual Connections (ResNets):** Shortcut connections $\mathbf{x} + \mathcal{F}(\mathbf{x})$ provide an uninterrupted identity gradient highway $\nabla(\mathbf{x} + \mathcal{F}) = \mathbf{I} + \nabla \mathcal{F}$. |
| **Exploding Gradients** | Excessively large initial weights, deep recurrent feedback, large learning rates | Loss suddenly spikes to `NaN` or `Inf`; weights explode; extreme parameter oscillation. | 1. **Gradient Clipping:** Rescales gradients if their $L_2$ norm exceeds a threshold $c$: $\mathbf{g} := \mathbf{g} \cdot \frac{c}{\max(c, \|\mathbf{g}\|_2)}$.<br>2. **Proper Weight Initialization:** Avoids large eigenvalues in initial weight matrices.<br>3. **Weight Regularization ($L_2$ Weight Decay):** Penalizes $\|\mathbf{w}\|_2^2$, exerting continuous contraction force.<br>4. **Reduced Learning Rate with Schedulers:** Warmup followed by cosine/exponential decay. |

*Reference:* [[neural_networks_visual_guide#11-problems-minima-saddles-vanishing-and-exploding-gradients|Neural Networks Guide §11]] and [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Activations Guide §5]]

---

### Question 3(b): ReLU Properties, Limitations & Leaky ReLU Solution [6 Marks]

> **(b)** Explain the Rectified Linear Unit (ReLU) activation function, highlighting its key properties and limitations. How does the Leaky ReLU activation function help address these limitations? **[6]**

#### Tier 2 Model Answer

![ReLU and Leaky ReLU Dynamics](pyq_images/pyq_fig02_activations_and_gradients.png)

##### 1. Definition and Key Properties of ReLU
The Rectified Linear Unit (ReLU), introduced by Nair & Hinton (2010), is defined piecewise as:
$$f(z) = \max(0, z) = \begin{cases} z & \text{if } z \ge 0 \\ 0 & \text{if } z < 0 \end{cases}$$
Its derivative is:
$$f'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z < 0 \end{cases}$$

**Key Properties & Advantages:**
1. **Zero Vanishing Gradient in the Positive Regime:** For all $z > 0$, the derivative is strictly $1.0$. The gradient passes through without attenuation, allowing deep networks (100+ layers) to train efficiently.
2. **Induction of True Representation Sparsity:** Any neuron receiving negative net input ($z \le 0$) outputs an exact zero ($a = 0$). In any forward pass, typically 50–70% of neurons are inactive, resulting in sparse, disentangled, and computationally efficient latent representations.
3. **Extreme Computational Simplicity:** Involves zero transcendental functions ($e^z$), logarithms, or divisions; evaluated via a simple CPU/GPU conditional branch or bitwise comparison (`z > 0 ? z : 0`), accelerating training throughput by $6\times$ compared to Sigmoid/Tanh.

##### 2. Limitations of Standard ReLU
1. **Non-Zero-Centered Outputs:** Because $f(z) \ge 0$ for all $z$, all activation outputs entering the subsequent layer are strictly non-negative ($\mathbf{a} \ge \mathbf{0}$). This forces all weight gradients into the same sign quadrant ($\frac{\partial \mathcal{L}}{\partial w_j} = \delta \cdot a_j$), inducing inefficient, oscillating "zig-zag" gradient updates.
2. **The "Dying ReLU" Problem (Permanent Neuronal Deactivation):**  
   If a large negative gradient update knocks a neuron's bias and weights such that $z = \mathbf{w}^T \mathbf{x} + b < 0$ for **all** training samples, the neuron outputs $0$ and its derivative becomes strictly $0$ ($f'(z) = 0$). Because backpropagation scales by $f'(z)$, no error signal ever flows through this neuron again:
   $$\Delta \mathbf{w} \propto f'(z) = 0$$
   The neuron is "dead"—it permanently ceases to learn or fire, effectively reducing network parameter capacity.

##### 3. How Leaky ReLU Resolves the Dying ReLU Problem
Leaky ReLU (Maas et al., 2013) introduces a tiny, non-zero slope $\alpha$ (typically $\alpha = 0.01$) in the negative domain:
$$f_{\text{Leaky}}(z) = \max(\alpha z, z) = \begin{cases} z & \text{if } z > 0 \\ \alpha z & \text{if } z \le 0 \end{cases}$$
Its derivative is:
$$f'_{\text{Leaky}}(z) = \begin{cases} 1 & \text{if } z > 0 \\ \alpha & \text{if } z \le 0 \end{cases}$$

- **Rescue from Death:** For negative net inputs ($z \le 0$), the neuron maintains a constant non-zero gradient $\alpha = 0.01$. The backpropagated error signal is:
  $$\Delta \mathbf{w} \propto \alpha \cdot \mathbf{x} \neq 0$$
  This allows the gradient descent optimizer to push the weights back into the active positive domain over subsequent training iterations, completely preventing permanent neuronal death.

*Reference:* [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Activations Guide §5]] and [[neural_networks_visual_guide#8-activation-functions|Neural Networks Guide §8]]

---

### Question 4(b): Batch Size, Batching Strategies & Epoch Relationship [7 Marks]

> 4. **(b)** What is meant by batch size in the context of gradient descent? Explain the different batching strategies used in gradient descent, along with their merits and demerits. How is batch size related to an epoch in these batching strategies? **[1 + 4.5 + 1.5 = 7]**

#### Tier 3 Model Answer

##### 1. Definition of Batch Size [1 Mark]
In gradient descent optimization, the **batch size ($B$)** denotes the number of distinct training exemplars propagated forward through the neural network to evaluate loss and backward to accumulate error gradients **before executing a single update step** to the model parameters $\boldsymbol{\theta}$.

##### 2. Comprehensive Comparison of Batching Strategies [4.5 Marks]

$$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \cdot \mathbf{g}_t, \quad \text{where } \mathbf{g}_t = \frac{1}{B} \sum_{i \in \mathcal{B}_t} \nabla_{\boldsymbol{\theta}} \mathcal{L}_i(\boldsymbol{\theta}_t)$$

| Dimension | Batch Gradient Descent (BGD) | Stochastic Gradient Descent (SGD) | Mini-Batch Gradient Descent (MBGD) |
|:---|:---|:---|:---|
| **Batch Size ($B$)** | **Entire Dataset ($B = m$)** | **Single Sample ($B = 1$)** | **Subset ($1 < B < m$), typically $32, 64, 128, 256$** |
| **Gradient Nature** | True, exact deterministic gradient of total empirical risk | Extremely noisy, high-variance unbiased estimator of true gradient | Low-variance, stable unbiased estimator of true gradient |
| **Optimization Trajectory** | Smooth, direct monotonic descent down the loss bowl | Highly erratic, noisy, stochastic random walk | Smooth descent with healthy exploration noise |
| **Escaping Saddle Points** | ❌ Gets easily stuck in flat saddle points and bad local minima | ✅ Stochastic kicks easily knock weights out of shallow local minima | ✅ Sufficient gradient noise escapes sharp minima, converges to flat minima |
| **Hardware Utilization** | Inefficient for big data; easily causes GPU Out-Of-Memory (OOM) | Poor; cannot exploit SIMD/tensor core parallelism on modern GPUs | **Optimal**; maximizes GPU tensor core concurrency and cache utilization |
| **Convergence Guarantee** | Guaranteed asymptotic convergence to stationary point with fixed $\eta$ | Requires decaying learning rate ($\eta_t = \frac{\eta_0}{1 + \alpha t}$) to avoid oscillating around minimum | Rapid, stable convergence to superior generalizable minima |

##### 3. Mathematical Relationship: Batch Size and Epoch [1.5 Marks]
- **Definition of an Epoch:** An **epoch** is defined as one complete, exhaustive pass through the entire training dataset of $m$ examples.
- **Mathematical Formula:**  
  The number of parameter update iterations per epoch ($N_{\text{iter}}$) is determined by:
  $$N_{\text{iter}} = \left\lceil \frac{m}{B} \right\rceil$$

###### Quantitative Relationship across the Three Strategies:
1. **Batch Gradient Descent ($B = m$):**  
   $$N_{\text{iter}} = \frac{m}{m} = \mathbf{1} \text{ update per epoch}$$
   A single step occurs only after evaluating all $m$ samples. For 100 epochs, exactly 100 weight updates occur.
2. **Stochastic Gradient Descent ($B = 1$):**  
   $$N_{\text{iter}} = \frac{m}{1} = \mathbf{m} \text{ updates per epoch}$$
   Parameters are updated $m$ times in every epoch. If $m = 100,000$, 100,000 updates occur in a single epoch.
3. **Mini-Batch Gradient Descent ($1 < B < m$):**  
   $$N_{\text{iter}} = \frac{m}{B} \text{ updates per epoch}$$
   *Concrete Example:* For an ImageNet subset with $m = 128,000$ images trained with mini-batch size $B = 64$:
   $$N_{\text{iter}} = \frac{128,000}{64} = \mathbf{2,000} \text{ weight updates per epoch}$$
   If training spans $50$ epochs, the network executes $50 \times 2,000 = 100,000$ gradient descent updates.

*Reference:* [[neural_networks_visual_guide#10-learning-rate-batches-and-epochs|Neural Networks Guide §10]] and [[ml_foundations_regression_classification_visual_guide#14-optimization-solvers-in-logistic-regression|Foundations Guide §14]]

---
## 2023 Mid-Semester Examination Solutions

> [!tip] 🎯 Exam Hall Selection Advisory
> **Status:** Answer any THREE questions ($3 \text{ Questions} \times 10 \text{ Marks} = 30 \text{ Marks}$).  
> **Total Marks:** 30 | **Time:** 2 Hours  
> **Golden Reference-Grounded Strategy (27 Marks Grounded!):**
> 1. **Question 3 [10 Marks Complete!]:** **Top-Priority Choice!**
>    - Q3(a) [5M]: Why Linear Regression fails for classification & Why MSE fails for Logistic Regression.
>    - Q3(b) [5M]: One-vs-All ($c$ classifiers) vs One-vs-One ($c(c-1)/2$ classifiers) multiclass classification.
> 2. **Question 4 [10 Marks Complete!]:** **Top-Priority Choice!**
>    - Q4(a) [3M]: Numerical evaluation of 3-input neuron with bias and sigmoid activation ($z = 0.45 \implies y = 0.6106$).
>    - Q4(b) [7M]: Analytical log-likelihood derivation for parameter $p$ in $N$ Bernoulli coin tosses.
> 3. **Question 1(a) [7 Marks]:** Gradient descent weight update derivation for non-linear polynomial hypothesis $h_\theta(x) = \theta_0 + \sum_{j=1}^n \theta_j(x_j + x_j^2)$ in form $\theta_j := \theta_j + \dots$.
> *(Questions 1(b), 2, and 5 cover SVM Kernels/KKT and RNN cells, which are deferred to the [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*

---

### Question 1(a): Gradient Descent Derivation for Polynomial Hypothesis [7 Marks]

> 1. **(a)** Derive a gradient descent training algorithm that minimizes the sum of the squared error cost function, for the following hypothesis:
>    
>    $$h_\theta(x) = \theta_0 + \theta_1 x_1 + \theta_1 x_1^2 + \theta_2 x_2 + \theta_2 x_2^2 + \dots + \theta_n x_n + \theta_n x_n^2$$
>    
>    where $(x_1, x_2, \dots, x_n)$ represents an instance having $n$ features and $\theta_i, 0 \le i \le n$ represents the parameters to be learned. Assume that there are $m$ instances in the training set. Express the answer in the form $\theta_j := \theta_j + \dots$ for $1 \le j \le n$. **[7]**

#### Tier 3 Model Answer

##### 1. Problem Formulation & Compact Notation
We are given a training dataset of $m$ instances: $\{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^m$, where $\mathbf{x}^{(i)} = (x_1^{(i)}, x_2^{(i)}, \dots, x_n^{(i)})^T \in \mathbb{R}^n$ and $y^{(i)} \in \mathbb{R}$.

The given parametric hypothesis $h_{\boldsymbol{\theta}}(\mathbf{x})$ ties the linear and quadratic terms of feature $j$ to the **same parameter $\theta_j$**:
$$h_{\boldsymbol{\theta}}(\mathbf{x}) = \theta_0 + \sum_{j=1}^n \theta_j \left( x_j + x_j^2 \right)$$

Let us define a composite feature variable $u_j \equiv x_j + x_j^2$ for $j = 1, \dots, n$, with $u_0 \equiv 1$. Then:
$$h_{\boldsymbol{\theta}}(\mathbf{x}) = \theta_0 + \sum_{j=1}^n \theta_j u_j$$

The standard Sum of Squared Errors (SSE) cost function over the $m$ training instances is:
$$J(\boldsymbol{\theta}) = \frac{1}{2} \sum_{i=1}^m \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right)^2$$
*(The scalar factor $\frac{1}{2}$ simplifies subsequent algebra without altering the parameter location of the minimum).*

---

##### 2. Step-by-Step Analytical Derivative

Under gradient descent, each parameter $\theta_j$ is adjusted iteratively along the negative gradient:
$$\theta_j := \theta_j - \alpha \frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j}$$
where $\alpha > 0$ is the learning rate.

Applying the chain rule of differential calculus to $J(\boldsymbol{\theta})$:
$$\frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j} = \frac{\partial}{\partial \theta_j} \left[ \frac{1}{2} \sum_{i=1}^m \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right)^2 \right] = \sum_{i=1}^m \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right) \cdot \frac{\partial h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)})}{\partial \theta_j}$$

Now we evaluate the partial derivative of the hypothesis $\frac{\partial h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)})}{\partial \theta_j}$:

- **For feature parameters $1 \le j \le n$:**
  $$h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) = \theta_0 + \theta_1 (x_1^{(i)} + (x_1^{(i)})^2) + \dots + \theta_j (x_j^{(i)} + (x_j^{(i)})^2) + \dots + \theta_n (x_n^{(i)} + (x_n^{(i)})^2)$$
  Differentiating with respect to $\theta_j$:
  $$\frac{\partial h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)})}{\partial \theta_j} = x_j^{(i)} + (x_j^{(i)})^2$$

- **Substituting back into the gradient expression:**
  $$\frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j} = \sum_{i=1}^m \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right) \left( x_j^{(i)} + (x_j^{(i)})^2 \right)$$

---

##### 3. Expressing in the Required Update Form: $\theta_j := \theta_j + \dots$
Substituting $\frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j}$ into the gradient descent update equation:
$$\theta_j := \theta_j - \alpha \sum_{i=1}^m \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right) \left( x_j^{(i)} + (x_j^{(i)})^2 \right)$$

Distributing the negative sign into the error residual term:
$$-\left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right) = \left( y^{(i)} - h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) \right)$$

Therefore, the exact gradient descent training algorithm expressed in the requested update form for $1 \le j \le n$ is:
$$\mathbf{\theta_j := \theta_j + \alpha \sum_{i=1}^m \left( y^{(i)} - h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) \right) \left( x_j^{(i)} + (x_j^{(i)})^2 \right)}$$

*(For completeness, the intercept parameter update is: $\theta_0 := \theta_0 + \alpha \sum_{i=1}^m \left( y^{(i)} - h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) \right)$).*

> [!caution] Exam Hall Trap Alert
> Note the explicit question requirement: *"Express the answer in the form $\theta_j := \theta_j + \dots$"*. If you write $\theta_j := \theta_j - \alpha \sum (y^{(i)} - h_\theta(x^{(i)}))\dots$, it is an algebraic sign error that will forfeit 2–3 marks. The positive update sign requires the residual $(y^{(i)} - h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}))$.

*Reference:* [[ml_foundations_regression_classification_visual_guide#4-simple-linear-regression-slr--the-least-squares-derivation|Foundations Guide §4]] and [[neural_networks_visual_guide#9-gradient-descent-and-the-delta-rule|Neural Networks Guide §9]]

---

### Question 3(a): Why Linear Regression Fails for Classification & Why MSE Fails for Logistic [5 Marks]

> 3. **(a)** State two reasons why linear regression is not ideal for use in classification. Why is the mean squared error cost function not used with logistic regression? Write the cost function that is used instead. **[5]**

#### Tier 2 Model Answer

##### 1. Two Reasons Why Linear Regression Fails for Classification [2 Marks]
1. **Unbounded Continuous Outputs (Probability Axiom Violation):**  
   Linear regression fits a linear hyperplane $h_{\mathbf{w}}(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b$. Its range is the entire real line $(-\infty, +\infty)$. For extreme feature values, it outputs predictions like $\hat{y} = -2.7$ or $\hat{y} = +4.3$. These values cannot be interpreted as valid posterior class probabilities because Kolmogorov probability axioms strictly require $P(Y=1|\mathbf{X}) \in [0, 1]$.
2. **Sensitivity to Extreme Outliers (Decision Boundary Distortion):**  
   Ordinary Least Squares minimizes squared residuals $(y - \mathbf{w}^T \mathbf{x})^2$. If an unambiguous, correct positive exemplar is placed far to the right of the existing positive cluster ($x \gg 0, y=1$), linear regression incurs a massive squared error penalty $(1 - 10)^2 = 81$ for having $\hat{y} \gg 1$. To minimize this irrelevant penalty on an already correct point, the regression line tilts dramatically, shifting the decision threshold ($h_{\mathbf{w}}(\mathbf{x}) = 0.5$) and causing severe misclassifications in the boundary region.

```
Linear Regression Sensitivity to Outlier:
   y
 1 +          o  o  o  o                         O (Outlier: y=1, huge x)
   |                                            /
0.5+-----------------x-------x'----------------/--- Threshold
   |                /       /                 /
 0 +   *  *  *  *  /       /                 /
   +--------------/-------/-----------------+------------------> x
             Original   Shifted by Outlier
             Boundary   (Misclassifies 'o' points!)
```

---

##### 2. Why Mean Squared Error (MSE) Fails with Logistic Regression [2 Marks]
If we compose the non-linear logistic sigmoid function $\hat{y} = \sigma(z) = \frac{1}{1 + e^{-\mathbf{w}^T \mathbf{x}}}$ with the Mean Squared Error loss function:
$$J_{\text{MSE}}(\mathbf{w}) = \frac{1}{2m} \sum_{i=1}^m \left( y^{(i)} - \sigma(\mathbf{w}^T \mathbf{x}^{(i)}) \right)^2$$

- **Loss Surface Non-Convexity:**  
  The sigmoid function has non-linear inflection points where its second derivative changes sign. Composing this with the quadratic square function creates an objective function whose Hessian $\nabla^2 J_{\text{MSE}}(\mathbf{w})$ is **non-positive-semidefinite**. The loss surface is **non-convex**, riddled with numerous spurious local minima, plateau saddle points, and flat ridges. Gradient descent becomes trapped in suboptimal local minima.
- **Severe Learning Saturation:**  
  The gradient is $\frac{\partial J_{\text{MSE}}}{\partial \mathbf{w}} = -(y - \hat{y}) \cdot \hat{y}(1 - \hat{y}) \cdot \mathbf{x}$. When the model makes an extremely confident wrong prediction ($y=1, \hat{y}=0.001$), $\hat{y}(1-\hat{y}) \approx 0$, causing the gradient to vanish and freezing learning when error is highest.

---

##### 3. The Correct Cost Function Used Instead [1 Mark]
Instead of MSE, we use **Binary Cross-Entropy (Log-Loss)**, derived from the Maximum Likelihood Estimation of a Bernoulli distribution:
$$\mathbf{J_{\text{BCE}}(\mathbf{w}) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln \sigma(\mathbf{w}^T \mathbf{x}^{(i)}) + (1 - y^{(i)}) \ln \Big(1 - \sigma(\mathbf{w}^T \mathbf{x}^{(i)})\Big) \right]}$$

- **Guaranteed Convexity:** $J_{\text{BCE}}(\mathbf{w})$ is strictly convex with respect to $\mathbf{w}$ (its Hessian is positive semi-definite: $\mathbf{H} = \frac{1}{m}\mathbf{X}^T \mathbf{S} \mathbf{X} \succeq \mathbf{0}$, where $S_{ii} = \hat{y}_i(1-\hat{y}_i) > 0$). Gradient descent is mathematically guaranteed to converge to the unique global minimum.

*Reference:* [[ml_foundations_regression_classification_visual_guide#8-why-linear-regression-fails-for-classification|Foundations Guide §8]] and [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Foundations Guide §10.1]]

---

### Question 3(b): Multiclass Classification: One-vs-All vs One-vs-One [5 Marks]

> **(b)** Explain briefly how multiclass classification can be performed with the binary logistic regression classifier using the following strategies: (i) One-vs-All and (ii) One-vs-One. If $c$ is the number of classes and $m$ is the number of training examples, state the number of binary classifiers required in each case. **[5]**

#### Tier 2 Model Answer

Binary logistic regression naturally distinguishes between two classes. When confronted with a multiclass classification task involving $c \ge 3$ discrete classes and $m$ training instances, two classic decomposition meta-strategies adapt binary classifiers:

##### 1. One-vs-All (OvA) / One-vs-Rest (OvR) Strategy
- **Working Mechanism:**  
  Trains an independent binary classifier for each individual class $k \in \{1, 2, \dots, c\}$. For classifier $k$, instances belonging to class $k$ are designated positive ($+1$), and all instances belonging to the remaining $c-1$ classes are aggregated into a single negative class ($0$).
- **Inference Decision Rule:**  
  For an unseen query instance $\mathbf{x}$, all $c$ models output probability estimates $\hat{p}_k(\mathbf{x}) = \sigma(\mathbf{w}_k^T \mathbf{x} + b_k)$. The instance is assigned to the class with the highest confidence score:
  $$\hat{y} = \arg\max_{k \in \{1, \dots, c\}} \hat{p}_k(\mathbf{x})$$
- **Number of Binary Classifiers Required:**
  $$\mathbf{N_{\text{OvA}} = c}$$
- **Data per Classifier:** Each classifier trains on the full dataset of $m$ examples (inheriting artificial class imbalance ratio of $1 : (c-1)$).

---

##### 2. One-vs-One (OvO) Strategy
- **Working Mechanism:**  
  Trains a dedicated binary classifier for **every unique pair of classes** $(i, j)$ where $1 \le i < j \le c$. All training examples not belonging to class $i$ or class $j$ are filtered out and ignored for that classifier.
- **Inference Decision Rule (Max-Voting Scheme):**  
  For an unseen test point $\mathbf{x}$, all pair classifiers evaluate $\mathbf{x}$. If classifier $(i, j)$ predicts class $i$, class $i$ receives $+1$ vote. The instance is assigned to the majority winner:
  $$\hat{y} = \arg\max_{k \in \{1, \dots, c\}} \sum_{j \neq k} \text{Vote}_{k, j}(\mathbf{x})$$
- **Number of Binary Classifiers Required:**  
  Determined by the combination formula $\binom{c}{2}$:
  $$\mathbf{N_{\text{OvO}} = \frac{c(c - 1)}{2}}$$
- **Data per Classifier:** Each classifier trains only on a small subset of size approximately $\frac{2m}{c}$ examples (assuming balanced classes).

---

##### 3. Systematic Summary Table
| Strategy | Number of Classifiers ($N$) | Training Samples per Classifier | Computational Complexity | Primary Vulnerability |
|:---|:---:|:---:|:---|:---|
| **One-vs-All (OvA)** | $\mathbf{c}$ | Full $m$ samples | $\mathcal{O}(c \cdot m)$ | Imbalanced training sets ($1$ vs $c-1$); uncalibrated probability scales between independent classifiers |
| **One-vs-One (OvO)** | $\mathbf{\frac{c(c-1)}{2}}$ | $\approx \frac{2m}{c}$ samples | $\mathcal{O}(c^2 \cdot \frac{m}{c}) = \mathcal{O}(c \cdot m)$ | Ambiguous voting ties; quadratic classifier explosion for large $c$ |

*Reference:* [[ml_foundations_regression_classification_visual_guide#12-multiclass-classification-one-vs-rest-vs-multinomial-softmax|Foundations Guide §12.1]]

---

### Question 4(a): Single Neuron Forward Pass Numerical [3 Marks]

> 4. **(a)** Calculate the output $y$ of a three input neuron with bias. The input feature vector is $(x_1, x_2, x_3) = (0.8, 0.6, 0.4)$ and weight values are $[w_1, w_2, w_3, b] = [0.2, 0.1, -0.3, 0.35]$. Use binary sigmoid function as activation function. **[3]**

#### Tier 2 Model Answer & Numerical Audit

##### 1. Mathematical Formulation
An artificial neuron performs two sequential operations:
1. **Affine Combination (Net Input $z$):**
   $$z = \sum_{j=1}^3 w_j x_j + b = w_1 x_1 + w_2 x_2 + w_3 x_3 + b$$
2. **Non-linear Sigmoid Activation:**
   $$y = \sigma(z) = \frac{1}{1 + e^{-z}}$$

##### 2. Step-by-Step Calculation
- **Given Inputs & Parameters:**
  - Feature Vector: $x_1 = 0.8, \; x_2 = 0.6, \; x_3 = 0.4$
  - Weights & Bias: $w_1 = 0.2, \; w_2 = 0.1, \; w_3 = -0.3, \; b = 0.35$

- **Step 1: Compute Linear Pre-activation ($z$):**
  $$z = (0.2 \times 0.8) + (0.1 \times 0.6) + (-0.3 \times 0.4) + 0.35$$
  $$z = 0.1600 + 0.0600 - 0.1200 + 0.3500$$
  $$z = 0.2200 - 0.1200 + 0.3500 = 0.1000 + 0.3500$$
  $$\mathbf{z = 0.4500}$$

- **Step 2: Evaluate Sigmoid Activation ($y = \sigma(0.45)$):**
  $$y = \frac{1}{1 + e^{-0.4500}}$$
  Evaluating $e^{-0.45}$:
  $$e^{-0.45} \approx 0.63762815$$
  Evaluating the denominator:
  $$1 + e^{-0.45} \approx 1 + 0.63762815 = 1.63762815$$
  Evaluating the quotient:
  $$y = \frac{1}{1.63762815} \approx \mathbf{0.610639}$$

##### 3. Final Conclusion
The output of the three-input neuron is:
$$\mathbf{y \approx 0.6106 \quad (61.06\%)}$$

*Reference:* [[neural_networks_visual_guide#1-from-brain-to-artificial-neuron|Neural Networks Guide §1]] and [[activation_crossentropy_backprop_visual_guide#4-sigmoid-function|Activations Guide §4]]

---

### Question 4(b): Log-Likelihood Derivation for Biased Coin Toss [7 Marks]

> **(b)** Consider a situation where a biased coin with probability of head ($p$) is tossed $N$ times and the outcomes ($\text{head}=1, \text{tail}=0$) are recorded in random variables, $x_n, n = 1, 2, \dots, N$. Derive the log-likelihood function for estimating parameter $p$. **[7]**

#### Tier 3 Model Answer

##### 1. Probabilistic Modeling & Likelihood Function
Let each coin toss outcome be represented by an independent and identically distributed (i.i.d.) Bernoulli random variable $X_n \in \{0, 1\}$ with parameter $p = P(X_n = 1)$ (where $0 < p < 1$):
- $P(X_n = 1) = p$ (Head)
- $P(X_n = 0) = 1 - p$ (Tail)

The probability mass function (PMF) for a single observation $x_n$ is expressed in exponential form:
$$P(X_n = x_n \mid p) = p^{x_n} (1 - p)^{1 - x_n}$$
- If $x_n = 1 \implies p^1 (1 - p)^0 = p$.
- If $x_n = 0 \implies p^0 (1 - p)^1 = 1 - p$.

Since the $N$ coin tosses are statistically independent, the joint probability (Likelihood function $L(p)$) of observing the sequence $\mathcal{D} = \{x_1, x_2, \dots, x_N\}$ is the product of individual probabilities:
$$L(p) = P(\mathcal{D} \mid p) = \prod_{n=1}^N P(X_n = x_n \mid p) = \prod_{n=1}^N p^{x_n} (1 - p)^{1 - x_n}$$

---

##### 2. Derivation of the Log-Likelihood Function
Because the product $\prod$ is computationally unwieldy and prone to numerical underflow, we apply the strictly monotonic natural logarithm function ($\ln$), which preserves the location of the extremum:

$$\ell(p) = \ln L(p) = \ln \left( \prod_{n=1}^N p^{x_n} (1 - p)^{1 - x_n} \right)$$

Using the logarithmic identity $\ln(A \cdot B) = \ln A + \ln B$:
$$\ell(p) = \sum_{n=1}^N \ln \left( p^{x_n} (1 - p)^{1 - x_n} \right)$$

Applying power rules $\ln(A^B) = B \ln A$:
$$\mathbf{\ell(p) = \sum_{n=1}^N \Big[ x_n \ln p + (1 - x_n) \ln (1 - p) \Big]}$$

Expanding the sum across the dataset:
$$\ell(p) = \ln p \sum_{n=1}^N x_n + \ln(1 - p) \sum_{n=1}^N (1 - x_n)$$

Let $k = \sum_{n=1}^N x_n$ denote the total number of heads observed in $N$ tosses, so $(N - k) = \sum_{n=1}^N (1 - x_n)$ represents the total number of tails:
$$\mathbf{\ell(p) = k \ln p + (N - k) \ln (1 - p)}$$

---

##### 3. Maximum Likelihood Estimator (MLE) Closed-Form Solution
To find the parameter $\hat{p}_{\text{MLE}}$ that maximizes $\ell(p)$, we compute the first derivative (the Fisher Score) and set it to zero:
$$\frac{d \ell(p)}{dp} = \frac{d}{dp} \left[ k \ln p + (N - k) \ln (1 - p) \right] = \frac{k}{p} - \frac{N - k}{1 - p} = 0$$

Equating the fractions:
$$\frac{k}{p} = \frac{N - k}{1 - p} \implies k(1 - p) = p(N - k)$$
$$k - k p = N p - k p \implies k = N p$$
$$\mathbf{\hat{p}_{\text{MLE}} = \frac{k}{N} = \frac{1}{N} \sum_{n=1}^N x_n}$$

Checking the second derivative to verify strict concavity (maximum):
$$\frac{d^2 \ell(p)}{dp^2} = -\frac{k}{p^2} - \frac{N - k}{(1 - p)^2} < 0 \quad \text{for all } p \in (0, 1)$$
Since the second derivative is strictly negative everywhere, the log-likelihood function is strictly concave, and $\hat{p} = \frac{k}{N}$ is the unique global maximum likelihood estimator. $\blacksquare$

*Reference:* [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Foundations Guide §10.2]]

---
## 2023 End-Semester Examination Solutions

> [!tip] 🎯 Exam Hall Selection Advisory
> **Status:** Answer any FIVE questions ($5 \text{ Questions} \times 10 \text{ Marks} = 50 \text{ Marks}$).  
> **Total Marks:** 50 | **Time:** 3 Hours  
> **Reference-Grounded Strategy (24 Marks Grounded):**
> 1. **Question 1 [10 Marks Complete!]:** **Must-Attempt High-Scoring Question!**
>    - Q1(a) [3M]: Linear Regression & MSE failure for classification.
>    - Q1(b) [3M]: One-vs-All vs One-vs-One decomposition.
>    - Q1(c) [4M]: Confusion matrix numerical (Precision $= 0.50$, Recall $= 1.00$, $\text{TPR} = 1.00$, $\text{F}_1 = 0.6667$).
> 2. **Question 2 [Partially Grounded - 4 Marks]:**
>    - Q2(c) [2M]: Why Linear Regression fails for classification & MSE fails for Logistic.
>    - Q2(d) [2M]: Differences between Feed-Forward and Recurrent Networks.
> 3. **Question 3 [Partially Grounded - 4 Marks]:**
>    - Q3(a) [4M]: Significance of ReLU activation function in deep networks.
> 4. **Question 4 [Partially Grounded - 6 Marks]:**
>    - Q4(a) [3M]: Numerical evaluation of 3-input neuron with sigmoid ($z = 0.45 \implies y = 0.6106$).
>    - Q4(b) [3M]: Biased coin toss log-likelihood and SGD algorithm derivation.
> *(Other sub-questions in Q2, Q3, Q4, Q5, Q6 cover Decision Trees, K-fold CV, Max-Unpooling, CNN pooling parameters, Autoencoders, and LSTM/GRU, which are deferred to the [Final Uncovered Section](#unanswered--uncovered-questions-not-in-reference-notes)).*

---

### Question 1: Classification Foundations & Numerical [10 Marks]

#### Question 1(a): Why Linear Regression Fails for Classification & Why MSE Fails for Logistic [3 Marks]

> 1. **(a)** State two reasons why linear regression is not ideal for use in classification. Why is the mean squared error cost function not used with logistic regression? Write the cost function that is used instead. **[3]**

##### Tier 1 Model Answer

1. **Why Linear Regression Fails for Classification:**
   - **Range Violation:** Linear regression fits an unconstrained hypersurface $h(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b \in (-\infty, +\infty)$, producing unbounded continuous outputs that violate Kolmogorov probability axioms ($P \notin [0, 1]$).
   - **Outlier Sensitivity:** Squaring residuals on distant, correctly classified positive points ($x \gg 0, y=1$) incurs massive penalties, violently tilting the decision boundary and misclassifying adjacent samples.

2. **Why MSE Fails for Logistic Regression:**
   - Composing MSE with non-linear sigmoid activations yields a **non-convex loss landscape** with numerous local minima and saddle points, causing gradient descent to get trapped. Furthermore, in saturation wings ($\hat{y} \approx 0$ or $1$), the sigmoid derivative vanishes ($\sigma'(z) \approx 0$), freezing learning when error is largest.

3. **Cost Function Used Instead:**  
   **Binary Cross-Entropy (Log-Loss):**
   $$\mathbf{J(\mathbf{w}) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln \sigma(\mathbf{w}^T \mathbf{x}^{(i)}) + (1 - y^{(i)})\ln(1 - \sigma(\mathbf{w}^T \mathbf{x}^{(i)})) \right]}$$
   It is strictly convex and analytically cancels the sigmoid derivative, ensuring error-proportional gradient flow.

*Reference:* [[ml_foundations_regression_classification_visual_guide#8-why-linear-regression-fails-for-classification|Foundations Guide §8]] and [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Foundations Guide §10.1]]

---

#### Question 1(b): One-vs-All vs One-vs-One Multiclass Classification [3 Marks]

> **(b)** Explain briefly how multiclass classification can be performed with the binary classifier using the following strategies: (i) One-vs-All and (ii) One-vs-One. If $c$ is the number of classes and $m$ is the number of training examples, state the number of binary classifiers required in each case. **[3]**

##### Tier 1 Model Answer

| Meta-Strategy | Working Mechanism | Inference Decision Rule | Number of Binary Classifiers Required |
|:---|:---|:---|:---:|
| **(i) One-vs-All (OvA)** | Trains a classifier for each class $k$ treating it as positive ($+1$) and all other $c-1$ classes as negative ($0$). | Pick class with maximum probability score: $\hat{y} = \arg\max_k \hat{p}_k(\mathbf{x})$. | $\mathbf{c}$ |
| **(ii) One-vs-One (OvO)** | Trains a classifier for every pairwise combination of classes $(i, j)$ on the subset of data belonging to those two classes. | Majority voting over all pairwise predictions: $\hat{y} = \arg\max_k \sum_{j \neq k} \text{Vote}_{k, j}(\mathbf{x})$. | $\mathbf{\frac{c(c - 1)}{2}}$ |

*Reference:* [[ml_foundations_regression_classification_visual_guide#12-multiclass-classification-one-vs-rest-vs-multinomial-softmax|Foundations Guide §12.1]]

---

#### Question 1(c): Confusion Matrix Numerical [4 Marks]

> **(c)** A classifier predicts labels for two classes, positive ($p$) and negative ($n$). Calculate, with respect to class $p$: (i) precision, (ii) recall, (iii) true positive rate, and (iv) F1 score from the table below: **[4]**
> 
> | No. | Prediction | Actual class |
> | :---: | :---: | :---: |
> | 1 | p | p |
> | 2 | p | n |
> | 3 | n | n |
> | 4 | p | n |
> | 5 | p | p |

##### Tier 2 Model Answer & Numerical Audit

##### 1. Sample-by-Sample Classification Audit
With respect to positive class $p$:
- **Instance 1:** Prediction = $p$, Actual = $p \implies$ **True Positive ($\text{TP}$)**
- **Instance 2:** Prediction = $p$, Actual = $n \implies$ **False Positive ($\text{FP}$)**
- **Instance 3:** Prediction = $n$, Actual = $n \implies$ **True Negative ($\text{TN}$)**
- **Instance 4:** Prediction = $p$, Actual = $n \implies$ **False Positive ($\text{FP}$)**
- **Instance 5:** Prediction = $p$, Actual = $p \implies$ **True Positive ($\text{TP}$)**

##### 2. Contingency Counts
- **True Positives ($\text{TP}$):** $2$ (Instances 1, 5)
- **False Positives ($\text{FP}$):** $2$ (Instances 2, 4)
- **True Negatives ($\text{TN}$):** $1$ (Instance 3)
- **False Negatives ($\text{FN}$):** $0$ (No positive instances predicted as $n$)
- Total Population: $N = \text{TP} + \text{FP} + \text{TN} + \text{FN} = 2 + 2 + 1 + 0 = 5$

---

##### 3. Step-by-Step Metric Evaluations
- **(i) Precision:**
  $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}} = \frac{2}{2 + 2} = \frac{2}{4} = \mathbf{0.50 \quad (50.00\%)}$$

- **(ii) Recall:**
  $$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{2}{2 + 0} = \frac{2}{2} = \mathbf{1.00 \quad (100.00\%)}$$

- **(iii) True Positive Rate ($\text{TPR}$):**  
  By definition, True Positive Rate is mathematically identical to Recall / Sensitivity:
  $$\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{2}{2} = \mathbf{1.00 \quad (100.00\%)}$$

- **(iv) $\text{F}_1$ Score:**  
  The harmonic mean of Precision and Recall:
  $$\text{F}_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \cdot \frac{0.50 \times 1.00}{0.50 + 1.00} = \frac{1.00}{1.50} = \frac{2}{3} \approx \mathbf{0.6667 \quad (66.67\%)}$$

*Reference:* [[ml_foundations_regression_classification_visual_guide#15-linear-regression-vs-logistic-regression-the-complete-comparison|Foundations Guide §15]]

---

### Question 2(c): Failure of Linear Regression & MSE for Classification [2 Marks]

> 2. **(c)** State two reasons why linear regression is not ideal for classification. Why is mean-squared-error cost not used with logistic regression? Write the cost function used instead. **[2]**

#### Tier 1 Model Answer

*(Note: This question re-tests the identical concept from Q1(a) with concise mark-adaptive density).*

1. **Why Linear Regression Fails:**  
   (i) Fits unbounded real outputs $(-\infty, +\infty)$ that cannot represent probabilities $P \in [0, 1]$; (ii) Outliers heavily distort decision boundaries due to squared error penalties on correct points.
2. **Why MSE Fails with Logistic Regression:**  
   Produces a **non-convex** loss surface with multiple suboptimal local minima, and causes learning saturation ($\nabla \mathcal{L} \approx 0$ when prediction error is high).
3. **Cost Function Used Instead:**  
   **Binary Cross-Entropy (Log-Loss):**
   $$J(\mathbf{w}) = -\frac{1}{m}\sum_{i=1}^m \Big[ y^{(i)}\ln \hat{y}^{(i)} + (1 - y^{(i)})\ln(1 - \hat{y}^{(i)}) \Big]$$

*Reference:* [[ml_foundations_regression_classification_visual_guide#8-why-linear-regression-fails-for-classification|Foundations Guide §8]] and [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Foundations Guide §10.1]]

---

### Question 2(d): Feedforward vs Recurrent Networks [2 Marks]

> **(d)** What are the basic differences between a feed-forward network and a recurrent network? **[2]**

#### Tier 1 Model Answer

| Architectural Property | Feedforward Neural Network (FNN) | Recurrent Neural Network (RNN) |
|:---|:---|:---|
| **Graph Topology** | Strictly **Directed Acyclic Graph (DAG)**; signals flow unidirectionally from input to output with zero feedback loops | Contains **directed cycles (feedback loops)** where neuron activations feed into subsequent temporal time steps |
| **Temporal Memory** | Stateless / Memoryless; treats each input $\mathbf{x}_t$ independently | Maintains an internal hidden state vector $\mathbf{h}_t = f(\mathbf{W}_h \mathbf{h}_{t-1} + \mathbf{W}_x \mathbf{x}_t + \mathbf{b})$, acting as dynamic temporal memory |
| **Input Structure** | Fixed-dimension independent feature vectors $\mathbf{x} \in \mathbb{R}^d$ (tabular, static images) | Variable-length sequential or time-series data $(\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_T)$ (text, speech, audio) |
| **Training Algorithm** | Standard Backpropagation | Backpropagation Through Time (BPTT) unrolled across sequence steps |

*Reference:* [[neural_networks_visual_guide#7-multilayer-feed-forward-networks|Neural Networks Guide §7 (Line 302)]]

---

### Question 3(a): Significance of ReLU Activation in Deep Networks [4 Marks]

> 3. **(a)** Explain the significance of ReLU Activation function in CNN. **[4]**

#### Tier 2 Model Answer

The Rectified Linear Unit ($\text{ReLU}(z) = \max(0, z)$) revolutionized deep Convolutional Neural Networks (CNNs) (Krizhevsky et al., 2012 / AlexNet) by addressing the crippling mathematical deficiencies of Sigmoid and Tanh activations:

1. **Resolution of the Vanishing Gradient Problem (Enabling True Depth):**  
   In deep CNNs with dozens of convolutional layers, backpropagating gradients through Sigmoid ($\sigma' \le 0.25$) or Tanh ($\tanh' \le 1.0$) causes gradients to vanish exponentially ($\prod \sigma' \to 0$). ReLU's derivative is strictly constant and unattenuated in the active positive domain:
   $$\frac{d}{dz} \text{ReLU}(z) = 1.0 \quad \forall z > 0$$
   This allows error signals to flow across very deep filter hierarchies without signal decay.

2. **Induction of Representational Sparsity:**  
   Biological sensory processing is sparse. ReLU outputs strictly zero for negative inputs ($z \le 0$). Typically, 50% to 75% of neurons in a trained CNN layer are inactive ($a = 0$) for any given image. This induces true mathematical sparsity, yielding disentangled feature maps that represent localized spatial features (e.g., edges, textures) with minimal crosstalk.

3. **Massive Computational Speedup:**  
   Sigmoid and Tanh require evaluating expensive transcendental exponential functions ($e^{-z}$) and divisions. ReLU requires only a trivial hardware-level conditional threshold check (`z > 0 ? z : 0`), accelerating forward and backward pass execution by up to $6\times$ on GPU hardware.

4. **Accelerated Optimization Convergence:**  
   Because ReLU does not saturate in the positive direction, gradient descent moves rapidly down linear loss slopes without stalling on asymptotic saturation plateaus, converging substantially faster than networks with saturating activations.

*Reference:* [[activation_crossentropy_backprop_visual_guide#5-relu-leaky-relu-and-sparse-gradients|Activations Guide §5]] and [[neural_networks_visual_guide#8-activation-functions|Neural Networks Guide §8]]

---

### Question 4(a): Single Neuron Forward Pass Numerical [3 Marks]

> 4. **(a)** Calculate the output $y$ of a three-input neuron with bias. The input feature vector is $(x_1, x_2, x_3) = (0.8, 0.6, 0.4)$ and weight values are $[w_1, w_2, w_3, b] = [0.2, 0.1, -0.3, 0.35]$. Use binary Sigmoid function as activation function. **[3]**

#### Tier 2 Model Answer & Numerical Audit

##### 1. Mathematical Model
$$z = \mathbf{w}^T \mathbf{x} + b = w_1 x_1 + w_2 x_2 + w_3 x_3 + b$$
$$y = \sigma(z) = \frac{1}{1 + e^{-z}}$$

##### 2. Numerical Computation
- **Linear Pre-activation ($z$):**
  $$z = (0.2 \times 0.8) + (0.1 \times 0.6) + (-0.3 \times 0.4) + 0.35$$
  $$z = 0.1600 + 0.0600 - 0.1200 + 0.3500$$
  $$z = 0.2200 - 0.1200 + 0.3500 = 0.1000 + 0.3500 = \mathbf{0.4500}$$

- **Sigmoid Activation Evaluation ($y = \sigma(0.45)$):**
  $$y = \frac{1}{1 + e^{-0.4500}} = \frac{1}{1 + 0.637628} = \frac{1}{1.637628} \approx \mathbf{0.610639}$$

##### 3. Final Result
$$\mathbf{y \approx 0.6106 \quad (61.06\%)}$$

*Reference:* [[neural_networks_visual_guide#1-from-brain-to-artificial-neuron|Neural Networks Guide §1]] and [[activation_crossentropy_backprop_visual_guide#4-sigmoid-function|Activations Guide §4]]

---

### Question 4(b): Biased Coin Toss Log-Likelihood & SGD Derivation [3 Marks]

> **(b)** Consider a situation where a biased coin with the probability of head ($p$) is tossed $N$ times and the outcomes ($\text{head}=1, \text{tail}=0$) are recorded in random variables, $x_n, n = 1, 2, \dots, N$. Derive the log-likelihood function for estimating parameter $p$. Derive SGD algorithm for solving the max-likelihood problem derived above. **[3]**

#### Tier 2 Model Answer

##### 1. Derivation of Log-Likelihood Function
For $N$ independent Bernoulli trials $x_n \in \{0, 1\}$ with $P(x_n = 1) = p$:
The likelihood is:
$$L(p) = \prod_{n=1}^N p^{x_n} (1 - p)^{1 - x_n}$$
Taking natural log ($\ln$):
$$\mathbf{\ell(p) = \sum_{n=1}^N \Big[ x_n \ln p + (1 - x_n) \ln(1 - p) \Big]}$$

##### 2. Derivation of Stochastic Gradient Descent (SGD) Algorithm
To **maximize** the log-likelihood via stochastic gradient ascent (or minimize negative log-likelihood $\mathcal{L}_n(p) = -[x_n \ln p + (1-x_n)\ln(1-p)]$ via SGD), we evaluate the gradient on a **single randomly sampled coin toss** $x_n$:

$$\frac{\partial \ell_n(p)}{\partial p} = \frac{d}{dp}\Big[ x_n \ln p + (1 - x_n)\ln(1 - p) \Big] = \frac{x_n}{p} - \frac{1 - x_n}{1 - p}$$

Combining fractions over a common denominator $p(1 - p)$:
$$\frac{\partial \ell_n(p)}{\partial p} = \frac{x_n(1 - p) - p(1 - x_n)}{p(1 - p)} = \frac{x_n - x_n p - p + x_n p}{p(1 - p)} = \mathbf{\frac{x_n - p}{p(1 - p)}}$$

Under Stochastic Gradient Ascent with learning rate $\alpha > 0$, the online parameter update after observing trial $x_n$ is:
$$\mathbf{p := p + \alpha \cdot \frac{x_n - p}{p(1 - p)}}$$

- **Intuition:** If $x_n = 1$ (Head) and current $p < 1$, the gradient $\frac{1 - p}{p(1-p)} = \frac{1}{p} > 0$, increasing $p$. If $x_n = 0$ (Tail), the gradient $-\frac{p}{p(1-p)} = -\frac{1}{1-p} < 0$, decreasing $p$.

*Reference:* [[ml_foundations_regression_classification_visual_guide#10-training-logistic-regression-log-loss--gradient-descent|Foundations Guide §10.2]] and [[neural_networks_visual_guide#9-gradient-descent-and-the-delta-rule|Neural Networks Guide §9]]

---
## Comprehensive Quick-Recall Formula Sheet

A high-density reference sheet of all fundamental formulas, tensor dimensions, loss gradients, and parameter updates derived across the 2023–2025 examinations:

### 1. Regression & Least Squares Formulations

| Concept / Model | Mathematical Formulation | Tensor Dimensions / Constraints |
|:---|:---|:---|
| **Simple Linear Regression (OLS)** | $w_1 = \frac{\sum_{i=1}^m (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^m (x_i - \bar{x})^2} = \frac{\text{Cov}(x, y)}{\text{Var}(x)}$<br>$w_0 = \bar{y} - w_1 \bar{x}$ | $x, y \in \mathbb{R}$<br>Line passes through centroid $(\bar{x}, \bar{y})$ |
| **Multiple Linear Regression (Matrix Form)** | $\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}, \quad \hat{\mathbf{Y}} = \mathbf{X}\hat{\boldsymbol{\beta}}$ | $\mathbf{Y} \in \mathbb{R}^{m \times 1}, \; \mathbf{X} \in \mathbb{R}^{m \times (n+1)}$<br>$\boldsymbol{\beta} \in \mathbb{R}^{(n+1) \times 1}$ |
| **Normal Equations Estimator** | $\mathbf{\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}}$ | $\text{rank}(\mathbf{X}) = n+1$<br>$(\mathbf{X}^T\mathbf{X})$ is symmetric positive definite |
| **Hat / Projection Matrix** | $\mathbf{H} = \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T, \quad \hat{\mathbf{Y}} = \mathbf{H}\mathbf{Y}$ | $\mathbf{H}^2 = \mathbf{H}$ (Idempotent)<br>$\mathbf{H}^T = \mathbf{H}$ (Symmetric) |
| **Orthogonality of Residuals** | $\mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}} = (\mathbf{I} - \mathbf{H})\mathbf{Y}$<br>$\mathbf{X}^T \mathbf{e} = \mathbf{0} \implies \mathbf{e} \perp \text{Col}(\mathbf{X})$ | Sum of residuals: $\sum_{i=1}^m e_i = 0$ (with intercept) |

---

### 2. Logistic Regression & Classification

| Concept / Model | Mathematical Formulation | Operational Significance |
|:---|:---|:---|
| **Logistic Hypothesis Function** | $h_{\mathbf{w}}(\mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$ | Outputs calibrated posterior probability $P(Y=1 \mid \mathbf{x}) \in (0, 1)$ |
| **Log-Odds (Logit Transformation)** | $\ln\left(\frac{p}{1 - p}\right) = \mathbf{w}^T \mathbf{x} + b$ | Maps non-linear probability $(0, 1)$ to linear space $(-\infty, +\infty)$ |
| **Binary Cross-Entropy (Log-Loss)** | $J(\mathbf{w}) = -\frac{1}{m}\sum_{i=1}^m \left[ y^{(i)}\ln \hat{y}^{(i)} + (1 - y^{(i)})\ln(1 - \hat{y}^{(i)}) \right]$ | Strictly convex loss function; derived from Bernoulli negative log-likelihood |
| **Log-Loss Gradient** | $\nabla_{\mathbf{w}} J(\mathbf{w}) = \frac{1}{m}\sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})\mathbf{x}^{(i)} = \frac{1}{m}\mathbf{X}^T(\hat{\mathbf{y}} - \mathbf{Y})$ | Identical functional form to linear regression OLS gradient |
| **Multi-class Softmax Function** | $p_k = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}} \quad \text{for } k = 1, \dots, K$ | Normalizes $\mathbf{z} \in \mathbb{R}^K$ to probability simplex: $\sum p_k = 1, \; p_k > 0$ |
| **Multi-class Cross-Entropy Gradient** | $\frac{\partial \mathcal{L}_{\text{CE}}}{\partial z_i} = p_i - y_i$ | Direct linear error difference between probability vector and one-hot target |

---

### 3. Activation Functions & Analytical Derivatives

| Activation Function | Formula: $\phi(z)$ | Derivative: $\phi'(z)$ | Saturation Wings / Extreme Limits |
|:---|:---|:---|:---|
| **Sigmoid ($\sigma$)** | $\frac{1}{1 + e^{-z}}$ | $\sigma(z)(1 - \sigma(z))$ | $\max \sigma'(0) = 0.25$; $\lim_{|z| \ge 4} \sigma'(z) \approx 0$ |
| **Hyperbolic Tangent ($\tanh$)** | $\frac{e^z - e^{-z}}{e^z + e^{-z}}$ | $1 - \tanh^2(z)$ | $\max \tanh'(0) = 1.0$; zero-centered; saturates for $|z| \ge 2.5$ |
| **Rectified Linear Unit ($\text{ReLU}$)** | $\max(0, z)$ | $\begin{cases} 1 & z > 0 \\ 0 & z < 0 \end{cases}$ | Constant gradient $1.0$ for $z>0$; Dying ReLU when $z \le 0$ |
| **Leaky $\text{ReLU}$** | $\max(\alpha z, z), \; \alpha \approx 0.01$ | $\begin{cases} 1 & z > 0 \\ \alpha & z \le 0 \end{cases}$ | Prevents permanent death by maintaining sub-gradient $\alpha = 0.01$ |

---

### 4. Neural Network Training & Regularization

| Technique / Rule | Mathematical Formula | Physical / Practical Effect |
|:---|:---|:---|
| **Perceptron Mistake Bound (Novikoff)** | $k \le \left(\frac{R}{\gamma}\right)^2$ | Upper bound on mistakes for linearly separable data with margin $\gamma$ and radius $R$ |
| **Output Layer Error ($\delta_{j, K}$) [SSE]** | $\delta_{j, K} = (y_j - O_{j, K}) \cdot O_{j, K}(1 - O_{j, K})$ | Stalls learning when neuron is confidently wrong ($O_{j, K}(1 - O_{j, K}) \to 0$) |
| **Output Layer Error ($\delta_{j, K}$) [BCE]** | $\delta_{j, K} = y_j - O_{j, K}$ (or $O_{j, K} - y_j$) | Constant linear sensitivity to error; zero saturation stall |
| **Hidden Layer Error ($\delta_{j, l}$)** | $\delta_{j, l} = \phi'(z_{j, l}) \sum_k w_{k, j, l+1} \, \delta_{k, l+1}$ | Backpropagates upstream error weighted by forward synaptic connections |
| **$L_2$ Ridge Weight Decay** | $w_j := w_j(1 - \eta \lambda) - \eta \frac{\partial \mathcal{L}_0}{\partial w_j}$ | Shrinks weights continuously toward zero; handles collinearity |
| **$L_1$ Lasso Sub-gradient Step** | $w_j := w_j - \eta \lambda \, \text{sgn}(w_j) - \eta \frac{\partial \mathcal{L}_0}{\partial w_j}$ | Drives small weights to exactly zero ($w_j = 0$); sparse feature selection |
| **Batch Normalization** | $\hat{z}_i = \frac{z_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}, \quad y_i = \gamma \hat{z}_i + \beta$ | Normalizes layer inputs across mini-batch; stabilizes and accelerates training |

---

### 5. Classification Contingency Metrics

$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}, \quad \text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

$$\text{Recall} = \text{Sensitivity} = \text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad \text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}, \quad \text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$

$$\text{F}_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}}$$

---

## Viva Voce & Oral Defense Preparation

Ten high-frequency questions favored by university external examiners, with authoritative first-principles defenses grounded in course theory:

### Q1: "Why can't we simply use Ordinary Least Squares linear regression to classify binary outcomes?"
- **Examiner's Defense:**  
  *"Linear regression models an unconstrained continuous conditional mean $\mathbb{E}[Y \mid \mathbf{x}] = \mathbf{w}^T \mathbf{x} + b \in (-\infty, +\infty)$, naturally producing outputs $< 0$ or $> 1$ which violate basic probability axioms. Furthermore, OLS penalizes squared residuals symmetrically: an extremely clear positive exemplar placed far from the decision boundary incurs a massive squared error $(y - \hat{y})^2 \gg 0$, which violently rotates the regression hyperplane and causes adjacent true positive points to be misclassified."*

### Q2: "Why does Mean Squared Error fail when paired with Sigmoid activation in classification?"
- **Examiner's Defense:**  
  *"Because the sigmoid function has inflection points, its composition with quadratic loss yields a non-convex loss surface riddled with spurious local minima and flat saddle plateaus. Crucially, the error gradient $\frac{\partial J}{\partial w} = -(y - \hat{y})\hat{y}(1-\hat{y})x$ contains the derivative term $\hat{y}(1-\hat{y})$. When the model makes a severe mistake (e.g., $y=1, \hat{y}=0.001$), this derivative vanishes to zero, causing the learning rate to stall precisely when error is highest."*

### Q3: "How does Cross-Entropy loss mathematically eliminate the learning stall in neural networks?"
- **Examiner's Defense:**  
  *"Differentiating Binary Cross-Entropy loss with respect to activation yields $\frac{\partial \mathcal{L}_{\text{BCE}}}{\partial a} = \frac{a - y}{a(1-a)}$. When applying the chain rule to reach pre-activation $z$, this term multiplies against the sigmoid derivative $\frac{\partial a}{\partial z} = a(1-a)$. The terms $a(1-a)$ cancel out analytically in numerator and denominator, leaving $\frac{\partial \mathcal{L}}{\partial z} = a - y$. The gradient is directly proportional to raw prediction error with zero saturation stall."*

### Q4: "Prove why a single-layer perceptron can solve AND and OR, but fails on XOR."
- **Examiner's Defense:**  
  *"A single perceptron defines a single linear hyperplanar decision boundary $\mathbf{w}^T \mathbf{x} + b = 0$. For AND and OR gates, positive and negative truth table vertices can be separated by a single straight line. For XOR, positive exemplars $(0, 1)$ and $(1, 0)$ lie on opposite vertices across the diagonal from negative exemplars $(0, 0)$ and $(1, 1)$. Their convex hulls intersect, making them linearly inseparable. Solving XOR requires at least one hidden layer that performs a non-linear coordinate projection to map the points into a representation space where they become linearly separable."*

### Q5: "What is the mathematical root cause of the Vanishing Gradient problem, and why does ReLU fix it?"
- **Examiner's Defense:**  
  *"During backpropagation, the gradient at layer $l$ is a product of upstream weight matrices and activation derivatives: $\prod_{k=l}^L \mathbf{W}_{k+1}^T \text{diag}(\phi'(\mathbf{z}_k))$. For sigmoid, $\max \phi'(z) = 0.25$. Multiplying these sub-unitary derivatives across $L$ layers causes the gradient to shrink exponentially ($\le 0.25^L \to 0$), freezing early layers. ReLU has a constant derivative $\phi'(z) = 1.0$ for all positive inputs $z > 0$, allowing error gradients to flow backward across arbitrarily deep architectures without exponential attenuation."*

### Q6: "What is the 'Dying ReLU' problem, and how does Leaky ReLU prevent it?"
- **Examiner's Defense:**  
  *"If a large negative gradient update pushes a neuron's weights such that $z = \mathbf{w}^T \mathbf{x} + b < 0$ for every sample in the training set, ReLU outputs $0$ and its derivative becomes $0$ everywhere. Because gradient updates are proportional to $\phi'(z)$, no error signal ever reaches the neuron again—it is permanently dead. Leaky ReLU introduces a small non-zero slope $\alpha \approx 0.01$ for $z \le 0$, ensuring a continuous non-zero gradient flow that allows gradient descent to resurrect the neuron."*

### Q7: "Why does L1 regularization cause weight sparsity while L2 regularization only shrinks weights?"
- **Examiner's Defense:**  
  *"Geometrically, the $L_1$ constraint region is a polytope with sharp corners that intersect the axes, where coordinates are exactly zero. Analytically, the $L_1$ sub-gradient is constant: $\frac{\partial}{\partial w_j} |w_j| = \text{sgn}(w_j)$, exerting a constant subtractive force that drives small coefficients to absolute zero. In contrast, the $L_2$ penalty derivative is proportional to weight magnitude ($\lambda w_j$), meaning the shrinkage force decays as weights approach zero, never pulling them to exact zero."*

### Q8: "In Multiple Linear Regression, what is the geometric meaning of the Normal Equations?"
- **Examiner's Defense:**  
  *"The target vector $\mathbf{Y} \in \mathbb{R}^m$ lives in $m$-dimensional observation space, while the columns of design matrix $\mathbf{X}$ span a lower-dimensional subspace $\text{Col}(\mathbf{X}) \subset \mathbb{R}^m$. The best least-squares fit $\hat{\mathbf{Y}} = \mathbf{X}\hat{\boldsymbol{\beta}}$ is the unique orthogonal projection of $\mathbf{Y}$ onto $\text{Col}(\mathbf{X})$. The normal equations $(\mathbf{X}^T\mathbf{X})\hat{\boldsymbol{\beta}} = \mathbf{X}^T\mathbf{Y}$ enforce the condition that the residual vector $\mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}}$ must be strictly orthogonal to every column in $\mathbf{X}$ ($\mathbf{X}^T\mathbf{e} = \mathbf{0}$)."*

### Q9: "Why is Batch Normalization inserted before the activation function, and what does it achieve?"
- **Examiner's Defense:**  
  *"Batch Normalization standardizes intermediate pre-activations ($\mathbf{z} = \mathbf{W}\mathbf{x} + \mathbf{b}$) across a mini-batch to zero mean and unit variance, followed by learned affine scaling $\gamma \hat{z} + \beta$. This prevents activations from drifting into the flat saturation wings of non-linear activations as upstream weights evolve (eliminating Internal Covariate Shift). It smooths the loss landscape, allowing higher learning rates and acting as a mild regularizer."*

### Q10: "Between One-vs-All and One-vs-One for multiclass classification, which one do you pick when $c = 100$?"
- **Examiner's Defense:**  
  *"For $c = 100$ classes, One-vs-All requires training only $c = 100$ binary classifiers, but each classifier trains on all $m$ examples with severe class imbalance ($1 : 99$). One-vs-One trains $\frac{c(c-1)}{2} = \frac{100 \times 99}{2} = 4,950$ binary classifiers! While each OvO classifier trains on a balanced pair subset of size $\approx \frac{2m}{c}$, managing and storing 4,950 separate models introduces heavy memory and inference overhead. In practice, for large $c$, One-vs-Rest or native Multinomial Softmax is strongly preferred over One-vs-One."*

---

## Unanswered / Uncovered Questions (Not in Reference Notes)

> [!important] Scope Enforcement Notice
> In accordance with user directives, the solutions above strictly cover only those questions whose underlying theory is presented in the authorized course guides:
> 1. `academics/ml/ml_foundations_regression_classification_visual_guide.md`
> 2. `academics/ml/activation_crossentropy_backprop_visual_guide.md`
> 3. `academics/ml/neural_networks_visual_guide.md`
>
> All remaining exam questions from topics outside these three reference documents (such as K-Nearest Neighbors, Decision Tree Entropy, Naive Bayes, Support Vector Machines QP/KKT, Convolutional Filter Dimension Calculations, AlexNet/VGG16, Autoencoders, and Recurrent Neural Networks / LSTMs / GRUs) are rigorously cataloged below with verbatim exam text, assigned marks, and explicit omission rationales.

---

### Uncovered Questions from 2025 Examinations

#### 2025 End-Semester Examination
> [!warning] Omitted: 2025 End Q2(c) — Early Stopping [3 Marks]
> **Verbatim Question:**  
> *"What is Early Stopping, and how does it act as a regularization method? [3]"*  
> **Omission Rationale:** Early stopping as an implicit regularization technique on validation loss curves is not covered in the three authorized reference notes.

> [!warning] Omitted: 2025 End Q4(b) — Sentence Semantic Representations [4 Marks]
> **Verbatim Question:**  
> *"Describe, with an example, how a deep learning model can be used to capture the semantic representations of sentences. [4]"*  
> **Omission Rationale:** Natural Language Processing (Word2Vec, sentence embeddings, transformer encoders) is not covered in the reference notes.

> [!warning] Omitted: 2025 End Q5(a, b) — VGG16 Architecture & Transfer Learning [10 Marks]
> **Verbatim Question:**  
> *"(a) Explain the architecture of the VGG16 model in detail with a neat diagram. Additionally, calculate the total number of parameters in both the first convolutional layer and the first pooling layer of the network. [6]"*  
> *"(b) What is transfer learning and how can VGG16 be used for transfer learning? [4]"*  
> **Omission Rationale:** VGG16 architecture specifications, convolutional parameter calculations, and transfer learning fine-tuning workflows are not covered in the reference notes.

> [!warning] Omitted: 2025 End Q6(a, b) — Denoising & Conditional Variational Autoencoders [10 Marks]
> **Verbatim Question:**  
> *"(a) Discuss the different types of noise that can be used in a Denoising Autoencoder. Describe how a Denoising Autoencoder learns to reconstruct clean input from noisy data. [2 + 3 = 5]"*  
> *"(b) Describe the architecture of a Conditional Variational Autoencoder (CVAE) with a neat diagram. What is the KL divergence term in CVAE, and what is its purpose? [3 + 2 = 5]"*  
> **Omission Rationale:** Unsupervised generative models, denoising autoencoders, and CVAE KL-divergence formulations are outside the scope of the three reference notes.

> [!warning] Omitted: 2025 End Q7(a, b) — Recurrent Neural Networks & GRU Architecture [10 Marks]
> **Verbatim Question:**  
> *"(a) Explain the architecture and working principle of a Recurrent Neural Network (RNN), and discuss the challenges encountered by standard RNNs during training. [3 + 2 = 5]"*  
> *"(b) Explain the architecture of a Gated Recurrent Unit (GRU) with the help of a diagram, and present the mathematical equations governing its operations, interpreting each term in detail. [5]"*  
> **Omission Rationale:** Gated Recurrent Units (GRU mathematical equations, reset and update gates) and deep RNN training dynamics are outside the reference guides.

---

### Uncovered Questions from 2024 Examinations

#### 2024 Mid-Semester Examination
> [!warning] Omitted: 2024 Mid Q1(b, c) — K-Nearest Neighbors (KNN) [6 Marks]
> **Verbatim Question:**  
> *"(b) What is the K-Nearest Neighbors (KNN) algorithm, and how does it function in both classification and regression tasks? [3]"*  
> *"(c) How is the parameter 'K' chosen in the KNN algorithm? What are the implications of choosing a small vs. a large 'K'? [3]"*  
> **Omission Rationale:** Instance-based learning, non-parametric KNN classification/regression, and distance metrics are not covered in the reference notes.

> [!warning] Omitted: 2024 Mid Q2(a, b) — Decision Tree Information Gain & Naive Bayes [6 Marks]
> **Verbatim Question:**  
> *"(a) Consider the dataset given below and compute the following: [Given that, $\log_2 3 = 1.6$, $\log_2 5 = 2.3$, $\log_2 7 = 2.8$] [3]"*  
> *"[Dataset with $O_1 \dots O_5$ on $F_1, F_2$ and Class label Y/N]"*  
> *"i) Entropy to classify an object"*  
> *"ii) Entropy to classify an object based on $F_2$"*  
> *"iii) Information gain based on $F_2$"*  
> *"(b) Use Naive Bayes classification algorithm to predict the class label of object $X = (F_1 = 2, F_2 = 2)$. Explain under what circumstances the object cannot be predicted, and provide a solution to resolve the problem. [3]"*  
> **Omission Rationale:** Shannon Entropy, Information Gain splitting algorithms (ID3/C4.5), and Naive Bayes conditional independence with Laplace smoothing are not present in the reference notes.

#### 2024 Final-Semester Examination
> [!warning] Omitted: 2024 Final Q1(b) — Support Vector Machine (SVM) Principle [7 Marks]
> **Verbatim Question:**  
> *"Explain the Working Principle of a Support Vector Machine. [7]"*  
> **Omission Rationale:** SVM maximum margin hyperplanes, Lagrangian duality, and support vectors are outside the reference notes.

> [!warning] Omitted: 2024 Final Q4(a) — CNN Sparsity & Weight Sharing [5.5 Marks]
> **Verbatim Question:**  
> *"Justify the properties of 'sparsity of connections' and 'weight sharing' in Convolutional Neural Networks (CNNs). Discuss the advantages of these properties in the context of CNN performance and efficiency. [3 + 2.5 = 5.5]"*  
> **Omission Rationale:** Specialized spatial convolution filter mechanisms (receptive fields, weight sharing across 2D feature maps) are not developed in the three reference guides.

> [!warning] Omitted: 2024 Final Q5(a, b) — CNN Feature Maps & Dropout/BN Overfitting [12.5 Marks]
> **Verbatim Question:**  
> *"(a) Briefly discuss the usefulness of the Convolutional layer and the Pooling layer in a Convolutional Neural Network (CNN). Given an input image of size $W \times H \times D$... calculate the volume of the resulting convolved feature map. [4 + 2.5 = 6.5]"*  
> *"(b) Explain how the regularization techniques of Dropout and Batch Normalization help in addressing the overfitting problem in deep neural networks. [6]"*  
> **Omission Rationale:** 3D feature map dimension formula $\lfloor \frac{W - F + 2P}{S} \rfloor + 1$ and detailed inverted dropout Bernoulli scaling are outside the reference notes.

> [!warning] Omitted: 2024 Final Q6(a, b) — AlexNet Architecture & Transfer Learning [12.5 Marks]
> **Verbatim Question:**  
> *"(a) Construct a high-level diagram of the AlexNet CNN architecture... calculate total weights and biases in the first conv layer and first pooling layer. [4 + 2.5 = 6.5]"*  
> *"(b) Describe the key steps involved in developing a transfer learning model... [3 + 3 = 6]"*  
> **Omission Rationale:** AlexNet architectural dimensions (11x11 filters, LRN layers) and transfer learning pipelines are not present in the reference notes.

> [!warning] Omitted: 2024 Final Q7(a, b) — Stacked Autoencoder & Variational Autoencoder (VAE) [12.5 Marks]
> **Verbatim Question:**  
> *"(a) Explain the structure of a stacked autoencoder with a diagram and emphasize its key benefits. [4 + 2 = 6]"*  
> *"(b) What is the primary purpose of a variational autoencoder (VAE), and how does it differ from a simple autoencoder? Explain the reparameterization trick and its significance in VAEs. [1.5 + 2 + 3 = 6.5]"*  
> **Omission Rationale:** Stacked autoencoders, VAE latent distributions $\mathcal{N}(\mu, \sigma^2)$, and reparameterization trick $z = \mu + \sigma \odot \epsilon$ are outside the reference guides.

> [!warning] Omitted: 2024 Final Q8(a, b) — CNN vs RNN & LSTM Backpropagation Through Time [12.5 Marks]
> **Verbatim Question:**  
> *"(a) Explain the main differences between CNN and RNN models. Describe the limitations of an RNN model. [3 + 2 = 5]"*  
> *"(b) Describe the architecture of LSTM and explain how backpropagation through time is used to train LSTM models. [4 + 3.5 = 7.5]"*  
> **Omission Rationale:** LSTM memory cell state $C_t$, gating equations (input, forget, output gates), and unrolled BPTT derivations are outside the reference guides.

---

### Uncovered Questions from 2023 Examinations

#### 2023 Mid-Semester Examination
> [!warning] Omitted: 2023 Mid Q1(b) — SVM Kernel & K-Fold Cross Validation [3 Marks]
> **Verbatim Question:**  
> *"What is a kernel in SVM and why do we use kernels? What is K-fold cross validation? How does it affect bias and variance? [3]"*  
> **Omission Rationale:** Mercer kernel trick and K-fold cross validation bias-variance mechanics are not covered in the reference notes.

> [!warning] Omitted: 2023 Mid Q2(a, b, c) — SVM Margins & Quadratic Programming / KKT Numerical [10 Marks]
> **Verbatim Question:**  
> *"(a) State the role of margin in SVM. [2]"*  
> *"(b) Explain the difference between Hard Margin and Soft Margin for SVM. [3]"*  
> *"(c) Consider a binary classification problem where the training data consists of 8 tuples... Find parameters $W$ and $b$ using quadratic programming and KKT constraints, and obtain Lagrange multipliers $\lambda_i$... [5]"*  
> **Omission Rationale:** Karush-Kuhn-Tucker (KKT) dual stationarity conditions and quadratic programming solvers for SVMs are not in the reference notes.

> [!warning] Omitted: 2023 Mid Q5(a, b, c) — RNN Parameter Calculation & LSTM Gating [10 Marks]
> **Verbatim Question:**  
> *"(a) Consider a vanilla RNN cell of the form $h_t = \tanh(V \cdot h_{t-1} + W \cdot x_t + b)$. Given dimensions $x_t \in \mathbb{R}^3$ and $h_t \in \mathbb{R}^5$, what is the number of parameters in the RNN cell? [3]"*  
> *"(b) Explain the main difficulties encountered while training RNNs, the ways to handle them, and the gating mechanisms in LSTM units. [3]"*  
> *"(c) What is the difference between vanilla RNN and LSTM? Why is LSTM not used for smaller datasets or problems? [4]"*  
> **Omission Rationale:** Recurrent weight tensor dimensions and LSTM cell mechanisms are outside the reference guides.

#### 2023 End-Semester Examination
> [!warning] Omitted: 2023 End Q2(a, b) — Decision Tree Greedy Construction & K-Fold CV [6 Marks]
> **Verbatim Question:**  
> *"(a) Using the dataset below, build a decision tree that classifies $Y$ as T/F given the binary variables A, B, and C. Draw the tree that the greedy algorithm would learn with zero training error. [4]"*  
> *"(b) What is K-fold cross validation? How does it affect bias and variance? [2]"*  
> **Omission Rationale:** Greedy top-down decision tree induction and cross-validation variance properties are not covered in the reference notes.

> [!warning] Omitted: 2023 End Q3(b, c) — Max-Unpooling & CNN vs ANN for Images [6 Marks]
> **Verbatim Question:**  
> *"(b) Explain Max-Unpooling operation for increasing the resolution of feature maps. [3]"*  
> *"(c) Why do we prefer Convolutional Neural networks (CNN) over Artificial Neural networks (ANN) for image data as input? [3]"*  
> **Omission Rationale:** Max-unpooling index caching and spatial 2D invariance of CNNs are outside the reference guides.

> [!warning] Omitted: 2023 End Q4(c) — Cross-Validation vs Dedicated Test Set [4 Marks]
> **Verbatim Question:**  
> *"Two common ways to estimate the performance of a classifier are (i) n-fold cross validation... and (ii) measuring the performance on a test set... When will you use cross-validation and when will you use a test set? Justify your answer. [4]"*  
> **Omission Rationale:** Empirical model evaluation methodologies (cross-validation vs holdout split tradeoffs) are not covered in the reference notes.

> [!warning] Omitted: 2023 End Q5(a, b, c) — RNN Vanishing Gradients, LSTM vs GRU, Autoencoder Denoising [10 Marks]
> **Verbatim Question:**  
> *"(a) What is vanishing/exploding gradient problem and how is it related to Recurrent Neural Network? [3]"*  
> *"(b) Explain LSTM and GRU. How do they differ from each other? [3]"*  
> *"(c) What is the objective of an Auto Encoder? How is an auto-encoder used in dimensionality reduction and image de-noising? [4]"*  
> **Omission Rationale:** Specialized recurrent architectures (LSTM vs GRU comparison) and autoencoder denoising manifolds are outside the reference guides.

> [!warning] Omitted: 2023 End Q6(a, b, c) — CNN Parameter Table, Sparse Autoencoders, VAE [10 Marks]
> **Verbatim Question:**  
> *"(a) A CNN has a database of images of size $100 \times 100 \times 3$... calculate the total number of parameters in each layer (Output, FC1, P2, C3, P1, C2, C1, Input). [3]"*  
> *"(b) How do auto-encoders handle sparse data? Explain their function with sparse data. Are specialized auto-encoder architectures designed for sparse inputs? [4]"*  
> *"(c) (i) What is the basic idea behind a variational auto-encoder? (ii) How have variational auto-encoders been integrated into transfer learning? Explain smooth latent-state representations with an example. [3]"*  
> **Omission Rationale:** Layer-by-layer CNN parameter counting tables and sparse/variational autoencoders are outside the reference notes.

---
