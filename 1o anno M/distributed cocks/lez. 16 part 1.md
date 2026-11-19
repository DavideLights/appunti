**theorem** flp. if $f>0$ then consensus is unsolvable in such system. (Every algorithm has a run that violates either safety or liveness). #gemini

In e-sync can we solve consensus? Yes, via **Paxos**. #gemini

## eventually synch PAXOS
> introduced in 1989 (*The Part-Time Parliament*), and no one understood it, too complex. Later simplified in *Paxos Made Simple* (2001). #gemini


**paxos**: solves eventually sync consensus with crash failures. #gemini
* **safety** is always guaranteed. So validity, integrity and agreement.
* **liveness**: the algorithm terminates only when the system is eventually synchronous and behaves in a good way for enough time. So after this time (when the sys is synchronous, the algorithm ensures that a decision consensus is shared and confirmed among all the process)
* **assumption**: majority of acceptors is correct ($f < \frac{|A|}{2}$), so it uses quorums, and eventually synchronous system. #gemini

**paxos protocol**: we can partition $\Pi$ in this way, 3 different subsets, or **roles**.
* **proposers**: proposes a value, it might be passed to it.
* **acceptors**: make the other process reach a commit/final decision on a value. It interacts with proposers
* **learners**: passively assist to the decision and obtain the final decided value by talking with acceptors. #gemini

**why we have roles**? 
* **ex**: on the same physical machine i can have a proposer, acceptor and a learner.
* majority assumption: we only need $f < \frac{|A|}{2}$ on the set of acceptors $A$. we cannot tolerate more acceptor failures. #gemini
* but we can tolerate at the same time any amount of failures for proposers and learners. #gemini
* another motivation: we can have clients and learners that can fail but are not related strictly to the algorithm.


what a consensus protocol should do:
* at a certain time we have to choose a value 
* but we might not know that at a moment, a value has been chosen.
* **difference**: moment in which we decide vs when we choose.
	* **choose**: we reach an agreement in the global system (a majority of acceptors accepts the same proposal). #gemini
	* **decide**: a process learns the chosen value and triggers the local decision. #gemini

other rules (Safety): #gemini
* **CS1 (Validity)**: only a value that has been proposed may be **chosen**
* **CS2 (Agreement)**: only a single value is **chosen**
* **CS3 (Integrity)**: a process never learns (**decides**) that a value has been chosen unless it actually has been
	* a process learns the chosen event only when it happened.

> **resuming**: the value **decided** must be the one that was **chosen**. #gemini

> **rules**: a process can play multiple roles simultaneously, and roles are fixed. #gemini

> **eventually synch**: channel delay, and time score... There is a period after which our system stabilizes and is under some delay bound.


# creating the algorithm
## first idea: single acceptor
1. proposer sends value to the single acceptor
2. the acceptor chooses the first proposed value it receives and rejects other requests
	1. so we cannot decide other values

**problem**: if the single acceptor crashes, the system blocks (dead end).


## second idea: multiple acceptors (first try: accept at most one value)
**solution to first idea**: use multiple acceptors (e.g., 3 acceptors) and choose a value when a **majority** of acceptors accepts it. #gemini

* **P1**: *An acceptor must accept the first proposal it receives* (needed so a value is chosen even if only a single proposer proposes one value). #gemini
1. proposer sends value to the acceptors 
2. the acceptors accept the first value they see and reject subsequent ones. #gemini
3. if a majority accepts the same value then that value is chosen.

**problem**: if several values are concurrently proposed by different proposers (e.g., $a_1$ gets $v=1$, $a_2$ gets $v=2$, $a_3$ gets $v=3$), none of them reaches a majority $\implies$ **deadlock**! #gemini


## third idea: accept multiple numbered proposals
**solution to second idea**: we cannot reject other requests. An acceptor must be allowed to accept **multiple proposals**. The proposals must be numbered so that we can order and recognize them. #gemini
* each proposal is a unique pair $\langle \text{round number}, \text{value} \rangle = \langle n, v \rangle$ (total order of proposals). #gemini
* note that across different proposal numbers, the proposed value may change, but within a single round number $n$, at most one value is proposed. #gemini
* $\text{round number}=\text{ballot number}=\text{ticket number}$

**invariant to reach**: a value is **chosen** when a single proposal $\langle n, v \rangle$ with that value is accepted by a majority of acceptors. #gemini


> **when a value is chosen**? when a single proposal $\langle n, v \rangle$ reaches a majority of acceptors! #gemini


Multiple proposals can be chosen across different rounds, so all chosen proposals must have the **same value**: #gemini
* **P2**: *If a proposal with value $v$ is chosen, every higher-numbered proposal that is chosen has value $v$.* #gemini
* Since any two majorities (quorums) of acceptors intersect in at least one acceptor, different chosen proposals are forced to share the same value. #gemini

how to send proposals without collision in numbers?
* partition round numbers across proposers (Slide 37): e.g., with 2 processes, $P_1$ assigns odd numbers, $P_2$ assigns even numbers; in general with $k$ proposers, $P_i$ uses $\{i, i+k, i+2k, \dots\}$. No communication needed. #gemini

> [!note] 28:30

how to show P2? $\text{P2c} \implies \text{P2b} \implies \text{P2a} \implies \text{P2}$ #gemini

> [!warning] P2 Invariant Chain (`P2c -> P2b -> P2a -> P2`) — Study Actively #gemini
> Review how each strengthening step resolves the asynchronous/crash edge case of the previous one (Slides 17–27 & Lamport's *Paxos Made Simple*, Sec. 2.2). Complete the inductive proof of `P2c -> P2b` on your own below. #gemini

## P2a
* **Why we need P2a**: For a proposal to be chosen, it must be accepted by at least one acceptor. #gemini
* **P2a formally**: *If a proposal with value $v$ is chosen, every higher-numbered proposal that is **accepted by any acceptor** has value $v$.* ($\text{P2a} \implies \text{P2}$) #gemini
* **Problem (P1 vs P2a — Slide 18)**: Since the system is asynchronous, a proposal $\langle 1, 0 \rangle$ can be chosen by a majority $\{a_1, a_2\}$ while acceptor $a_3$ never saw any message. If a new proposer wakes up and sends $\langle 2, 1 \rangle$ to $a_3$, by **P1** $a_3$ would be forced to accept it, violating **P2a**! #gemini

> **recall**: to prevent $a_3$ from accepting a different value, we must prevent proposers from even *issuing* $\langle 2, 1 \rangle$ once $v=0$ is chosen. #gemini

## P2b
* **P2b formally**: *If a proposal with value $v$ is chosen, every higher-numbered proposal **issued by any proposer** has value $v$.* ($\text{P2b} \implies \text{P2a} \implies \text{P2}$) #gemini
> **meaning**: once a majority of acceptors chooses $v$, any proposer issuing a higher round number $n$ must propose that same value $v$. #gemini

Before proposing in round $n$, the proposer must: #gemini
* ask a majority of acceptors what they have already accepted in rounds $< n$ #gemini
* pick the value accepted in the highest round $< n$ (or its own value if none of them accepted anything yet). #gemini

**quorum intersection property**: the acceptors $Q$ that chose $v$ in round $m < n$ form a majority quorum, and the acceptors $S$ queried by the proposer in round $n$ also form a majority quorum $\implies Q \cap S \neq \emptyset$. #gemini

* **Inductive argument (`P2c -> P2b`, Slides 20–22)**: * [INSERT HERE] #gemini

## P2c
* **P2c formally (Slide 22)**: *For any $v$ and $n$, if a proposal with value $v$ and round number $n$ is issued, then there is a set $S$ consisting of a majority of acceptors such that either:* #gemini
	* *(a) no acceptor in $S$ has accepted any proposal round-numbered less than $n$, or* #gemini
	* *(b) $v$ is the value of the highest-numbered proposal among all proposals round-numbered less than $n$ accepted by the acceptors in $S$.* #gemini

**meaning**: 
* **case (a)**: wait for a majority $S$ of acceptors; if none of them accepted any proposal in rounds $< n$ (all reply $\bot$), you are free to propose your own value. #gemini
* **case (b)**: otherwise, if at least one acceptor in $S$ has already accepted a proposal with round $< n$, you **must** adopt the value $v$ of the proposal with the **highest round number** $< n$ among all replies in $S$. #gemini

## prepare & promise idea
To maintain **P2c**, a proposer wanting to issue a proposal with round $n$ must learn the highest-numbered proposal with round $< n$ that **has been accepted** *or* **will be accepted** by each acceptor in a majority $S$ (Slide 23): #gemini
1. the proposer sends `Prepare(n)` to acceptors asking what they have accepted so far. #gemini
2. collect answers from a majority $S$. #gemini

**problem without promises (Slide 25)**: 
* Suppose $p_3$ sends `Prepare(3)` to all acceptors (all currently $\bot$) and gets back "no proposal accepted". Before $p_3$ sends `Propose(<3, 0>)`, another proposer $p_1$ runs `Prepare(1)` and makes all acceptors accept `<1, 5>`. When $p_3$ finally sends `Propose(<3, 0>)`, it violates **P2c** because at the time `<3, 0>` is issued/accepted, the highest-numbered proposal $< 3$ accepted in $S$ is `<1, 5>`, not $\bot$! #gemini

**solution (Promises — Slide 26)**: when an acceptor responds to `Prepare(n)`, it **promises** not to accept any future proposal with round number $< n$ (so it rejects both `Prepare` and `Accept` with round $< n$). #gemini
* In Slide 26, after acceptors reply to `Prepare(rnd=3)`, they promise not to accept round $\le 2$, so $p_1$'s `Prepare(rnd=1)` is rejected ("I cannot accept"). #gemini

**note (Slide 27)**: what if $p_1$ completed `Prepare(num=1)` *before* $p_3$'s `Prepare(num=3)`, and only sends `Propose(<1, 0>)` *after* `<3, 5>` was accepted? This **does not violate P2c** — why? #gemini
* * [INSERT HERE] #gemini


# alg
*(Ref: Slides 28–33, Lamport's Paxos)* #gemini

The protocol executes in two phases per round $n$: #gemini

**Phase 1 (Prepare / Promise)**: #gemini
1. **Proposer (`Prepare`)**: A proposer chooses a new unique proposal round number $n$ and sends `(PREPARE, n)` to a majority of acceptors (asking: *(a)* can I make a proposal with number $n$? *(b)* if yes, do you suggest some value?). #gemini
2. **Acceptor (`Promise` / `NACK`)**: #gemini
	* If an acceptor receives `(PREPARE, n)` with $n > n'$ for every `(PREPARE, n')` it has already responded to, it sends `(ACK, n, n', v')` (or `(ACK, n, \bot, \bot)` if it never accepted anything), where: #gemini
		* *(a)* it promises **not** to accept any more proposals numbered $< n$, and #gemini
		* *(b)* it suggests the value $v'$ of the highest-numbered proposal $n'$ ($n' < n$) that it has already accepted, else $\bot$. #gemini
	* If an acceptor receives `(PREPARE, n)` with $n \le n'$ from any prepare request $n'$ it has already responded to, it ignores it or sends `(NACK, n')` (denying the request as the proposal round is too old). #gemini

**Phase 2 (Accept /Accepted)**: #gemini
3. **Proposer (`Accept`)**: If the proposer receives `ACK` responses from a majority of acceptors for round $n$, it issues an accept request `(ACCEPT, n, v)` to acceptors where: #gemini
	* *(a)* $n$ is the round number from the `(PREPARE, n)` request, and #gemini
	* *(b)* $v$ is the value $v'$ of the highest-numbered proposal $n'$ among all received `ACK` responses (or the proposer's own value if all responses reported $\bot$). #gemini
4. **Acceptor (`Vote`)**: If an acceptor receives `(ACCEPT, n, v)`, it accepts (votes for) the proposal **unless** it has already responded to a `(PREPARE, n')` request having a number $n' > n$. #gemini
