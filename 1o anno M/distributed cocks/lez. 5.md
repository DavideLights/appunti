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

two events $e$ and $e'$ are related by happened-before relation $(e \to e')$: 
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

# vector clock
**Vector Clock**: guarantee IF $L(e) < L(e')$ then $e \to e'$

**intuition**: $L(e)$ describes a list of events that happened before $e$![[Pasted image 20261106002111.png]]

now we append the last event received to my historu