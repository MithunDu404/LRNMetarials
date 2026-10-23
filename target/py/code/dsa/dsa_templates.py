"""Copy-paste DSA templates for Python, each checked against brute force in test_dsa_templates.py.

Every template is standard-library only (no sortedcontainers), so it also works on
Codeforces/AtCoder. Run the tests:  py -3.12 -m pytest -q target/py/code/dsa
"""
from __future__ import annotations

import heapq
from bisect import bisect_left
from collections import deque
from collections.abc import Callable, Iterable


# ---------------------------------------------------------------- Union-Find
class DSU:
    """Disjoint set union with path halving + union by size. Near-O(1) per op."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        parent = self.parent              # local alias: attribute lookups are slow in loops
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving: no recursion, no RecursionError
            x = parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


# ---------------------------------------------------------------- Fenwick tree
class Fenwick:
    """Point update, prefix sum, both O(log n). Indices are 0-based for the caller."""

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    @classmethod
    def from_list(cls, values: list[int]) -> Fenwick:
        """O(n) build instead of n updates (O(n log n))."""
        fw = cls(len(values))
        t = fw.tree
        for i, v in enumerate(values, 1):
            t[i] += v
            j = i + (i & -i)
            if j <= fw.n:
                t[j] += t[i]
        return fw

    def add(self, i: int, delta: int) -> None:
        i += 1
        t, n = self.tree, self.n
        while i <= n:
            t[i] += delta
            i += i & -i                   # i & -i is the lowest set bit

    def prefix(self, i: int) -> int:
        """Sum of values[0:i]."""
        s, t = 0, self.tree
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    def range_sum(self, lo: int, hi: int) -> int:
        """Sum of values[lo:hi]."""
        return self.prefix(hi) - self.prefix(lo)


# ---------------------------------------------------------------- Segment tree
class SegTree:
    """Iterative (bottom-up) segment tree for any associative op with an identity.

    SegTree(values, min, float('inf')), SegTree(values, max, -inf), SegTree(values, gcd, 0)...
    Point assign and half-open range query [lo, hi), both O(log n).
    """

    def __init__(self, values: list, op: Callable, identity):
        self.n = n = len(values)
        self.op, self.e = op, identity
        self.t = [identity] * n + list(values)
        for i in range(n - 1, 0, -1):
            self.t[i] = op(self.t[2 * i], self.t[2 * i + 1])

    def set(self, i: int, value) -> None:
        t, op = self.t, self.op
        i += self.n
        t[i] = value
        while i > 1:
            i >>= 1
            t[i] = op(t[2 * i], t[2 * i + 1])

    def query(self, lo: int, hi: int):
        t, op = self.t, self.op
        left = right = self.e
        lo += self.n
        hi += self.n
        while lo < hi:
            if lo & 1:
                left = op(left, t[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                right = op(t[hi], right)
            lo >>= 1
            hi >>= 1
        return op(left, right)


# ---------------------------------------------------------------- Graphs
Graph = list[list[tuple[int, int]]]  # adj[u] = [(v, weight), ...]


def dijkstra(adj: Graph, src: int) -> list[float]:
    """Lazy-deletion Dijkstra: push duplicates, skip stale pops. O((V + E) log E)."""
    dist = [float("inf")] * len(adj)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:                   # stale entry: a shorter path was already found
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def bfs_01(adj: Graph, src: int) -> list[float]:
    """Shortest paths when every weight is 0 or 1: deque instead of heap, O(V + E)."""
    dist = [float("inf")] * len(adj)
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                (dq.appendleft if w == 0 else dq.append)(v)
    return dist


def topo_sort(n: int, edges: Iterable[tuple[int, int]]) -> list[int] | None:
    """Kahn's algorithm. Returns an order, or None if there is a cycle."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None


def iterative_dfs_order(adj: list[list[int]], root: int) -> tuple[list[int], list[int]]:
    """Pre-order and post-order without recursion (safe for 10^6-deep paths).

    The (node, child_index) stack mimics exactly what recursion would do, so
    post-order is correct -- needed for tree DP (subtree sizes, etc.).
    """
    pre, post = [], []
    seen = [False] * len(adj)
    seen[root] = True
    stack = [(root, 0)]
    pre.append(root)
    while stack:
        u, i = stack[-1]
        if i < len(adj[u]):
            stack[-1] = (u, i + 1)
            v = adj[u][i]
            if not seen[v]:
                seen[v] = True
                pre.append(v)
                stack.append((v, 0))
        else:
            stack.pop()
            post.append(u)
    return pre, post


# ---------------------------------------------------------------- Trie
class Trie:
    """Dict-of-dicts trie. '$' marks end of word; a count gives prefix frequencies."""

    END = "$"

    def __init__(self):
        self.root: dict = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
            node["#"] = node.get("#", 0) + 1     # how many words pass through here
        node[self.END] = True

    def contains(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and self.END in node

    def count_prefix(self, prefix: str) -> int:
        node = self._walk(prefix)
        return 0 if node is None else node.get("#", 0)

    def _walk(self, s: str):
        node = self.root
        for ch in s:
            node = node.get(ch)
            if node is None:
                return None
        return node


# ---------------------------------------------------------------- Monotonic structures
def next_greater(nums: list[int]) -> list[int]:
    """Index of the next strictly greater element to the right, or -1. O(n) monotonic stack."""
    res = [-1] * len(nums)
    stack: list[int] = []                 # indices whose values are decreasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = i
        stack.append(i)
    return res


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """Max of every window of size k. O(n) monotonic deque."""
    dq: deque[int] = deque()              # indices, values decreasing front to back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


# ---------------------------------------------------------------- Binary search
def first_true(lo: int, hi: int, pred: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi) with pred(x) True, assuming pred is False...False True...True.

    Returns hi if pred is never True. The one binary search you need to remember:
    'binary search on the answer' is first_true over the answer range.
    """
    while lo < hi:
        mid = (lo + hi) // 2              # Python ints never overflow: no lo + (hi-lo)//2 needed
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def lis_length(nums: list[int]) -> int:
    """Longest strictly increasing subsequence, O(n log n) patience sorting."""
    tails: list[int] = []                 # tails[k] = smallest tail of an increasing run of length k+1
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


# ---------------------------------------------------------------- Strings
def prefix_function(s: str) -> list[int]:
    """KMP prefix function: pi[i] = length of the longest proper border of s[:i+1]."""
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def find_all(text: str, pattern: str) -> list[int]:
    """All start indices of pattern in text, O(n + m) via the prefix function."""
    if not pattern:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern + "\x00" + text)
    m = len(pattern)
    return [i - 2 * m for i in range(len(pi)) if pi[i] == m]


# ---------------------------------------------------------------- Modular arithmetic
MOD = 10**9 + 7


def build_factorials(n: int, mod: int = MOD) -> tuple[list[int], list[int]]:
    """fact[i] and inverse fact[i] for nCr mod p in O(1) after O(n) setup."""
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], -1, mod)        # Python 3.8+: modular inverse built in
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % mod
    return fact, inv


def ncr(n: int, r: int, fact: list[int], inv: list[int], mod: int = MOD) -> int:
    if r < 0 or r > n:
        return 0
    return fact[n] * inv[r] % mod * inv[n - r] % mod


# ---------------------------------------------------------------- Bitmask DP
def tsp_min_cost(dist: list[list[int]]) -> int:
    """Travelling salesman from city 0 and back, O(2^n * n^2). Classic bitmask DP.

    dp[mask][v] = cheapest way to start at 0, visit exactly the cities in mask, end at v.
    """
    n = len(dist)
    INF = float("inf")
    full = 1 << n
    dp = [[INF] * n for _ in range(full)]
    dp[1][0] = 0
    for mask in range(full):
        if not mask & 1:
            continue
        row = dp[mask]
        for v in range(n):
            cost = row[v]
            if cost == INF or not (mask >> v) & 1:
                continue
            for w in range(n):
                if (mask >> w) & 1:
                    continue
                nm = mask | (1 << w)
                if cost + dist[v][w] < dp[nm][w]:
                    dp[nm][w] = cost + dist[v][w]
    return min(dp[full - 1][v] + dist[v][0] for v in range(n))
