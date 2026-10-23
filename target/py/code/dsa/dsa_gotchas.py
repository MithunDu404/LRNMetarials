"""C++ -> Python behaviour differences that silently change DSA answers. Each prints real output.

Run:  py -3.12 target/py/code/dsa/dsa_gotchas.py
"""
import heapq
import math
import sys
from functools import cache


def header(t):
    print(f"\n--- {t} ---")


header("1. Division and modulo round toward minus infinity (C++ truncates toward zero)")
print("-7 // 2 =", -7 // 2, "   (C++: -3)")
print("-7 % 2  =", -7 % 2, "   (C++: -1)")
print("int(-7 / 2) =", int(-7 / 2), "  <- truncates like C++, but goes through a float")
print("math.fmod(-7, 2) =", math.fmod(-7, 2), " <- C-style remainder")
print("(-1) % (10**9 + 7) =", (-1) % (10**9 + 7), " <- always non-negative: no '+ MOD' fix-up needed")

header("2. Big integers: no overflow, but printing huge ones is limited")
big = 7 ** 10_000
print("7**10000 has", int(10_000 * math.log10(7)) + 1, "decimal digits; arithmetic on it is fine:", big % 1000)
try:
    str(big)
except ValueError as e:
    print("str(7**10000) ->", type(e).__name__ + ":", str(e)[:75] + "...")
sys.set_int_max_str_digits(0)          # 0 = no limit; put this at the top of CP solutions that print big ints
print("after sys.set_int_max_str_digits(0): printed", len(str(big)), "digits fine")

header("3. Bit operations treat ints as infinite two's complement")
print("~5 =", ~5, "  -5 >> 1 =", -5 >> 1, "  -1 & 0xFF =", -1 & 0xFF)
print("(1 << 64) =", 1 << 64, "  <- no wrap-around; mask with & ((1 << 64) - 1) to emulate uint64")
print("(13).bit_count() =", (13).bit_count(), "  (13).bit_length() =", (13).bit_length(),
      "  lowbit 12 & -12 =", 12 & -12)

header("4. round() is banker's rounding; floats are doubles")
print("round(0.5), round(1.5), round(2.5) =", round(0.5), round(1.5), round(2.5))
print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3, "  math.isclose ->", math.isclose(0.1 + 0.2, 0.3))
n = 10**18 - 1
print("int(math.sqrt(10**18 - 1)) =", int(math.sqrt(n)), " math.isqrt =", math.isqrt(n), "<- the float is wrong, isqrt is exact")
print("float(2**53 + 1) == 2**53 ->", float(2**53 + 1) == 2**53)

header("5. Heap tuples compare element by element; ties reach the payload")
try:
    h = []
    heapq.heappush(h, (1, {"node": "a"}))
    heapq.heappush(h, (1, {"node": "b"}))
except TypeError as e:
    print("push (1, dict) twice ->", type(e).__name__ + ":", e)
h = []
for i, payload in enumerate([{"node": "a"}, {"node": "b"}]):
    heapq.heappush(h, (1, i, payload))   # unique counter as tie-breaker
print("with (priority, counter, payload):", [x[2]["node"] for x in (heapq.heappop(h), heapq.heappop(h))])

header("6. Sorting: stable, key-based, and mixed types fail")
pairs = [("b", 2), ("a", 1), ("c", 2), ("d", 1)]
print("sorted by number only (stable keeps letter order):", sorted(pairs, key=lambda p: p[1]))
try:
    sorted([3, "a", 1])
except TypeError as e:
    print("sorted([3, 'a', 1]) ->", type(e).__name__ + ":", e)
print("max with key + default:", max([], default=None), max(["bb", "a", "ccc"], key=len))

header("7. 'is' is identity, '==' is value")
a, b = 256, 256
c, d = int("257"), int("257")
print("256 is 256 ->", a is b, " | int('257') is int('257') ->", c is d, " | == ->", c == d)
print("use 'is' only for None: x is None")

header("8. Strings: immutable, compared by code point, no char type")
print("'Z' < 'a' ->", "Z" < "a", "  ord('a') =", ord("a"), "  chr(98) =", chr(98))
print("'abc'[::-1] =", "abc"[::-1], "  'a,b,,c'.split(',') =", "a,b,,c".split(","), "  ' x '.split() =", " x ".split())
cnt = [0] * 26
for ch in "banana":
    cnt[ord(ch) - 97] += 1
print("letter counts of 'banana' via ord(ch) - 97:", {chr(i + 97): c for i, c in enumerate(cnt) if c})

header("9. Default arguments and @cache persist across calls / test cases")


@cache
def ways(n):
    return 1 if n <= 1 else ways(n - 1) + ways(n - 2)


print("ways(30) =", ways(30), " cache_info:", ways.cache_info())
ways.cache_clear()
print("after cache_clear():", ways.cache_info())

header("10. Copying 2D grids")
grid = [[0] * 3] * 2
grid[0][0] = 1
print("[[0]*3]*2 after grid[0][0]=1:", grid, " <- one row, two references")
grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 1
print("[[0]*3 for _ in range(2)]:   ", grid)
shallow = grid[:]
shallow[1][1] = 9
print("grid[:] is shallow, so grid changed too:", grid, " -> use [row[:] for row in grid]")
