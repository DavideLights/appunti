**previous lecture**: [[lez. 7]] — **next lecture**: [[lez. 10]] — **homeworks**: [[lez. 8 hm]] #gemini

# alive - leader election
how to know who is alive?

**leader election spec.** (`LeaderElection`, instance $le$, for crash-stop processes):
* **Events**:
	* Indication: $\langle le, \text{Leader} \mid p\rangle$ indicates that $p$ is elected as leader.
* **Properties**:
	* **LE1** (*Eventual detection*): Either there is no correct process, or some correct process is **EVENTUALLY** elected as the leader.
	* **LE2** (*Accuracy*): If a process is leader, then all previously elected leaders have crashed.

**stabilized**: when a unique leader is determined and does not change again.


![[Pasted image 20261111184934.png]]
* **Slide 43 (`POSSIBLE?` — Yes!)**: initially $p_0$ is elected by all; after $p_0$ crashes, $p_1$ detects the crash first and elects $\{p_1\}$, while $p_2$ has not yet detected $p_0$'s crash and still considers $\{p_0\}$ leader (valid: `LE1` only requires *eventual* detection, and `LE2` holds since $p_0$ has crashed). #gemini

![[Pasted image 20261111222412.png]]
* **Slide 45–46 (`POSSIBLE?` — No! $p_1$ is alive)**: here $p_1$ elects $\{p_1\}$, and later $p_2$ elects $\{p_2\}$ while $p_1$ is **still alive**. This violates **LE2 (Accuracy)**, which requires that if $p_2$ is elected leader, all previously elected leaders ($p_0$ *and* $p_1$) must have crashed. #gemini

# leader election alg. (`Monarchical Leader Election`)
**how it works**? we can do leader election just by electing a non-suspected process with highest rank (process ID), using a `PerfectFailureDetector` instance $\mathcal{P}$.

**upon event** $\langle le, \text{Init}\rangle$ **do**:
* $\text{suspected} := \emptyset$
* $\text{leader} := \bot$

**upon event** $\langle \mathcal P, \text{Crash} \mid p\rangle$ **do**:
* $\text{suspected} := \text{suspected} \cup \{ p \}$

**upon** $\text{leader} \neq \text{maxrank}(\Pi \setminus \text{suspected})$ **do**:
* $\text{leader} := \text{maxrank}(\Pi \setminus \text{suspected})$
* **trigger** $\langle le, \text{Leader} \mid \text{leader}\rangle$

**correctness**:
* **eventual detection (`LE1`)**: comes from the strong completeness of $\mathcal P$ (`PFD1`).
* **accuracy (`LE2`)**: from the strong accuracy of $\mathcal P$ (`PFD2`) and the fact that process IDs form a strict total order when ranking (`maxrank` only decreases as previous leaders crash).

# eventual leader election $\Omega$
**why**? we use it when the failure detector is not perfect (e.g., $\diamond \mathcal{P}$ in partial synchrony).

**Events**:
* **indication**: $\langle \Omega, \text{Trust} \mid p\rangle$: indicates that $p$ is trusted to be leader.

**Properties**:
* **ELD1** (*Eventual accuracy*): There is a time after which every correct process trusts some correct process.
* **ELD2** (*Eventual agreement*): There is a time after which no two correct processes trust different correct processes.

> **note**: $\Omega$ ensures that eventually all correct processes will elect the same correct process as their leader.


using $\Omega$ implies that (before stabilization):
* **arbitrary**: leaders can change in an arbitrary way and for an arbitrary period of time.
* **different leaders**: multiple leaders may be elected during the same period of time without having crashed.

![[Pasted image 20261111225410.png]]
* **Slide 52 (Study of Properties)**:
	* **Run 1**: after $p_2$ and $p_3$ crash, the remaining correct processes forever trust $p_3$ (which is crashed) $\implies$ **ELD2 (Eventual Agreement)** holds (they agree on $p_3$), but **ELD1 (Eventual Accuracy)** is violated ($p_3$ is not correct). #gemini
	* **Run 2**: after crashes, correct $p_1$ trusts $p_4$ while correct $p_4$ trusts $p_1$ (both $p_1, p_4$ are correct) $\implies$ **ELD1 (Eventual Accuracy)** holds, but **ELD2 (Eventual Agreement)** is violated (they trust different leaders). #gemini

* **Slide 53 (How to build $\Omega$ from $\diamond\mathcal{P}$)**: under crash-stop processes, $\Omega$ is obtained directly from $\diamond\mathcal{P}$ by applying a **deterministic rule** (`maxrank`) on the set of processes not suspected by $\diamond\mathcal{P}$ ($\Pi \setminus \text{suspected}$): each process trusts the highest-ID non-suspected process. #gemini

# eventual leader election $\Omega$ alg. (`Monarchical Eventual Leader Detection`)
**uses**: $\text{EventuallyPerfectFailureDetector}$, instance $\diamond \mathcal P$.

**upon event $\langle \Omega, \text{Init}\rangle$ do**:
1. $\text{suspected} := \emptyset$
2. $\text{leader} := \bot$

**upon event $\langle \diamond \mathcal P, \text{Suspect} \mid p\rangle$ do**:
1. $\text{suspected} := \text{suspected} \cup \{ p \}$

**upon event $\langle \diamond \mathcal P, \text{Restore} \mid p\rangle$ do**: #gemini
1. $\text{suspected} := \text{suspected} \setminus \{ p \}$

**upon $\text{leader} \neq \text{maxrank}(\Pi \setminus \text{suspected})$ do:**
1. $\text{leader} := \text{maxrank}(\Pi \setminus \text{suspected})$
2. **trigger** $\langle \Omega, \text{Trust} \mid \text{leader}\rangle$

# proof $\Omega$
**ELD1 Eventual Accuracy**: by strong completeness (`EPFD1`) and eventual strong accuracy (`EPFD2`) of $\diamond \mathcal P$, eventually $\text{suspected}$ contains all and only crashed processes, so $\Pi \setminus \text{suspected}$ contains only correct processes (or is empty). #gemini

**ELD2 Eventual Agreement**: for any pair of correct processes, by the stabilization lemma of $\diamond \mathcal P$, their $\text{suspected}$ sets eventually stabilize to the exact same content. 
* thus if $\Pi \setminus \text{suspected}$ is equal on both processes,
* then `maxrank` returns the exact same ID for the leader on both processes.

# crash failure models (three models) 
Three system models defined by combining crash-stop processes, perfect links, and failure detectors:
* **Fail-Stop**: crash failures with a **Perfect Failure Detector ($\mathcal{P}$)** + Perfect Links. 
	* Crashes are accurately and permanently detected without false suspicions ($\text{PFD1} \land \text{PFD2}$). 
	* Implementable in **synchronous** systems. 
* **Fail-Noisy**: crash failures with an **Eventually Perfect Failure Detector ($\diamond \mathcal{P}$)** + Perfect Links. 
	* Can make mistakes (false suspicions) during asynchronous periods, but eventually stabilizes ($\text{EPFD1} \land \text{EPFD2}$). 
	* Implementable in **eventually synchronous** systems.
* **Fail-Silent**: crash failures with **no failure detector** (or no accuracy guarantees) + Perfect Links. 
	* When a process crashes, it simply ceases communication silently without detection. 
	* Corresponds to **asynchronous** systems. 

* **Model strength**: $\text{Synchronous} \implies \text{Fail-Stop} \implies \text{Fail-Noisy} \implies \text{Fail-Silent}$ #gemini
	* Fail-Stop is **stronger** than Fail-Noisy (any Fail-Stop system is also Fail-Noisy and Fail-Silent)
	* which is **stronger** than Fail-Silent
* **Set of solvable problems**: 
  $$\text{Problems}(\text{Fail-Silent}) \subset \text{Problems}(\text{Fail-Noisy}) \subset \text{Problems}(\text{Fail-Stop}) \subset \text{Problems}(\text{Synchronous})$$
* **$\text{Synchronous}$ vs $\text{Fail-Stop}$ (Slides 59–62)**:
	* **Slide 59–60**: `SYNC` $\to$ `Fail-Stop` (`(B)`): a Synchronous system can implement `Fail-Stop` (Perfect Link + $\mathcal{P}$), whereas `Fail-Stop` cannot implement `SYNC` because $\mathcal{P}$ and Perfect Links hide real-time bounds. #gemini
	* **Slide 61–62**: $\text{Synchronous}$ is **strictly stronger** than $\text{Fail-Stop}$ ($\text{Problems}(\text{Fail-Stop}) \subsetneq \text{Problems}(\text{Synch})$). Slide 62 shows that **Clock Synchronization** (and **Timed Delivery**, Slide 79) lies inside `Synch` but *outside* `Fail-Stop`: these problems explicitly depend on real-time / physical bounds, whereas `Fail-Stop` only exposes asynchronous-style events (`Deliver`, `Crash`) with *eventual* guarantees. #gemini

![[Pasted image 20261112085408.png]]![[Pasted image 20261112085426.png]]


# applications of fd and le

> **note**: $\text{FD} = \text{Failure Detector}$, $\text{LE} = \text{Leader Election}$

## 1. Fault-tolerant Lamport Mutual Exclusion (using $\mathcal{P}$)
> **note**: $\mathcal P$ is a Perfect Failure Detector

**Events**:
* `Request`: From upper layer — Requests access to Critical Section (CS).
* `Grant`: To upper layer — Grants access to CS.
* `Release`: From upper layer — Releases the CS.

**Properties**:
* **Mutual Exclusion (Safety)**: At any time $t$, at most **one non-crashed process** is inside the CS.
* **Liveness**: If a correct process $p$ requests access, then it eventually enters the CS.
* **Fairness**: If a correct process $p$ requests access before ($\to$) a process $q$, then $q$ cannot access the CS before $p$.

![[Pasted image 20261112132136.png]]

### Algorithm 1 (The original ONE): Lamport’s ME Algorithm on process $p_i$ #gemini
> **Original Algorithm** — Messages are $\text{REQ}, \text{ACK}, \text{RLS}$ . There are 2 critical points in it.

**upon event** $\text{Init}$ **do**: 
1. $\text{Requests} = \text{Acks} = \emptyset$ 
2. $\text{scalar\_clock} = 0$ 
3. $\text{my\_req} = \bot$ 
4. $\Pi = \{p_0, p_1, \dots, p_{n-1}\}$ *(set of all processes)* 

> Request access to CS from upper layer 
**upon event** $\text{Request}$ **do**:
1. $\text{scalar\_clock} = \text{scalar\_clock} + 1$ 
2. $\text{my\_req} = (\text{REQ}, \text{ts} = \langle i, \text{scalar\_clock} \rangle)$ 
3. **for all** $p_j \in \Pi$ **do**: 
	* $\text{Send FIFOPERFECTLINK}(p_j, \text{my\_req})$ *(send REQ containing ID $i$ and ts to all $p \in \Pi$)* 

> Release CS from upper layer, *if i crash its possible that i'll never release.*

**upon event** $\text{Release}$ **do**: 
1. $\text{Requests} = \text{Requests} \setminus \{\text{my\_req}\}$ 
2. $\text{scalar\_clock} = \text{scalar\_clock} + 1$ 
3. **for all** $p_j \in \Pi$ **do**: 
	* $\text{Send FIFOPERFECTLINK}(p_j, (\text{RLS}, \text{ts} = \langle i, \text{scalar\_clock} \rangle))$ 

> $\text{ts}(x) < \text{ts}(y)$ when $\text{scalar\_clock}(x) < \text{scalar\_clock}(y)$, or $\text{scalar\_clock}(x) = \text{scalar\_clock}(y) \land \text{id}(x) < \text{id}(y)$ 

> If other process crashes, they'll never send me an ack, so i cannot access.
**upon event** $\nexists \text{req} \in \text{Requests} : \text{ts}(\text{req}) < \text{ts}(\text{my\_req}) \land \forall p \in \Pi : \exists m \in \text{Acks} \mid \text{ts}(m) > \text{ts}(\text{my\_req})$ **do**: 
1. **trigger event** $\text{Granted}$
2. **note**: this follows the same logic as other algorithms

**upon event** $\text{Deliver Message}(m)$ **do**: 
1. $\text{scalar\_clock} = \max(\text{clock}(m), \text{scalar\_clock}) + 1$ 
	1. **note**: as always, apply the rule to update correctly the clock.
2. **if** $m$ is a $\text{REQ}$ **then**: 
	* $\text{Requests} = \text{Requests} \cup \{ m \}$ 
	* $\text{scalar\_clock} = \text{scalar\_clock} + 1$ 
	* $\text{Send FIFOPERFECTLINK}(\text{sender}(m), (\text{ACK}, \text{ts} = \langle i, \text{scalar\_clock} \rangle))$
3. **else if** $m$ is an $\text{ACK}$ **then**: 
	* $\text{Acks} = \text{Acks} \cup \{ m \}$ 
4. **else if** $m$ is a $\text{RLS} \land \exists \text{req} \in \text{Requests} : \text{sender}(\text{req}) = \text{sender}(m)$ **then**: 
	* $\text{Requests} = \text{Requests} \setminus \{ \text{req} \}$ 

> [!error] Critical Points of the algorithm (Slide 66)
> 1. If a process crashes while in CS (or with a pending `REQ`), it **cannot send `RLS`** $\implies$ its request remains in everyone's $\text{Requests}$ forever.
> 2. If a process crashes, it **cannot send `ACK`** $\implies$ other processes waiting for its `ACK` block forever.

# patching the algorithm (First Attempt — Incorrect, Slide 67–68)

**upon event** $\text{Init}$ **do**: 
1. $\text{Requests} = \text{Acks} = \emptyset$ 
2. $\text{scalar\_clock} = 0$ 
3. $\text{my\_req} = \bot$ 
4. $\Pi = \{p_0, p_1, \dots, p_{n-1}\}$ *(set of all processes)* 
5. $\text{Crashed} = \emptyset$

**upon event** $\text{Crash}(\text{process } p_{j})$ **do**:
1. $\text{Crashed} = \text{Crashed} \cup \{ p_{j} \}$
2. **for all** $\text{req} \in \text{Requests}$ s.t. $p_{j}$ is the sender of $\text{req}$ **do**:
	1. remove $\text{req}$ from $\text{Requests}$

**upon event** $\nexists \text{req} \in \text{Requests}: \text{ts}(\text{req}) < \text{ts}(\text{my\_req}) \land \forall p \in (\Pi \setminus \text{Crashed}) : \exists m \in \text{Acks}\mid \text{ts}(m)>\text{ts}(\text{my\_req})$ **do**:
1. **trigger event** $\text{Granted}$


# patching (again) the algorithm (Correct Patch — Slide 70–71)
**scenario**: what if you receive an old in-flight `REQ` from $p_{j}$ *after* $\mathcal{P}$ already triggered $\text{Crash}(p_j)$? (Because $\mathcal{P}$ and the `FIFOPerfectLink` are independent modules, `Crash` can be notified before the last `REQ` of $p_j$ is delivered!). #gemini
![[Pasted image 20261112152537.png]]
1. increment scalar clock
2. send `ACK`
3. **store the request locally** in $\text{Requests}$
4. since $\text{Crash}(p_j)$ already fired and will never fire again, this zombie `REQ` is never removed $\implies$ **no process with a higher timestamp will ever be able to enter the CS!**

**upon event** $\text{Init}$ **do**:
1. $\text{Requests} = \text{Acks} = \emptyset$
2. $\text{scalar\_clock}=0$
3. $\text{my\_req} = \bot$
4. $\Pi = \{ p_{0},p_{1},\dots,p_{n-1} \}$
5. $\text{Crashed} = \emptyset$

**upon event** $\text{Crash}(\text{process } p_{j})$ **do**:
1. $\text{Crashed} = \text{Crashed} \cup \{ p_{j} \}$
2. **for all** $\text{req} \in \text{Requests}$ s.t. $p_{j}$ is the sender of $\text{req}$ **do**:
	1. remove $\text{req}$ from $\text{Requests}$

**upon event** $\nexists \text{req} \in \text{Requests}: \text{ts}(\text{req}) < \text{ts}(\text{my\_req}) \land \forall p \in (\Pi \setminus \text{Crashed}): \exists m \in \text{Acks}\mid \text{ts}(m)>\text{ts}(\text{my\_req})$ **do**:
1. **trigger event** $\text{Granted}$

**upon event** $\text{Deliver Message}(m)$ **do**: 
1. **if** $m$ is a $\text{REQ}$ **and** $\text{sender}(m) \notin \text{Crashed}$ **then**: #gemini
	* $\text{scalar\_clock} = \max(\text{clock}(m), \text{scalar\_clock}) + 1$ #gemini
	* $\text{Requests} = \text{Requests} \cup \{ m \}$ 
	* $\text{scalar\_clock} = \text{scalar\_clock} + 1$ 
	* $\text{Send FIFOPERFECTLINK}(\text{sender}(m), (\text{ACK}, \text{ts} = \langle i, \text{scalar\_clock} \rangle))$
2. **else if** $m$ is an $\text{ACK}$ **then** ...

## 2. Mutual exclusion using FD ($\mathcal{P}$) and LE (Slides 72–76)
![[Pasted image 20261112153949.png]]

**ideas**:
* **election**: use `LE` to elect a coordinator (leader).
* **requests**: processes send a `Request` message to the current leader to enter the CS, and a `Release` message when done.
* **leader**: grants access to the CS in **FIFO order** on received requests.
* **crash detection**: when the leader detects $\langle \mathcal{P}, \text{Crash} \mid p\rangle$:
	* if $p$ is **not in CS**, the leader removes $p$'s pending request (if any) from its queue;
	* if $p$ **is in CS**, the leader acts as if $p$ released the CS (grants CS to the next waiting process).
* **problem**: what to do when the leader crashes and a **new leader is elected**? How to transfer the old leader's knowledge?
	* only the old leader knew who was currently in the CS (if that process also crashed, it is fine; if it is alive, it will answer a query).
	* **solution (`new_leader` phase)**: the newly elected leader first runs a `new_leader` phase where it **interrogates all non-faulty processes** ($\Pi \setminus \text{Crashed}$) to check if any alive process is currently inside the CS, and updates its state accordingly (waiting for that process to release or crash before granting new requests). #gemini
	* **retransmit**: when a new leader is elected, processes **retransmit their unsatisfied pending requests** to the new leader; after the `new_leader` phase completes, the new leader serves requests normally. #gemini
