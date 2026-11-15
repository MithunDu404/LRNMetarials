# p2_s10_recap.py: recap of Part 2 (no new facts; numbers re-checked here).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *


class P2S10Recap(CnnScene):
    def construct(self):
        assert conv_out(227, 11, 0, 4) == 55 and 96 * (11 * 11 * 3 + 1) == 34944
        assert conv_out(32, 5, 0, 1) == 28 and 6 * (5 * 5 * 1 + 1) == 156
        self.recap("Recap of Part 2", [
            r"1. $W_2 = \left\lfloor \dfrac{W_1 - F + 2P}{S} \right\rfloor + 1$, \quad $D_2 = K$",
            r"2. AlexNet: $55 \times 55 \times 96$, 34,944 parameters. LeNet-5: $28 \times 28 \times 6$, 156",
            r"3. CNNs: sparse connections and weight sharing",
            r"4. Pooling: smaller $W$ and $H$, no parameters, same depth",
            r"5. Flatten: a vector of $W \cdot H \cdot C$ values for the classifier",
        ])
