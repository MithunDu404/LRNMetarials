# p1_s11_recap.py: recap of Part 1 (no new facts).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *


class P1S11Recap(CnnScene):
    def construct(self):
        self.recap("Recap of Part 1", [
            r"1. Convolution: slide a kernel, take a dot product (really cross-correlation)",
            r"2. No padding: output shrinks by $F - 1$. Same padding: $P = \dfrac{F-1}{2}$",
            r"3. Smoothing sums to 1, edges sum to 0, unsharp $=$ identity $+$ Laplacian",
            r"4. Dilation: wider reach, same number of weights",
            r"5. Volumes: filter depth $=$ input depth; $K$ filters give depth $K$",
        ])
