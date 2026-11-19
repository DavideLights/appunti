**learners** (Slide 34): #gemini
* Whenever an acceptor accepts a proposal, it sends `(ACCEPT, n, v)` (or $\langle\text{LEARN}, n, v\rangle$) to all learners. #gemini
* A learner that receives `(ACCEPT, n, v)` for the **same round $n$ and value $v$** from a majority of acceptors **decides $v$**, and sends `(DECIDE, v)` to all other learners. #gemini
* Learners that receive `(DECIDE, v)` also **decide $v$**. #gemini

**note**: everyone is also a learner, because they have to know if a value for the consensus has been decided.

**every physical node typically runs** (Slide 35): acceptor, learner and proposer agents/threads on the same physical process. #gemini

**why paxos works even if messages are lost**? because it works in an asynchronous/eventually-synchronous model where lost messages are indistinguishable from messages with arbitrary/infinite delay (proposers simply use timeouts and start a new round). #gemini

> **note**: actually the goal for single-decree Paxos is to reach consensus on a single value, and after that we cannot no more change the value (in practice, **Multi-Paxos** chains multiple instances to agree on a sequence/log of values — Slide 53). #gemini

why we cannot wait for round $i$ instead of accepting rounds with $j>i$?
* because the proposer who issued round $i$ might have crashed; to avoid remaining stuck forever, acceptors must be able to move on to higher rounds $j > i$. #gemini

### Example: Chosen vs. Decided (Slides 34 & 36) #gemini
* **Slide 34**: $p_2$ runs `Prepare(num=2)` and gets promises from $\{a_1, a_2\}$ (majority of 3). In Phase 2, $p_2$ sends `<n=2, v=0>`.
	* **Chosen**: at the exact instant the **second acceptor** ($a_2$) accepts `<n=2, v=0>` (since $\{a_1, a_2\}$ is a majority of acceptors for the same round $2$). #gemini
	* **Decided**: later, when a **learner** receives the two `(ACCEPT, 2, 0)` messages from $a_1$ and $a_2$, realizes a majority was reached in round $2$, and triggers `Decide(0)`. #gemini
* **Slide 36 (Competing Proposers)**:
	* $p_2$ (`Prepare(2)`) gets promises from $\{a_1, a_2\}$, sends `<n=2, v=2>`, which is accepted **only by $a_1$** because $a_2$ already promised `num >= 3` to $p_3$ $\implies v=2$ is **not chosen** (no majority). #gemini
	* $p_3$ (`Prepare(3)`) gets promises from $\{a_2, a_3\}$, sends `<n=3, v=5>`, accepted only by $a_2$ before $p_4$ preempts with `Prepare(4)` $\implies v=5$ is **not chosen yet** in round $3$, but $p_4$ sees `<n=3, v=5>` from $a_2$, is forced to adopt $v=5$, and gets `<n=4, v=5>` accepted by $\{a_2, a_3\}$ $\implies v=5$ is **chosen** in round $4$! #gemini


# algorithm
*(Ref: Slides 38–40, from "A Simpler Proof for Paxos and Fast Paxos" by Marzullo, Mei, Meling)* #gemini

**Variables & State**: #gemini
* **Constants**: $A$ = set of acceptors ($n = |A|$, fault threshold $f = \lfloor(n-1)/2\rfloor$, quorum size $n - f = \lfloor n/2 \rfloor + 1$); $L$ = set of learners. #gemini
* **Proposer $p$**: #gemini
	* `crnd` (init $-1$): current round number chosen by $p$ (via `pickNextRound(crnd)`). #gemini
	* `cval`: value currently being proposed by $p$ in round `crnd`. #gemini
	* `P` (init $\emptyset$): set of pairs `(vrnd, vval)` collected from acceptors' `PROMISE` messages in the current round. #gemini
* **Acceptor $a$**: #gemini
	* `rnd` (init $-1$): highest round number $a$ has ever seen/promised (rejects any message with round $< \text{rnd}$). #gemini
	* `vrnd` (init $-1$): highest round number in which $a$ has **voted** (accepted a value). #gemini
	* `vval` (init $-1$ / $\bot$): value that $a$ voted for in round `vrnd`. #gemini
* **Learner $l$**: #gemini
	* `V` (init $\emptyset$): multiset of pairs `(i, v)` received in `LEARN` messages from acceptors. #gemini

**Algorithm 1 — Paxos Proposer $p$**: #gemini
```text
Constants: A, n = |A|, f = floor((n - 1) / 2)
Init:
    crnd <- -1                                      // Current round number

on <PROPOSE, val> do
    crnd <- pickNextRound(crnd)
    cval <- val
    P <- ∅
    send <PREPARE, crnd> to A

on <PROMISE, rnd, vrnd, vval> with rnd = crnd from acceptor a do
    P <- P ∪ {(vrnd, vval)}

on event |P| >= n - f do
    j <- max{vrnd : (vrnd, vval) ∈ P}
    if j >= 0 then
        V <- {vval : (j, vval) ∈ P}
        cval <- pick(V)                             // Pick proposed value vval with largest vrnd
    send <ACCEPT, crnd, cval> to A
```

**Algorithm 2 — Paxos Acceptor $a$**: #gemini
```text
Constants: L                                        // Set of learners
Init:
    rnd <- -1; vrnd <- -1; vval <- -1

on <PREPARE, prnd> with prnd > rnd from proposer p do
    rnd <- prnd
    send <PROMISE, rnd, vrnd, vval> to proposer p

on <ACCEPT, i, v> with i >= rnd from proposer p do
    rnd <- i
    vrnd <- i
    vval <- v
    send <LEARN, i, v> to L
```

**Algorithm 3 — Paxos Learner $l$**: #gemini
```text
Init:
    V <- ∅

on <LEARN, (i, v)> from acceptor a do
    V <- V ⊎ {(i, v)}                               // Multiset union

on event ∃i, v : |{(i, v) : (i, v) ∈ V}| >= n - f do
    v is chosen (decide v)
```

i'll promise you that we will sbor

# proof
*(Ref: Slides 41–50)* #gemini

To prove **Safety**, we need three properties (Slide 41): #gemini
1. **CS1 (Validity)**: Only a value proposed can be chosen (trivial: acceptors only vote for values proposed by proposers). #gemini
2. **CS2 (Agreement)**: A single value is chosen. #gemini
3. **CS3 (Integrity)**: Only a chosen value is learned by learners (trivial: a learner needs $n - f$ `LEARN` messages for the same `(i, v)`, which is the exact definition of `(i, v)` being chosen). #gemini

> [!warning] Safety Proof (CS2 by Induction) & Slide 49 Exercise — Study Actively #gemini
> Study the inductive proof of the core safety claim (Slides 42–46) and solve the Slide 49 question on your own. #gemini

* **Core Safety Claim (Theorem 1 — Slide 42)**: *If acceptor $a$ has voted for value $v$ at round $i$, then no value $v' \neq v$ can be chosen in any previous round $r < i$.* #gemini
	* **Why does this imply CS2 ("A single value is chosen")?** (Hint: can two different values be chosen in the *same* round $i$?) * [INSERT HERE] #gemini
	* **Proof by strong induction on round $i$ (Slides 43–46)**: Let $Q$ ($|Q| \ge n - f$) be the quorum of acceptors that sent `PROMISE` for round $i$, and let $\langle r=j, v \rangle$ be the vote with the highest round seen in $Q$ ($j < i$).
		* **Base case ($i = 0$)**: * [INSERT HERE] #gemini
		* **Inductive step — Case 1 (rounds between $j+1$ and $i-1$, Slide 45)**: Why can *no* value be chosen in any round $r \in [j+1, i-1]$? * [INSERT HERE] #gemini
		* **Inductive step — Case 2 (rounds between $0$ and $j$, Slide 46)**: Using the inductive hypothesis on round $j$, why can no value $v' \neq v$ be chosen in $r \in [0, j]$? * [INSERT HERE] #gemini

* **What is missing? Termination / Liveness (47:25, Slides 47–48, 50)**: #gemini
	* **Termination** is **not** guaranteed in purely asynchronous runs (due to **FLP**) — two competing proposers can indefinitely preempt each other's `Prepare` phase before either gets `Accept` through (livelock / "dueling proposers", Slide 48: $p_1$ sends `Prepare(2)`, $p_2$ sends `Prepare(3)` before $p_1$'s `<num=2, val=0>` arrives, $p_1$ sends `Prepare(4)` before $p_2$'s `Accept(3)` arrives, etc.). #gemini
	* **How to fix Liveness (Slide 50)**: Use an **eventual leader detector $\Omega$** on proposers; once the system becomes synchronous after $T$, a single proposer is elected leader and Paxos terminates. #gemini

# questions
**message complexity best case (1 proposer, no contention — Slide 35)**: #gemini
* at the best case how many communication steps (delays) to decide? **$3$ message delays** (`Prepare` $\to$ `Promise` $\to$ `Accept/Learn`, or $4$ if counting `Decide` broadcast among learners). #gemini
* at the best case how many messages to decide? * [INSERT HERE] #gemini
* at the best case how many rounds? **$1$ Paxos round** (Phase 1 + Phase 2). #gemini

**worst case complexity (asynchronous / competing proposers)**:
* **no upper bound**, each proposer could kill each other's requests using higher round numbers (Slide 48). answer: **unbounded ($\infty$)**.

**Slide 49 Question (Split Vote Scenario)**: #gemini
* Suppose in round $j$, $P_1$ makes $n/2 - 1$ acceptors ($a_1, \dots, a_{n/2 - 1}$) vote for value $3$; in round $j+1$, $P_2$ makes $n/2 - 1$ acceptors ($a_{n/2 + 1}, \dots, a_n$) vote for value $42$; and $a_{n/2}$ never received any proposal. Is it possible that a different proposer, in round $j+k$, makes acceptors decide on value $7$? #gemini
* **Answer**: * [INSERT HERE] #gemini
