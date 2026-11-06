**D1**: how frequently must two $\rho$-correct clocks be resynchronized to keep their skew strictly below $\Delta$? (worst-case rates, $\Delta / 2\rho$) #gemini
* **R1**: in the worst case one clock runs at $1+\rho$ and the other at $1-\rho$, diverging at rate $2\rho\tau$; to keep $\text{Skew}_{1,2}(\tau) < \Delta$, the resynchronization period must be strictly shorter than $\tau = \frac{\Delta}{2\rho}$. #gemini
**D2**: why is moving a fast clock backward dangerous, and how does slewing preserve monotonicity? ($t' > t \implies C_i(t') > C_i(t)$, hiding interrupts) #gemini
* **R2**: setting a clock backward can assign a newer event a smaller timestamp than an older event on the same process (reversing causal order); **slewing** preserves monotonicity by slowing the clock rate (hiding hardware timer interrupts) until real time catches up. #gemini
**D3**: what is the difference between External and Internal synchronization, and why does External sync within $D$ imply Internal sync within $2D$? (UTC reference $S$, accuracy vs agreement, triangle inequality) #gemini
* **R3**: External sync bounds accuracy w.r.t. UTC ($|C_i(t)-S(t)| < D$), whereas Internal sync bounds agreement between pairs ($|C_i(t)-C_j(t)| < D$). By the triangle inequality, $|C_i(t)-C_j(t)| \le |C_i(t)-S(t)| + |S(t)-C_j(t)| < 2D$ (one clock $+D$ ahead, the other $-D$ behind $S$). #gemini
**D4**: how does Cristian's algorithm estimate the time, what is its core assumption, and what is its worst-case error bound? ($\hat{C}_p = t_s + \frac{RTT}{2}$, symmetry, $\pm(\frac{RTT}{2}-d_{\min})$) #gemini
* **R4**: the client sets $\hat{C}_p = t_s + \frac{RTT}{2}$ assuming **symmetric one-way delays** ($d_{\text{out}} \approx d_{\text{back}}$); the estimation error is $\frac{|d_{\text{out}}-d_{\text{back}}|}{2}$, and if minimum one-way delay $d_{\min}$ is known, $d_{\min} \le d_{\text{back}} \le RTT - d_{\min}$ gives max error $\le \frac{RTT}{2} - d_{\min}$. #gemini
**D5**: how does Berkeley's algorithm achieve internal synchronization, and why does having one UTC-synced node in the group not guarantee external sync? (master polling, outlier filtering, $\text{Adj}_i = \bar{\Delta}-\Delta_i$) #gemini
* **R5**: a master polls all clocks, estimates offsets $\Delta_i$, excludes outliers exceeding threshold $\gamma$ (or max $RTT$), computes the average $\bar{\Delta}$, and sends corrections $\text{Adj}_i = \bar{\Delta}-\Delta_i$; a single UTC-synced node might be discarded as an outlier or pulled away from UTC by the group average. #gemini
**D6**: how is NTP organized, and what is the difference between a Wall Clock and a Monotonic Clock? (strata hierarchy, UTC vs elapsed time) #gemini
* **R6**: NTP uses a hierarchy of **strata** (Stratum 0: atomic/GPS references; Stratum 1: primary servers; Stratum 2+: secondary servers) for scalability and redundancy. A **Wall clock** tracks UTC via NTP and can jump backward; a **Monotonic clock** measures elapsed time and never moves backward, but is not a UTC timestamp. #gemini
**D7**: what is the difference between Global Skew and Local Skew in arbitrary graphs? (all pairs vs neighbors, tree-like vs fully distributed) #gemini
* **R7**: **Global skew** is the max skew between *any two nodes* in $G$, while **Local skew** is the max skew between *adjacent neighbors* in $G$; tree-like sync bounds global skew w.r.t. the root but can leave high local skew between adjacent branches, whereas fully distributed averaging smooths local skew between neighbors. #gemini
**D8**: when can physical timestamps with error bound $\mathcal{E}$ safely establish the order of two events $e_1, e_2$? (uncertainty intervals $[c-\mathcal{E}, c+\mathcal{E}]$) #gemini
* **R8**: only when their uncertainty intervals do not overlap, i.e., $c_1 + \mathcal{E} < c_2 - \mathcal{E}$ (or $|c_2 - c_1| > 2\mathcal{E}$); if they overlap (common in fast systems generating many events per ms), physical timestamps cannot determine the true causal order. #gemini

# bounding clock skew & monotonicity 

How frequently must two clocks be **resynchronized** to keep their skew below a chosen tolerance?
* Let $\Delta>0$ be the maximum skew we can accept.
* Imagine a *perfect synchronization primitive* s.t.: $|C_{1}(0) - C_{2}(0)|=0$, this means that $p_{1}$ and $p_{2}$ agree perfectly at $t_{0}=0$ for example.

**Worst case skew**:
* clock 1 runs at maximum rate $1+\rho$
	* $\Delta C_{1}=(1+\rho)\tau$
* clock 2 runs at minimum rate $1-\rho$
	* $\Delta C_{2} = (1-\rho)\tau$

Since they started with the same reading $C_1(0) = C_2(0)$ at $t=0$, after $\tau$ real-time units the Skew is: #gemini
$$
\text{Skew}_{1,2}(\tau) \leq (1+\rho)\tau - (1-\rho)\tau = 2 \rho \tau
$$
* we want to bound $\text{Skew}_{1,2}(\tau) < \Delta$
* we can find the critical value for the Skew, fixed $\rho$:
* $\tau = \frac{\Delta}{2\rho}$
	* just solved $2\rho \tau = \Delta$

To prevent the worst case we need to have a resynchronization period strictly shorter than $\frac{\Delta}{2\rho}$:
* **strictly shorter** ($\tau < \frac{\Delta}{2\rho}$): at $\tau = \frac{\Delta}{2\rho}$ the worst-case skew equals $\Delta$; to guarantee $\text{Skew}_{1,2}(t) < \Delta$ (strict inequality), we must resynchronize *before* $\tau$ reaches $\frac{\Delta}{2\rho}$. #gemini

**moving backward**:
* we have clock 1 at 12:00
* we have clock 2 at 11:00 #gemini
* it's **dangerous** to move the faster clock (clock 1) backwards to 11:00
* **why dangerous?** if $p_1$ timestamps $m_1$ at 12:00, moves its clock back to 11:00, and timestamps $m_2$ at 11:00, an observer comparing timestamps could reverse the order of events coming from the same process. #gemini

**wall-clock**: software clock that measures the **real-world time of day** (calendar/UTC time, like a physical clock on the wall); it can jump forward or backward when synchronized with external time sources. #gemini

**monotonicity**: is the main requirement for a software clock:
$$
t' > t \implies C_{i}(t') > C_{i}(t)
$$
* An application that needs this guarantee should not blindly use a wall-clock reading that can be corrected backward: OS wall-clocks (e.g., `CLOCK_REALTIME`) can jump backward when adjusted by NTP; to guarantee monotonicity, the application must use a dedicated **monotonic clock** (`CLOCK_MONOTONIC`). #gemini

**slewing**: the clock continues to work without jumping backward, by gradually changing its rate $\alpha$:
* if the clock is **ahead** we slow the clock rate until synchronization (implemented in hardware/OS by **hiding timer interrupts**: skipping $\frac{\text{slowdown time}}{\text{interrupt period}}$ interrupts so the local clock is not updated) #gemini
* if the clock is **behind** we speed up the clock rate (or advance it).

# UTC

**what does it mean to synchronize clocks?**
* use a reference outside our system (**external synchronization**)
* keep a process clock close to another process's (**internal synchronization**)

**Coordinated Universal Time (UTC)**: 
* international standard time reference
* based on **International Atomic Time (TAI)**: $1\text{ s}$ is the time a Cesium-133 atom needs for $9{,}192{,}631{,}770$ state transitions (atomic oscillators have drift rate $\sim 10^{-13}$). Broadcast via shortwave radio ($\sim 1\text{ ms}$ accuracy) or GPS satellites ($\sim 1\ \mu\text{s}$ accuracy). #gemini
* UTC has to remain aligned with **astronomical time** 

**astronomical time**: #gemini
* solar time based on Earth's rotation, which gradually slows down;
* UTC occasionally inserts *leap seconds* to keep atomic time aligned with day/night cycles —
* UTC is simply treated as the authoritative external reference $S(t)$. 

**How to use UTC as a reference**? Directly via a UTC receiver (GPS/radio) or indirectly using time servers / synchronization services.

**external synch**: a system is externally synchronized with:
* $C_{i}$: the local clock for process $p_{i}$
* $S$: the external reference, e.g., UTC-synchronized server
* $D$: the accuracy bound

iff for all $i$ and $t \in I$:
$$
|C_{i}(t)-S(t)|<D
$$
> **Note**: tolerance $D$ might not be the same as $\Delta$

**internal sync**: based on an agreement within a group of clocks:
$$
\forall i,j \;\;\;
|C_{i}(t) - C_{j}(t)| <D
$$
* use case: isolated network with no access to UTC
* **consequence**: processes' clocks may agree with each other while drifting collectively (e.g., all being one hour wrong with respect to UTC).

**internal sync bound and external sync bound**:
* suppose two clocks are **externally synched** to $S$ with bound $D$
* worst case: 
	* **clock 1**: $D$ units ahead of the reference
	* **clock 2**: $D$ units behind the reference
* external synchronization with bound $D$ $\implies$ internal synchronization within $2D$ (the converse does **not** hold).

**using triangle inequality**:
$$
\begin{aligned}
|C_i(t)-C_j(t)|
&\leq |C_i(t)-S(t)|+|S(t)-C_j(t)|\\
&<D+D=2D.
\end{aligned}
$$

* **accuracy**: bounded difference with UTC ($|S(t)-C_i(t)| < D$, external sync)
* **agreement**: bounded difference between processes ($|C_i(t)-C_j(t)| < D$, internal sync)


## Cristian's Algorithm
**scenario**: Request-driven **external synchronization** where client $p$ wants to sync with time server $S$ following UTC (works probabilistically in async systems if $RTT$ is small w.r.t. required accuracy). #gemini
* client asks the time by sending request $m_r$
* server replies with message $m_t$ containing its current timestamp $t_{s}$
* **trivial mistake**: setting $C_p = t_s$ directly, because when client receives $t_{s}$ it's already an old value (time $d_{\text{back}}$ has passed while $m_t$ traveled back).

**solution**:
$$
\hat{C}_{p} = t_{s} + \frac{RTT}{2}
$$
> **RTT**: round-trip time ($T_{\text{round}}$) measured locally by $p$ from sending $m_r$ to receiving $m_t$.

**Cristian's algorithm assumption**: the delay between $p$ and $S$ is **symmetric** ($d_{\text{out}} \approx d_{\text{back}}$; it does *not* require a tiny delay if both directions are symmetric). #gemini

Let the request delay be $d_{\text{out}}$, the return delay be $d_{\text{back}}$, and server processing time be negligible:
* $\text{RTT}= d_{\text{out}} + d_{\text{back}}$
* when $p$ receives the reply, the **actual server time** is $t_{s}+d_{\text{back}}$ #gemini
* Cristian's algorithm sets $\hat{C}_p = t_{s} + \frac{RTT}{2}$
* **estimating the error**: $\left|\frac{RTT}{2} - d_{\text{back}}\right|= \frac{|d_{\text{out}}-d_{\text{back}}|}{2}$
	* if $RTT$ is symmetric ($d_{\text{out}} = d_{\text{back}}$), then $\frac{RTT}{2}- d_{\text{back}} = 0$
	* else the error grows proportionally to the **asymmetry** $|d_{\text{out}} - d_{\text{back}}|$ between outward and return delays. #gemini

**worst-case bound**:
$$
d_{\min} \leq d_{\text{back}} \leq RTT-d_{\min}
$$
**what is $d_{\min}$ ($\min$ in slides)?** 
* The **known minimum one-way transmission delay** between $p$ and $S$ (physical/network lower bound when there is zero queuing delay). 
* Since $d_{\text{out}} \ge d_{\min}$ and $d_{\text{back}} \ge d_{\min}$,
* $d_{\text{back}}$ cannot be smaller than $d_{\min}$ or larger than $RTT - d_{\min}$. #gemini

$$
\text{max absolute error} \leq \frac{RTT}{2}- d_{\min} \quad \left(\text{accuracy is } \pm\left(\frac{RTT}{2} - d_{\min}\right)\right)
$$
* **Case 1** ($d_{\text{back}}$ is max, $d_{\text{back}} = RTT - d_{\min}$): $\Delta = \frac{RTT}{2} - (RTT - d_{\min}) = -\left(\frac{RTT}{2} - d_{\min}\right)$ #gemini
* **Case 2** ($d_{\text{back}}$ is min, $d_{\text{back}} = d_{\min}$): $\Delta = \frac{RTT}{2} - d_{\min} = +\left(\frac{RTT}{2} - d_{\min}\right)$ #gemini
* Therefore the maximum absolute estimation error is always bounded by $\frac{RTT}{2}- d_{\min}$.

**what if the time server crashes or is malicious**? 
* Single server is a **single point of failure** $\implies$ Cristian suggests polling a **cluster of synchronized time servers** (synchronization group) for redundancy, plus **authentication** against faulty/malicious servers. #gemini

## Berkeley's Algorithm
* **internal synch** algorithm (master-slave broadcast/polling, Gusella & Zatti 1989)
* **master ($p_m$)**: 
	1. periodically polls all processes (sending $t_1$, receiving reply $t_2$ at local time $t_3$)
	2. discards readings with $RTT = t_3 - t_1 > RTT_{\max}$) #gemini
	3. estimates how much each clock is ahead or behind the master ($\Delta_i$, accounting for $RTT/2$)
* **accuracy**: the master might not be the most accurate clock
* **average of accepted differences**: instead of forcing everyone to adopt the master's clock (which may drift), averaging all valid offsets pulls the group toward a **shared consensus time** ($\text{master} + \bar{\Delta}$), canceling out individual drifts. #gemini

> **Note**: the master is essentially the one to decide who is in the mean and who is not.

**offsets**:
* master has $\Delta_{m} =0$
* discard **abnormal (faulty)** measurements from processes where $|\Delta_i| > \gamma$ (**threshold**) or $RTT > RTT_{\max}$ #gemini
* computes the mean $\bar{\Delta}$ of **accepted** offsets
* **individual correction**: $\text{Adj}_{i} = \bar{\Delta}-\Delta_{i}$ sent and applied individually to every process 
	* including outliers; 
	* negative adjustments are applied via **slewing** / slowing down the clock). #gemini

**example**:

| Process | Clock reading | Offset from master ($\Delta_i$) | $\text{Adj}_{i} = \bar{\Delta} - \Delta_i$ |
| ------- | ------------- | ------------------------------- | ------------------------------------------ |
| Master  | 03:05         | $0$ min                         | $-5 - 0 = -5$ min                          |
| $p_1$   | 02:55         | $-10$ min                       | $-5 - (-10) = +5$ min                      |
| $p_2$   | 03:00         | $-5$ min                        | $-5 - (-5) = 0$ min                        |
| $p_3$   | 03:25         | $+20$ min                       | $-5 - 20 = -25$ min                        |
* master marks $p_{3}$ as an outlier (excluded from $\bar{\Delta}$, but still receives its adjustment $\text{Adj}_3 = -25\text{ min}$ so all clocks converge to **03:00**): #gemini
$$
\bar{\Delta}=\frac{0-10-5}{3}=-5 \text{ min}
$$

**fault tolerance**:
* slave does not answer (or $RTT > RTT_{\max}$): master proceeds without it.
* slave has a **wildly different value** ($|\Delta_i| > \gamma$): master excludes it from the average (tolerates faulty/erroneous slave readings).
* **faulty master**: if the master crashes, we have to **elect another master** (leader election, takes unknown time).
	* we do not cover a Byzantine master sending malicious adjustments.

**external synch inside Berkeley group**:
* having one externally (UTC) synched participant in a Berkeley group **does not guarantee** bounded external synch for everyone for two reasons:
	1. **exclusion**: it might be treated as an outlier and excluded from the average
	2. **mean**: even if included, the group average $\bar{\Delta}$ is pulled by the other nodes' offsets away from UTC.


## NTP (Network Time Protocol)
Used on large networks (Internet) to synchronize clients with UTC.

**strata**: hierarchical levels (synchronization subnet) used to organize the algorithm:
0. **stratum 0 (time-reference devices)**: atomic clocks, GPS/radio receivers.
1. **stratum 1 (primary servers)**: directly connected to stratum 0 reference devices.
2. **stratum 2+ (secondary servers)**: synchronize with stratum 1, stratum 3 with stratum 2 (down to user machines at the lowest level; servers can dynamically change stratum depending on path quality). #gemini

**why strata?**
* distribute time-reference devices across multiple servers instead of forcing everyone to contact a single central source
* **scalability**: spreads client requests across the hierarchy
* **redundancy / reliability**: servers query multiple time sources and paths to filter out network jitter and faulty peers. #gemini

> [!note] Diff between Wall clock and Monotonic clock #gemini
> * **Wall clock** (e.g., `CLOCK_REALTIME`): represents the actual time of day (synchronized with UTC via NTP). 
> 	* **can jump backward** 
> * **Monotonic clock** (e.g., `CLOCK_MONOTONIC`): measures **elapsed time** from an arbitrary reference point. 
> 	* It is guaranteed to **never move backward** ($t' > t \implies C(t') > C(t)$. #gemini

## Synchronization in Arbitrary Graphs (Global vs Local Skew) #gemini
When nodes are connected over an arbitrary communication graph $G = (V, E)$ rather than a single complete graph: #gemini
* **Global skew**: maximum skew between **any two nodes** in $G$: $\max_{u,v \in V} |C_u(t) - C_v(t)|$. #gemini
* **Local skew**: maximum skew between **neighboring (adjacent) nodes** in $G$: $\max_{(u,v) \in E} |C_u(t) - C_v(t)|$. #gemini
* **Two synchronization approaches**: #gemini
	1. **Tree-like** (a root server imposes its clock down a spanning tree): keeps **global skew** bounded w.r.t. the root, but adjacent nodes belonging to different branches can accumulate high **local skew** (e.g., in the slide graph with global skew $|5-1|=4$, two neighbors have readings $1$ and $4$, giving local skew $3$ or $2$). #gemini
	2. **Fully distributed** (every node periodically averages/adjusts its clock based on its **neighbors**): minimizes **local skew** between adjacent nodes, though global skew across distant ends of the graph shrinks more slowly. #gemini

## when we can establish order using timestamps?

**estimate**: a synchronized software clock is only an estimate of real time within an error bound $\mathcal E$.
* let $e$ be an event occurring with timestamp $c$
* then the true event time $t(e)$ lies in the uncertainty interval $[c-\mathcal E,\; c+\mathcal E]$

To be sure that two uncertainty intervals **do not overlap**:
* with $c_{1}<c_{2}$
* and the same error bound $\mathcal E$ on the two events

the sufficient condition is:
$$
c_{1} + \mathcal E < c_{2} - \mathcal E \quad \Longleftrightarrow \quad c_2 - c_1 > 2\mathcal E
$$
* If the intervals **overlap** ($c_1 + \mathcal E \ge c_2 - \mathcal E$), timestamps alone **cannot** establish the true order: $e_1$ may have $c_1 < c_2$ even though $e_1$ actually occurred after $e_2$. #gemini
* **fast systems**: if events are created very frequently (e.g., many events per millisecond), millisecond-accurate physical clocks will have overlapping uncertainty intervals and **cannot** safely distinguish the true order $\implies$ we need **logical clocks** (Lamport / Vector clocks). #gemini

### summary: clock synchronization algorithms #gemini

| Algorithm | Goal | Architecture | Time Estimate / Correction | Accuracy / Error Bound | Fault Tolerance & Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cristian** | **External** ($\text{UTC}$) | Client–Server (request-driven) | $\hat{C}_p = t_s + \frac{RTT}{2}$ | $\pm\left(\frac{RTT}{2} - d_{\min}\right)$ (relies on **symmetric** delay) | Single server is SPOF; use server cluster + auth |
| **Berkeley** | **Internal** (agreement) | Master–Slave (polling/broadcast) | $\text{Adj}_i = \bar{\Delta} - \Delta_i$ (filters outliers $> \gamma$) | Depends on $RTT_{\max}$ | Master crash $\implies$ leader election; ignores faulty slave offsets |
| **NTP** | **External** ($\text{UTC}$) | Hierarchical **Strata** ($0, 1, 2, \dots$) | Cristian-like over synchronization subnet | Milliseconds (LAN/Internet) | High scalability & redundancy; wall-clock may jump back |