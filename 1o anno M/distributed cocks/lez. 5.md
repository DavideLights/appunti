**D1**: why can physical clocks not be used to order events in asynchronous systems? (delay estimation, uncertainty) #gemini
* **R1**: [INSERT HERE] #gemini
**D2**: state the 3 rules that define Lamport's happened-before relation ($\to$). (local, send-rcv, transitivity) #gemini
* **R2**: [INSERT HERE] #gemini
**D3**: what algebraic structure does $(\mathcal{E}, \to)$ form, and when are two events concurrent ($e \parallel e'$)? (poset, incomparability) #gemini
* **R3**: [INSERT HERE] #gemini
**D4**: state the update rules of Lamport's Scalar Logical Clock. (init, rule 1 local/send, rule 2 receive) #gemini
* **R4**: [INSERT HERE] #gemini
**D5**: what is the fundamental limitation of Lamport's Scalar Clock? (implication direction, concurrency) #gemini
* **R5**: [INSERT HERE] #gemini
**D6**: how does Vector Clock achieve $e \to e' \iff V(e) < V(e')$? (causal histories, vector of lengths) #gemini
* **R6**: [INSERT HERE] #gemini
**D7**: how are two vector timestamps $V, V'$ compared? ($=, \le, <, \parallel$) #gemini
* **R7**: [INSERT HERE] #gemini
**D8**: which distributed applications typically use Scalar Clocks vs Vector Clocks? (total order vs causal tracking) #gemini
* **R8**: [INSERT HERE] #gemini

---

# 1. the need for logical time #gemini

**why physical clocks fail over event ordering?**
* **trasmission delay**: algorithms for synchronization are based on **transmission delay**
* its hard to get a **good estimation**.
* we want to know
	* not when things happen
	* but in which order they happened
* **logical clock**: each system has it own logical clock
	* clocks not aligned $\to$ impossible to order events.


**motivating scenario: distributed chat** (mission-critical workplace): #gemini
* **why distributed**? no central **point of failure**, no server stores encrypted messages/data records.
* **why asynchronous model**? because should work when system **looses synchrony**.
* **why**? we cannot synchronise, **we cannot timestamp** the software clock.

![[Pasted image 20261105231941.png]]

* **core requirement / goal**: bob should know what generated his message.

---

# 2. the happened-before relation ($\to$, Lamport 1978) #gemini
**happened-before relation**:
* introduced by lamport
* $\to_{i}$: denotes the ordering relation **inside** $p_{i}$
* $\to$: denotes the ordering relation **between any pair of events**

**(from lamport paper)**, two events $e$ and $e'$ are related by happened-before relation ($e \to e'$) if one of the three is true:
* $a$ and $b$ are events in the same process and $a$ comes before $b$
* $a$ is the sending of a message by one process and $b$ is the receipt of the same message by another process.
* if $a \to b$ and $b\to c$, then $a\to c$

(**from slides**) two events $e$ and $e'$ are related by happened-before relation $(e \to e')$: 
1. **Local ordering**: $\exists p_i$ such that $e \to_i e'$. $e'$ starts after $e$ inside $p_{i}$
2. **Send-receive ordering**: $\forall m, \; \text{send}(m) \to \text{receive}(m)$
	1. $e=\text{send}(m)$
	2. $e' = \text{receive}(m)$
3. **Transitivity**: $\exists e'' : (e \to e'') \land (e'' \to e') \implies e \to e'$

thanks to transitivity we can say $e_{1}\to e_{3}$:
![[Pasted image 20261105235149.png]]


we can so define a casual ordered sequence: $e_{1},e_{2},\dots,e_{n}$
* **uniqueness**: the seq is not necessarly unique
* **no happened-before relation**: it may exists $e_{1},e_{2}$ s.t. there is no relation.
* **concurrent** $e_{3}||e_{4}$: if there is no happened-before relation
* for any $e_{x}, e_{y}$: $e_{x} \to e_{y}$, $e_{y} \to e_{x}$, $e_{y}||e_{x}$
![[Pasted image 20261105235503.png]]

![[Pasted image 20261105235630.png]]

# Logical Clock
**logical clock**: monotonically increasing software counting register
* $\neq$ physical clock
* $p_{i}$: each has its own $L_{i}$ logical clock.
* **events**: logical clock time stamp is attached to events
* **logical time stamp assigned**: $L_{i}(e)$ is the logical clock applied from $p_{i}$ to $e$
* $e \to e'$ then $L(e) < L(e')$

> the ordering relation obtained trough logical timestamps is a partial order and are not sufficient to relate events.

**scalar logical clock**:
* each $p_{i}$ initializes to $L=0$
* when: $p_{i}$ sends message $m$
	1. create event $\text{send}(m)$
	2. increase $L_{i}$
	3. attach $m$ with timestamp $t=L_{i}$
* when: $p_{i}$ receives message $m$
	1. $L_{i} = \max(t,L_{i})$
	2. produce $\text{receive}(m)$
	3. increase $L_{i}$

![[Pasted image 20261106000933.png]]

![[Pasted image 20261106001050.png]]

logical clock guarantees:
* IF $e \to e'$ then $L(e) < L(e')$
* does not guarantee: IF $L(e) < L(e')$ then $e \to e'$
* **what does this mean**? looking only at the scalar clocks, we cannot determine if two events are **concurrent** or correlated by **happened-before rel**.

[!note] think about when $L(e) < L(e')$ but $e \not \to e'$, but its trivial???

# vector clock (from the book)
**how to track causality**? using vector clocks
* is simple if we assign each event a unique name
* this name will be the combination of a process ID and a locally incrementing counter $p_{k}$.
* $p_{k}$ is the $k^{th}$ event that happened in process $p$

**Assume**: 
* let event $p_{k}$ for some $k$ in $P$ describing that: $P$ sends a message to $Q$
* let $q_{1}$ the event in $Q$ describing the arrival of the message.

**How to track causality**?
* $P$ also send his local history
* assume $P$'s history is made of $\{ p_{1},p_{2} \}$ extended with $p_{3}$ (describing the send event)
* assume $Q$'s history is made of $\{ q_{1} \}$
* on arrival $Q$ records:
	* $P$'s history $\{ p_{1},p_{2},p_{3} \}$ 
	* the deliver event $q_{2}$ 
	* so he merges the two histories together obtaining $\{ p_{1},p_{2},p_{3},q_{1},q_{2} \}$

How to chec if $p$ causally precedes $q$?
$$
\text{check } H(p) \subset H(q)
$$
How we represent $H(p)$?
* assign a sequential index to each process
* use a vector $\text{VC}_{j}$ inside process $P_{j}$
* its just the logical clock at process $P_{j}$
* each entry of the vector describes what $P_{j}$ **knows** about the logical clock of $P_{i}$
 $$
 \text{VC}_{j}[i]= \text{number of events that have occurred so far at } P_{j}
$$

**property**: if $\text{VC}_{i}[j]=k$ then $P_{i}$ knows that $k$ events occourred at $P_{j}$

**how to use a vector clock**:
1. before executing an event
	1. $P_{i}$ executes $\text{VC}_{i}[i] \gets \text{VC}_{i}[i] + 1$
	2. **note**: we just recorded that a new event happened
2. when $P_{i}$ sends a message $m$ to $P_{j}$
	1. $m$'s timestamp $ts(m)$ is set to $\text{VC}_{i}$
	2. **note**: done after increment
3. when $P_{j}$ receives the message
	1. $\forall k \text{VC}_{j}[k] \gets \max \{  \text{VC}_{j}[k], \text{ts}(m)[k] \}$
	2. **note**: just maximize for each entry of the vector clock the values.

**note**: for an event $a$ with timestamp $\text{ts}(a)$ then $\text{ts}(a)[i]-1$ is the number of events processed at $P_{i}$ preceding $a$.

**conseguence**: $P_{j}$ receiving $ts(a)$ know the number of events that caused $a$ inside $P_{i}$

## slides
we introduced vector clocks talking about history of an event looking at this example:
![[Pasted image 20261106195204.png]]

we noted that:
* $L(e) = [\text{History}_{p_{0}}: [e_{0}], \text{History}_{p_{1}}: [e_{1},e_{3}], \dots]$ describes the history of events behing $e$ for all processes in the system 
* we need two rules: update send rule and update rcv rule.
* $L(e_{i}) > L(e_{j})$ iff two conditions hold
	* $\forall k: L(e_{j})_{\text{History}_{k}} \subseteq L(e_{i})_{\text{History}_{k}}$
	* $\exists x: L(e_{j})_{\text{History}_{x}} \subset L(e_{i})_{\text{History}_{x}}$
* if $e \to e'$ then $L(e) < L(e')$ because one "contains" the other.
* if $L(e) < L(e')$ then $e \to e'$ because $L(e')$ contains e and a causal path from $e$ to $e'$

![[Pasted image 20261106195737.png]]

* $\text{History}_{x} \subset \text{History'}_{x} \to \text{History}_{x}$ is a prefix for $\text{History'}_{x}$ 
* $\text{History}_{x} \subset \text{History'}_{x} \to \text{len}(\text{History}_{x}) < \text{len}(\text{History'}_{x})$


## vector clock implementation, example and properties from slides

**properties**: let $V, V'$ be two vector clocks
* $V=V'$ iff $V[j]=V'[j] \;\; \forall j \in \{ 1,\dots,N \}$
* $V \leq V'$ iff $V[j] \leq V'[j] \;\; \forall j \in \{ 1,\dots,N \}$
* $V < V'$ iff $V \leq V' \land \exists j: V[j] < V'[j]$


![[Pasted image 20261106213940.png]]![[Pasted image 20261106214842.png]]![[Pasted image 20261106214847.png]]

**what problem does vector clock solve**? causal broadcast.![[Pasted image 20261106214954.png]]![[Pasted image 20261106215007.png]]![[Pasted image 20261106215014.png]]

