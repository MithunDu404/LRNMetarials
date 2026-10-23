"""Every template is checked against a slow, obviously-correct version on random inputs."""
import itertools
import math
import random

import pytest

from dsa_templates import (
    DSU, Fenwick, SegTree, Trie, bfs_01, build_factorials, dijkstra, find_all, first_true,
    iterative_dfs_order, lis_length, ncr, next_greater, prefix_function, sliding_window_max,
    topo_sort, tsp_min_cost,
)

rng = random.Random(2026)


def test_dsu_matches_brute_force_components():
    for _ in range(50):
        n = rng.randint(1, 30)
        dsu = DSU(n)
        label = list(range(n))                       # brute force: relabel on every union
        for _ in range(rng.randint(0, 40)):
            a, b = rng.randrange(n), rng.randrange(n)
            merged = dsu.union(a, b)
            assert merged == (label[a] != label[b])
            old, new = label[b], label[a]
            label = [new if x == old else x for x in label]
            assert dsu.components == len(set(label))
            assert (dsu.find(a) == dsu.find(b))


def test_fenwick_matches_list_sums():
    for _ in range(50):
        vals = [rng.randint(-50, 50) for _ in range(rng.randint(1, 40))]
        fw = Fenwick.from_list(vals)
        for _ in range(60):
            i = rng.randrange(len(vals))
            d = rng.randint(-10, 10)
            vals[i] += d
            fw.add(i, d)
            lo = rng.randint(0, len(vals))
            hi = rng.randint(lo, len(vals))
            assert fw.range_sum(lo, hi) == sum(vals[lo:hi])


@pytest.mark.parametrize("op,e", [(min, math.inf), (max, -math.inf), (math.gcd, 0), (lambda a, b: a + b, 0)])
def test_segtree_matches_slices(op, e):
    for _ in range(30):
        vals = [rng.randint(0, 100) for _ in range(rng.randint(1, 40))]
        st = SegTree(vals, op, e)
        for _ in range(60):
            i = rng.randrange(len(vals))
            vals[i] = rng.randint(0, 100)
            st.set(i, vals[i])
            lo = rng.randint(0, len(vals) - 1)
            hi = rng.randint(lo + 1, len(vals))
            expect = e
            for v in vals[lo:hi]:
                expect = op(expect, v)
            assert st.query(lo, hi) == expect


def random_graph(n, m, weights):
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = rng.randrange(n), rng.randrange(n)
        adj[u].append((v, rng.choice(weights)))
    return adj


def bellman_ford(adj, src):
    dist = [math.inf] * len(adj)
    dist[src] = 0
    for _ in range(len(adj)):
        for u in range(len(adj)):
            for v, w in adj[u]:
                dist[v] = min(dist[v], dist[u] + w)
    return dist


def test_dijkstra_and_01bfs_match_bellman_ford():
    for _ in range(40):
        n = rng.randint(1, 15)
        g = random_graph(n, rng.randint(0, 40), weights=range(0, 20))
        assert dijkstra(g, 0) == bellman_ford(g, 0)
        g01 = random_graph(n, rng.randint(0, 40), weights=(0, 1))
        assert bfs_01(g01, 0) == bellman_ford(g01, 0)


def test_topo_sort_valid_or_detects_cycle():
    for _ in range(60):
        n = rng.randint(1, 10)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 15))]
        order = topo_sort(n, edges)
        has_cycle = not any(
            all(p.index(u) < p.index(v) for u, v in edges) for p in itertools.permutations(range(n))
        )
        if has_cycle:
            assert order is None
        else:
            pos = {v: i for i, v in enumerate(order)}
            assert all(pos[u] < pos[v] for u, v in edges)


def test_iterative_dfs_matches_recursive_and_survives_deep_paths():
    for _ in range(30):
        n = rng.randint(1, 30)
        adj = [[] for _ in range(n)]
        for v in range(1, n):                           # random tree
            u = rng.randrange(v)
            adj[u].append(v)
            adj[v].append(u)
        pre_r, post_r, seen = [], [], set()

        def rec(u):
            seen.add(u)
            pre_r.append(u)
            for v in adj[u]:
                if v not in seen:
                    rec(v)
            post_r.append(u)

        rec(0)
        assert iterative_dfs_order(adj, 0) == (pre_r, post_r)
    n = 200_000                                         # a path 200k deep: recursion would die
    path = [[i + 1] if i + 1 < n else [] for i in range(n)]
    pre, post = iterative_dfs_order(path, 0)
    assert pre[-1] == n - 1 and post[0] == n - 1


def test_trie():
    words = ["app", "apple", "apply", "bat", "bath"]
    t = Trie()
    for w in words:
        t.insert(w)
    assert t.contains("app") and not t.contains("ap")
    assert t.count_prefix("app") == 3 and t.count_prefix("ba") == 2 and t.count_prefix("z") == 0


def test_monotonic_helpers():
    for _ in range(100):
        a = [rng.randint(0, 9) for _ in range(rng.randint(1, 25))]
        brute = [next((j for j in range(i + 1, len(a)) if a[j] > a[i]), -1) for i in range(len(a))]
        assert next_greater(a) == brute
        k = rng.randint(1, len(a))
        assert sliding_window_max(a, k) == [max(a[i:i + k]) for i in range(len(a) - k + 1)]


def test_first_true_and_lis():
    for _ in range(100):
        cut = rng.randint(0, 50)
        assert first_true(0, 50, lambda x: x >= cut) == cut
        a = [rng.randint(0, 20) for _ in range(rng.randint(0, 9))]
        brute = max((len(s) for r in range(len(a) + 1) for s in itertools.combinations(a, r)
                     if all(x < y for x, y in zip(s, s[1:]))), default=0)
        assert lis_length(a) == brute
    # binary search on the answer: integer square root
    assert first_true(0, 10**6 + 1, lambda x: x * x > 10**9) - 1 == math.isqrt(10**9)


def test_kmp_matches_naive_search():
    for _ in range(200):
        text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 30)))
        pat = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
        naive = [i for i in range(len(text) - len(pat) + 1) if text[i:i + len(pat)] == pat]
        assert find_all(text, pat) == naive
    assert prefix_function("abacaba") == [0, 0, 1, 0, 1, 2, 3]


def test_ncr_matches_math_comb():
    fact, inv = build_factorials(200)
    for n in range(0, 60):
        for r in range(-1, n + 2):
            expect = math.comb(n, r) % (10**9 + 7) if 0 <= r <= n else 0
            assert ncr(n, r, fact, inv) == expect


def test_tsp_matches_permutations():
    for _ in range(15):
        n = rng.randint(2, 7)
        d = [[0 if i == j else rng.randint(1, 30) for j in range(n)] for i in range(n)]
        brute = min(sum(d[a][b] for a, b in zip((0, *p), (*p, 0))) for p in itertools.permutations(range(1, n)))
        assert tsp_min_cost(d) == brute
