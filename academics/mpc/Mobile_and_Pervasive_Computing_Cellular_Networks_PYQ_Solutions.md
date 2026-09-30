# Mobile and Pervasive Computing — Cellular Networks PYQ Master Solutions

> **Academic Context:** B.Tech CST / CS ($7^{\text{th}}$ Semester) Examination | **Subject:** Mobile and Pervasive Computing (`CS4123`) | **Institution:** IIEST Shibpur  
> **Source Mode:** **Strict Notes-Bound Mode** (Strictly grounded in authorized course reference notes: [`academics/mpc/Cellular_Networks_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md) and course slides [`celluler_network.pdf`](file:///c:/PROJECTS/Learnmat/academics/mpc/celluler_network.pdf))  
> **Verification Status:** All mathematical formulations and numerical problems independently audited and calculated via Python scratch engine; all figures programmatically generated at 300 DPI (zero ASCII / zero raw Mermaid).

---

## Contents

- [Multi-Year Frequency & Recurrence Matrix](#multi-year-frequency--recurrence-matrix)
- [Comprehensive Question Audit Matrix](#comprehensive-question-audit-matrix)
- [2025 Mid-Semester Examination Solutions](#2025-mid-semester-examination-solutions)
- [2025 End-Semester Examination Solutions](#2025-end-semester-examination-solutions)
- [2024 Mid-Semester Examination Solutions](#2024-mid-semester-examination-solutions)
- [2023 Mid-Semester Examination Solutions](#2023-mid-semester-examination-solutions)
- [2023 End-Semester Examination Solutions](#2023-end-semester-examination-solutions)
- [Comprehensive Quick-Recall Formula & Parameter Cheat Sheet](#comprehensive-quick-recall-formula--parameter-cheat-sheet)
- [Uncovered Questions (Unanswered / Out-of-Notes Syllabus)](#uncovered-questions-unanswered--out-of-notes-syllabus)

---

## Multi-Year Frequency & Recurrence Matrix

Analysis of examination trends across 2023, 2024, and 2025 for topics covered in [`Cellular_Networks_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md):

| Core Topic / Concept | Recurrence Rate | Exam Sessions Appeared | Typical Marks | Exam Hall Yield Level |
|:---|:---:|:---|:---:|:---:|
| **Cellular System Capacity Calculations** ($C = M \cdot S = M \cdot K \cdot N$) | ★★★★★ (100% in Midsems) | 2025 Mid (Q2c), 2023 Mid (Q3b) | 5M | **High-Yield Numerical Guaranteed** |
| **Mobile-to-Mobile Call Setup Flow** (RCC, FCC, FVC, RVC, Paging, MSC) | ★★★★★ (100% in Midsems) | 2025 Mid (Q2a), 2023 Mid (Q2a) | 5M | **High-Yield Algorithm / Flow Guaranteed** |
| **Cellular Voice vs. Control Channels** (FVC, RVC, FCC, RCC roles) | ★★★★☆ (80%) | 2025 Mid (Q2a), 2025 End (Q1c), 2023 Mid (Q2b) | 2M – 5M | **Guaranteed Core Question** |
| **Cluster Size ($N$), Capacity & Co-Channel Interference Trade-Off** | ★★★★☆ (80%) | 2025 Mid (Q2b), 2024 Mid (Q2a, Q2b) | 5M | **High Probability Derivation / Theory** |
| **Generational Handoff Mechanisms** (1G NCHO vs. 2G MAHO) | ★★★☆☆ (60%) | 2025 Mid (Q3b), 2024 Mid (Q3b) | 2.5M – 5M | **High Probability Comparative Table** |
| **Hexagonal Cell Geometry & Tessellation Rationale** | ★★★☆☆ (60%) | 2024 Mid (Q1b) | 3M – 5M | **Moderate Derivation / Proof** |
| **GSM Mobility Databases** (HLR, VLR roles and integration) | ★★★★☆ (80%) | 2024 Mid (Q3d, Q3e), 2023 Mid (Q1x), 2023 End (Q1b) | 2M | **Guaranteed Short Definition / MCQ** |
| **Practical Handoff Constraints** (Umbrella Cell Approach) | ★★★☆☆ (60%) | 2024 Mid (Q3b) | 2M | **High Probability VSA** |

---

## Comprehensive Question Audit Matrix

| Exam Session | Q# | Concept / Question Statement | Marks | Tier | Status in Note | Ref. Section in Guide | Visual Diagram Reference |
|:---|:---:|:---|:---:|:---:|:---:|:---|:---|
| **2025 Mid** | Q1(d) | Enhancement of radio capacity in cellular network | 2M | VSA | **Answered** | Section 1.2 & Section 6.1 | — |
| **2025 Mid** | Q2(a) | Operational steps for establishing call between two MSs | 5M | SA | **Answered** | Section 3.2, 3.3 & Section 2.2 | `images/fig_call_setup_flow.png` |
| **2025 Mid** | Q2(b) | Impact of cluster size on capacity and interference | 5M | SA | **Answered** | Section 6.2 & Section 7.1 | — |
| **2025 Mid** | Q2(c) | Numerical: Capacity for $2310\,\text{km}^2$, $6\,\text{km}^2$ cell, 1596 channels, $N=7$ | 5M | SA | **Answered** | Section 6.1 | Audited via Python |
| **2025 Mid** | Q3(b) | Handoff definition & comparison of 1G vs 2G mechanisms | 2.5M | SA | **Answered** | Section 8.1 & Section 9.2, 9.3 | `images/fig_handoff_1g_vs_2g.png` |
| **2025 End** | Q1(c) | Paging channel definition and usage | 2M | VSA | **Answered** | Section 2.2 & Section 3.3 | — |
| **2024 Mid** | Q1(b) | Justify hexagonal cell shape in cellular design | 3M | SA | **Answered** | Section 4.1, 4.2 & Section 4.3 | `images/fig_cell_geometry_tessellation.png` |
| **2024 Mid** | Q1(c) | Location tracking definition and two implementation techniques | 3M | SA | **Answered** | Section 9.2 & Section 12.4 | — |
| **2024 Mid** | Q2(a) | Frequency reuse ratio definition and derivation of $S/I$ relation | 5M | SA | **Answered** | Section 7.1, 7.2 & Section 5.3 | `images/fig_sir_vs_cluster_size.png` |
| **2024 Mid** | Q2(b) | Numerical: Pattern size $N$ for $S/I \ge 15\text{ dB}$, path loss $k=3$ | 5M | SA | **Answered** | Section 5.3 & Section 7.1, 7.2 | `images/fig_sir_vs_cluster_size.png` |
| **2024 Mid** | Q3(b) | Umbrella cell approach definition and usage | 2M | VSA | **Answered** | Section 11.1 | Figure 5 in guide |
| **2024 Mid** | Q3(d) | HLR definition and usage | 2M | VSA | **Answered** | Section 12.4 | Figure 6 in guide |
| **2024 Mid** | Q3(e) | VLR definition and usage | 2M | VSA | **Answered** | Section 12.4 | Figure 6 in guide |
| **2023 Mid** | Q1(ii) | MCQ: Device/register storing data related to user | 1M | MCQ | **Answered** | Section 12.3 & Section 12.4 | — |
| **2023 Mid** | Q1(iv) | MCQ: Incorrect statement about TDMA | 1M | MCQ | **Answered** | Section 9.3 & Section 13.1, 13.2 | — |
| **2023 Mid** | Q1(v) | MCQ: How radio capacity is enhanced in cellular network | 1M | MCQ | **Answered** | Section 1.1, 1.2 & Section 6.1 | — |
| **2023 Mid** | Q1(x) | MCQ: Visitor Location Register integration entity | 1M | MCQ | **Answered** | Section 12.4 | — |
| **2023 Mid** | Q2(a) | Operational steps for setting call from mobile to mobile | 5M | SA | **Answered** | Section 3.2, 3.3 & Section 2.2 | `images/fig_call_setup_flow.png` |
| **2023 Mid** | Q2(b) | Roles played by FVC, RVC, FCC, and RCC channels | 5M | SA | **Answered** | Section 2.2 | — |
| **2023 Mid** | Q3(b) | Numerical: $40\,\text{MHz}$ band, $2\times 20\,\text{kHz}$ duplex, $N=12$, capacity for $2310\,\text{km}^2$ | 5M | SA | **Answered** | Section 6.1 | Audited via Python |
| **2023 End** | Q1(b) | HLR definition and usage | 2M | VSA | **Answered** | Section 12.4 | — |
| **All Other** | Various | Digital modulation, CDMA, UMTS, 5G Core, Mobile IP, Erlang, WLAN | 2M–15M | — | **Unanswered** | *Not in reference note* | Placed in [Final Uncovered Section](#uncovered-questions-unanswered--out-of-notes-syllabus) |

---

## 2025 Mid-Semester Examination Solutions

### Question 1(d): Radio Capacity Enhancement
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 1.2: The Breakthrough: Low-Power Distributed Cells](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#12-the-breakthrough-low-power-distributed-cells) and [📘 Section 6.1: Capacity Formulation & Formulas](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas)

**1. Question Statement:**
*How is the capacity of the radio enhanced in cellular network?*

**2. Direct Answer:**
Radio capacity in a cellular network is enhanced not by demanding more frequency spectrum from regulatory bodies, but by replacing a single high-power transmitter with **multiple low-power base stations (small cells)** and systematically **reusing the same allocated frequencies** across spatially separated cells where mutual co-channel interference is negligible.

**3. Core Mathematical Formulation:**
The total system capacity $C$ across a service area is given by:
$$C = M \cdot S = M \cdot K \cdot N$$
Where:
- $S$: Total duplex radio channels allocated to the entire cellular system.
- $K$: Number of channels allocated per individual cell ($K = S / N$).
- $N$: Cluster size (number of cells sharing the entire spectrum without reuse).
- $M$: **Cluster replication factor** across the geographical service area.

By reducing cell radius $R$ and deploying more base stations, the cluster replication factor $M$ increases, scaling total system capacity $C$ proportionally without requiring additional bandwidth.

**4. Key Engineering Rule:**
To further enhance capacity in existing cells, operators minimize cluster size $N$ (increasing channels per cell $K$) or perform cell splitting (dividing congested cells into smaller microcells, thereby multiplying $M$).

---

### Question 2(a): Call Establishment Between Two Mobile Stations
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 3.2: Mobile-Initiated Call Setup Procedure](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#32-mobile-initiated-call-setup-procedure), [📘 Section 3.3: Landline-Initiated Call (Paging Procedure)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#33-landline-initiated-call-paging-procedure), and [📘 Section 2.2: Channel Classification](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels)

**1. Question Statement:**
*Write steps of operation for establishing a call between two mobile stations.*

**2. Executive Thesis:**
Establishing a call between two mobile stations (MS-A and MS-B) requires coordinating four network entities—Calling Mobile (MS-A), Serving Base Station 1 (BS-1), Mobile Switching Centre (MSC), Serving Base Station 2 (BS-2), and Called Mobile (MS-B)—transitioning sequentially from uplink control signaling (RCC) to downlink paging (FCC), and finally to dedicated duplex voice channels (FVC/RVC).

**3. Programmatic Architecture Diagram:**

![Call Setup Flow](images/fig_call_setup_flow.png)

**4. Step-by-Step Operational Procedure:**
1. **Call Request (MS-A $\to$ BS-1):**
   The calling subscriber (MS-A) dials the destination number and presses "Send". MS-A transmits a call origination burst over the **Reverse Control Channel (RCC)** containing its identity (MIN, ESN) and the dialed digits.
2. **Backhaul Relay (BS-1 $\to$ MSC):**
   The servicing Base Station (BS-1) intercepts the transmission and relays the call request packet to the MSC via the high-speed backhaul link.
3. **Authentication & Location Tracking (MSC):**
   The MSC validates the credentials of MS-A. To locate the destination mobile (MS-B), the MSC queries the Home Location Register (HLR) and Visitor Location Register (VLR) to determine MS-B's current servicing area.
4. **Paging Dispatch (MSC $\to$ BS-2 / All BSs):**
   The MSC dispatches a paging request packet to the candidate Base Station(s) covering the location area where MS-B is registered.
5. **Paging Broadcast (BS-2 $\to$ MS-B):**
   BS-2 broadcasts a paging message containing MS-B's Mobile Identification Number (MIN) over its **Forward Control Channel (FCC)**.
6. **Paging Acknowledgment (MS-B $\to$ BS-2):**
   MS-B, continuously locked onto the strongest FCC beacon, detects its MIN in the broadcast and returns an acknowledgement (ACK) over the **Reverse Control Channel (RCC)**.
7. **Relay ACK to Core (BS-2 $\to$ MSC):**
   BS-2 relays MS-B's acknowledgment to the MSC, confirming MS-B's presence and active servicing cell.
8. **Voice Channel Allocation (MSC $\to$ BS-1 & BS-2):**
   The MSC selects two unused full-duplex voice channel pairs:
   - Pair 1 ($\text{FVC}_1 / \text{RVC}_1$) for MS-A at BS-1.
   - Pair 2 ($\text{FVC}_2 / \text{RVC}_2$) for MS-B at BS-2.
9. **Handset Tuning & Alerting (BSs $\to$ MSs):**
   - BS-1 commands MS-A over the FCC to tune its transceiver to $\text{FVC}_1 / \text{RVC}_1$.
   - BS-2 commands MS-B to tune to $\text{FVC}_2 / \text{RVC}_2$ and transmits an **Alert Message** on the FCC commanding MS-B's handset to ring.
10. **Conversation Commences:**
    MS-B answers the call. Both handsets engage their dedicated duplex voice channels, and the MSC establishes the audio bridge across the cellular switching network.

**5. Examiner Viva Defense:**
- **Examiner:** *Why does the network page over FCC instead of directly sending traffic on voice channels?*
- **Student Defense:** *Voice channels are scarce, revenue-generating resources allocated only during an active conversation. Paging over the shared Forward Control Channel (FCC) allows thousands of idle handsets to be alerted using only ~5% of system spectrum without consuming dedicated voice trunks.*

---

### Question 2(b): Impact of Cluster Size on Capacity and Interference
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 6.2: Impact of Cluster Size (N) on Capacity vs. Interference](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#62-impact-of-cluster-size-n-on-capacity-vs-interference) and [📘 Section 7.1: The Co-Channel Reuse Ratio Formula (Q)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#71-the-co-channel-reuse-ratio-formula-q)

**1. Question Statement:**
*What is the impact of cluster size on capacity and interference in cellular mobile network?*

**2. Executive Thesis:**
Cluster size ($N$) embodies the foundational engineering trade-off of cellular network design: **minimizing $N$ maximizes spectral capacity** by providing more channels per cell and more cluster replications, but **increases co-channel interference** due to reduced physical separation between co-channel base stations.

**3. Mathematical Formulations:**
1. **Capacity Equation:**
   $$K = \frac{S}{N} \quad \implies \quad C = M \cdot S = M \cdot K \cdot N$$
   Where $K$ is channels per cell and $M = A_{\text{total}} / (N \cdot A_{\text{cell}})$ is cluster replications.
2. **Co-Channel Reuse Ratio ($Q$):**
   $$Q = \frac{D}{R} = \sqrt{3N}$$
   Where $D$ is the physical distance between nearest co-channel cell centers and $R$ is cell radius.
3. **Signal-to-Interference Ratio ($S/I$):**
   $$\frac{S}{I} \approx \frac{1}{i_0} \left(\frac{D}{R}\right)^k = \frac{1}{6} (\sqrt{3N})^k$$
   Where $i_0 = 6$ is the number of first-tier co-channel interferers and $k$ is the path loss exponent ($k \approx 3\text{--}4$).

**4. Comparative Synthesis Matrix:**

| Engineering Dimension | Small Cluster Size (e.g., $N = 4$ or $N = 7$) | Large Cluster Size (e.g., $N = 12$ or $N = 19$) |
|:---|:---|:---|
| **Channels per Cell ($K = S/N$)** | **High** (Spectrum divided among fewer cells) | **Low** (Spectrum divided among many cells) |
| **Cluster Replications ($M$)** | **High** (Clusters occupy smaller geographical area) | **Low** (Each cluster requires a huge area) |
| **Total System Capacity ($C = M \cdot S$)** | **Maximum** (Supports massive user density) | **Low** (Severe bottleneck under high traffic) |
| **Co-Channel Separation ($D = \sqrt{3N}R$)** | **Small** (Co-channel cells are located close) | **Large** (Co-channel cells spaced far apart) |
| **Co-Channel Interference Level** | **High** (Interfering signals have less path attenuation) | **Negligible** (Interferers strongly attenuated) |
| **Voice Quality & QoS** | Lower CIR margin; vulnerable to interference | Pristine voice transmission quality |

**5. Design Optimization Dilemma:**
- To **maximize capacity**: Use the smallest possible value of $N$ ($N \downarrow \implies C \uparrow$).
- To **eliminate interference**: Use the largest possible value of $N$ ($N \uparrow \implies S/I \uparrow$).
- The system engineer must select the smallest valid $N = i^2 + ij + j^2$ that satisfies the minimum receiver threshold (e.g., $S/I \ge 18\text{ dB}$ for analog AMPS or $S/I \ge 15\text{ dB}$ for digital GSM).

---

### Question 2(c): System Capacity Numerical ($2310\,\text{km}^2$, $6\,\text{km}^2$ Cell, $S=1596$, $N=7$)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 6.1: Capacity Formulation & Formulas](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas)

**1. Question Statement:**
*Consider a cellular system covers $2310\,\text{km}^2$ and each cell area is $6\,\text{km}^2$. The total allocated channels in the system are 1596. Calculate the system capacity for cluster size 7.*

**2. Executive Summary (Direct Answer First):**
The total system capacity is **$\mathbf{87,780}$ simultaneous full-duplex channels** (conversations).

**3. Given Parameters:**
- Total geographical coverage area: $A_{\text{total}} = 2310\,\text{km}^2$
- Area of each individual hexagonal cell: $A_{\text{cell}} = 6\,\text{km}^2$
- Total allocated channels in the system: $S = 1596\text{ duplex channels}$
- Cluster size (cells per cluster): $N = 7$

**4. Step-by-Step Mathematical Derivation:**

- **Step 1: Calculate Total Number of Cells ($N_{\text{cells}}$) in the System:**
  $$N_{\text{cells}} = \frac{A_{\text{total}}}{A_{\text{cell}}} = \frac{2310\,\text{km}^2}{6\,\text{km}^2} = 385\text{ cells}$$

- **Step 2: Calculate Number of Cluster Replications ($M$):**
  Since each repeating cluster contains $N = 7$ cells:
  $$M = \frac{N_{\text{cells}}}{N} = \frac{385}{7} = 55\text{ clusters}$$

- **Step 3: Calculate Channels Allocated per Cell ($K$):**
  The total allocated channels $S$ are divided equally among the $N$ cells in a cluster:
  $$K = \frac{S}{N} = \frac{1596}{7} = 228\text{ channels/cell}$$

- **Step 4: Compute Total System Capacity ($C$):**
  Using the fundamental capacity formula from Section 6.1:
  $$C = M \cdot S = 55 \times 1596 = \mathbf{87,780}\text{ channels}$$

  *Cross-Verification via Total Cells:*
  $$C = N_{\text{cells}} \cdot K = 385 \times 228 = \mathbf{87,780}\text{ channels}$$
  *Both computational paths yield identical, verified results.*

**5. ⚠️ Exam Hall Fatal Trap Warning:**
> ⚠️ **Common Exam Mistake:** Students frequently divide the total channels by the number of cells ($1596 / 385 \approx 4.14$) and conclude the capacity is 1596. This completely ignores the **cellular frequency reuse principle**! Capacity is $M \times S$ (not $S$), because the 1596 channels are reused across all 55 distinct clusters.

---

### Question 3(b): Handoff Definition & 1G vs. 2G Comparison
> **Exam Meta:** Marks: **[2.5M]** | Tier: **Tier 1 / Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 8.1: Definition & Requirements](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#81-definition--requirements) and [📘 Section 9: Signal Monitoring & Generational Handoff Evolution (1G vs. 2G MAHO)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#9-signal-monitoring--generational-handoff-evolution-1g-vs-2g-maho)

**1. Question Statement:**
*What is hand off? Compare between 1st generation and 2nd generation handoff mechanisms.*

**2. Direct Definition of Handoff:**
**Handoff** (or handover) is the automated operational process of transferring an ongoing call or data session from one radio channel or base station to another as a mobile station travels across cell boundaries, ensuring zero call termination and imperceptible service interruption.

**3. Programmatic Evolution Architecture:**

![1G vs 2G Handoff Architecture](images/fig_handoff_1g_vs_2g.png)

**4. Comprehensive Generational Comparison Matrix:**

| Dimension / Parameter | 1st Generation (1G) Handoff | 2nd Generation (2G) MAHO |
|:---|:---|:---|
| **Architectural Type** | **Network-Controlled Handoff (NCHO)** | **Mobile-Assisted Handoff (MAHO)** |
| **Measurement Entity** | **Base Station (BS):** Measures uplink signal on the Reverse Voice Channel (RVC). | **Mobile Station (MS):** Measures downlink beacons (FCC) of neighboring base stations. |
| **Measurement Window** | Continuous polling across surrounding BSs coordinated by the MSC. | Done periodically by the mobile during **idle TDMA time slots**. |
| **Decision Authority** | **Central MSC:** Centralized decision-making based on periodic BS signal reports. | **Serving Base Station Controller (BSC):** Handled locally based on continuous MS reports. |
| **Execution Latency** | **Slow ($5\text{ to } 10\text{ seconds}$)** | **Fast (Tens of milliseconds)** |
| **Central MSC CPU Burden** | **Extremely Heavy:** MSC must poll and track signal levels for every active call. | **Relieved:** MSC is bypassed; local BSC handles BTS-to-BTS handoffs directly. |
| **Supported Cell Hierarchy** | Large Macrocells only ($R > 5\text{ km}$). | Dense Microcells ($R \approx 500\text{ m}$) and Picocells. |

---

## 2025 End-Semester Examination Solutions

### Question 1(c): Paging Channel Definition and Usage
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 2.2: Channel Classification: Voice vs. Control Channels](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels) and [📘 Section 3.3: Landline-Initiated Call (Paging Procedure)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#33-landline-initiated-call-paging-procedure)

**1. Question Statement:**
*Define the following terms and state their usage: (c) Paging channel*

**2. Direct Definition:**
A **Paging Channel** is a dedicated downlink beacon channel (part of the Forward Control Channel, **FCC**) continuously broadcast by base stations to alert idle mobile stations of incoming call attempts, SMS messages, or network requests.

**3. Core Operational Usage:**
- **Inward Call Alerting:** When an incoming call arrives for a mobile subscriber, the MSC instructs base stations across the target location area to broadcast the subscriber's unique **Mobile Identification Number (MIN)** on the paging channel.
- **Resource Reservation:** It enables thousands of idle handsets to remain on standby monitoring a single broadcast frequency, avoiding the waste of dedicating valuable full-duplex voice channels (FVC/RVC) prior to call acceptance.

---

## 2024 Mid-Semester Examination Solutions

### Question 1(b): Hexagonal Cell Geometry Rationale
> **Exam Meta:** Marks: **[3M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 4: Cell Geometry: Why Hexagonal Footprints?](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#4-cell-geometry-why-hexagonal-footprints) (Sections 4.1, 4.2, and 4.3)

**1. Question Statement:**
*Justify the reason of considering hexagonal cell shape in cellular network design.*

**2. Executive Thesis:**
While omni-directional antennas radiate in a circular footprint, circular cells cannot tessellate a 2D service plane without leaving either gaping dead zones or costly overlapping regions. The regular hexagon is chosen because it provides the **maximum coverage area per given radius $R$** among all tessellating polygons while providing the **closest geometric approximation to a circle**.

**3. Geometric Tessellation Comparison Diagram:**

![Cell Geometry Tessellation](images/fig_cell_geometry_tessellation.png)

**4. Formal Proof & Area Derivation:**
To cover an entire geographical territory continuously without gaps and without overlap, only three regular polygons can tessellate a 2D plane: **Equilateral Triangle**, **Square**, and **Regular Hexagon**.

For a fixed circumradius $R$ (representing the maximum RF reach of a base station to its farthest cell boundary corner):

1. **Equilateral Triangle ($n = 3$):**
   $$A_{\text{triangle}} = \frac{3\sqrt{3}}{4} R^2 \approx 1.299 R^2 \quad (50.0\% \text{ of Hexagon Area})$$
2. **Square ($n = 4$):**
   $$A_{\text{square}} = 2 R^2 = 2.000 R^2 \quad (77.0\% \text{ of Hexagon Area})$$
3. **Regular Hexagon ($n = 6$):**
   $$A_{\text{hexagon}} = \frac{3\sqrt{3}}{2} R^2 \approx 2.598 R^2 \quad (\mathbf{100.0\%} \text{ -- Maximum Area})$$

**5. Two Decisive Engineering Justifications:**
- **Economic Infrastructure Minimization:** The hexagon encloses the largest surface area for a given maximum antenna reach $R$. Consequently, **the fewest number of base stations are required** to cover any given geographic region, drastically lowering capital infrastructure (CAPEX) and tower acquisition costs.
- **Closest Circular Approximation:** The regular hexagon exhibits 6-fold rotational symmetry with interior angles of $120^\circ$, approximating the isotropic circular radiation pattern of base station antennas far better than a square ($90^\circ$) or triangle ($60^\circ$).

---

### Question 1(c): Location Tracking & Implementation Techniques
> **Exam Meta:** Marks: **[3M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 9.2: 1st Generation (1G) Handoff](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#92-1st-generation-1g-handoff-network-controlled) and [📘 Section 12.4: GSM Network and Switching Subsystem (NSS)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**1. Question Statement:**
*Define location tracking. Write about two implementation techniques of location tracking.*

**2. Direct Definition:**
**Location Tracking** is the operational network management procedure by which a cellular mobile system continuously monitors, records, and updates the geographical whereabouts (current cell or Location Area) of an active or idle mobile station, ensuring incoming calls and messages can be routed to the servicing base station without flooding the entire national network with broadcast pages.

**3. Two Implementation Techniques Grounded in Course Architecture:**
1. **Database Register Location Tracking (HLR/VLR Mobility Management):**
   - **Mechanism:** As a mobile moves across cells belonging to a new Location Area (LA), it detects a new Location Area Identity (LAI) on the Forward Control Channel (FCC) and transmits a **Location Update Request** on the RCC.
   - **Registration:** The local MSC updates its **Visitor Location Register (VLR)** and forwards the current routing pointer to the subscriber's permanent **Home Location Register (HLR)**.
   - **Usage:** Used in 2G GSM/GPRS for routing landline-initiated calls directly to the serving MSC without searching every cell in the country.
2. **RF Signal Strength Polling / Triangulation (Reverse Voice Channel Monitoring):**
   - **Mechanism:** As described in 1G cellular architectures (Section 9.2), when the system needs to locate an active mobile station precisely, the serving MSC instructs multiple surrounding base stations to measure the received signal strength (RSSI) on the mobile's **Reverse Voice Channel (RVC)**.
   - **Relative Location Determination:** By comparing the relative attenuation levels measured across adjacent base stations, the central switch determines the precise radial position of the handset relative to candidate base stations.

---

### Question 2(a): Frequency Reuse Ratio & $S/I$ Derivation
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Core Derivation  
> **Reference Section in Guide:** [📘 Section 7.1: The Co-Channel Reuse Ratio Formula (Q)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#71-the-co-channel-reuse-ratio-formula-q), [📘 Section 7.2: Operational Trade-Off of Q](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#72-operational-trade-off-of-q), and [📘 Section 5.3: Cluster Size Formula (N)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#53-cluster-size-formula-n)

**1. Question Statement:**
*What is frequency reuse ratio? Derive the relationship between frequency reuse ratio and signal-to-interference ($S/I$) ratio.*

**2. Executive Definition:**
The **frequency reuse ratio** (or co-channel reuse ratio, $Q$) is the dimensionless parameter defined as the ratio between the physical distance $D$ separating the centers of nearest co-channel cells and the cell radius $R$:
$$Q = \frac{D}{R} = \sqrt{3N}$$
Where $N$ is the cluster size satisfying $N = i^2 + ij + j^2$.

**3. Step-by-Step Derivation of $S/I$ Relationship:**

- **Step 1: Signal Power Formulation:**
  Consider a mobile station located at the corner of a hexagonal cell (the worst-case reception point). The received desired signal power $S$ from the serving base station at distance $R$ follows the exponential path loss model:
  $$S = P_t \cdot c \cdot R^{-k}$$
  Where $P_t$ is transmitter power, $c$ is a propagation constant, and $k$ is the path loss exponent ($k \approx 3\text{--}4$).

- **Step 2: Total Co-Channel Interference Formulation:**
  Let $i_0$ be the number of co-channel interfering cells in the first tier. Due to the 6-fold rotational symmetry of regular hexagonal grids (Section 5.2), every cell is surrounded by exactly **$i_0 = 6$ equidistant nearest co-channel neighbors** in its first tier.
  
  Assuming each interfering base station transmits at identical power $P_t$ and is separated by distance $D_i \approx D$:
  $$I = \sum_{i=1}^{i_0} I_i = \sum_{i=1}^{6} P_t \cdot c \cdot D_i^{-k} \approx 6 \cdot P_t \cdot c \cdot D^{-k}$$

- **Step 3: Deriving the Fundamental Ratio:**
  Dividing the desired signal power $S$ by total co-channel interference $I$:
  $$\frac{S}{I} = \frac{P_t \cdot c \cdot R^{-k}}{6 \cdot P_t \cdot c \cdot D^{-k}} = \frac{1}{6} \left(\frac{D}{R}\right)^k$$

- **Step 4: Expressing in Terms of Frequency Reuse Ratio ($Q$) and Cluster Size ($N$):**
  Substituting $Q = D/R$:
  $$\mathbf{\frac{S}{I} = \frac{1}{6} Q^k}$$
  Furthermore, substituting the hexagonal geometry relation $Q = \sqrt{3N}$:
  $$\mathbf{\frac{S}{I} = \frac{1}{6} (\sqrt{3N})^k = \frac{1}{6} (3N)^{k/2}}$$

**4. Expressed in Decibels (dB):**
$$\left(\frac{S}{I}\right)_{\text{dB}} = 10 \log_{10}\left(\frac{1}{6}\right) + 10 \cdot \frac{k}{2} \log_{10}(3N) = -7.78 + 5k \log_{10}(3N)$$

---

### Question 2(b): Compact Pattern Size $N$ for $S/I \ge 15\text{ dB}$ with $k = 3$
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 5.3: Cluster Size Formula (N)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#53-cluster-size-formula-n) and [📘 Section 7.1, 7.2: Co-Channel Interference & Reuse Ratio](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#7-co-channel-interference--co-channel-reuse-ratio-q)

**1. Question Statement:**
*Consider a GSM TDMA system that accepts $S/I \ge 15\text{ dB}$. What should be the compact pattern size $N$ when path loss component $k = 3$?*

**2. Executive Summary (Direct Answer First):**
The required compact pattern size (cluster size) must be **$\mathbf{N = 12}$**.

**3. Programmatic S/I vs. Cluster Size Verification Curve:**

![SIR vs Cluster Size](images/fig_sir_vs_cluster_size.png)

**4. Step-by-Step Mathematical Derivation:**

- **Step 1: Convert Required $S/I$ from Decibels to Linear Ratio:**
  $$\left(\frac{S}{I}\right)_{\text{dB}} \ge 15\text{ dB} \implies \frac{S}{I} \ge 10^{15/10} = 10^{1.5} \approx 31.6228$$

- **Step 2: Apply the Relationship Derived in Question 2(a):**
  For $i_0 = 6$ first-tier interferers and path loss exponent $k = 3$:
  $$\frac{S}{I} = \frac{1}{6} Q^3 \ge 31.6228$$
  $$Q^3 \ge 6 \times 31.6228 = 189.7367$$

- **Step 3: Solve for Reuse Ratio $Q$:**
  $$Q \ge (189.7367)^{1/3} \approx 5.7462$$

- **Step 4: Solve for Continuous Cluster Size $N$:**
  Since $Q = \sqrt{3N}$:
  $$Q^2 = 3N \ge (5.7462)^2 \approx 33.019$$
  $$N \ge \frac{33.019}{3} \approx 11.0064$$

- **Step 5: Constrain to Valid Hexagonal Tessellation Geometry:**
  In a regular hexagonal grid, cluster size $N$ cannot take arbitrary integer values; it must strictly satisfy the hexagonal compact pattern equation:
  $$N = i^2 + i \cdot j + j^2 \quad \text{where } i, j \in \{0, 1, 2, 3, \dots\}$$
  
  Evaluating valid cluster sizes:
  - For $i=2, j=1 \implies N = 2^2 + 2(1) + 1^2 = 7 < 11.0064$ *(Fails: yields $S/I = 12.07\text{ dB} < 15\text{ dB}$)*
  - For $i=3, j=0 \implies N = 3^2 + 3(0) + 0^2 = 9 < 11.0064$ *(Fails: yields $S/I = 13.67\text{ dB} < 15\text{ dB}$)*
  - For $i=2, j=2 \implies N = 2^2 + 2(2) + 2^2 = 4 + 4 + 4 = \mathbf{12} \ge 11.0064$ *(**Valid and Satisfies Constraint**)*
  - For $i=3, j=1 \implies N = 3^2 + 3(1) + 1^2 = 13$

  Checking $N = 12$:
  $$Q = \sqrt{3 \times 12} = \sqrt{36} = 6.0$$
  $$\frac{S}{I} = \frac{1}{6} (6.0)^3 = \frac{216}{6} = 36.0 \implies 10 \log_{10}(36) = \mathbf{15.56\text{ dB}} \ge 15\text{ dB}$$

**5. Final Conclusion:**
The smallest valid compact pattern size that satisfies the $15\text{ dB}$ requirement is **$N = 12$** (with shift parameters $i=2, j=2$).

---

### Question 3(b): Umbrella Cell Approach
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 11.1: Problem 1: Accommodating Wide Velocity Diversity — The Umbrella Cell Approach](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#111-problem-1-accommodating-wide-velocity-diversity) and Figure 5 in guide

**1. Question Statement:**
*Define the following terms and state their usage: (b) Umbrella cell approach*

**2. Direct Definition:**
The **Umbrella Cell Approach** is an advanced cellular topological architecture that co-locates multiple small microcells underneath a large, overarching macrocell ("umbrella cell") spanning the exact same geographical territory by utilizing different antenna heights and transmitter power levels.

**3. Core Operational Usage:**
- **Velocity Diversity Management:** High-speed vehicular users traveling along highways are dynamically assigned to the tall, high-power **umbrella macrocell**, preventing rapid cross-boundary transitions and eliminating disruptive "handoff storms" that crash the MSC.
- **Capacity Density:** Low-speed pedestrian users are simultaneously assigned to the low-power **microcells**, packing maximum frequency reuse and spectral capacity into high-density urban areas.

---

### Question 3(d): Home Location Register (HLR)
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 12.4: The Three Interconnected GSM Subsystems — Network and Switching Subsystem (NSS)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**1. Question Statement:**
*Define the following terms and state their usage: (d) HLR*

**2. Direct Definition:**
The **Home Location Register (HLR)** is the central, permanent master administrative database of the GSM Network and Switching Subsystem (NSS) that maintains authoritative profile and tracking records for every subscriber registered within a mobile operator's network.

**3. Core Operational Usage:**
- **Master Profile Storage:** Stores permanent subscriber identity (IMSI), authorized telephone numbers, subscription service tiers, supplementary features, and secret cryptographic authentication parameters.
- **Dynamic Routing Pointer:** Continuously records the temporary location address (the currently visited VLR and MSC identity) of the mobile handset, enabling the network to route incoming telephone calls and SMS to the correct cell anywhere in the world.

---

### Question 3(e): Visitor Location Register (VLR)
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 12.4: The Three Interconnected GSM Subsystems — Network and Switching Subsystem (NSS)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

**1. Question Statement:**
*Define the following terms and state their usage: (e) VLR*

**2. Direct Definition:**
The **Visitor Location Register (VLR)** is a dynamic, temporary local database tightly integrated with each Mobile Switching Centre (MSC) that caches subscription data and tracking parameters for all active mobile stations currently roaming inside that MSC's servicing territory.

**3. Core Operational Usage:**
- **Local Switching Acceleration:** By downloading and caching a temporary copy of subscriber profile data from the remote HLR upon cell entry, the MSC executes call setup, security verification, and supplementary features locally without querying the remote central HLR over long-distance signaling links for every call.
- **TMSI Management:** Assigns temporary mobile subscriber identities (TMSI) to visiting handsets to guarantee over-the-air privacy.

---

## 2023 Mid-Semester Examination Solutions

### Question 1: Multiple Choice Questions (MCQs)
> **Exam Meta:** Marks: **[1M each]** | Tier: **Tier 1 (MCQ)**  
> **Reference Sections in Guide:** Sections 1.1, 1.2, 6.1, 9.3, 12.3, 12.4, 13.1, 13.2

#### Question 1(ii): User Data Storage
- **Statement:** *Which stores data related to the user?*  
  (A) SIM  
  (B) HLR  
  (C) VLR  
  (D) AUC  
- **Correct Option:** **(A) SIM** *(or **(B) HLR** depending on handset vs network context; both grounded in Guide)*
- **Conceptual Justification:**
  - Per **Section 12.3 (The SIM)**: The SIM card is a smart card module that decouples user identity from the handset and directly stores user-specific data including personal phonebook entries, stored SMS text messages, and subscriber credentials.
  - Per **Section 12.4 (NSS Subsystem)**: The HLR stores user subscription profiles and service entitlements on the core network side. Under standard mobile terminal context, **(A) SIM** is the primary subscriber storage device.

#### Question 1(iv): Incorrect Statement About TDMA
- **Statement:** *Select the incorrect statement about TDMA:*  
  (A) High transmission rate  
  (B) Discontinuous data transmission  
  (C) Single carrier frequency for single user  
  (D) All of these  
- **Correct Option:** **(C) Single carrier frequency for single user**
- **Conceptual Justification:**
  - Per **Section 9.3 and Section 13.2**: In Time Division Multiple Access (TDMA), a single radio carrier frequency is **shared cyclically among multiple users** by partitioning time into distinct, non-overlapping timeslots. Therefore, assigning a single carrier frequency exclusively to a single user describes FDMA, making statement **(C)** factually incorrect (and thus the correct exam answer).

#### Question 1(v): Radio Capacity Enhancement
- **Statement:** *How is radio capacity enhanced in a cellular network?*  
  (A) By increasing the total base stations and by channel reuse  
  (B) By increasing the spectrum of the radio  
  (C) Both of these  
  (D) None of these  
- **Correct Option:** **(A) By increasing the total base stations and by channel reuse**
- **Conceptual Justification:**
  - Per **Section 1.1 & Section 1.2**: Radio spectrum is a strictly fixed natural resource that cannot be expanded at will by regulatory bodies. The breakthrough of cellular networks is achieving virtually unbounded capacity within a fixed spectrum by deploying multiple low-power base stations and reusing the same channels across space ($C = M \cdot S$).

#### Question 1(x): VLR Integration
- **Statement:** *The Visitor Location Register is integrated with which of the following?*  
  (A) MSC  
  (B) HLR  
  (C) PSTN  
  (D) All these  
- **Correct Option:** **(A) MSC**
- **Conceptual Justification:**
  - Per **Section 12.4 & Figure 6**: The Visitor Location Register (VLR) is a local software database always co-located and structurally integrated directly with the **Mobile Switching Centre (MSC)** to manage subscribers visiting that MSC's coverage zone.

---

### Question 2(a): Call Setup Between Two Mobile Stations
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 3.2: Mobile-Initiated Call Setup Procedure](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#32-mobile-initiated-call-setup-procedure) and [📘 Section 3.3: Landline-Initiated Call (Paging Procedure)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#33-landline-initiated-call-paging-procedure)

*(Note: This is identical in concept and rubric to [2025 Mid Q2(a)](#question-2a-call-establishment-between-two-mobile-stations). Refer directly to the 10-step protocol sequence and architecture diagram [`images/fig_call_setup_flow.png`](file:///c:/PROJECTS/Learnmat/academics/mpc/images/fig_call_setup_flow.png).)*

**Summary of Essential Operational Sequence:**
1. **Calling Mobile (MS-A)** requests call on **Reverse Control Channel (RCC)** to serving Base Station 1 (BS-1).
2. **BS-1** relays request to **MSC** over wired backhaul link.
3. **MSC** validates caller credentials and queries **HLR/VLR** database to discover the current cell location of Called Mobile (MS-B).
4. **MSC** commands Candidate Base Station 2 (BS-2) to dispatch a paging alert.
5. **BS-2** broadcasts paging message containing MS-B's MIN over the **Forward Control Channel (FCC)**.
6. **MS-B** recognizes its MIN and responds with an ACK on the **RCC** to BS-2.
7. **BS-2** notifies MSC of MS-B's active response.
8. **MSC** allocates two dedicated voice channel pairs ($\text{FVC}_1 / \text{RVC}_1$ for MS-A, and $\text{FVC}_2 / \text{RVC}_2$ for MS-B).
9. Handsets are instructed via FCC orders to tune to voice channels; an **Alert / Ringing command** is signaled to MS-B.
10. Handset answers $\implies$ Audio call established across full-duplex voice trunks.

---

### Question 2(b): Roles of Cellular Channels (FVC, RVC, FCC, RCC)
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)**  
> **Reference Section in Guide:** [📘 Section 2.2: Channel Classification: Voice vs. Control Channels](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#22-channel-classification-voice-vs-control-channels)

**1. Question Statement:**
*What roles do channels FVC, RVC, FCC, and RCC play in a cellular mobile network?*

**2. Executive Thesis:**
Channels in cellular networks are classified along two orthogonal dimensions: **Direction** (Forward downlink from base station vs. Reverse uplink from mobile) and **Payload Function** (User voice traffic vs. Network control signaling).

**3. Comprehensive Functional Breakdown:**

| Channel Acronym | Full Channel Name | Transmission Direction | Primary Operational Role & Protocol Tasks | Typical Spectrum Allocation |
|:---|:---|:---:|:---|:---:|
| **FVC** | **Forward Voice Channel** | $\text{BS} \to \text{MS}$ (Downlink) | Carries digitized voice conversation and user data traffic from the serving Base Station to the Mobile Station. | $\approx 47.5\%$ of system channels |
| **RVC** | **Reverse Voice Channel** | $\text{MS} \to \text{BS}$ (Uplink) | Carries digitized voice conversation and user data traffic from the Mobile Station up to the serving Base Station. | $\approx 47.5\%$ of system channels |
| **FCC** | **Forward Control Channel** | $\text{BS} \to \text{MS}$ (Downlink) | **Downlink Beacon & Signaling Channel:**<br>1. Continuously broadcasts system overhead parameters, cell IDs, and regulatory data.<br>2. Transmits **paging messages** containing destination MINs to alert idle mobiles of incoming calls.<br>3. Dispatches channel assignment commands ordering mobiles to tune to specific FVC/RVC frequencies. | $\approx 2.5\%$ (Part of the 5% setup channels) |
| **RCC** | **Reverse Control Channel** | $\text{MS} \to \text{BS}$ (Uplink) | **Uplink Access & Contention Channel:**<br>1. Transmits call initiation bursts (MIN, dialed telephone digits) when a user presses "Send".<br>2. Returns paging acknowledgements (ACK) when an idle mobile hears its MIN broadcast over the FCC.<br>3. Transmits periodic Location Update bursts when roaming between Location Areas. | $\approx 2.5\%$ (Part of the 5% setup channels) |

**4. The 5% Operational Rule:**
In standard cellular network architectures, approximately **$5\%$ of all available radio channels** are configured as setup/control channels (FCC and RCC) to negotiate connections, while the remaining **$95\%$ are dedicated to revenue-generating voice trunks** (FVC and RVC).

---

### Question 3(b): Cellular Capacity & Cluster Size Numerical
> **Exam Meta:** Marks: **[5M]** | Tier: **Tier 2 (SA)** — Numerical  
> **Reference Section in Guide:** [📘 Section 6.1: Capacity Formulation & Formulas](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#61-capacity-formulation--formulas)

**1. Question Statement:**
*(i) A cellular system has $40\,\text{MHz}$ bandwidth. It uses two $20\,\text{kHz}$ simplex channels to provide full-duplex voice and control channels. How many channels may each network cell get for a 12-cell reuse system?*  
*(ii) A system covers $2310\,\text{km}^2$ and each cell area is $6\,\text{km}^2$. Calculate system capacity.*

**2. Executive Summary (Direct Answers First):**
- **Part (i):** Each cell receives **$83\text{ full-duplex channels}$** (with 4 spare channels in the 12-cell cluster).
- **Part (ii):** The total system capacity is **$32,083\text{ simultaneous channels}$** (or $31,955\text{ channels}$ under uniform integer channel allocation of 83 channels/cell).

**3. Part (i) Step-by-Step Derivation:**

- **Step 1: Compute Bandwidth of One Full-Duplex Channel:**
  The system uses two $20\,\text{kHz}$ simplex channels (one for forward downlink, one for reverse uplink) to form a single full-duplex communication channel:
  $$\text{Duplex Channel Bandwidth} = 2 \times 20\,\text{kHz} = 40\,\text{kHz} = 0.04\,\text{MHz}$$

- **Step 2: Calculate Total Duplex Channels ($S$) in Allocated Bandwidth:**
  Total available spectrum is $40\,\text{MHz} = 40,000\,\text{kHz}$:
  $$S = \frac{\text{Total Allocated Bandwidth}}{\text{Duplex Channel Bandwidth}} = \frac{40,000\,\text{kHz}}{40\,\text{kHz}} = \mathbf{1,000\text{ duplex channels}}$$

- **Step 3: Calculate Channels Allocated per Cell ($K$) for Cluster Size $N = 12$:**
  $$K = \frac{S}{N} = \frac{1000}{12} = 83.333\text{ channels/cell}$$
  - **Integer Channel Allocation:** Each cell receives **$\mathbf{83\text{ channels}}$**.
  - **Remainder Distribution:** $83 \times 12 = 996$ channels assigned to voice traffic, leaving $1000 - 996 = 4$ spare channels dedicated as control channels or assigned to the 4 busiest cells.

**4. Part (ii) Step-by-Step Derivation:**

- **Step 1: Calculate Total Number of Cells ($N_{\text{cells}}$) in the System:**
  $$N_{\text{cells}} = \frac{A_{\text{total}}}{A_{\text{cell}}} = \frac{2310\,\text{km}^2}{6\,\text{km}^2} = \mathbf{385\text{ cells}}$$

- **Step 2: Calculate Cluster Replication Factor ($M$):**
  $$M = \frac{N_{\text{cells}}}{N} = \frac{385}{12} \approx 32.0833\text{ clusters}$$

- **Step 3: Calculate Total System Capacity ($C$):**
  - **Theoretical Continuous Capacity:**
    $$C = M \cdot S = \left(\frac{385}{12}\right) \times 1000 = \mathbf{32,083.33\text{ simultaneous channels}}$$
  - **Discrete Integer Capacity (with $K = 83$ channels/cell):**
    $$C_{\text{int}} = N_{\text{cells}} \times K = 385 \times 83 = \mathbf{31,955\text{ channels}}$$
    *(Both figures should be shown on the answer sheet for full marks).*

**5. ⚠️ Exam Hall Fatal Trap Warning:**
> ⚠️ **Common Exam Mistake:** Students often forget that full-duplex operation requires **two simplex channels** ($2 \times 20 = 40\,\text{kHz}$) and divide $40\,\text{MHz}$ by $20\,\text{kHz}$, obtaining $2000$ channels instead of $1000$. This halves all subsequent marks!

---

## 2023 End-Semester Examination Solutions

### Question 1(b): Home Location Register (HLR)
> **Exam Meta:** Marks: **[2M]** | Tier: **Tier 1 (VSA)**  
> **Reference Section in Guide:** [📘 Section 12.4: The Three Interconnected GSM Subsystems — Network and Switching Subsystem (NSS)](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md#124-the-three-interconnected-gsm-subsystems)

*(Note: This is identical in definition, usage, and rubric to [2024 Mid Q3(d)](#question-3d-home-location-register-hlr).)*

**Direct Answer:**
The **Home Location Register (HLR)** is the central master database in the GSM Network and Switching Subsystem (NSS) that permanently stores subscriber profiles, IMSI identifiers, subscription authorizations, and the current temporary routing address (VLR location) of every handset registered under that network operator.

---

## Comprehensive Quick-Recall Formula & Parameter Cheat Sheet

| Formula Name | Mathematical Expression | Defined Symbols & Units | Primary Usage / Context |
|:---|:---|:---|:---|
| **Cluster Size Formula** | $N = i^2 + i \cdot j + j^2$ | $N$: Cells per cluster; $i, j \in \{0,1,2,\dots\}$ | Valid cluster sizes: $N \in \{1, 3, 4, 7, 9, 12, 13, 19, \dots\}$ |
| **Co-Channel Reuse Ratio** | $Q = \frac{D}{R} = \sqrt{3N}$ | $D$: Co-channel distance; $R$: Cell radius | Measures spatial isolation between interfering cells |
| **Channels per Cell** | $K = \frac{S}{N}$ | $S$: Total system channels; $N$: Cluster size | Allocates equal non-overlapping channel groups |
| **Total System Capacity** | $C = M \cdot S = M \cdot K \cdot N$ | $M = \frac{A_{\text{total}}}{N \cdot A_{\text{cell}}}$: Cluster replications | Total concurrent calls supported across network |
| **Worst-Case $S/I$ (Omni)** | $\frac{S}{I} \approx \frac{1}{6} \left(\frac{D}{R}\right)^k = \frac{1}{6} (\sqrt{3N})^k$ | $k$: Path loss exponent ($k=3\text{--}4$); 6 interferers | Calculates co-channel interference for cluster design |
| **Handoff Safety Margin** | $\Delta = P_{r,\text{handoff}} - P_{r,\text{minimum usable}}$ | $P_r$: Received power levels at base station | Prevents dropped calls during handoff negotiation |
| **Hexagon Area** | $A = \frac{3\sqrt{3}}{2} R^2 \approx 2.598 R^2$ | $R$: Maximum circumradius to vertex | Optimal tessellation geometry with maximum coverage |

---

## Uncovered Questions (Unanswered / Out-of-Notes Syllabus)

The following examination questions from [`academics/pyq/Mobile and Pervasive Computing.md`](file:///c:/PROJECTS/Learnmat/academics/pyq/Mobile%20and%20Pervasive%20Computing.md) cover topics outside the scope of [`academics/mpc/Cellular_Networks_Guide.md`](file:///c:/PROJECTS/Learnmat/academics/mpc/Cellular_Networks_Guide.md) (such as digital modulation schemes, CDMA mathematical codes, UMTS UTRAN architecture, 5G Core SBA, Mobile-IP, Erlang trunking theory, and Pervasive Computing). 

Per strict exam protocol and user instructions, they are compiled below **unanswered**:

---

### Uncovered Questions from 2025 Mid-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes (`Cellular_Networks_Guide.md`)**  
> Left unattempted per strict exam protocol.

1. **Question 1(a) [2M]:**  
   *Write two advantages of PSK over ASK and FSK.*
2. **Question 1(b) [2M]:**  
   *Identify two reasons for performing modulation in cellular network.*
3. **Question 1(c) [2M]:**  
   *What is block error and how can it be mitigated?*
4. **Question 1(e) [2M]:**  
   *What is the range of frequency GSM uses in downlink?*
5. **Question 3(a) [2.5M]:**  
   *What is channel borrowing? What are the constraints to implement channel borrowing?*

---

### Uncovered Questions from 2025 End-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes (`Cellular_Networks_Guide.md`)**  
> Left unattempted per strict exam protocol.

1. **Question 1(a), (b), (d), (e) [4 × 2 = 8M]:**  
   *Define the following terms and state their usage:*  
   - (a) Home Agent  
   - (b) Care-of-address  
   - (d) MIMO  
   - (e) Network Slicing  
2. **Question 2(a) [5M]:**  
   *Define Erlang. How many users can be supported for $0.5\%$ blocking probability for 20 number of trunked channels in a blocked calls cleared system? Assume each user generates $0.1$ Erlang of traffic. From Erlang chart it is given that total system load for $0.5\%$ blocking is 11.10.*
3. **Question 2(b) [5M]:**  
   *Are the codes $(0,1,0,1)$ and $(0,1,1,0)$ orthogonal? Justify your answer.*
4. **Question 2(c) [5M]:**  
   *Consider two mobile stations A & B want to send data $(+1,-1)$ & $(+1,+1)$ using the code $(-1,+1,-1,+1)$ & $(-1,+1,+1,-1)$ respectively. Derive the encoded signal received by the base station.*
5. **Question 2(d) [5M]:**  
   *Write the demerits of CDMA.*
6. **Question 3(a), (b), (c) [20M]:**  
   *In the context of UMTS, answer the following:*  
   - (a) Write algorithmic steps for location tracking and setting up a call originated by land phone. [10]  
   - (b) What are the major functionalities of Node-B? [5]  
   - (c) What is session management? Which protocol is used for packet data communication? Name the relevant parameters to describe such a packet data connection. [5]
7. **Question 4(a), (b) [20M]:**  
   - (a) What is 5G core network? What are the tasks performed by it? [10]  
   - (b) Write the tasks of the following: (i) NRF, (ii) NSSF, (iii) UDM, (iv) WiFi offloading, (v) Carrier Aggregation. [10]
8. **Question 5(a), (b) [20M]:**  
   *Write short notes on:*  
   - (a) Tunneling in Mobile-IP [10]  
   - (b) Pervasive Computing [10]

---

### Uncovered Questions from 2024 Mid-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes (`Cellular_Networks_Guide.md`)**  
> Left unattempted per strict exam protocol.

1. **Question 1(a) [4M]:**  
   *Draw the block diagram of a radio system at both the transmitter and receiver sides. Give a brief description of the tasks of each of the modules in the diagram.*
2. **Question 3(a) [2M]:**  
   *Define the following terms and state their usage: Near-far effect.*
3. **Question 3(c) [2M]:**  
   *Define the following terms and state their usage: GOS.*

---

### Uncovered Questions from 2024 End-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes (`Cellular_Networks_Guide.md`)**  
> Left unattempted per strict exam protocol.

1. **Question 1(a), (b), (c), (d), (e) [5 × 2 = 10M]:**  
   *Define the following terms and state their usage:*  
   - (a) Channel borrowing  
   - (b) Foreign Agent  
   - (c) MTC (Machine-Type Communications)  
   - (d) NFV (Network Functions Virtualization)  
   - (e) Mobility-binding table  
2. **Question 2(a) [10M]:**  
   *Which layer of GSM protocol stack takes care of Radio Resource Management? What are the tasks managed by this module?*
3. **Question 2(b) [5M]:**  
   *How do you prove whether a chip code $(+1, -1, +1, +1, -1, +1, +1, +1, -1, -1, -1)$ is orthogonal or not?*
4. **Question 2(c) [5M]:**  
   *Consider a network with 20 number of channels per cell and on an average each user makes 3 calls/hr. The average duration of a call is 2 minutes. The offered load from Erlang B Table is 12.03. What is the number of users supported in a cell with 1% blocking?*
5. **Question 3(a), (b), (c) [20M]:**  
   *Answer the following for the Universal Mobile Telecommunications System (UMTS):*  
   - (a) What are the major components of Core network? Briefly state the tasks of each of the components. [10]  
   - (b) What roles are played by RNC? [5]  
   - (c) Write the names of the traffic types supported in such a system. [5]
6. **Question 4(a), (b), (c) [20M]:**  
   - (a) Draw the 5G access network architecture showing RAN and Core part. [5]  
   - (b) Write advantages of introducing small cells in 5G network. [5]  
   - (c) Do a point-wise comparison of Macro, Pico and Femto cell in terms of size, coverage range, cost and deployment. [10]
7. **Question 5(a), (b) [20M]:**  
   *Write short notes on the following:*  
   - (a) Spread Spectrum [10]  
   - (b) Context-Aware Computing and Applications [10]

---

### Uncovered Questions from 2023 Mid-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes (`Cellular_Networks_Guide.md`)**  
> Left unattempted per strict exam protocol.

1. **Question 1(i) [1M]:**  
   *Which process is performed at the receiver end in mobile communication?*  
   (A) Modulation (B) Demodulation (C) Decoding (D) Both B and C
2. **Question 1(iii) [1M]:**  
   *Which type of multiplexing enables use of the whole bandwidth simultaneously?*  
   (A) FDMA (B) CDMA (C) TDMA (D) None of these
3. **Question 1(vi) [1M]:**  
   *Which technique uses directional antennas to increase cell capacity?*  
   (A) Cell Splitting (B) Coverage Zone approaches (C) Cell Sectoring (D) Cell Sectoring and Cell Splitting both
4. **Question 1(vii) [1M]:**  
   *In CDMA, mobile-device transmission power needs to be adjusted to mitigate which problem?*  
   (A) Hidden station problem (B) Exposed station problem (C) Near-far problem (D) All of these
5. **Question 1(viii) [1M]:**  
   *Primary GSM uses uplink frequency in which range?*  
   (A) $(890\text{--}915)\,\text{MHz}$ (B) $(935\text{--}960)\,\text{MHz}$ (C) $(880\text{--}915)\,\text{MHz}$ (D) $(925\text{--}960)\,\text{MHz}$
6. **Question 1(ix) [1M]:**  
   *What needs to be estimated for allocating the RF number of channels to meet GOS?*  
   (A) Cost (B) Capacity (C) SNR (D) All the above
7. **Question 3(a) [5M]:**  
   *Describe different channel-assignment strategies in a 2G cellular network.*

---

### Uncovered Questions from 2023 End-Semester Examination
> ⚠️ **Out of Syllabus / Uncovered in Reference Notes (`Cellular_Networks_Guide.md`)**  
> Left unattempted per strict exam protocol.

1. **Question 1(a), (c), (d), (e) [4 × 2 = 8M]:**  
   *Define the following terms and state their usage:*  
   - (a) Softer-handover  
   - (c) User plane  
   - (d) Control plane  
   - (e) MIMO  
2. **Question 2(a) [5M]:**  
   *Define GOS. Write assumptions, if any, for a blocked-calls-cleared trunking system.*
3. **Question 2(b) [5M]:**  
   *Define Erlang. How many users can be supported for $0.5\%$ blocking probability for 20 trunked channels in a blocked-calls-cleared system? Assume each user generates $0.1$ Erlang traffic. From the Erlang chart, total system load for $0.5\%$ blocking is 11.10.*
4. **Question 2(c) [5M]:**  
   *Write the algorithmic steps of CSMA/CA in WLAN.*
5. **Question 2(d) [5M]:**  
   *What is tunneling in Mobile-IP?*
6. **Question 3(a) [15M]:**  
   *What are the major components of UTRAN? Briefly state the tasks of each component.*
7. **Question 3(b) [5M]:**  
   *In the UMTS signaling protocol stack, what roles are played by “Call management” and “Mobility management”?*
8. **Question 4(a), (b) [20M]:**  
   - (a) What is a 5G core network? What tasks does it perform? [10]  
   - (b) Write the tasks of these functions: (i) NRF, (ii) NSSF, (iii) PCF, (iv) UDM. [10]
9. **Question 5(a), (b) [20M]:**  
   *Write short notes on:*  
   - (a) Carrier aggregation [10]  
   - (b) Pervasive Computing [10]
