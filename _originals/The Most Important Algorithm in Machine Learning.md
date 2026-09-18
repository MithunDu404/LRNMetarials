# Backpropagation: Building the Algorithm from Scratch

## Why Backpropagation Matters

Systems as different as GPT, Midjourney, AlphaFold, and various computational models of the brain share almost nothing in terms of architecture or training data — yet all of them are trained using the same underlying algorithm: **backpropagation**. It is the computational foundation of essentially the entire field of machine learning, even though its mechanics are frequently glossed over. Interestingly, the very thing that makes backpropagation so effective for artificial networks is also what makes it biologically implausible — a topic reserved for a follow-up video on synaptic plasticity in the brain.

## A Brief History

Tracing certain mathematical roots back to Leibniz in the 17th century, the modern form of backpropagation is usually credited to Seppo Linnainmaa, who published it in his 1970 master's thesis (without connecting it to neural networks). The pivotal moment for machine learning came in 1986, when David Rumelhart, Geoffrey Hinton, and Ronald Williams published *"Learning representations by back-propagating errors."* They applied the algorithm to multi-layer perceptrons and showed, for the first time, that this training method allows a network to discover meaningful internal representations — hidden units that capture real regularities in the task. Since then, models have grown enormously in scale and architecture has diversified, but the core training principle has stayed the same.

## Setting Up the Problem: Curve Fitting

To build intuition for backpropagation from the ground up, consider a concrete problem: you have a set of data points $(x, y)$ on a plane, and you want to find a curve $y(x)$ that best describes their relationship.

Since infinitely many functions could fit any data set, an assumption is needed to make the problem tractable. Here, the assumption is that the curve should be a **degree-5 polynomial**:

$$y(x) = k_0 + k_1 x + k_2 x^2 + k_3 x^3 + k_4 x^4 + k_5 x^5$$

Each $k_i$ is a real-valued coefficient. Fitting the curve now means finding the right values for $k_0$ through $k_5$.

### Quantifying "Best Fit": The Loss Function

Eyeballing which curve looks best is subjective and doesn't scale. Instead, a numerical measure of fit quality is needed. A standard choice is the **sum of squared vertical distances** between each data point and the curve. A large value means the curve is far from the data (bad fit); a small value means the curve is close (good fit). This quantity is called the **loss**, and the goal of fitting is to minimize it.

It's important to keep two different functions straight:

- $y(x)$: the curve itself — one number in, one number out, of a fixed polynomial form determined by the $k_i$'s.
- The **loss function**: takes the six coefficients $(k_0, \dots, k_5)$ as input, internally constructs the corresponding curve, measures its total squared distance to the data, and returns a single number — the loss.

So fitting the curve reduces to an optimization problem: find the configuration of $k_i$'s that **minimizes the loss function**. Once found, plugging those optimal $k_i$'s back into the polynomial gives the best-fit curve.

## The "Curve Fitter 6000": A Naive Approach

Imagine a machine with six knobs, one per coefficient $k_0$ through $k_5$. You feed in the data points; for any knob setting, the machine evaluates the curve, computes the loss, and displays it.

A naive optimization strategy — **random perturbation** — is to nudge one knob slightly, see if the loss goes up or down, keep the change if it helps and revert it if it doesn't, then move to the next knob, and repeat this many times over. This works in principle, but it's inefficient: you're "wandering in the dark," learning only after the fact whether an adjustment helped.

### The Goal: A Machine That Predicts the Future

The improvement being sought is a machine with a small screen next to each knob that tells you, *before* you turn it, which direction to turn it and by how much, in order to decrease the loss — without actually performing the trial adjustment. This sounds like it requires seeing into the future, but it rests on ordinary calculus, specifically the concept of a **derivative**.

## Derivatives: The Mathematical Foundation

### The Single-Knob Case

Simplify first: suppose five of the six knobs are already frozen at their optimal values, and only $k_1$ is free. Now the loss is a function of one variable, visualizable as a 2D curve, and the goal is to find the input $k_1$ that sits at the minimum.

The catch: you don't have access to the full shape of this loss curve — only to the value at whatever point you currently sample. But if you also knew whether the function was increasing or decreasing at that point, you'd know which way to turn the knob.

### Defining the Derivative

Take a sampled point $(x_0, y_0)$ on the loss curve. Nudge the input by a small amount $\Delta x$, producing a change in output $\Delta y$. The ratio

$$\frac{\Delta y}{\Delta x}$$

is the slope of the straight line (secant line) connecting $(x_0, y_0)$ and $(x_0 + \Delta x, y_0 + \Delta y)$. As $\Delta x$ shrinks, this secant line hugs the curve more and more tightly near $x_0$. Taking the limit as $\Delta x \to 0$ gives the **derivative**:

$$\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x}$$

Geometrically, this is the slope of the line *tangent* to the curve at that point — the instantaneous rate of change, or steepness. Since steepness varies from point to point, the derivative is itself a function of $x$: it maps each input to the local steepness of the original function there. Note: derivatives may fail to exist at sharp corners or discontinuities, but for this discussion all functions involved are assumed smooth and differentiable.

### Using the Derivative to Optimize

Imagine you can now query the machine not just for the loss but also for the derivative of the loss with respect to $k_1$ at any point — a peek into local behavior that tells you how the loss will respond to a nudge without actually performing it.

The optimization procedure becomes:
1. Start at a random $k_1$.
2. Query the loss and its derivative at that point.
3. Step in the direction *opposite* the derivative (if the derivative is negative — loss decreasing as $k_1$ increases — increase $k_1$; if positive, decrease it).
4. Repeat until the derivative reaches zero, i.e., the tangent line is flat — the minimum.

This is analogous to a ball rolling downhill along the loss curve until it settles in a valley.

### Extending to Multiple Dimensions: Partial Derivatives and the Gradient

With two free knobs, $k_1$ and $k_2$, the loss becomes a function of two variables — visualized as a surface rather than a curve. Now there's ambiguity: does "the derivative" mean the rate of change with respect to $k_1$, or $k_2$, or both? This is resolved with **partial derivatives**:

$$\frac{\partial L}{\partial k_1} \quad \text{(change per unit change in } k_1 \text{, holding } k_2 \text{ fixed)}$$
$$\frac{\partial L}{\partial k_2} \quad \text{(change per unit change in } k_2 \text{, holding } k_1 \text{ fixed)}$$

Geometrically, slicing the surface with a plane parallel to one axis at the point of interest produces a 1D cross-section curve; the slope of its tangent line there is the corresponding partial derivative.

Packing both partial derivatives into a vector gives the **gradient vector**. This vector points in the direction of **steepest ascent** of the function. To minimize the loss, you step in the direction *opposite* the gradient. This iterative procedure — repeatedly stepping opposite the gradient — is **gradient descent**, the multi-dimensional generalization of the "ball rolling downhill" picture.

This generalizes cleanly beyond two dimensions, even though it can no longer be visualized directly: with all six knobs free, the loss is a hypersurface in six dimensions, the gradient vector has six components, and gradient descent still works exactly the same way — take small steps opposite the gradient until reaching the minimum.

Returning to the original goal of "screens on the knobs": those screens are just the components of the gradient vector. A positive $\partial L/\partial k_1$ means increasing $k_1$ increases the loss, so the screen should indicate "turn left" (decrease $k_1$), and so on for each knob.

## Computing Derivatives: How Backpropagation Actually Works

Gradient descent depends entirely on being able to compute the gradient at any point — but so far, that gradient was simply assumed to be available. Actually computing derivatives of an arbitrarily complicated function is the real problem backpropagation solves.

### Building Blocks

A handful of simple functions have known derivatives from calculus, the kind memorized in a first course:

- Linear function: derivative is a constant equal to its slope.
- $x^2$: derivative is $2x$; more generally, $x^n$ has derivative $nx^{n-1}$.
- Exponentials and logarithms have their own standard derivative formulas.

To combine these atomic pieces into derivatives of more complex expressions, a few combination rules are needed:

- **Sum rule**: the derivative of a sum of functions is the sum of their derivatives.
- **Product rule**: a known formula for differentiating a product of two functions (e.g., needed for something like $3x^2 - e^x$... more precisely for products like $x^2 \cdot e^x$).

### The Chain Rule

The rule that "powers the entire field of machine learning" is the **chain rule**, which tells you how to differentiate a composition of functions — one function's output feeding into another's input.

**Setup**: imagine a machine computing $j(x)$, whose output feeds into a second machine computing $f$, producing the composite output $f(j(x))$. Treated as a single black box, this composite function has some derivative — how does nudging the input $x$ affect the final output?

**Reasoning it through**:
- At input $x$, the first machine's local rate of change is $j'(x)$ (the derivative of $j$ at $x$).
- The value actually fed into the second machine is $j(x)$, not $x$ — so the second machine's local rate of change at that point is $f'(j(x))$, the derivative of $f$ evaluated at $j(x)$.
- Nudge the input by a small $\delta$. After passing through the first machine, the output changes by approximately $\delta \cdot j'(x)$ — this is now a small nudge to the *input* of the second machine.
- That nudge, passing through the second machine, gets scaled by $f'(j(x))$, producing a total change of $\delta \cdot j'(x) \cdot f'(j(x))$.
- Dividing by $\delta$, the derivative of the composite function is:

$$\frac{d}{dx} f(j(x)) = f'(j(x)) \cdot j'(x)$$

This can be pictured as three interlocking cogwheels: turning the input wheel $x$ turns the middle wheel $j(x)$ by an amount scaled by $j'(x)$, which in turn turns the output wheel $f(j(x))$ by an amount scaled by $f'(j(x))$ — the two scaling factors multiply together.

With the sum rule, product rule, and chain rule in hand, the derivative of essentially any function built from these building blocks can be computed, no matter how deeply composed.

## Applying This to the Curve-Fitting Problem

### Building the Computational Graph (The Forward Pass)

To connect this machinery to curve fitting, first create an input "knob" for every number the loss depends on: not just the six coefficients $k_0$–$k_5$, but also the data coordinates themselves. During optimization, the data points are held fixed (they aren't adjustable), but conceptually they can still be thought of as knobs frozen at a set position, useful for tracking how the computation flows.

Working through a concrete example: for the first data point $(x_1, y_1)$, compute the predicted value

$$\hat{y}_1 = k_0 + k_1 x_1 + k_2 x_1^2 + k_3 x_1^3 + k_4 x_1^4 + k_5 x_1^5$$

then compute the squared difference $(y_1 - \hat{y}_1)^2$ — this data point's contribution to the loss. Repeating this for every data point and summing all the squared differences gives the total loss.

This process — computing the loss for a given knob configuration by working through the arithmetic — is the **forward step**. It can be drawn as a **computational graph**: a network of nodes, each performing one simple differentiable operation (addition, multiplication, squaring), with computation flowing left to right from inputs to the final loss value.

### The Backward Step

To perform gradient descent, the gradient of the loss with respect to each parameter knob is needed. This is found by unrolling the computational graph in reverse — the **backward step** — exploiting the fact that every node is a simple, easily differentiable operation, so the chain rule can be applied node by node.

For each node, the goal is to find its **gradient**: the partial derivative of the final loss $L$ with respect to that node's value. This is computed working backward from the output, assuming the gradient of everything "downstream" of a node is already known.

**Rule for an addition node**: if $A$ and $B$ feed into a node computing $A + B$, and the gradient of $L$ with respect to $A+B$ is already known, then nudging $A$ by some amount nudges $A+B$ by the *same* amount (since $\partial(A+B)/\partial A = 1$). So the downstream gradient simply **passes through unchanged** to both $A$ and $B$:

$$\frac{\partial L}{\partial A} = \frac{\partial L}{\partial (A+B)}, \qquad \frac{\partial L}{\partial B} = \frac{\partial L}{\partial (A+B)}$$

**Rule for a multiplication node**: if $A$ and $B$ feed into a node computing $A \cdot B$, nudging $A$ scales the product's change by a factor of $B$ (since $\partial(AB)/\partial A = B$). So the downstream gradient gets **multiplied crossways** by the other input's value:

$$\frac{\partial L}{\partial A} = \frac{\partial L}{\partial (AB)} \cdot B, \qquad \frac{\partial L}{\partial B} = \frac{\partial L}{\partial (AB)} \cdot A$$

Similar rules follow directly from the chain rule for other building-block operations like exponentiation or logarithms.

**Rule for branching**: if a single node $A$ feeds into *multiple* downstream operations that each independently contribute to the loss, then nudging $A$ affects the loss through both paths simultaneously. The gradients contributed by each branch simply **add together**:

$$\frac{\partial L}{\partial A} = \left(\frac{\partial L}{\partial A}\right)_{\text{branch 1}} + \left(\frac{\partial L}{\partial A}\right)_{\text{branch 2}}$$

### Walking Through the Backward Pass on the Curve-Fitting Graph

Starting at the rightmost node — the loss $L$ itself — its gradient with respect to itself is trivially $1$.

The loss is a sum of terms $(\Delta y_i)^2$ (where $\Delta y_i = y_i - \hat{y}_i$). Applying the summation rule, the gradient of $1$ passes through unchanged to each $(\Delta y_i)^2$ node.

Each of those nodes squares $\Delta y_i$; using the power rule, the gradient of the loss with respect to $\Delta y_i$ itself is $2 \Delta y_i$ — a number already known from the forward pass.

Continuing to propagate this way, applying the addition/multiplication/branching rules at each node moving leftward, gradients eventually reach the leftmost nodes: the data knobs and the parameter knobs. The gradients with respect to the data don't matter (data isn't adjustable), but the **gradients with respect to the parameters $k_0$ through $k_5$** are exactly what's needed.

### Putting It Together: The Training Loop

With the parameter gradients in hand, one step of gradient descent can be performed: nudge each knob in the direction opposite its gradient, with step size equal to the gradient magnitude times a small **learning rate** (e.g., $0.01$):

$$k_i \leftarrow k_i - \text{(learning rate)} \cdot \frac{\partial L}{\partial k_i}$$

Because this changes the knob configuration, the previously computed loss and gradients are now stale. So the whole cycle must repeat: run the forward pass again to get the new loss, run the backward pass again to get new gradients, nudge again, and so on.

This loop — **forward pass, backward pass, nudge, repeat** — is backpropagation, and it is the training procedure underlying essentially every modern machine learning system. As long as a model's computation can be broken down into differentiable atomic operations, the chain rule can be applied systematically through the computational graph to find how every parameter affects the loss, and gradient descent can then optimize them.

## Generalizing Beyond Curve Fitting

A feedforward neural network is, at its core, just a much larger arrangement of the same kind of atomic operations: multiplications, summations, and a handful of nonlinear activation functions inserted between layers — all differentiable. The same computational-graph-plus-backward-pass procedure applies directly, computing how each connection weight influences the loss. Because neural networks with enough neurons can in principle approximate essentially any function, chaining together enough of these differentiable building blocks and training them with backpropagation is what allows such networks to solve tasks like image classification or text generation.

## Looking Ahead

This raises the natural question of whether the brain does anything resembling this: does it minimize a loss function, does it compute derivatives via something like a computational graph and chain rule, or is biological learning built on entirely different principles? That comparison — between backpropagation and biological synaptic plasticity — is the subject of the next video in this series.

---

Source: [The Most Important Algorithm in Machine Learning](https://youtu.be/SmZmBKc7Lrs?si=ktQHq8JMCmJ1AAFH) — Artem Kirsanov
