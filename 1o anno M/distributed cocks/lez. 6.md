**previous lecture**: [[lez. 5|lez. 5 (Happened-before, Logical & Vector Clocks)]] #gemini

# lamport's algorithm mutual exclusion
**assume**: $\text{Request CS} \to \text{Grant CS} \to \text{Release CS}$.
* two grants of critical section cannot overlap in time between `Grant` and `Release`.

![[Pasted image 20261106221320.png]]

**assume**: use of a **FIFO Perfect Point-to-Point Link** (`FIFOPerfectLink`), otherwise the algorithm does not work.

**properties**:
* **Safety (Mutual Exclusion)**: at most $1$ process gets the critical section at a time; once we break this rule the execution is permanently unsafe.
* **Liveness (Progress / No-Starvation)**: if $p$ requests the critical section, it will eventually get it.
* **Fairness (Causal ordering)**: if the request of $p$ **happens-before** ($\to$) the request of $q$, then $q$ cannot access the CS before $p$.

**lamport's algorithm properties**:
* assumes **$f = 0$ crashes**; otherwise a crashed process never sends `ACK`/`RLS` and can block everyone forever.
* scalar clocks mantain history of operations.

**idea of the lamport algorithm**:
* you can enter the critical section only if you get responses (`ACK`) from all other processes.
* you broadcast your timestamped request to everyone, wait for everyone's `ACK`, and order requests totally by `<scalarClock, process_id>`.

**assuming**: FIFO link.
### pseudocode (Algorithm 1 — process $p_i$) #gemini

**upon event** `init`:
1. $\text{Requests} = \text{Acks} = \emptyset$ 
	1. *set $\text{Acks}$ stores responses to requests;*
	2. *set $\text{Requests}$ stores active CS requests*.
2. $\text{scalarClock} = 0$ (**Lamport Clock**).
3. $\text{myReq} = \bot$ *(Null)*.
4. $\Pi = \{ p_{0},\dots, p_{n-1}\}$ *(set of all processes from which $p_i$ expects a response)*.

> increment `scalarClock` an then send `myReq` to every process.
**upon event** `request`:
1. $\text{scalarClock} \gets \text{scalarClock} + 1$
	1. **note**: always increment, then attach the $\text{scalarClock}$
2. $\text{myReq} \gets (\text{REQ}, \text{ts} = \langle i, \text{scalarClock}\rangle)$
3. $\forall p_j \in \Pi$:
	1. **SEND** $\text{FIFOPerfectLink}(p_j, \text{myReq})$
	2. (sent also to myself, or added directly to $\text{Requests}$)*.

> empty `my_req`, then say to everyon that i have released.
**upon event** `release`:
1. $\text{my\_req} = \bot$
2. $\text{scalar\_clock} = \text{scalar\_clock} + 1$
3. **for all $p_{j} \in \Pi$ do**:
	1. **SEND** $\text{FIFOPerfectLink}(p_{j}, (RLS, ts=<i,\text{scalar\_clock}>))$

> **grant only if**
> 1. $\not \exists \text{req} \in \text{Requests}: ts(\text{req}) < ts(\text{my\_req})$:
> 	1. i have the **oldest** `req` sent in the system
> 	2. = i have the request with the oldest timestamp
> 2. $\forall p \in \Pi: \exists m \in \text{Acks}|ts(m) > ts(\text{my\_req}) \land \text{sender}(m)=p$: i received   **all the acks** for my request

**upon event** $\not \exists \text{req} \in \text{Requests}: ts(\text{req}) < ts(\text{my\_req}) \land \forall p \in \Pi: \exists m \in \text{Acks}|ts(m) > ts(\text{my\_req}) \land \text{sender}(m)=p$:
1. trigger event GRANTED.

`deliver_message(m: message)`:
1. $\text{scalarClock} \gets \max(\text{clock}(m), \text{scalarClock}) + 1$
	* apply here lamport's receive rule since we are about to deliver a message received.
2. if $m$ is $\text{REQ}$:
	1. $\text{Requests} \gets \text{Requests} \cup \{ m \}$
	2. $\text{scalarClock} \gets \text{scalarClock} + 1$ 
		1. **note**: *increment again because sending the reply is a new event*
	3. $\text{Send FIFOPerfectLink}(\text{sender}(m), (\text{ACK}, \text{ts} = \langle i, \text{scalarClock}\rangle))$
3. else if $m$ is $\text{ACK}$:
	1. $\text{Acks} \gets \text{Acks} \cup \{ m \}$
4. **else if $m$ is a** $\text{RLS} \land \exists \text{req} \in \text{Request\_set}: \text{sender}(req)=\text{sender}(m)$ **then**
	1. **note**: is there a request in my $\text{Request\_set}$ wich sender is the same of $m$ that released its request?
	2. $\text{Requests}=\text{Requests} \setminus \{ req \}$

`critical section test` (**upon event** guard for `trigger Granted`):
* **Total order on timestamps**: $\text{ts}(x) < \text{ts}(y) \iff \text{clock}(x) < \text{clock}(y) \;\lor\; (\text{clock}(x) = \text{clock}(y) \land \text{id}(x) < \text{id}(y))$. #gemini
* **Guard condition** (both must hold): #gemini
	1. $\nexists \text{req} \in \text{Requests} : \text{ts}(\text{req}) < \text{ts}(\text{myReq})$ *(my request has the smallest timestamp in $\text{Requests}$)* #gemini
	2. $\forall p \in \Pi, \exists m \in \text{Acks} : \text{sender}(m) = p \land \text{ts}(m) > \text{ts}(\text{myReq})$ *(I received an `ACK` from every process with timestamp strictly greater than my current request)* #gemini
* **why check $\text{ts}(\text{ack}) > \text{ts}(\text{myReq})$?** Because we never remove old `ACK`s from $\text{Acks}$; requiring $\text{ts}(m) > \text{ts}(\text{myReq})$ ensures that `ACK`s from a first request cannot unlock a second, newer request (which has a higher timestamp).

### running example
* **blue arrow**: regular program message exchanged between processes (not part of the ME algorithm, but still increments the Lamport clock).
* $p_{3}$: starts the request message with $(\text{REQ}, \langle \text{id}:3, \text{clock}:3\rangle)$ (clock was $2$, incremented to $3$).
* $p_{1}$: receives $p_3$'s `REQ`, updates clock from $3$ to $\max(3,3)+1 = 4$, then increments to $5$ to send $(\text{ACK}, \langle \text{id}:1, \text{clock}:5\rangle)$ to $p_{3}$.
* $p_{2}$: does the same (clock $0 \to 4 \to 5$, sends `ACK` to $p_3$).
* *(each process also sends `REQ`/`ACK` to itself)*.

What if $p_{1}$ also wants to access the critical section right after?
* $p_1$ increments its clock to $6$ and sends $(\text{REQ}, \langle \text{clock}:6, \text{id}:1\rangle)$.
* **note**: everyone always replies with an `ACK` upon receiving a `REQ`, even if already waiting for the critical section!

$p_{3}$ and $p_{1}$ both sent a request and both received `ACK`s from $\{ p_{1},p_{2},p_{3} \}$ with $\text{ts}(\text{ACK}) > \text{ts}(\text{myReq})$. Who enters the critical section?
* Look at the $\text{Requests}$ set at both processes:
	* $p_{1}.\text{Requests} = \{ (p_{3}, t=3), (p_1, t=6) \}$
	* $p_{3}.\text{Requests} = \{ (p_{3}, t=3), (p_{1}, t=6) \}$
* **$p_{3}$ enters the CS first!** Because we compare **scalar clock $t$ first** ($t_3 = 3 < t_1 = 6$), and process `id` is used **only as a tie-breaker when the scalar clocks are equal** ($t_i = t_j$). Once $p_3$ exits and broadcasts `RLS` (removing $(p_3, 3)$ from $p_1.\text{Requests}$), $p_1$ becomes the minimum and enters the CS. #gemini

> **why not remove `ACK`s on release?** You can, and it saves memory, so keeping all `ACK`s and checking $\text{ts}(\text{ack}) > \text{ts}(\text{myReq})$ is simply a specification simplification.


# safety & fairness proofs

### safety proof (mutual exclusion)
**idea**: requests are totally ordered by $\langle \text{clock}, \text{id}\rangle$, and FIFO links force at least one process (or both) to see the other's request before receiving its `ACK`.

**proof by contradiction**: suppose both $p_{i}$ and $p_{j}$ ($i < j$) are in the CS at the same time.
* Since $p_{i}$ entered the CS
	* it received an `ACK` from $p_{j}$ with $\text{ts}(\text{ack}_{j \to i}) > \text{ts}(\text{req}_i)$
	* and when $p_{j}$ sent that `ACK` it had already inserted $\text{req}_i$ into $p_j.\text{Requests}$.
	* **resuming**: one saw the other first and sent him an ACK.
* Symmetrically, $p_{j}$ 
	* received an `ACK` from $p_{i}$ with $\text{ts}(\text{ack}_{i \to j}) > \text{ts}(\text{req}_j)$, 
	* so $p_i$ had inserted $\text{req}_j$ into $p_i.\text{Requests}$ when sending that `ACK`.
* we have two cases: **BEFORE** and **AFTER** sending **ACK**.
* **Case 1 ($p_j$ requests *after* sending `ACK` to $p_i$)**:
	* Then $\text{ts}(\text{req}_j) > \text{ts}(\text{ack}_{j \to i}) > \text{ts}(\text{req}_i)$
	* and $\text{req}_i$ is already in $p_j.\text{Requests}$ with a smaller timestamp
	* $\implies p_j$ cannot enter the CS (contradiction).
	* $\square$
* **Case 2 ($p_j$ requests *before* sending `ACK` to $p_i$, e.g., concurrent requests with SAME or DIFFERENT clocks)**:
	* Since $p_j$ sent $\text{req}_j$ to $p_i$ **before** sending $\text{ack}_{j \to i}$ to $p_i$,
	* by the **FIFO link property** $\text{req}_j$ is delivered to $p_i$ **before** $\text{ack}_{j \to i}$. #gemini
	* Thus, when both have collected all `ACK`s, $p_i.\text{Requests}$ contains $\{\text{req}_i, \text{req}_j\}$ and $p_j.\text{Requests}$ contains $\{\text{req}_i, \text{req}_j\}$.
	* Because $\langle \text{clock}, \text{id}\rangle$ is a strict **total order** 
		* total order $\equiv$ **if clocks are equal** we count on the fact that process ids are different!
		* $i < j \implies \text{ts}(\text{req}_i) < \text{ts}(\text{req}_j)$)
		* both cannot simultaneously be the minimum in their $\text{Requests}$ set (contradiction) $\square$. #gemini

![[Pasted image 20261107001134.png]]
![[Pasted image 20261107001139.png]]
### fairness property proof
**Claim**: if $\text{req}_j \to \text{req}_i$, then $p_i$ cannot enter the CS before $p_j$.
* **By contradiction**: suppose $p_i$ enters before $p_j$.
* Since $\text{req}_j \to \text{req}_i$, by the Scalar Clock property we have $\text{ts}(\text{req}_j) < \text{ts}(\text{req}_i)$. #gemini
* To enter the CS, $p_i$ must first receive $\text{ack}_{j \to i}$ with $\text{ts}(\text{ack}_{j \to i}) > \text{ts}(\text{req}_i) > \text{ts}(\text{req}_j)$, meaning $p_j$ sent $\text{ack}_{j \to i}$ **after** sending $\text{req}_j$. #gemini
* By **FIFO links**, $p_i$ delivers $\text{req}_j$ **before** delivering $\text{ack}_{j \to i}$, so $\text{req}_j \in p_i.\text{Requests}$ with $\text{ts}(\text{req}_j) < \text{ts}(\text{req}_i)$, preventing $p_i$ from entering before $p_j$ releases (contradiction) $\square$. #gemini

# performance & questions
In the best case, when a process wants to enter the CS, how many messages are sent?
* $p_{i}$ sends $N-1$ requests (or $N$ including self)
* all other processes reply with an `ACK`: $N-1$ messages (or $N$)
* $p_{i}$ releases and sends `RLS` to everyone: $N-1$ messages (or $N$)
* **Total message complexity**: $3(N-1)$ network messages ($3N$ with self-messages) $= O(N)$ messages per CS access. #gemini

How do we compute time (message delay)?
* Assume each message takes $1$ unit of time (message delay) in a synchronous / best-case execution:
	* all `REQ`s are sent in parallel ($1$ unit)
	* all `ACK`s are sent back in parallel ($1$ unit)
* **Best-case access delay** (no one in CS, only $1$ requester): **$2$ message delays** ($1$ for `REQ` + $1$ for `ACK`).

In the worst case, how many units are needed?
* If all $N$ processes request concurrently, I receive all `ACK`s in $2$ units but may have to wait for a chain of $N-1$ `RLS` messages before my request becomes the minimum.

---

# failure detection (*Time 3*)
**note**: in asynchronous systems the only ordering is given by the happened-before relationship.

**why failure detection?**: instead of abstracting time inside the link to achieve an syncrhonous system **we abstract an object that reflects if process are synchronized**.

> **crash-stop abstraction**: in this abstraction a process is faulty if it crashes at some time during the excution and its correct if it never crashes and executes an infinite number of esteps.

**assuming crash-stop abstraction**: we can to failuder detection using timeouts.

> [!todo] MISSING FROM SLIDES (*Time 3*, slides 1–4): Recap on Timing Assumptions #gemini
> * Why Eventual Synchrony needs **abstract timing assumptions**: Option 1 (bake timing bounds directly into links/processes — makes proofs complex and error-prone) vs **Option 2 (encapsulate timing assumptions inside separate abstractions: Failure Detectors & Leader Election)**. #gemini




Two core abstractions that encapsulate timing assumptions:
* **Failure Detector (FD)**
* **Leader Election (LE)**
* *(Note: only work for **Crash Failures**, not Byzantine; and if you can solve one, you can build the other).*

**note**: we want to avoid manipulating time directly inside distributed algorithms because explicit timers/delays make protocols and correctness proofs complex and prone to errors!

**failure detector**: software module that encapsulates synchrony/partial-synchrony assumptions, characterized by two properties:
1. **Accuracy**: ability to avoid mistakes (false suspicions) when detecting failures.
2. **Completeness**: ability to eventually detect actual failures.
3. Based on the idea of **pinging (heartbeats)**.

**how to detect a crash?** Ping the other process and wait for a reply within a bounded timeout.

### Perfect Failure Detector ($\mathcal{P}$)

what does this bullet list mean gemini?
**system model**:
* **Synchronous system**
* **Crash failures** (crash-stop)
* **Perfect Synchronous Point-to-Point Link**: Perfect P2P link + **synchronous delivery** 
	* if a correct process $p$ sends $m$ at time $t$
	* ifthe destination does not crash by $t+\text{max\_delay}$
	* then $m$ is delivered by at most $t+\text{max\_delay}$

**can we do so in asynch**?
* in sync, using clocks we can infer a crash for a process.

![[Pasted image 20261107004404.png]]


**idea**: start a timer $\Delta$ and send a heartbeat request to $p_{2}$; $p_{2}$ replies immediately:
* if $p_{2}$ doesn't answer within $\Delta \ge 2\cdot\text{max\_delay}$ (where $\text{max\_delay}$ is the max one-way channel delay), then $p_2$ is dead. This works in **synchronous** systems.
* **what about asynchronous systems?** In async you **cannot distinguish** between a slow message/process and a crashed process: any timeout-based detector may falsely suspect a slow process.

**gemini**: what is the teacher trying to say? can we do failure detection in asynch models or no?

**Perfect Failure Detector ($\mathcal{P}$) specification** (Indication event: $\langle \mathcal{P}, \text{Crash} \mid p \rangle$):
* **PFD1 (Strong Completeness)**: Eventually, every process that crashes is permanently detected by every correct process *(Liveness property)*.
* **PFD2 (Strong Accuracy)**: If a process $p$ is detected by any process, then $p$ has actually crashed *(Safety property — never suspect a correct/alive process)*.

### perfect failure detector algorithm
> **aka**: Exclude on timeout

**uses**: $\text{PerfectPointToPointLinks}$

> **note**: perfect p2p is a channel that: odes not **lose, duplicate, create spurious messages.**

**upon event $<\mathcal P, \text{Init}>$ do**:
1. $\text{alive} := \Pi$
2. $\text{detected} = \emptyset$
3. $\text{starttimer}(\Delta)$

**upon event $<\text{Timeout}>$ do**:
1. **forall $p \in \Pi$ do**
	1. if $(p \notin alive ) \land (p \not\in \text{detected})$
		1. $\text{detected} = \text{detected} \cup \{ p \}$
		2. **trigger** $<\mathcal P, \text{Crash}|p>$
	2. **trigger** $<\text{pl, Send}|p,[\text{HeartbeatRequest}]>$
2. $\text{alive} = \emptyset$
3. $\text{starttimer}(\Delta)$

**upon event $<\text{pl, Deliver}|q, [\text{HeartbeatRequest}]>$ do**:
1. **trigger** $<pl, \text{Deliver}|p,[\text{HeartbeatReply}]>$

**upon event $<\text{pl, Deliver}|q, [\text{HeartbeatReply}]>$ do**:
1. $\text{alive} = \text{alive}\cup \{ p \}$


> [!todo] MISSING FROM SLIDES (*Time 3*, slides 10–25 — after PFD specification) #gemini
> 1. **Algorithm 2.5 (`Exclude on Timeout`) pseudocode**: #gemini
> 	* Sets `alive := \Pi`, `detected := \emptyset`, periodic `starttimer(\Delta)`. #gemini
> 	* On `Timeout`: any $p \notin \text{alive} \land p \notin \text{detected}$ is added to `detected` and triggers $\langle \mathcal{P}, \text{Crash} \mid p \rangle$; then sends `HEARTBEAT REQUEST` to all $p \in \Pi$, resets `alive := \emptyset`, and restarts timer $\Delta$. #gemini
> 	* On delivering `HEARTBEAT REQUEST`: replies with `HEARTBEAT REPLY`; on delivering `HEARTBEAT REPLY` from $p$: adds $p$ to `alive`. #gemini
> 2. **Correctness Proofs of `Exclude on Timeout`**: #gemini
> 	* **Strong Completeness**: if $p_1$ crashes at $t$, $p_0$ detects it at most by $t + 2\Delta$. #gemini
> 	* **Strong Accuracy**: holds iff $\Delta \ge 2\cdot\text{max\_delay}$ (proof by contradiction: if $p$ is alive, both `REQ` and `REPLY` arrive within $\text{max\_delay}$ each). #gemini
> 3. **Key Conceptual Questions on $\mathcal{P}$ (slides 13–20)**: #gemini
> 	* Can different processes detect $p_3$ at different instants? **Yes** (`PFD1` only requires *eventual* detection; the exact bound $t + 2\Delta$ comes from the specific implementation). #gemini
> 	* If $p \notin \text{detected}$ at time $t$, can we conclude $p$ is alive at time $t$? **NO** — processes only observe the system via messages with delay $d$ (state at $t-d$); no FD can know if a process is alive at the exact current instant $t$. #gemini
> 4. **Improving $\mathcal{P}$ — Round-Based Failure Detector $\mathcal{P}$ & Round Model (slides 21–28)**: #gemini
> 	* *"In synchronous networks, silences are expressive"*: cut messages in half by sending one-way `BEAT` messages at the start of each round (no `REQUEST` needed). #gemini
> 	* Requires synchronized clocks with global skew $\delta$ and round length $T$ (Algorithm 3: `Round-Based P` + Algorithm 4: `Max Clock Synchronizer`; Homework: minimum $T$). #gemini
> 	* **Equivalence `Synchronous = Round-Based`**: abstracting synchronous execution into discrete rounds $r, r+1$ where processes switch rounds together and messages sent at the start of round $r$ are delivered by the end of round $r$. #gemini
> 5. **Next part of *Time 3* (if covered in Lez. 6/7)**: Fault-Tolerant patch to Lamport's ME using $\mathcal{P}$ (Algorithm 15 — why ignoring late `REQ`s from `Crashed` is required!) and Simple ME using $\mathcal{P} + \text{LE}$. #gemini