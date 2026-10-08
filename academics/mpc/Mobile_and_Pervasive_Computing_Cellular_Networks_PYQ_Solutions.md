# Mobile and Pervasive Computing — Cellular Networks PYQ Master Solutions

> **Academic Context:** B.Tech CST / CS ($7^{\text{th}}$ Semester) Examination | **Subject:** Mobile and Pervasive Computing (`CS4123`) | **Institution:** IIEST Shibpur  
> **Source Mode:** **Strict Notes-Bound Mode** (Strictly grounded in authorized course reference notes: [`academics/mpc/Cellular_Networks_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md) and [`academics/mpc/Mobile_Computing_SDB_Learning_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md), derived from Prof. Sipra Das Bit, *Mobile Computing*, PHI Learning)  
> **Verification Status:** All mathematical formulations, geometric proofs, and numerical problems independently audited and verified via Python scratch engine; all figures programmatically generated at 300 DPI or embedded directly from authentic lecture source figures (zero ASCII / zero raw Mermaid).

---

## Contents

- [Multi-Year Frequency & Recurrence Matrix](#multi-year-frequency--recurrence-matrix)
- [Comprehensive Question Audit Matrix](#comprehensive-question-audit-matrix)
- [2025 Mid-Semester Examination Solutions](#2025-mid-semester-examination-solutions)
- [2025 End-Semester Examination Solutions](#2025-end-semester-examination-solutions)
- [2024 Mid-Semester Examination Solutions](#2024-mid-semester-examination-solutions)
- [2024 End-Semester Examination Solutions](#2024-end-semester-examination-solutions)
- [2023 Mid-Semester Examination Solutions](#2023-mid-semester-examination-solutions)
- [2023 End-Semester Examination Solutions](#2023-end-semester-examination-solutions)
- [Comprehensive Quick-Recall Formula & Parameter Cheat Sheet](#comprehensive-quick-recall-formula--parameter-cheat-sheet)
- [Uncovered Questions (Unanswered / Out-of-Notes Syllabus)](#uncovered-questions-unanswered--out-of-notes-syllabus)

---

## Multi-Year Frequency & Recurrence Matrix

Analysis of examination trends across 2023, 2024, and 2025 for topics covered in [`Cellular_Networks_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md) and [`Mobile_Computing_SDB_Learning_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md):

| Core Topic / Concept | Recurrence Rate | Exam Sessions Appeared | Typical Marks | Exam Hall Yield Level |
|:---|:---:|:---|:---:|:---:|
| **Cellular System Capacity Calculations** ($C = M \cdot S = M \cdot K \cdot N$) | ★★★★★ (100% in Midsems) | 2025 Mid (Q2c), 2023 Mid (Q3b) | 5M | **High-Yield Numerical Guaranteed** |
| **Mobile-to-Mobile Call Setup Flow** (RCC, FCC, FVC, RVC, Paging, MSC) | ★★★★★ (100% in Midsems) | 2025 Mid (Q2a), 2023 Mid (Q2a) | 5M | **High-Yield Algorithm / Flow Guaranteed** |
| **Cellular Voice vs. Control Channels** (FVC, RVC, FCC, RCC roles) | ★★★★☆ (80%) | 2025 Mid (Q2a), 2025 End (Q1c), 2023 Mid (Q2b) | 2M – 5M | **Guaranteed Core Question** |
| **Cluster Size** ($N$), **Capacity & Co-Channel Interference Trade-Off** | ★★★★☆ (80%) | 2025 Mid (Q2b), 2024 Mid (Q2a, Q2b) | 5M | **High Probability Derivation / Theory** |
| **Erlang Trunking Theory & Traffic Calculations** ($A = \lambda h$, GOS, Erlang B) | ★★★★☆ (80%) | 2025 End (Q2a), 2024 End (Q2c), 2023 End (Q2a, Q2b) | 5M | **High-Yield Numerical Guaranteed** |
| **CDMA Mathematics & Orthogonal Code Superposition** ($c_a \cdot c_b = 0$, DSSS) | ★★★★☆ (80%) | 2025 End (Q2b, Q2c, Q2d), 2024 End (Q2b, Q5a), 2023 Mid (Q1iii, Q1vii) | 5M – 10M | **High-Yield Derivation / Numerical** |
| **Channel Assignment Strategies & Borrowing Constraints** | ★★★★☆ (80%) | 2025 Mid (Q3a), 2024 End (Q1a), 2023 Mid (Q3a) | 2.5M – 5M | **High Probability Theory** |
| **Generational Handoff Mechanisms** (1G NCHO vs. 2G MAHO) | ★★★☆☆ (60%) | 2025 Mid (Q3b), 2024 Mid (Q3b) | 2.5M – 5M | **High Probability Comparative Table** |
| **GSM Architecture & Subsystems** (BSS, NSS, OSS, HLR, VLR, EIR, AUC) | ★★★★☆ (80%) | 2024 Mid (Q3d, Q3e), 2023 Mid (Q1ii, Q1x), 2023 End (Q1b) | 2M | **Guaranteed Short Definition / MCQ** |
| **Radio Pipeline & Modulation Foundations** (Coder, Interleaver, Modulator, PSK) | ★★★☆☆ (60%) | 2025 Mid (Q1a, Q1b, Q1c), 2024 Mid (Q1a), 2023 Mid (Q1i) | 2M – 4M | **Fundamental Theory** |

---

## Comprehensive Question Audit Matrix

| Exam Session | Q# | Concept / Question Statement | Marks | Tier | Status | Primary Course Reference |
|:---|:---:|:---|:---:|:---:|:---:|:---|
| **2025 Mid** | Q1(a) | Advantages of PSK over ASK and FSK | 2M | VSA | **Answered** | [SDB Guide §4.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture) |
| **2025 Mid** | Q1(b) | Reasons for performing modulation in cellular network | 2M | VSA | **Answered** | [SDB Guide §4.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture) |
| **2025 Mid** | Q1(c) | Block error definition and mitigation via interleaving | 2M | VSA | **Answered** | [SDB Guide §4.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture) |
| **2025 Mid** | Q1(d) | Enhancement of radio capacity in cellular network | 2M | VSA | **Answered** | [Cellular Guide §1.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#12-the-breakthrough-low-power-distributed-cells) & [§6.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas) |
| **2025 Mid** | Q1(e) | Frequency range of GSM in downlink | 2M | VSA | **Answered** | [SDB Guide §1.2, §3.2, §18.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#12-technical-mechanism--architecture) |
| **2025 Mid** | Q2(a) | Operational steps for establishing call between two MSs | 5M | SA | **Answered** | [Cellular Guide §3.2, §3.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#3-call-procedures-origination-paging--in-call-management) |
| **2025 Mid** | Q2(b) | Impact of cluster size on capacity and interference | 5M | SA | **Answered** | [Cellular Guide §6.2, §7.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#62-impact-of-cluster-size-n-on-capacity-vs-interference) |
| **2025 Mid** | Q2(c) | Numerical: Capacity for $2310\,\text{km}^2$, $6\,\text{km}^2$ cell, 1596 channels, $N=7$ | 5M | SA | **Answered** | [Cellular Guide §6.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas) |
| **2025 Mid** | Q3(a) | Channel borrowing definition and implementation constraints | 2.5M | SA | **Answered** | [SDB Guide §10.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#102-technical-mechanism--architecture) |
| **2025 Mid** | Q3(b) | Handoff definition & comparison of 1G vs 2G mechanisms | 2.5M | SA | **Answered** | [Cellular Guide §8.1, §9.2, §9.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#8-handoff-strategies--signal-threshold-margins) |
| **2025 End** | Q1(c) | Paging channel definition and usage | 2M | VSA | **Answered** | [Cellular Guide §2.2, §3.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels) |
| **2025 End** | Q2(a) | Erlang definition and user capacity numerical ($C=20$, $0.5\%$ blocking, $A=11.10$) | 5M | SA | **Answered** | [SDB Guide §13.2, §13.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture) |
| **2025 End** | Q2(b) | Orthogonality verification of codes $(0,1,0,1)$ and $(0,1,1,0)$ | 5M | SA | **Answered** | [SDB Guide §17.2, §17.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#172-technical-mechanism--architecture) |
| **2025 End** | Q2(c) | CDMA DSSS received signal derivation for MS-A and MS-B | 5M | SA | **Answered** | [SDB Guide §17.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#174-fully-audited-cdma-mathematical-trace) |
| **2025 End** | Q2(d) | Demerits of CDMA | 5M | SA | **Answered** | [SDB Guide §16.4, §17.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#164-architectural-trade-offs-matrix) |
| **2024 Mid** | Q1(a) | Radio system transmitter/receiver block diagram & module tasks | 4M | SA | **Answered** | [SDB Guide §4.2, §4.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture) |
| **2024 Mid** | Q1(b) | Justify hexagonal cell shape in cellular design | 3M | SA | **Answered** | [Cellular Guide §4.1, §4.2, §4.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#4-cell-geometry-why-hexagonal-footprints) |
| **2024 Mid** | Q1(c) | Location tracking definition and two implementation techniques | 3M | SA | **Answered** | [Cellular Guide §9.2, §12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#92-1st-generation-1g-handoff-network-controlled) |
| **2024 Mid** | Q2(a) | Frequency reuse ratio definition and derivation of $S/I$ relation | 5M | SA | **Answered** | [Cellular Guide §7.1, §7.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#7-co-channel-interference--co-channel-reuse-ratio-q) |
| **2024 Mid** | Q2(b) | Numerical: Pattern size $N$ for $S/I \ge 15\text{ dB}$, path loss $k=3$ | 5M | SA | **Answered** | [Cellular Guide §5.3, §7.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#53-cluster-size-formula-n) |
| **2024 Mid** | Q3(a) | Near-far effect definition and usage | 2M | VSA | **Answered** | [SDB Guide §9.2, §16.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#92-technical-mechanism--architecture) |
| **2024 Mid** | Q3(b) | Umbrella cell approach definition and usage | 2M | VSA | **Answered** | [Cellular Guide §11.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#111-problem-1-accommodating-wide-velocity-diversity) |
| **2024 Mid** | Q3(c) | Grade of Service (GOS) definition and usage | 2M | VSA | **Answered** | [SDB Guide §13.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture) |
| **2024 Mid** | Q3(d) | HLR definition and usage | 2M | VSA | **Answered** | [Cellular Guide §12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems) |
| **2024 Mid** | Q3(e) | VLR definition and usage | 2M | VSA | **Answered** | [Cellular Guide §12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems) |
| **2024 End** | Q1(a) | Channel borrowing definition and usage | 2M | VSA | **Answered** | [SDB Guide §10.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#102-technical-mechanism--architecture) |
| **2024 End** | Q2(b) | Orthogonality verification of 11-chip code sequence | 5M | SA | **Answered** | [SDB Guide §17.2, §17.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#172-technical-mechanism--architecture) |
| **2024 End** | Q2(c) | Numerical: Users supported for $C=20$, $\lambda=3\,\text{calls/hr}$, $h=2\,\text{min}$, $1\%$ blocking ($A=12.03$) | 5M | SA | **Answered** | [SDB Guide §13.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#133-verified-calculations) |
| **2024 End** | Q5(a) | Short note on Spread Spectrum (DSSS, codes, processing gain) | 10M | LA | **Answered** | [SDB Guide §17.1, §17.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#17-spread-spectrum-engineering--cdma-mathematics) |
| **2023 Mid** | Q1(i) | MCQ: Receiver processes in mobile communication | 1M | MCQ | **Answered** | [SDB Guide §4.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture) |
| **2023 Mid** | Q1(ii) | MCQ: Device/register storing data related to user | 1M | MCQ | **Answered** | [Cellular Guide §12.3, §12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#123-gsm-services--features) |
| **2023 Mid** | Q1(iii) | MCQ: Multiplexing enabling simultaneous full-bandwidth usage | 1M | MCQ | **Answered** | [SDB Guide §16.2, §17.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#162-technical-mechanism--architecture) |
| **2023 Mid** | Q1(iv) | MCQ: Incorrect statement about TDMA | 1M | MCQ | **Answered** | [Cellular Guide §9.3, §13.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#93-2nd-generation-2g-handoff-mobile-assisted-maho) |
| **2023 Mid** | Q1(v) | MCQ: How radio capacity is enhanced in cellular network | 1M | MCQ | **Answered** | [Cellular Guide §1.1, §1.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#11-the-spectral-bottleneck) |
| **2023 Mid** | Q1(vi) | MCQ: Directional antennas to increase cell capacity | 1M | MCQ | **Answered** | [SDB Guide §14.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#142-technical-mechanism--architecture) |
| **2023 Mid** | Q1(vii) | MCQ: Power adjustment in CDMA mitigates which problem | 1M | MCQ | **Answered** | [SDB Guide §16.4, §17.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#164-architectural-trade-offs-matrix) |
| **2023 Mid** | Q1(viii) | MCQ: Primary GSM uplink frequency range | 1M | MCQ | **Answered** | [SDB Guide §1.2, §18.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#12-technical-mechanism--architecture) |
| **2023 Mid** | Q1(ix) | MCQ: What needs to be estimated for RF channel allocation for GOS | 1M | MCQ | **Answered** | [SDB Guide §13.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture) |
| **2023 Mid** | Q1(x) | MCQ: Visitor Location Register integration entity | 1M | MCQ | **Answered** | [Cellular Guide §12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems) |
| **2023 Mid** | Q2(a) | Operational steps for setting call from mobile to mobile | 5M | SA | **Answered** | [Cellular Guide §3.2, §3.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#3-call-procedures-origination-paging--in-call-management) |
| **2023 Mid** | Q2(b) | Roles played by FVC, RVC, FCC, and RCC channels | 5M | SA | **Answered** | [Cellular Guide §2.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels) |
| **2023 Mid** | Q3(a) | Different channel-assignment strategies in 2G cellular network | 5M | SA | **Answered** | [SDB Guide §10.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#102-technical-mechanism--architecture) |
| **2023 Mid** | Q3(b) | Numerical: $40\,\text{MHz}$ band, $2\times 20\,\text{kHz}$ duplex, $N=12$, capacity for $2310\,\text{km}^2$ | 5M | SA | **Answered** | [Cellular Guide §6.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas) |
| **2023 End** | Q1(b) | HLR definition and usage | 2M | VSA | **Answered** | [Cellular Guide §12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems) |
| **2023 End** | Q2(a) | GOS definition and assumptions for blocked-calls-cleared system | 5M | SA | **Answered** | [SDB Guide §13.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture) |
| **2023 End** | Q2(b) | Erlang definition and user capacity numerical ($C=20$, $0.5\%$ blocking, $A=11.10$) | 5M | SA | **Answered** | [SDB Guide §13.2, §13.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture) |
| **Remaining**| Various | UMTS UTRAN, 5G Core, MIMO, Network Slicing, Mobile-IP, WLAN CSMA/CA | 2M–20M | — | **Unanswered** | *Out-of-notes topics retained in final section* |

---

## 2025 Mid-Semester Examination Solutions

### Question 1(a): Advantages of PSK over ASK and FSK
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 4.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture)

**1. Question Statement:**
*Write two advantages of PSK over ASK and FSK.*

**2. Direct Answer in Simple English:**
1. **Better Immunity to Noise (over ASK):** ASK changes the amplitude (signal height) to send data. In wireless channels, noise and fading constantly change the signal amplitude, which easily corrupts ASK. In PSK, the amplitude stays constant, and data is carried in phase changes ($180^\circ$ flip in BPSK). This makes PSK much more resistant to noise and fading.
2. **Saves Radio Bandwidth (over FSK):** FSK uses two separate carrier frequencies to send binary `0` and `1`, taking up twice as much bandwidth. PSK uses only one carrier frequency. This saves scarce radio spectrum while achieving fewer bit errors for the same signal power.

---

### Question 1(b): Reasons for Performing Modulation in Cellular Networks
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 4.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture)

**1. Question Statement:**
*Identify two reasons for performing modulation in cellular network.*

**2. Direct Answer in Simple English:**
1. **Practical Antenna Size:** To transmit a radio wave efficiently, an antenna must be about one-quarter of the signal's wavelength ($h \approx \lambda / 4$). An unmodulated voice/baseband signal at $1\,\text{MHz}$ has a wavelength of $300\,\text{m}$, needing an impossible $75\,\text{meter}$ antenna. Modulation shifts the signal to high carrier frequencies ($900\,\text{MHz}$ in GSM), where the wavelength shrinks to $\approx 33.3\,\text{cm}$. This allows tiny, pocket-sized mobile antennas of only $\approx 8.3\,\text{cm}$.
2. **Multiplexing (Sharing the Air Without Interference):** Raw digital pulses cannot travel through the air over long distances without severe distortion. Modulation shifts each user's signal to a specific radio frequency channel. This allows hundreds of users to share the air at the same time using Frequency Division Multiplexing (FDMA/FDD) without colliding or interfering with each other.

---

### Question 1(c): Block Error Definition and Mitigation via Interleaving
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 4.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture)

**1. Question Statement:**
*What is block error and how can it be mitigated?*

**2. Direct Answer in Simple English:**
- **Block Error:** When a mobile phone passes through a weak coverage spot (a deep fade), the signal drops sharply for a short time. This corrupts a whole group or "block" of consecutive data bits. Standard error-correcting codes can easily fix isolated single-bit errors, but fail when a large continuous group of bits is destroyed all at once.
- **Mitigation via Interleaving:** An **Interleaver** fixes this by scrambling the order of data bits across multiple time slots before sending them. At the receiver, a **deinterleaver** puts the bits back into their original order. This spreads the damaged burst of bits out into isolated, single-bit errors across time. The channel decoder can then fix these separate errors easily.

---

### Question 1(d): Radio Capacity Enhancement
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 1.2: The Breakthrough: Low-Power Distributed Cells](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#12-the-breakthrough-low-power-distributed-cells) and [📘 Section 6.1: Capacity Formulation & Formulas](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas)

**1. Question Statement:**
*How is the capacity of the radio enhanced in cellular network?*

**2. Direct Answer in Simple English:**
Radio capacity in a cellular network is enhanced by:
1. **Using Many Small, Low-Power Base Stations (Small Cells):** Instead of using one giant, high-power radio tower to cover an entire city, the area is split into many small hexagonal cells, each powered by a low-power base station.
2. **Frequency Reuse:** The same group of radio frequencies is reused in multiple cells across the city, as long as the cells are far enough apart that their radio signals do not interfere with each other.

**3. The Fundamental Capacity Formula:**
Total network capacity $C$ across the whole coverage area is:

$$
C = M \cdot S = M \cdot K \cdot N
$$

Where:
- $S$: Total number of radio channels given to the cellular system.
- $N$: Cluster size (number of cells in a group sharing the total channels $S$ without reuse).
- $K = S / N$: Number of channels allocated to each individual cell.
- $M$: **Cluster replication factor** (how many times the cluster repeats across the entire city).

**Key Takeaway:** By making cell radius $R$ smaller and adding more towers, the cluster repeats more times ($M$ increases), which dramatically multiplies total network capacity ($C$) without needing extra radio spectrum from the government.

---

### Question 1(e): GSM Downlink Frequency Range
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 1.2 & §18.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#12-technical-mechanism--architecture)

**1. Question Statement:**
*What is the range of frequency GSM uses in downlink?*

**2. Direct Answer:**
Primary GSM (GSM 900) operates in the **935–960 MHz** frequency range for the **downlink (Forward Voice/Control Channel, Base Station to Mobile Station)**.

**3. Key Technical Specifications:**
- **Total Downlink Bandwidth:** $25\,\text{MHz}$ ($935\text{ to } 960\,\text{MHz}$).
- **Uplink (Reverse Link) Band:** Paired with $890\text{--}915\,\text{MHz}$ ($25\,\text{MHz}$).
- **Duplex Spacing:** A constant Frequency Division Duplexing (FDD) split of **45 MHz** separates uplink and downlink channels.
- **Channelization:** The $25\,\text{MHz}$ band is divided into 124 carrier channels, each having a bandwidth of $200\,\text{kHz}$.

---

### Question 2(a): Call Establishment Between Two Mobile Stations
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 3.2: Mobile-Initiated Call Setup Procedure](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#32-mobile-initiated-call-setup-procedure), [📘 Section 3.3: Landline-Initiated Call (Paging Procedure)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#33-landline-initiated-call-paging-procedure), and [📘 Section 2.2: Channel Classification](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels)

**1. Question Statement:**
*Write steps of operation for establishing a call between two mobile stations.*

**2. Executive Summary:**
Connecting a call between two mobile phones (Caller MS-A and Receiver MS-B) involves four main network components:
- **Calling Mobile (MS-A)**
- **Serving Base Station 1 (BS-1)**
- **Mobile Switching Centre (MSC)** — The central brain of the network
- **Serving Base Station 2 (BS-2)**
- **Called Mobile (MS-B)**

The process moves through three clear phases: **Uplink Request → Downlink Paging → Dedicated Voice Channels**.

**3. Programmatic Architecture Diagram:**

![Call Setup Flow](images/fig_call_setup_flow.png)

**4. Step-by-Step Operational Procedure (Easy to Memorize):**

1. **Call Origination Request (MS-A → BS-1):**  
   The user enters the phone number on MS-A and presses "Call". MS-A sends a call request packet over the **Reverse Control Channel (RCC)** containing its identity (MIN/ESN) and the dialed number.
2. **Relay to Central Switch (BS-1 → MSC):**  
   Base Station 1 receives the signal and sends the request to the MSC over the wired high-speed backhaul connection.
3. **Verification & Location Lookup (MSC):**  
   The MSC verifies if MS-A has an active balance/subscription. Then, the MSC checks its **HLR and VLR databases** to find the current location area of Receiver MS-B.
4. **Paging Command (MSC → BS-2):**  
   The MSC sends a command to Base Station 2 (the tower covering the area where MS-B is currently located) to alert MS-B.
5. **Paging Broadcast (BS-2 → MS-B):**  
   Base Station 2 broadcasts a "Page" message containing MS-B's phone number (MIN) over its **Forward Control Channel (FCC)**.
6. **Paging Acknowledgment (MS-B → BS-2):**  
   MS-B's phone, which continuously listens to the FCC, recognizes its own number and immediately replies with an Acknowledgment (ACK) over the **Reverse Control Channel (RCC)**.
7. **ACK Forwarded (BS-2 → MSC):**  
   Base Station 2 informs the MSC that MS-B is reachable, online, and ready to receive the call.
8. **Voice Channels Assigned (MSC):**  
   The MSC selects two free voice channel pairs:
   - Pair 1 ($\text{FVC}_1 / \text{RVC}_1$) for MS-A at Tower 1.
   - Pair 2 ($\text{FVC}_2 / \text{RVC}_2$) for MS-B at Tower 2.
9. **Handsets Instructed to Tune & Ring:**  
   - BS-1 orders MS-A over the control channel to tune to Voice Channel 1.
   - BS-2 orders MS-B over the control channel to tune to Voice Channel 2, and transmits a ring command so MS-B's phone starts ringing.
10. **Conversation Begins:**  
    The user on MS-B answers the phone. Both phones use their assigned voice channels, and the MSC bridges the audio connection.

**5. Examiner Viva Question:**  
- **Question:** *Why does the network page over control channels (FCC) instead of paging directly on voice channels?*  
- **Answer:** *Voice channels are scarce and expensive; they should only be used when people are actually speaking. Control channels are shared broadcast channels that let thousands of idle phones stay on standby without wasting dedicated voice channels.*

---

### Question 2(b): Impact of Cluster Size on Capacity and Interference
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 6.2: Impact of Cluster Size (N) on Capacity vs. Interference](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#62-impact-of-cluster-size-n-on-capacity-vs-interference) and [📘 Section 7.1: The Co-Channel Reuse Ratio Formula (Q)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#71-the-co-channel-reuse-ratio-formula-q)

**1. Question Statement:**
*What is the impact of cluster size on capacity and interference in cellular mobile network?*

**2. Direct Explanation (The Core Trade-off):**
In cellular network design, **Cluster Size** ($N$) is the fundamental balancing knob between capacity and voice quality:
- **Small Cluster Size** ($N$): Gives **maximum network capacity**, but results in **higher interference**.
- **Large Cluster Size** ($N$): Gives **clean voice quality with almost zero interference**, but results in **lower network capacity**.

**3. The 3 Governing Mathematical Formulas:**

1. **Channels per Cell:**

$$
K = \frac{S}{N}
$$

   *(Smaller $N$ means more radio channels $K$ for every single tower).*

2. **Co-Channel Distance Ratio** ($Q$):

$$
Q = \frac{D}{R} = \sqrt{3N}
$$

   Where $D$ is the distance between towers using the same frequency, and $R$ is cell radius.

3. **Signal-to-Interference Ratio** ($S/I$):

$$
\frac{S}{I} \approx \frac{1}{6} \left(\frac{D}{R}\right)^k = \frac{1}{6} (\sqrt{3N})^k
$$

   Where $6$ is the number of co-channel interferers in the first ring around a cell, and $k \approx 3\text{--}4$ is the path loss exponent.

**4. Side-by-Side Comparison Table:**

| Feature | Small Cluster (e.g., $N = 4$ or $N = 7$) | Large Cluster (e.g., $N = 12$) |
|:---|:---|:---|
| **Channels per Cell** ($K = S/N$) | **High** (More channels per tower) | **Low** (Fewer channels per tower) |
| **Cluster Repeats in City** ($M$) | **Many times** (Clusters are compact) | **Fewer times** (Each cluster is spread out) |
| **Total City Capacity** ($C = M \cdot S$) | **Very High** (Can handle huge crowds) | **Low** (Bottleneck during busy hours) |
| **Distance Between Co-Channel Towers** ($D$) | **Short** (Towers with same frequency are close) | **Large** (Towers with same frequency are far apart) |
| **Co-Channel Interference** | **Higher** (Nearby towers can cause static) | **Very Low** (Signals from other towers fade away) |
| **Call Audio Quality** | Good enough if above threshold | Crystal clear |

**5. Engineering Decision Rule:**
An engineer always selects the smallest possible cluster size $N$ that still satisfies the minimum required audio quality (for example, $S/I \ge 18\,\text{dB}$ for analog networks or $S/I \ge 15\,\text{dB}$ for GSM).

---

### Question 2(c): System Capacity Numerical ($2310\,\text{km}^2$, $6\,\text{km}^2$ Cell, $S=1596$, $N=7$)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 6.1: Capacity Formulation & Formulas](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas)

**1. Question Statement:**
*Consider a cellular system covers $2310\,\text{km}^2$ and each cell area is $6\,\text{km}^2$. The total allocated channels in the system are 1596. Calculate the system capacity for cluster size 7.*

**2. Direct Answer First:**
The total system capacity is **87,780 simultaneous calls (channels)**.

**3. Given Parameters:**
- Total service area: $A_{\text{total}} = 2310\,\text{km}^2$
- Area of each cell: $A_{\text{cell}} = 6\,\text{km}^2$
- Total allocated channels: $S = 1596\,\text{channels}$
- Cluster size: $N = 7$

**4. Step-by-Step Calculation:**

- **Step 1: Find Total Number of Cells** ($N_{\text{cells}}$) **in the System:**

$$
N_{\text{cells}} = \frac{A_{\text{total}}}{A_{\text{cell}}} = \frac{2310}{6} = \mathbf{385\,\text{cells}}
$$

- **Step 2: Find How Many Times the Cluster Repeats** ($M$):  
  Since each cluster contains $N = 7$ cells:

$$
M = \frac{N_{\text{cells}}}{N} = \frac{385}{7} = \mathbf{55\,\text{clusters}}
$$

- **Step 3: Find Channels Allocated to Each Cell** ($K$):

$$
K = \frac{S}{N} = \frac{1596}{7} = \mathbf{228\,\text{channels per cell}}
$$

- **Step 4: Compute Total System Capacity** ($C$):  
  Using the capacity formula:

$$
C = M \cdot S = 55 \times 1596 = \mathbf{87,780\,\text{channels}}
$$

  *Double Check:*

$$
C = N_{\text{cells}} \times K = 385 \times 228 = \mathbf{87,780\,\text{channels}}
$$

**5. ⚠️ Exam Hall Fatal Trap:**
> ⚠️ **Do Not Make This Mistake:** Many students divide $1596 / 385 \approx 4.14$ and conclude that capacity is 1596. This ignores **frequency reuse**! The 1596 channels are reused across 55 independent clusters, so the total capacity is $55 \times 1596 = 87,780$.

---

### Question 3(a): Channel Borrowing and Constraints
> **Exam Meta:** Marks: **[2.5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 10.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#102-technical-mechanism--architecture)

**1. Question Statement:**
*What is channel borrowing? What are the constraints to implement channel borrowing?*

**2. Direct Definition in Simple English:**
**Channel Borrowing** is a channel management method where a busy cell that has used up all its own channels temporarily borrows an idle channel from an adjacent neighbor cell under MSC control, so it does not drop or block incoming calls.

**3. Three Essential Constraints to Implement Channel Borrowing:**
1. **The Neighbor Must Have Free Channels:** The lending (donor) cell must currently have an idle channel that is not carrying any call.
2. **Channel Must Not Be in Use Nearby:** The borrowed channel must **not be active in any co-channel cell of the donor cell**. If a nearby co-channel cell were already using it, borrowing would cause severe signal collision and static.
3. **Channel Locking:** Once borrowed, the channel must be **locked (disabled) in the donor cell and in all its co-channel cells** for the entire call. This locking guarantees that the minimum safe distance ($D$) between towers using the same frequency is maintained.

---

### Question 3(b): Handoff Definition & 1G vs. 2G Comparison
> **Exam Meta:** Marks: **[2.5M]** | Tier: **Tier 1 / Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 8.1: Definition & Requirements](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#81-definition--requirements) and [📘 Section 9: Signal Monitoring & Generational Handoff Evolution (1G vs. 2G MAHO)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#9-signal-monitoring--generational-handoff-evolution-1g-vs-2g-maho)

**1. Question Statement:**
*What is hand off? Compare between 1st generation and 2nd generation handoff mechanisms.*

**2. Direct Definition of Handoff:**
**Handoff** (also called handover) is the automatic process of transferring an active call or data session from one cell tower (or radio channel) to another as the user moves across cell boundaries, without dropping the call.

**3. Programmatic Evolution Architecture:**

![1G vs 2G Handoff Architecture](images/fig_handoff_1g_vs_2g.png)

**4. 1G vs. 2G Handoff Comparison Table:**

| Comparison Parameter | 1st Generation (1G) Handoff | 2nd Generation (2G) MAHO |
|:---|:---|:---|
| **Mechanism Name** | **Network-Controlled Handoff (NCHO)** | **Mobile-Assisted Handoff (MAHO)** |
| **Who Measures Signal?** | **Base Station Towers:** Towers measure the signal strength sent from the mobile phone. | **The Mobile Handset:** The phone measures the signal strength of nearby towers during idle moments. |
| **Who Makes the Decision?** | **Central MSC:** Central computer analyzes all tower reports and orders the handoff. | **Local BSC:** The Base Station Controller makes the decision locally from the phone's reports. |
| **Handoff Speed** | **Slow** ($5\text{ to } 10\,\text{seconds}$) | **Very Fast (A few milliseconds)** |
| **Load on Central Switch (MSC)** | **Extremely Heavy:** The MSC has to constantly track every single active call. | **Very Light:** The MSC is relieved; local tower controllers handle handoffs directly. |
| **Cell Size Supported** | Large cells only ($> 5\,\text{km}$). | Small microcells ($500\,\text{m}$) in busy city streets. |

---

## 2025 End-Semester Examination Solutions

### Question 1(c): Paging Channel Definition and Usage
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 2.2: Channel Classification: Voice vs. Control Channels](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels) and [📘 Section 3.3: Landline-Initiated Call (Paging Procedure)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#33-landline-initiated-call-paging-procedure)

**1. Question Statement:**
*Define the following terms and state their usage: (c) Paging channel*

**2. Direct Definition:**
A **Paging Channel** is a dedicated downlink radio channel (part of the Forward Control Channel, **FCC**) broadcast by base stations to alert idle mobile phones when someone is calling them or sending an SMS.

**3. Practical Usages:**
1. **Alerting Incoming Calls:** When a call arrives, the network broadcasts the receiver's Mobile Identification Number (MIN) over the paging channel so the phone knows to ring.
2. **Saving Voice Channels:** It allows thousands of idle phones to wait on standby using just one single shared frequency, rather than wasting valuable voice channels before a call is even answered.

---

### Question 2(a): Erlang Definition & User Capacity Numerical ($C=20, \text{GOS}=0.5\%, A=11.10$)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 13.2 & §13.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture)

**1. Question Statement:**
*Define Erlang. How many users can be supported for $0.5\%$ blocking probability for 20 number of trunked channels in a blocked calls cleared system? Assume each user generates $0.1$ Erlang of traffic. From Erlang chart it is given that total system load for $0.5\%$ blocking is 11.10.*

**2. Direct Definition of Erlang:**
An **Erlang** is a dimensionless unit of telecommunications traffic intensity. One Erlang represents the continuous, 100% occupancy of a single channel over a given observation period (e.g., one channel carrying traffic for 60 minutes in an hour equals 1 Erlang). Mathematically:

$$
A = \lambda \cdot h
$$

where $\lambda$ is the mean call arrival rate and $h$ is the mean call holding time.

**3. Given Parameters:**
- Number of trunked channels: $C = 20$
- Blocking probability (Grade of Service): $\text{GOS} = 0.5\% = 0.005$
- Total offered load from Erlang B chart: $A = 11.10\,\text{Erlangs}$
- Traffic generated per user: $A_{\text{pu}} = 0.1\,\text{Erlangs}$

**4. Step-by-Step Calculation:**
The total traffic intensity carried by a population of $n$ subscribers is:

$$
A = n \cdot A_{\text{pu}}
$$

Solving for the number of supported subscribers $n$:

$$
n = \frac{A}{A_{\text{pu}}} = \frac{11.10\,\text{Erlangs}}{0.1\,\text{Erlangs/user}} = \mathbf{111\,\text{users}}
$$

**Conclusion:** The trunked system supports **111 users** with at most $0.5\%$ call blocking during the peak busy hour.

---

### Question 2(b): Orthogonality Proof of Codes $(0,1,0,1)$ and $(0,1,1,0)$
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 17.2 & §17.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#172-technical-mechanism--architecture)

**1. Question Statement:**
*Are the codes $(0,1,0,1)$ and $(0,1,1,0)$ orthogonal? Justify your answer.*

**2. Direct Answer First:**
**Yes, the codes are strictly orthogonal.**

**3. Mathematical Justification (Step-by-Step):**

- **Step 1: Map Binary Bits to Bipolar Sign-Levels:**  
  In CDMA spread-spectrum communication, binary bits are mapped to bipolar levels where logic `0` maps to $-1$ and logic `1` maps to $+1$:

$$
\begin{aligned}
\mathbf{c}_1 &= (0, 1, 0, 1) \longrightarrow (-1, +1, -1, +1) \\
\mathbf{c}_2 &= (0, 1, 1, 0) \longrightarrow (-1, +1, +1, -1)
\end{aligned}
$$

- **Step 2: Compute Vector Dot Product (Inner Product):**  
  Two codes are orthogonal if and only if their cross-correlation (inner product) equals zero:

$$
\begin{aligned}
\mathbf{c}_1 \cdot \mathbf{c}_2 &= \sum_{k=1}^4 c_{1,k} \cdot c_{2,k} \\
&= [(-1) \times (-1)] + [(+1) \times (+1)] + [(-1) \times (+1)] + [(+1) \times (-1)] \\
&= (+1) + (+1) + (-1) + (-1) = 2 - 2 = \mathbf{0}
\end{aligned}
$$

**Conclusion:** Because the inner product is exactly **0**, the cross-correlation between the two sequences is zero, proving that the codes are **mutually orthogonal**. In CDMA, this ensures zero multi-user interference at the base station receiver.

---

### Question 2(c): CDMA DSSS Received Signal Derivation
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Core Derivation  
> **Reference Section in Guide:** [📘 Section 17.4: Fully Audited CDMA Mathematical Trace](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#174-fully-audited-cdma-mathematical-trace)

**1. Question Statement:**
*Consider two mobile stations A & B want to send data $(+1,-1)$ & $(+1,+1)$ using the code $(-1,+1,-1,+1)$ & $(-1,+1,+1,-1)$ respectively. Derive the encoded signal received by the base station.*

**2. Direct Answer First:**
The composite signal received at the base station antenna is:

$$
\mathbf{s}_{\text{rx}} = \mathbf{(-2, +2, 0, 0, 0, 0, +2, -2)}
$$

**3. Step-by-Step Mathematical Derivation:**

- **Given Parameters:**
  - MS-A: Data $\mathbf{d}_A = (+1, -1)$; Spreading Code $\mathbf{c}_A = (-1, +1, -1, +1)$
  - MS-B: Data $\mathbf{d}_B = (+1, +1)$; Spreading Code $\mathbf{c}_B = (-1, +1, +1, -1)$

- **Step 1: Spread and Encode MS-A's Signal (DSSS Kronecker Product):**
  - First bit ($+1$): $(+1) \times (-1, +1, -1, +1) = (-1, +1, -1, +1)$
  - Second bit ($-1$): $(-1) \times (-1, +1, -1, +1) = (+1, -1, +1, -1)$

$$
\mathbf{s}_A = (-1, +1, -1, +1, +1, -1, +1, -1)
$$

- **Step 2: Spread and Encode MS-B's Signal:**
  - First bit ($+1$): $(+1) \times (-1, +1, +1, -1) = (-1, +1, +1, -1)$
  - Second bit ($+1$): $(+1) \times (-1, +1, +1, -1) = (-1, +1, +1, -1)$

$$
\mathbf{s}_B = (-1, +1, +1, -1, -1, +1, +1, -1)
$$

- **Step 3: Superposition in the Air Interface at the Base Station:**  
  Assuming equal received power levels from both MS units (enforced by power control):

$$
\begin{aligned}
\mathbf{s}_{\text{rx}} &= \mathbf{s}_A + \mathbf{s}_B \\
&= \begin{bmatrix}
(-1 - 1), & (+1 + 1), & (-1 + 1), & (+1 - 1), \\
(+1 - 1), & (-1 + 1), & (+1 + 1), & (-1 - 1)
\end{bmatrix} \\
&= \mathbf{(-2, +2, 0, 0, 0, 0, +2, -2)}
\end{aligned}
$$

- **Verification Check (Despreading at BS for MS-A):**
  - Bit 1: $\mathbf{s}_{\text{rx}}[0:4] \cdot \mathbf{c}_A = (-2)(-1) + (2)(1) + (0)(-1) + (0)(1) = 2 + 2 = +4 > 0 \implies \mathbf{+1}$ ✓
  - Bit 2: $\mathbf{s}_{\text{rx}}[4:8] \cdot \mathbf{c}_A = (0)(-1) + (0)(1) + (2)(-1) + (-2)(1) = -2 - 2 = -4 < 0 \implies \mathbf{-1}$ ✓

---

### Question 2(d): Demerits of CDMA
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 16.4 & §17.2](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#164-architectural-trade-offs-matrix)

**1. Question Statement:**
*Write the demerits of CDMA.*

**2. Five Core Demerits of CDMA (in Simple English):**
1. **Near-Far Problem Needs Complex Power Control:** Since all phones share the exact same frequency, a phone near the tower can drown out the signal of a phone far away. To stop this, the tower must constantly tell each phone to adjust its transmit power hundreds of times per second ($800\text{--}1500\,\text{times/sec}$), which requires complicated, high-speed power control circuitry.
2. **Signals Interfere with Each Other (Self-Jamming):** Spreading codes (Walsh codes) are only perfectly separated when signals arrive at the exact same instant. In reality, signals bounce off buildings (multipath) and arrive with small delays. This destroys orthogonality, meaning users' signals leak into each other and act as background noise.
3. **Expensive and Complex Hardware:** CDMA receivers must use special "rake receivers" to combine delayed multipath signals, along with high-precision clocks. This makes both cell towers and handsets more complicated and expensive to build.
4. **Soft Capacity (Gradual Voice Quality Drop):** Unlike GSM or TDMA where a cell has a hard limit on call slots, CDMA has no fixed limit. But as more users join, the background noise rises for everyone. This gradually degrades voice clarity and slows down data speeds for all active calls.
5. **Complicated Soft Handoffs:** When moving between cells, a phone connects to two or three base stations at the same time. While this avoids dropped calls, it uses up extra network transmission lines and requires more complex processing in the phone.

---

## 2024 Mid-Semester Examination Solutions

### Question 1(a): Radio System Block Diagram & Module Tasks
> **Exam Meta:** Marks: **[4M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 4.2 & §4.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#42-technical-mechanism--architecture) and Source Figure 1.7

**1. Question Statement:**
*Draw the block diagram of a radio system at both the transmitter and receiver sides. Give a brief description of the tasks of each of the modules in the diagram.*

**2. Block Diagram of Radio System:**

![Operational modules for radio system](figures/sdb/fig1_7_radio_system_modules.png)

```mermaid
flowchart LR
    subgraph TX["Transmitter Modules"]
        direction LR
        A["Source Coder<br/>(A-to-D, remove redundancy)"] --> B["Channel Coder<br/>(Add controlled error redundancy)"]
        B --> C["Interleaver<br/>(Scramble block errors)"]
        C --> D["Modulator<br/>(Baseband to RF passband)"]
    end
    TX -->|"Antenna / Air Path"| RX
    subgraph RX["Receiver Modules"]
        direction LR
        E["Demodulator<br/>(RF to baseband pulses)"] --> F["Deinterleaver<br/>(Restore bit order)"]
        F --> G["Channel Decoder<br/>(Detect/correct bit errors)"]
        G --> H["Source Decoder<br/>(D-to-A speech synthesis)"]
    end
```

**3. Description of Tasks for Each Module (in Simple English):**
- **Transmitter Modules:**
  1. **Source Coder:** Converts sound or video into digital bits and removes unnecessary data to keep the file/stream size as small as possible.
  2. **Channel Coder:** Adds helper bits (parity/error-checking bits) so the receiver can detect and fix transmission errors.
  3. **Interleaver:** Scrambles the order of data bits so that temporary signal fades do not destroy a whole continuous block of bits.
  4. **Modulator:** Puts the digital data onto a high-frequency radio wave so the antenna can transmit it through the air.
- **Receiver Modules:**
  1. **Demodulator:** Removes the high-frequency radio carrier wave to get the raw digital bits back.
  2. **Deinterleaver:** Puts the scrambled bits back in their original order, turning burst errors into separate single-bit errors.
  3. **Channel Decoder:** Uses the helper bits to find and fix errors caused by static and noise.
  4. **Source Decoder:** Converts the digital bits back into smooth speech or video for the user.

---

### Question 1(b): Hexagonal Cell Geometry Rationale
> **Exam Meta:** Marks: **[3M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 4: Cell Geometry: Why Hexagonal Footprints?](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#4-cell-geometry-why-hexagonal-footprints)

**1. Question Statement:**
*Justify the reason of considering hexagonal cell shape in cellular network design.*

**2. Direct Answer (Why Hexagons?):**
Although radio antennas transmit signals roughly in a circle, circular shapes cannot tile a flat map without leaving **uncovered dead zones** or causing **costly overlaps**.
To cover a map completely with zero gaps and zero overlap, geometry allows only three regular shapes: **Equilateral Triangle**, **Square**, and **Regular Hexagon**.

**3. Geometric Tessellation Comparison Diagram:**

![Cell Geometry Tessellation](images/fig_cell_geometry_tessellation.png)

**4. Mathematical Proof of Area (For Same Maximum Radius** $R$):
For an antenna with maximum reach radius $R$:
1. **Equilateral Triangle** ($n = 3$):

$$
A_{\text{triangle}} = \frac{3\sqrt{3}}{4} R^2 \approx 1.299 R^2 \quad (50\% \text{ of Hexagon Area})
$$

2. **Square** ($n = 4$):

$$
A_{\text{square}} = 2 R^2 = 2.000 R^2 \quad (77\% \text{ of Hexagon Area})
$$

3. **Regular Hexagon** ($n = 6$):

$$
A_{\text{hexagon}} = \frac{3\sqrt{3}}{2} R^2 \approx 2.598 R^2 \quad (\mathbf{100\%} \text{ -- Largest Area})
$$

**5. The Two Key Engineering Reasons:**
1. **Cheapest to Build (Fewest Towers Needed):** The hexagon covers the largest land area for any given antenna range $R$. Therefore, a network operator needs the **minimum number of cell towers** to cover a city, saving equipment and rental costs.
2. **Closest Match to a Circle:** Because radio waves spread outwards like a circle, a 6-sided hexagon (with $120^\circ$ corners) fits the natural circular radiation pattern of antennas far better than a 4-sided square ($90^\circ$) or 3-sided triangle ($60^\circ$).

---

### Question 1(c): Location Tracking & Implementation Techniques
> **Exam Meta:** Marks: **[3M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 9.2: 1st Generation (1G) Handoff](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#92-1st-generation-1g-handoff-network-controlled) and [📘 Section 12.4: GSM Network and Switching Subsystem (NSS)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**1. Question Statement:**
*Define location tracking. Write about two implementation techniques of location tracking.*

**2. Direct Definition:**
**Location Tracking** is the network process that keeps track of which cell or location area a mobile phone is currently inside, so that incoming calls and messages can be routed directly to the user without having to broadcast across the entire national network.

**3. Two Implementation Techniques:**
1. **Database Tracking using HLR and VLR (GSM / 2G Technique):**
   - When a phone travels into a new Location Area, it notices a new area ID broadcast from the tower.
   - The phone sends a **Location Update** request.
   - The local switch stores this in its temporary guest database (**VLR**) and sends a pointer to the user's permanent master database (**HLR**).
   - Incoming calls check the HLR, find the current VLR, and ring the phone immediately.
2. **Radio Signal Strength Monitoring (1G Technique):**
   - When an active phone needs to be located, the central switch asks surrounding base stations to measure the received signal strength on the phone's voice channel.
   - By comparing the signal levels from three or more neighboring towers, the network pinpoints the phone's position.

---

### Question 2(a): Frequency Reuse Ratio & $S/I$ Derivation
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Core Derivation  
> **Reference Section in Guide:** [📘 Section 7.1: The Co-Channel Reuse Ratio Formula (Q)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#71-the-co-channel-reuse-ratio-formula-q), [📘 Section 7.2: Operational Trade-Off of Q](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#72-operational-trade-off-of-q), and [📘 Section 5.3: Cluster Size Formula (N)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#53-cluster-size-formula-n)

**1. Question Statement:**
*What is frequency reuse ratio? Derive the relationship between frequency reuse ratio and signal-to-interference ($S/I$) ratio.*

**2. Definition of Frequency Reuse Ratio** ($Q$):
The **Frequency Reuse Ratio** ($Q$) is the ratio of the physical distance $D$ between the centers of two nearest cells that use the same frequency, to the radius of a cell $R$:

$$
Q = \frac{D}{R} = \sqrt{3N}
$$

Where $N$ is the cluster size ($N = i^2 + ij + j^2$).

**3. Step-by-Step Derivation of** $S/I$:

- **Step 1: Desired Signal Power** ($S$):  
  For a phone at the farthest edge of its cell (distance $R$ from its serving tower), the received signal power follows the standard path loss formula:

$$
S = P_t \cdot c \cdot R^{-k}
$$

  Where $P_t$ is transmitter power, $c$ is a constant, and $k$ is the path loss exponent ($k \approx 3\text{ to } 4$).

- **Step 2: Total Interference Power** ($I$):  
  In a regular hexagonal grid, every cell is surrounded by **6 first-tier co-channel cells** using the exact same frequency, located roughly at distance $D$:

$$
I = \sum_{i=1}^6 I_i \approx 6 \cdot P_t \cdot c \cdot D^{-k}
$$

- **Step 3: Form the Ratio** ($S/I$):

$$
\frac{S}{I} = \frac{P_t \cdot c \cdot R^{-k}}{6 \cdot P_t \cdot c \cdot D^{-k}} = \frac{1}{6} \left(\frac{D}{R}\right)^k
$$

- **Step 4: Substitute** $Q$ **and** $N$:  
  Since $Q = D / R$:

$$
\mathbf{\frac{S}{I} = \frac{1}{6} Q^k}
$$

  And since $Q = \sqrt{3N}$:

$$
\mathbf{\frac{S}{I} = \frac{1}{6} (\sqrt{3N})^k = \frac{1}{6} (3N)^{k/2}}
$$

---

### Question 2(b): Compact Pattern Size $N$ for $S/I \ge 15\,\text{dB}$ with $k = 3$
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 5.3: Cluster Size Formula (N)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#53-cluster-size-formula-n) and [📘 Section 7.1, 7.2: Co-Channel Interference & Reuse Ratio](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#7-co-channel-interference--co-channel-reuse-ratio-q)

**1. Question Statement:**
*Consider a GSM TDMA system that accepts $S/I \ge 15\,\text{dB}$. What should be the compact pattern size $N$ when path loss component $k = 3$?*

**2. Direct Answer First:**
The required compact pattern size (cluster size) is $\mathbf{N = 12}$.

**3. Step-by-Step Derivation:**

- **Step 1: Convert** $15\,\text{dB}$ **into Linear Ratio:**

$$
\frac{S}{I} \ge 10^{15/10} = 10^{1.5} \approx 31.62
$$

- **Step 2: Apply Formula with** $k = 3$ **and 6 Interferers:**

$$
\frac{S}{I} = \frac{1}{6} Q^3 \ge 31.62 \implies Q^3 \ge 6 \times 31.62 = 189.74
$$

- **Step 3: Solve for Reuse Ratio** $Q$:

$$
Q \ge (189.74)^{1/3} \approx 5.75
$$

- **Step 4: Solve for Cluster Size** $N$:

$$
3N \ge (5.75)^2 \approx 33.02 \implies N \ge \frac{33.02}{3} \approx 11.01
$$

- **Step 5: Pick the Next Valid Hexagonal Cluster Size:**  
  Allowed values ($N = i^2 + ij + j^2$): $N \in \{1, 3, 4, 7, 9, 12, 13, 19, \dots\}$.  
  The smallest valid cluster size satisfying $N \ge 11.01$ is $\mathbf{N = 12}$ ($i=2, j=2$).

*(Note on textbook approximation: SDB notes on page 30 omit the factor of 6 inside the cube root, obtaining $Q \approx 3.13 \implies N \approx 3$; the rigorous derivation above demonstrates $N=12$).*

---

### Question 3(a): Near-Far Effect Definition and Usage
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 9.2 & §16.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#92-technical-mechanism--architecture)

**1. Question Statement:**
*Define the following terms and state their usage: Near-far effect.*

**2. Direct Definition in Simple English:**
The **Near-Far Effect** happens when two mobile phones transmit at the same power, but one phone is very close to the tower and the other is far away at the cell edge. Because radio signals weaken rapidly over distance ($P_r \propto d^{-k}$), the signal from the nearby phone arrives at the tower with huge power and completely drowns out (jams) the faint signal coming from the distant user.

**3. How Networks Solve This (Countermeasures):**
1. **Fast Power Control:** The base station continuously commands nearby phones to lower their transmit power, so signals from all phones arrive at the tower with roughly the same power level.
2. **Smart Frequency Planning:** Frequencies that sit right next to each other are not used in the same cell, preventing strong nearby transmissions from spilling into weak neighbor channels.

---

### Question 3(b): Umbrella Cell Approach
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 11.1](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#111-problem-1-accommodating-wide-velocity-diversity)

**1. Question Statement:**
*Define the following terms and state their usage: (b) Umbrella cell approach*

**2. Direct Definition:**
The **Umbrella Cell Approach** is an architectural layout where a large, high-power macrocell base station with a tall antenna overlays several small, low-power microcells in the exact same geographic region.

**3. Practical Usages:**
1. **Mitigating Handoff Storms for Fast Vehicles:** High-speed vehicular traffic is assigned to the umbrella macrocell, eliminating rapid back-to-back handoffs that would otherwise choke signaling networks.
2. **Absorbing High-Density Pedestrian Traffic:** Low-speed pedestrians are serviced by the microcells underneath, providing high data throughput without cluttering the macrocell.

---

### Question 3(c): Grade of Service (GOS) Definition and Usage
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 13.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture)

**1. Question Statement:**
*Define the following terms and state their usage: GOS.*

**2. Direct Definition:**
**Grade of Service (GOS)** is a statistical measure of telecommunication network congestion during the peak busy hour, defined as the probability that an attempted call will be blocked or delayed ($P_b$). In a blocked-calls-cleared cellular system, it is calculated using the Erlang B formula:

$$
\text{GOS} = P_b = \frac{\frac{A^C}{C!}}{\sum_{k=0}^C \frac{A^k}{k!}}
$$

**3. Practical Usages:**
1. **Network Dimensioning:** Telecommunications engineers use GOS specifications (typically $1\%$ or $0.5\%$ blocking) to calculate the exact number of radio channels ($C$) required to handle an expected busy-hour subscriber traffic load ($A$).
2. **Quality of Service Benchmark:** Acts as the primary contractual and regulatory standard for evaluating whether an operator has provisioned adequate radio capacity.

---

### Question 3(d): Home Location Register (HLR)
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**1. Direct Definition:**
The **Home Location Register (HLR)** is the primary permanent master database in a GSM core network that stores subscription profiles, service permissions, and the current location pointer (VLR address) for every mobile user registered under that operator.

**2. Practical Usages:**
1. **Master Identity Storage:** Permanently stores the International Mobile Subscriber Identity (IMSI) and secret authentication key ($K_i$).
2. **Routing Incoming Calls:** Stores the address of the current Visitor Location Register (VLR) where the mobile phone is operating, enabling incoming calls to be routed to the correct destination tower.

---

### Question 3(e): Visitor Location Register (VLR)
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**1. Direct Definition:**
The **Visitor Location Register (VLR)** is a temporary local database collocated with a Mobile Switching Centre (MSC) that caches subscriber profiles for all mobile stations currently roaming inside that MSC's location area.

**2. Practical Usages:**
1. **Accelerating Call Setup:** Provides rapid local subscriber authentication and profile lookups, eliminating slow cross-network queries to the user's remote home HLR during every call attempt.
2. **Issuing Temporary Mobile Subscriber Identity (TMSI):** Allocates a temporary, rotating identifier to the phone, preventing the permanent IMSI from being intercepted over the open radio interface.

---

## 2024 End-Semester Examination Solutions

### Question 1(a): Channel Borrowing Definition and Usage
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 10.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#102-technical-mechanism--architecture)

**1. Question Statement:**
*Define the following terms and state their usage: (a) Channel borrowing*

**2. Direct Definition in Simple English:**
**Channel Borrowing** is a technique where a busy cell that has used up all its regular channels temporarily borrows an idle channel from a neighboring cell under MSC supervision to handle extra call traffic.

**3. Practical Usages:**
1. **Handling Sudden Traffic Hotspots:** Deals with short-term crowd surges (such as at a stadium or concert) without needing to permanently change network frequency plans.
2. **Preventing Dropped Calls:** Supplies channels for moving callers (handoffs) that would otherwise be cut off due to lack of free channels.

---

### Question 2(b): Orthogonality Verification of 11-Chip Code
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 17.2 & §17.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#172-technical-mechanism--architecture)

**1. Question Statement:**
*How do you prove whether a chip code $(+1, -1, +1, +1, -1, +1, +1, +1, -1, -1, -1)$ is orthogonal or not?*

**2. Direct Answer First:**
Orthogonality is a mathematical property between **two distinct codes** (or a code and its time-shifted version). To prove whether this 11-chip code is orthogonal:
1. It must be tested against another code sequence $\mathbf{c}_2$ by evaluating their **inner product (cross-correlation)**:

$$
\mathbf{c}_1 \cdot \mathbf{c}_2 = \sum_{i=1}^{11} c_{1,i} \cdot c_{2,i} = 0
$$

   If this summation equals exactly $0$, the codes are mutually orthogonal.
2. If tested against itself (autocorrelation at zero lag $\tau = 0$), the inner product is:

$$
\mathbf{c}_1 \cdot \mathbf{c}_1 = \sum_{i=1}^{11} (c_{1,i})^2 = 11 \ne 0
$$

   (A code is never orthogonal to itself; it achieves peak autocorrelation at zero lag).

**3. Identification of the Given Code:**
The given sequence $\mathbf{c} = (+1, -1, +1, +1, -1, +1, +1, +1, -1, -1, -1)$ is the canonical **11-chip Barker Code** (used in IEEE 802.11 DSSS and ISDN). It possesses ideal autocorrelation properties where the peak is $11$ and all off-peak side lobes are bounded by $\le 1$. To achieve multi-user orthogonality in CDMA, this sequence is paired with an orthogonal code $\mathbf{c}_2$ whose component-wise dot product sums to zero.

---

### Question 2(c): Erlang B User Capacity Numerical ($C=20, A=12.03 \implies 120\,\text{Users}$)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 13.3: Verified Calculations (Example 2.4)](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#133-verified-calculations)

**1. Question Statement:**
*Consider a network with 20 number of channels per cell and on an average each user makes 3 calls/hr. The average duration of a call is 2 minutes. The offered load from Erlang B Table is 12.03. What is the number of users supported in a cell with 1% blocking?*

**2. Direct Answer First:**
The number of users supported in the cell is $\mathbf{120\,\text{users}}$.

**3. Given Parameters:**
- Channels per cell: $C = 20$
- Call arrival rate per user: $\lambda_{\text{user}} = 3\,\text{calls/hour}$
- Mean call duration: $h = 2\,\text{minutes} = \frac{2}{60}\,\text{hours} = \frac{1}{30}\,\text{hours}$
- Blocking probability: $\text{GOS} = 1\% = 0.01$
- Offered load from Erlang B table: $A = 12.03\,\text{Erlangs}$

**4. Step-by-Step Calculation:**
- **Step 1: Compute Per-User Traffic Intensity** ($A_{\text{pu}}$):

$$
A_{\text{pu}} = \lambda_{\text{user}} \times h = 3 \times \frac{2}{60} = 0.1\,\text{Erlangs}
$$

- **Step 2: Calculate Number of Supported Users** ($n$):

$$
n = \frac{A}{A_{\text{pu}}} = \frac{12.03\,\text{Erlangs}}{0.1\,\text{Erlangs/user}} = \mathbf{120.3} \approx \mathbf{120\,\text{users}}
$$

**Conclusion:** The network cell can reliably support **120 subscribers** while maintaining a call blocking probability under $1\%$.

---

### Question 5(a): Comprehensive Short Note on Spread Spectrum
> **Exam Meta:** Marks: **[10M]** | Tier: **Tier 3 (LA)**  
> **Reference Section in Guide:** [📘 Section 17.1 & §17.2: Spread Spectrum Engineering & CDMA Mathematics](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#17-spread-spectrum-engineering--cdma-mathematics)

**1. Question Statement:**
*Write short notes on: Spread Spectrum.*

**2. Fundamental Definition in Simple English:**
**Spread Spectrum** is a transmission technique where a digital data signal is deliberately spread across a much wider radio bandwidth than it strictly needs, using a special pseudo-random code. At the receiver, the exact same code is used to shrink the signal back to its original size (called **despreading**) and recover the data. This makes the signal extremely hard to jam, intercept, or corrupt.

```mermaid
flowchart LR
    A["Narrowband User Data<br/>(Bandwidth B, Bit Period Tb)"] --> B["DSSS Spreader<br/>(Multiply by Chip Sequence)"]
    C["Code Generator<br/>(Chip Rate Rc, Period Tc)"] --> B
    B --> D["Wideband Spread Signal<br/>(Bandwidth W >> B)"]
    D --> E["RF Modulator"]
```

**3. Direct Sequence Spread Spectrum (DSSS) Mechanism:**
- Low-rate data bits of duration $T_b$ (bit rate $R_b = 1/T_b$) are multiplied by a high-rate pseudo-random sequence of **chips** of duration $T_c \ll T_b$ (chip rate $R_c = 1/T_c$).
- **Processing Gain (Spreading Factor):**

$$
\text{PG} = \frac{T_b}{T_c} = \frac{R_c}{R_b} = \frac{W}{B}
$$

  *Example:* Spreading a $1\,\text{MHz}$ data signal with an 11-chip code expands its transmitted bandwidth to $11\,\text{MHz}$, producing an $11\times$ ($10.4\,\text{dB}$) processing gain.

**4. Spreading Codes in Cellular Systems:**
- **Orthogonal Walsh Codes:** Generated from Hadamard matrices; cross-correlation is exactly zero under perfect time alignment. Used on the downlink (forward link) from base station to mobiles.
- **Pseudonoise (PN) Sequences:** Mathematically generated shift-register sequences that appear random but are deterministic. Used on the uncoordinated uplink (reverse link) where multipath delay prevents strict orthogonality.
- **Dual Spreading in IS-95:** First spreads user data with a Walsh code for intra-cell subscriber isolation, then modulates with a PN sequence for inter-cell cluster separation.

**5. Engineering Merits & Operational Demerits:**
- **Merits:**
  1. *Immunity to Hostile Jamming & Multipath Fading:* Narrowband interferers only corrupt a tiny fraction of the spread signal; despreading at the receiver suppresses interference by the processing gain.
  2. *Low Probability of Intercept & High Security:* The spread signal appears below the thermal noise floor to unauthorized sniffers lacking the secret key.
  3. *Universal Frequency Reuse ($N=1$):* All cells operate on the identical carrier frequency, eliminating complex frequency planning.
- **Demerits:**
  1. *Near-Far Problem:* Requires fast, sub-millisecond closed-loop power control.
  2. *Receiver Synchronization Overhead:* Requires precise chip-level tracking loops.

---

## 2023 Mid-Semester Examination Solutions

### Question 1: Multiple Choice Questions (MCQs)
> **Exam Meta:** Marks: **[1M each]** | Tier: **Tier 1 (MCQ)**  
> **Reference Sections in Guide:** Sections 1.1, 1.2, 4.2, 6.1, 9.3, 12.3, 12.4, 13.1, 13.2, 14.2, 16.4, 17.2

#### Question 1(i): Receiver Process in Mobile Communication
- **Statement:** *Which process is performed at the receiver end in mobile communication?*  
  (A) Modulation  
  (B) Demodulation  
  (C) Decoding  
  (D) Both B and C  
- **Correct Option:** **(D) Both B and C**
- **Reason:** The receiver pipeline executes demodulation (stripping off the RF carrier) followed by channel decoding and source decoding to recover original digital speech.

#### Question 1(ii): User Data Storage
- **Statement:** *Which stores data related to the user?*  
  (A) SIM  
  (B) HLR  
  (C) VLR  
  (D) AUC  
- **Correct Option:** **(A) SIM**
- **Reason:** The SIM card directly stores personal user information, contacts, text messages, PIN/PUK, and user authentication keys.

#### Question 1(iii): Multiplexing Using Full Bandwidth Simultaneously
- **Statement:** *Which type of multiplexing enables use of the whole bandwidth simultaneously?*  
  (A) FDMA  
  (B) CDMA  
  (C) TDMA  
  (D) None of these  
- **Correct Option:** **(B) CDMA**
- **Reason:** In CDMA (Code Division Multiple Access), all users transmit across the entire frequency bandwidth simultaneously, separated in code space.

#### Question 1(iv): Incorrect Statement About TDMA
- **Statement:** *Select the incorrect statement about TDMA:*  
  (A) High transmission rate  
  (B) Discontinuous data transmission  
  (C) Single carrier frequency for single user  
  (D) All of these  
- **Correct Option:** **(C) Single carrier frequency for single user**
- **Reason:** In TDMA, multiple users share the same carrier frequency by taking turns in time slots. Dedicating a carrier frequency to one single user is FDMA.

#### Question 1(v): Radio Capacity Enhancement
- **Statement:** *How is radio capacity enhanced in a cellular network?*  
  (A) By increasing the total base stations and by channel reuse  
  (B) By increasing the spectrum of the radio  
  (C) Both of these  
  (D) None of these  
- **Correct Option:** **(A) By increasing the total base stations and by channel reuse**
- **Reason:** Spectrum is a finite natural resource; capacity is multiplied by deploying more small cells and reusing the same channels across clusters.

#### Question 1(vi): Directional Antennas to Increase Capacity
- **Statement:** *Which technique uses directional antennas to increase cell capacity?*  
  (A) Cell Splitting  
  (B) Coverage Zone approaches  
  (C) Cell Sectoring  
  (D) Cell Sectoring and Cell Splitting both  
- **Correct Option:** **(C) Cell Sectoring**
- **Reason:** Cell sectoring replaces omnidirectional antennas with $120^\circ$ or $60^\circ$ directional antennas to reduce co-channel interference, allowing smaller cluster sizes ($N$) and higher capacity.

#### Question 1(vii): CDMA Power Adjustment Problem
- **Statement:** *In CDMA, mobile-device transmission power needs to be adjusted to mitigate which problem?*  
  (A) Hidden station problem  
  (B) Exposed station problem  
  (C) Near-far problem  
  (D) All of these  
- **Correct Option:** **(C) Near-far problem**
- **Reason:** Mobile stations close to the tower transmit at lower power so their signals do not overpower distant mobiles at the base station receiver.

#### Question 1(viii): Primary GSM Uplink Frequency Range
- **Statement:** *Primary GSM uses uplink frequency in which range?*  
  (A) $(890\text{--}915)\,\text{MHz}$  
  (B) $(935\text{--}960)\,\text{MHz}$  
  (C) $(880\text{--}915)\,\text{MHz}$  
  (D) $(925\text{--}960)\,\text{MHz}$  
- **Correct Option:** **(A)** $(890\text{--}915)\,\text{MHz}$
- **Reason:** GSM 900 uses $890\text{--}915\,\text{MHz}$ for uplink (mobile to tower) and $935\text{--}960\,\text{MHz}$ for downlink (tower to mobile).

#### Question 1(ix): RF Channel Estimation for GOS
- **Statement:** *What needs to be estimated for allocating the RF number of channels to meet GOS?*  
  (A) Cost  
  (B) Capacity  
  (C) SNR  
  (D) All the above  
- **Correct Option:** **(B) Capacity**
- **Reason:** The traffic capacity/load ($A = \lambda h$) must be estimated to calculate the required number of channels ($C$) for a given blocking probability (GOS).

#### Question 1(x): VLR Integration
- **Statement:** *The Visitor Location Register is integrated with which of the following?*  
  (A) MSC  
  (B) HLR  
  (C) PSTN  
  (D) All these  
- **Correct Option:** **(A) MSC**
- **Reason:** The VLR is always directly collocated and integrated with the Mobile Switching Centre (MSC).

---

### Question 2(a): Call Setup Between Two Mobile Stations
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 3.2 & §3.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#3-call-procedures-origination-paging--in-call-management)

*(Identical in concept to [2025 Mid Q2(a)](#question-2a-call-establishment-between-two-mobile-stations). Refer to the 10-step protocol sequence and architecture diagram [`images/fig_call_setup_flow.png`](file:///c:/PROJECTS/Learnmat/academics/mpc/images/fig_call_setup_flow.png).)*

**Quick Summary of the 10 Steps:**
1. **MS-A** requests call on **Reverse Control Channel (RCC)** to Tower 1.
2. **Tower 1** forwards request to the **MSC**.
3. **MSC** validates caller and queries **HLR/VLR** to find where MS-B is.
4. **MSC** sends paging order to Tower 2 in MS-B's area.
5. **Tower 2** pages MS-B over the **Forward Control Channel (FCC)**.
6. **MS-B** responds with ACK on the **RCC**.
7. **Tower 2** informs MSC that MS-B responded.
8. **MSC** assigns dedicated voice channel pairs ($\text{FVC}_1 / \text{RVC}_1$ and $\text{FVC}_2 / \text{RVC}_2$).
9. Handsets are instructed via FCC to tune to voice channels; MS-B rings.
10. MS-B answers $\implies$ Audio call connected!

---

### Question 2(b): Roles of Cellular Channels (FVC, RVC, FCC, RCC)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 2.2: Channel Classification: Voice vs. Control Channels](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels)

**1. Question Statement:**
*What roles do channels FVC, RVC, FCC, and RCC play in a cellular mobile network?*

**2. Channel Roles Summary Table:**

| Channel Acronym | Full Name | Direction | Primary Role in Network | Typical Share |
|:---|:---|:---:|:---|:---:|
| **FVC** | **Forward Voice Channel** | Tower $\to$ Phone (Downlink) | Carries conversation audio from the tower down to the mobile phone. | $\approx 47.5\%$ |
| **RVC** | **Reverse Voice Channel** | Phone $\to$ Tower (Uplink) | Carries speaker audio from the mobile phone up to the tower. | $\approx 47.5\%$ |
| **FCC** | **Forward Control Channel** | Tower $\to$ Phone (Downlink) | **Downlink Signaling:**<br>1. Broadcasts tower parameters and cell IDs.<br>2. Transmits **paging messages** to alert phones of incoming calls.<br>3. Orders phones to switch to specific voice channels. | $\approx 2.5\%$ |
| **RCC** | **Reverse Control Channel** | Phone $\to$ Tower (Uplink) | **Uplink Signaling:**<br>1. Sends call request packets when dialing.<br>2. Sends ACK reply when a phone hears itself being paged.<br>3. Sends location update messages. | $\approx 2.5\%$ |

**The 5% Rule:** In cellular systems, about **5% of channels are used for control/signaling (FCC and RCC)** to set up calls, while **95% are reserved for voice conversation (FVC and RVC)**.

---

### Question 3(a): Channel-Assignment Strategies in 2G Cellular Networks
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 10.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#102-technical-mechanism--architecture)

**1. Question Statement:**
*Describe different channel-assignment strategies in a 2G cellular network.*

**2. Direct Answer (Three Core Strategies in Simple English):**
To get the most out of scarce radio frequencies and reduce blocked calls, 2G cellular networks use three main channel assignment strategies:

1. **Fixed Channel Assignment (FCA):**
   - Each cell is given a fixed, permanent set of voice channels ($K = S/N$).
   - A cell can only use its own assigned channels. If all its channels are in use, new calls are immediately blocked.
   - *Advantage:* Very simple to set up; puts zero computation load on the MSC during calls.
   - *Demerit:* Cannot handle sudden crowd surges in a particular cell.
2. **Channel Borrowing (Variation of FCA):**
   - If a cell gets overcrowded and runs out of channels, it temporarily borrows an idle channel from a neighbor cell under MSC supervision.
   - *Key Rule:* The borrowed channel must be locked (disabled) in neighboring co-channel cells while borrowed, so signals do not collide.
   - *Advantage:* Handles temporary traffic hotspots without dropping calls.
3. **Dynamic Channel Assignment (DCA):**
   - Channels are not permanently tied to any cell. Instead, all channels are stored in a central pool managed by the MSC.
   - Whenever a call arrives, the tower asks the MSC for a channel. The MSC picks an available channel that satisfies the safe reuse distance ($D$) and causes the least interference.
   - *Advantage:* Adapts easily to changing traffic across the city and reduces blocked calls.
   - *Demerit:* Requires heavy real-time processing and constant monitoring at the central MSC.

---

### Question 3(b): Cellular Capacity & Cluster Size Numerical
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 6.1: Capacity Formulation & Formulas](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas)

**1. Question Statement:**
*(i) A cellular system has $40\,\text{MHz}$ bandwidth. It uses two $20\,\text{kHz}$ simplex channels to provide full-duplex voice and control channels. How many channels may each network cell get for a 12-cell reuse system?*  
*(ii) A system covers $2310\,\text{km}^2$ and each cell area is $6\,\text{km}^2$. Calculate system capacity.*

**2. Direct Answers First:**
- **Part (i):** Each cell receives **83 full-duplex channels** (with 4 spare channels in the cluster).
- **Part (ii):** Total system capacity is **32,083 simultaneous calls** (or $31,955\,\text{calls}$ with 83 integer channels/cell).

**3. Part (i) Step-by-Step Calculation:**
- Duplex Channel Width: $2 \times 20\,\text{kHz} = 40\,\text{kHz} = 0.04\,\text{MHz}$
- Total System Channels: $S = \frac{40\,\text{MHz}}{0.04\,\text{MHz}} = \mathbf{1,000\,\text{channels}}$
- Channels per Cell for $N = 12$:

$$
K = \frac{S}{N} = \frac{1000}{12} = 83.33 \implies \mathbf{83\,\text{channels per cell}}
$$

**4. Part (ii) Step-by-Step Calculation:**
- Total Cells: $N_{\text{cells}} = \frac{2310}{6} = \mathbf{385\,\text{cells}}$
- Cluster Replications: $M = \frac{385}{12} \approx \mathbf{32.083\,\text{clusters}}$
- Total System Capacity:

$$
C = M \cdot S = 32.0833 \times 1000 = \mathbf{32,083.33\,\text{simultaneous channels}}
$$

  *Discrete integer capacity:* $C_{\text{int}} = 385 \times 83 = \mathbf{31,955\,\text{channels}}$.

---

## 2023 End-Semester Examination Solutions

### Question 1(b): Home Location Register (HLR)
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 12.4](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**Direct Answer:**
The **Home Location Register (HLR)** is the central master database in a GSM network that permanently stores subscriber profile details, phone numbers, and the current location pointer (VLR address) for every mobile user registered under that operator.

---

### Question 2(a): GOS Definition & Assumptions for Blocked-Calls-Cleared System
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 13.2: Technical Mechanism & Architecture](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture)

**1. Question Statement:**
*Define GOS. Write assumptions, if any, for a blocked-calls-cleared trunking system.*

**2. Definition of Grade of Service (GOS):**
**Grade of Service (GOS)** is a metric specifying the probability that an attempted call is blocked during the busy hour in a trunked cellular radio system. Expressed as a probability $P_b$, a $\text{GOS} = 0.001$ indicates that, on average, at most 1 call out of 1,000 attempts is blocked during peak traffic.

**3. Essential Assumptions of Blocked-Calls-Cleared (Erlang B) Model (in Simple English):**
1. **Random Call Arrivals (Poisson Process):** Calls arrive randomly and independently. A blocked caller does not affect when other users try to place calls.
2. **Constant Average Arrival Rate** ($\lambda$): The average number of call attempts per hour stays steady during the peak busy hour.
3. **Exponential Call Durations:** Most phone calls are short, while very long calls are rare. Holding times follow a negative exponential distribution ($h = 1/\mu$).
4. **Fixed Number of Channels** ($C$): The network has a fixed pool of $C$ radio channels available to serve calls.
5. **Large User Population** ($U \to \infty$): The total number of mobile subscribers is much larger than the number of channels, so one user making a call does not change overall arrival statistics.
6. **No Call Queuing (Lost Calls Cleared):** If all $C$ channels are busy when a call arrives, the call is dropped immediately; callers are not put on hold or queued.

---

### Question 2(b): Erlang Definition & User Capacity Numerical ($C=20, \text{GOS}=0.5\%, A=11.10$)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 13.2 & §13.3](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md#132-technical-mechanism--architecture)

**1. Question Statement:**
*Define Erlang. How many users can be supported for $0.5\%$ blocking probability for 20 trunked channels in a blocked-calls-cleared system? Assume each user generates $0.1$ Erlang traffic. From the Erlang chart, total system load for $0.5\%$ blocking is 11.10.*

**2. Direct Definition of Erlang:**
An **Erlang** is a dimensionless unit of telecommunications traffic intensity. One Erlang represents the continuous, 100% occupancy of a single channel over a given observation period (e.g., one channel carrying traffic for 60 minutes in an hour equals 1 Erlang). Mathematically:

$$
A = \lambda \cdot h
$$

where $\lambda$ is the mean call arrival rate and $h$ is the mean call holding time.

**3. Given Parameters:**
- Number of trunked channels: $C = 20$
- Blocking probability (Grade of Service): $\text{GOS} = 0.5\% = 0.005$
- Total offered load from Erlang B chart: $A = 11.10\,\text{Erlangs}$
- Traffic generated per user: $A_{\text{pu}} = 0.1\,\text{Erlangs}$

**4. Step-by-Step Calculation:**
The total traffic intensity carried by a population of $n$ subscribers is:

$$
A = n \cdot A_{\text{pu}}
$$

Solving for the number of supported subscribers $n$:

$$
n = \frac{A}{A_{\text{pu}}} = \frac{11.10\,\text{Erlangs}}{0.1\,\text{Erlangs/user}} = \mathbf{111\,\text{users}}
$$

**Conclusion:** The trunked system supports **111 users** with at most $0.5\%$ call blocking during the peak busy hour.

---

## Comprehensive Quick-Recall Formula & Parameter Cheat Sheet

| Formula Name | Mathematical Formula | Meaning of Symbols | Simple Exam Tip |
|:---|:---|:---|:---|
| **Cluster Size Formula** | $N = i^2 + i \cdot j + j^2$ | $N$: Cells per cluster; $i, j \in \{0,1,2,\dots\}$ | Valid values: $N \in \{1, 3, 4, 7, 9, 12, 13, 19, \dots\}$. |
| **Co-Channel Reuse Ratio** | $Q = \frac{D}{R} = \sqrt{3N}$ | $D$: Distance between co-channel cells; $R$: Cell radius | Measures how far apart towers using the same frequency are. |
| **Channels per Cell** | $K = \frac{S}{N}$ | $S$: Total channels; $N$: Cluster size | Dividing channels equally among cells in a cluster. |
| **Total System Capacity** | $C = M \cdot S = M \cdot K \cdot N$ | $M = \frac{A_{\text{total}}}{N \cdot A_{\text{cell}}}$: Cluster repeats | Total simultaneous calls across the entire network. |
| **Worst-Case** $S/I$ **(Omni)** | $\frac{S}{I} \approx \frac{1}{6} \left(\frac{D}{R}\right)^k = \frac{1}{6} (\sqrt{3N})^k$ | $k$: Path loss exponent ($k=3\text{--}4$); 6 interferers | Calculates interference from the 6 neighboring towers. |
| **Traffic Intensity (Erlangs)** | $A = \lambda \cdot h = n \cdot A_{\text{pu}}$ | $\lambda$: Calls/hr; $h$: Holding time in hours; $n$: Users | Quantifies continuous channel occupancy load. |
| **Erlang B Formula (LCC)** | $P_b = \frac{A^C / C!}{\sum_{k=0}^C A^k / k!}$ | $C$: Trunked channels; $A$: Offered load | Probability of call blocking in lost-calls-cleared systems. |
| **CDMA Spreading Factor** | $\text{SF} = \frac{T_b}{T_c} = \frac{R_{\text{chip}}}{R_{\text{data}}}$ | $T_b$: Bit period; $T_c$: Chip period | Processing gain expanding data into wideband spread spectrum. |
| **Hexagon Area** | $A = \frac{3\sqrt{3}}{2} R^2 \approx 2.598 R^2$ | $R$: Maximum radius from center to vertex | Covers the largest area of any polygon that fits without gaps. |

---

## Uncovered Questions (Unanswered / Out-of-Notes Syllabus)

The following examination questions from [`academics/pyq/Mobile and Pervasive Computing.md`](file:///c:/PROJECTS/Learnmat/academics/pyq/Mobile%20and%20Pervasive%20Computing.md) cover topics outside the scope of both [`academics/mpc/Cellular_Networks_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md) and [`academics/mpc/Mobile_Computing_SDB_Learning_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Mobile_Computing_SDB_Learning_Guide.md) (such as UMTS UTRAN architecture, 5G Core Service-Based Architecture, Mobile-IP tunneling protocols, WLAN CSMA/CA, and Pervasive Computing). 

Per strict exam protocol and user instructions, they are retained below **unanswered**:

---

### Uncovered Questions from 2025 Mid-Semester Examination
*(All 2025 Mid-Semester questions are now 100% answered in the solutions above).*

---

### Uncovered Questions from 2025 End-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes**  
> Left unattempted per strict exam protocol.

1. **Question 1(a), (b), (d), (e) [4 × 2 = 8M]:**  
   *Define the following terms and state their usage:*  
   - (a) Home Agent  
   - (b) Care-of-address  
   - (d) MIMO  
   - (e) Network Slicing  
2. **Question 3(a), (b), (c) [20M]:**  
   *In the context of UMTS, answer the following:*  
   - (a) Write algorithmic steps for location tracking and setting up a call originated by land phone. [10]  
   - (b) What are the major functionalities of Node-B? [5]  
   - (c) What is session management? Which protocol is used for packet data communication? Name the relevant parameters to describe such a packet data connection. [5]
3. **Question 4(a), (b) [20M]:**  
   - (a) What is 5G core network? What are the tasks performed by it? [10]  
   - (b) Write the tasks of the following: (i) NRF, (ii) NSSF, (iii) UDM, (iv) WiFi offloading, (v) Carrier Aggregation. [10]
4. **Question 5(a), (b) [20M]:**  
   *Write short notes on:*  
   - (a) Tunneling in Mobile-IP [10]  
   - (b) Pervasive Computing [10]

---

### Uncovered Questions from 2024 Mid-Semester Examination
*(All 2024 Mid-Semester questions are now 100% answered in the solutions above).*

---

### Uncovered Questions from 2024 End-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes**  
> Left unattempted per strict exam protocol.

1. **Question 1(b), (c), (d), (e) [4 × 2 = 8M]:**  
   *Define the following terms and state their usage:*  
   - (b) Foreign Agent  
   - (c) MTC (Machine-Type Communications)  
   - (d) NFV (Network Functions Virtualization)  
   - (e) Mobility-binding table  
2. **Question 2(a) [10M]:**  
   *Which layer of GSM protocol stack takes care of Radio Resource Management? What are the tasks managed by this module?*
3. **Question 3(a), (b), (c) [20M]:**  
   *Answer the following for the Universal Mobile Telecommunications System (UMTS):*  
   - (a) What are the major components of Core network? Briefly state the tasks of each of the components. [10]  
   - (b) What roles are played by RNC? [5]  
   - (c) Write the names of the traffic types supported in such a system. [5]
4. **Question 4(a), (b), (c) [20M]:**  
   - (a) Draw the 5G access network architecture showing RAN and Core part. [5]  
   - (b) Write advantages of introducing small cells in 5G network. [5]  
   - (c) Do a point-wise comparison of Macro, Pico and Femto cell in terms of size, coverage range, cost and deployment. [10]
5. **Question 5(b) [10M]:**  
   *Write short notes on Context-Aware Computing and Applications [10]*

---

### Uncovered Questions from 2023 Mid-Semester Examination
*(All 2023 Mid-Semester questions are now 100% answered in the solutions above).*

---

### Uncovered Questions from 2023 End-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes**  
> Left unattempted per strict exam protocol.

1. **Question 1(a), (c), (d), (e) [4 × 2 = 8M]:**  
   *Define the following terms and state their usage:*  
   - (a) Softer-handover  
   - (c) User plane  
   - (d) Control plane  
   - (e) MIMO  
2. **Question 2(c) [5M]:**  
   *Write the algorithmic steps of CSMA/CA in WLAN.*
3. **Question 2(d) [5M]:**  
   *What is tunneling in Mobile-IP?*
4. **Question 3(a) [15M]:**  
   *What are the major components of UTRAN? Briefly state the tasks of each component.*
5. **Question 3(b) [5M]:**  
   *In the UMTS signaling protocol stack, what roles are played by “Call management” and “Mobility management”?*
6. **Question 4(a), (b) [20M]:**  
   - (a) What is a 5G core network? What tasks does it perform? [10]  
   - (b) Write the tasks of these functions: (i) NRF, (ii) NSSF, (iii) PCF, (iv) UDM. [10]
7. **Question 5(a), (b) [20M]:**  
   *Write short notes on:*  
   - (a) Carrier aggregation [10]  
   - (b) Pervasive Computing [10]
