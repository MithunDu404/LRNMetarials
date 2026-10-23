"""Worked LeetCode-style patterns in idiomatic Python. Each prints its answer; the guide pastes this output.

Run:  py -3.12 target/py/code/dsa/dsa_patterns.py
"""
import itertools
import operator
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cmp_to_key, reduce

from dsa_templates import DSU, Fenwick, dijkstra, first_true, topo_sort


def show(title, value):
    print(f"{title:<52} {value}")


print("=== The standard-library toolkit ===")
a = [3, 1, 4, 1, 5, 9, 2, 6]
show("prefix sums  accumulate(a, initial=0)", list(itertools.accumulate(a, initial=0)))
show("running max  accumulate(a, max)", list(itertools.accumulate(a, max)))
show("adjacent pairs  pairwise(a) -> diffs", [y - x for x, y in itertools.pairwise(a)])
show("combinations('abc', 2)", ["".join(c) for c in itertools.combinations("abc", 2)])
show("product([0,1], repeat=3)  (all bitstrings)", ["".join(map(str, p)) for p in itertools.product([0, 1], repeat=3)])
show("groupby on SORTED data: run lengths of 'aaabccdd'", [(k, len(list(g))) for k, g in itertools.groupby("aaabccdd")])
show("chain.from_iterable([[1,2],[3],[4,5]])", list(itertools.chain.from_iterable([[1, 2], [3], [4, 5]])))
show("reduce(operator.xor, [4,1,2,1,2])  (single number)", reduce(operator.xor, [4, 1, 2, 1, 2]))
show("Counter('banana').most_common(2)", Counter("banana").most_common(2))
show("zip(*matrix)  (transpose)", list(zip(*[[1, 2, 3], [4, 5, 6]])))
show("divmod(17, 5)", divmod(17, 5))
show("sorted by length then alphabet", sorted(["bb", "a", "ccc", "ab"], key=lambda s: (len(s), s)))

print("\n=== Sliding window: longest substring without repeats ===")


def longest_unique(s: str) -> int:
    last = {}
    best = left = 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1           # jump the window past the previous copy
        last[ch] = right
        best = max(best, right - left + 1)
    return best


for s in ("abcabcbb", "bbbbb", "pwwkew"):
    show(f"longest_unique({s!r})", longest_unique(s))

print("\n=== Two pointers on a sorted array: pair with target sum ===")


def pair_sum(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == target:
            return i, j
        if s < target:
            i += 1
        else:
            j -= 1
    return None


show("pair_sum([1,2,4,7,11,15], 15)", pair_sum([1, 2, 4, 7, 11, 15], 15))

print("\n=== Binary search on the answer: minimum ship capacity in D days ===")


def ship_within_days(weights, days):
    def can(cap):
        need, load = 1, 0
        for w in weights:
            if load + w > cap:
                need, load = need + 1, 0
            load += w
        return need <= days
    return first_true(max(weights), sum(weights) + 1, can)


show("ship_within_days([1..10], 5)", ship_within_days(list(range(1, 11)), 5))
arr = [1, 2, 2, 2, 5]
show("count of 2 in sorted arr: bisect_right - bisect_left", bisect_right(arr, 2) - bisect_left(arr, 2))

print("\n=== Intervals: merge overlapping ===")


def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


show("merge([[1,3],[8,10],[2,6],[15,18]])", merge([[1, 3], [8, 10], [2, 6], [15, 18]]))

print("\n=== Monotonic stack: days until a warmer temperature ===")


def daily_temperatures(t):
    res, stack = [0] * len(t), []
    for i, x in enumerate(t):
        while stack and t[stack[-1]] < x:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


show("daily_temperatures([73,74,75,71,69,72,76,73])", daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))

print("\n=== Grid BFS: shortest path, 4 directions ===")


def grid_shortest(grid):
    R, C = len(grid), len(grid[0])
    dist = [[-1] * C for _ in range(R)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "." and dist[nr][nc] < 0:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist[R - 1][C - 1]


show("grid_shortest(4x4 maze)", grid_shortest(["..#.", "#...", ".#.#", "...."]))

print("\n=== Graphs with the templates ===")
show("topo_sort: 4 courses, prereqs 0->1, 0->2, 1->3, 2->3", topo_sort(4, [(0, 1), (0, 2), (1, 3), (2, 3)]))
show("topo_sort with a cycle 0->1->0", topo_sort(2, [(0, 1), (1, 0)]))
adj = [[] for _ in range(4)]
for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]:
    adj[u].append((v, w))
show("dijkstra from 0", dijkstra(adj, 0))
dsu = DSU(5)
redundant = next((e for e in [(0, 1), (1, 2), (3, 4), (2, 0)] if not dsu.union(*e)), None)
show("union-find: first edge closing a cycle", redundant)

print("\n=== DP, written the Python way ===")


def edit_distance(a, b):
    prev = list(range(len(b) + 1))        # rolling 1-D rows: O(len(b)) memory
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def knapsack(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):   # backwards: each item used at most once
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]


def coin_ways(coins, amount):
    dp = [1] + [0] * amount
    for coin in coins:                    # coins outer: combinations, not permutations
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]
    return dp[amount]


show("edit_distance('horse', 'ros')", edit_distance("horse", "ros"))
show("knapsack(w=[1,3,4,5], v=[1,4,5,7], cap=7)", knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))
show("coin_ways([1,2,5], 5)", coin_ways([1, 2, 5], 5))

print("\n=== Counting with a Fenwick tree: inversions ===")


def inversions(nums):
    rank = {v: i for i, v in enumerate(sorted(set(nums)))}   # coordinate compression
    fw, inv = Fenwick(len(rank)), 0
    for seen, x in enumerate(nums):
        r = rank[x]
        inv += seen - fw.prefix(r + 1)    # earlier elements greater than x
        fw.add(r, 1)
    return inv


show("inversions([8, 4, 2, 1])", inversions([8, 4, 2, 1]))
show("inversions([3, 1, 2])", inversions([3, 1, 2]))

print("\n=== Custom comparison when a key won't do ===")
nums = [3, 30, 34, 5, 9]
order = sorted(map(str, nums), key=cmp_to_key(lambda x, y: (y + x > x + y) - (y + x < x + y)))
show("largest number from [3,30,34,5,9]", "".join(order))

print("\n=== Grouping: anagrams with a tuple key ===")
groups = defaultdict(list)
for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
    groups[tuple(sorted(w))].append(w)
show("group anagrams", list(groups.values()))

try:
    from sortedcontainers import SortedList

    print("\n=== Ordered set (LeetCode has sortedcontainers; Codeforces does not) ===")
    sl = SortedList([5, 1, 9, 3])
    sl.add(4)
    show("SortedList after add(4)", list(sl))
    show("first >= 4 (lower_bound)", sl[sl.bisect_left(4)])
    show("largest < 4 (predecessor)", sl[sl.bisect_left(4) - 1])
    sl.remove(9)
    show("after remove(9); k-th smallest sl[2]", sl[2])
except ImportError:
    pass
