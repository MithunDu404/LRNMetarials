import math, random

class Value:
    """A number that remembers how it was computed, so it can backpropagate."""
    def __init__(self, data, parents=(), op=""):
        self.data, self.grad = data, 0.0
        self._parents, self._op = parents, op
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")
        def _backward():                 # ADD rule: copy the gradient
            self.grad += out.grad
            other.grad += out.grad       # += handles branching (gradients add up)
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")
        def _backward():                 # MULTIPLY rule: swap the inputs
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, n):                # n is a plain number
        out = Value(self.data ** n, (self,), f"**{n}")
        def _backward():                 # power rule
            self.grad += n * self.data ** (n - 1) * out.grad
        out._backward = _backward
        return out

    def __neg__(self): return self * -1
    def __sub__(self, other): return self + (-other)
    def __rsub__(self, other): return (-self) + other
    __radd__, __rmul__ = __add__, __mul__

    def backward(self):
        order, seen = [], set()
        def visit(v):                    # topological sort: children before parents
            if v not in seen:
                seen.add(v)
                for p in v._parents: visit(p)
                order.append(v)
        visit(self)
        self.grad = 1.0                  # dL/dL = 1
        for v in reversed(order):        # walk the graph backward
            v._backward()

# --- 1. Reproduce the worked example: x=2, y=3, k0=1, k1=0.5
k0, k1 = Value(1.0), Value(0.5)
L = (3.0 - (k0 + k1 * 2.0)) ** 2
L.backward()
print(f"L = {L.data},  dL/dk0 = {k0.grad},  dL/dk1 = {k1.grad}")   # 1.0, -2.0, -4.0

# --- 2. Fit a degree-5 polynomial with gradient descent
random.seed(0)
xs = [i / 10 - 1 for i in range(21)]
ys = [0.6 * math.sin(3.2 * x) + 0.3 * x * x for x in xs]
k = [Value(random.uniform(-0.5, 0.5)) for _ in range(6)]

for step in range(3001):
    loss = sum(((sum(k[p] * x ** p for p in range(6)) - y) ** 2 for x, y in zip(xs, ys)), Value(0.0))
    for kp in k: kp.grad = 0.0           # 1. reset old gradients
    loss.backward()                      # 2. backward pass
    for kp in k: kp.data -= 0.01 * kp.grad   # 3. nudge every knob downhill
    if step % 1000 == 0:
        print(f"step {step:4d}   loss {loss.data:.4f}")
