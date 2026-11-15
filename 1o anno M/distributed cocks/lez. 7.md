**previous lecture**: [[lez. 6]] — **next lecture**: [[lez. 8]] #gemini

# perfect failure detection proofs
**Correctness (Strong Completeness)**: assuming $p_{1}$ crashes at time $t$, then $p_{0}$ detects it at most by time $t+2\Delta$:
1. time $t+\Delta$ (at most): $p_{0}$ sends a `HeartbeatRequest`
2. time $t+2 \Delta$: $p_{0}$ does not receive the `HeartbeatReply` $\implies p_1$ is detected as dead.

**Strong Accuracy**: assuming $2\cdot\text{max\_delay} \leq \Delta$:
* Proof by contradiction: if $p$ is detected as faulty by $p_0$ at timeout $\Delta$ but $p$ is alive, then either:
	1. `HeartbeatRequest` did not reach $p$ before $p_0$'s timeout, or
	2. `HeartbeatReply` did not reach $p_0$ before the timeout.
	3. Both cases require the round-trip time to exceed $\Delta$, contradicting $2\cdot\text{max\_delay} \le \Delta$. #gemini

> It is impossible for `REQ` + `REPL` not to complete before the timeout if $2\cdot\text{max\_delay} \le \Delta$. #gemini

**PFD1** (*Strong Completeness*): **Eventually**, every process that crashes is permanently detected by every correct process.

**PFD2** (*Strong Accuracy*): If a process $p$ is detected by any process, then $p$ has crashed.

**example of PFD1** (Slides 14–18):
![[Pasted image 20261111112612.png]]

* **Is it possible for a generic $\mathcal{P}$ that $p_0, p_2$ detect $p_3$ at $t'''$ while $p_1, p_5, p_6$ detect it later at $t''+x$?** **Yes**, because `PFD1` only requires *eventual* detection. #gemini
* **When is $p_3$ detected by everyone ($x = ?$)?** With `Exclude on Timeout`, $x = 2\Delta$ (by $t'' + 2\Delta$ all correct processes have $p_3 \in \text{detected}$). #gemini

> **note**: `PFD1` only says *eventually*; the specific algorithm (`Exclude on Timeout`) determines the exact latency bound ($2\Delta$).

## improving $\mathcal P$
> If at time $t$ I do not have process $p$ in my `detected` set, can I state that $p$ is alive at time $t$? **NO**.

**NO:** Because no algorithm can know what is happening at the exact current instant $t$.

**What do we know?** We only observe the system through messages with delay $d$, so at time $t$ we only know how the system looked at time $t-d$. No Failure Detector can state if a process is alive at the current time $t$.

**Can we use silence instead of messages (cut messages in half)?** ![[Pasted image 20261111115330.png]]
* *"In synchronous networks, silences are expressive"* (N. Santoro): instead of `REQ` + `REPLY`, processes just send one-way `BEAT` messages at every round. #gemini
* Assume a clock synchronizer with global skew $\delta$, and a synchronous link with maximum delay $\text{max\_delay}$ and $\text{min\_delay} > \delta$.

# alg. **round-based** $\mathcal P$

> [!note] Missing from notes — Algorithm 4: `Max` Clock Synchronizer on process $v$ (Slides 24–25) #gemini
> * **upon event** `Init`: $C_v = 0$; send frequency $T$. #gemini
> * **upon event** `tick` from hardware clock: $C_v = C_v + 1$ *(where $H_v(t) = \int_0^t h(\tau)d\tau$)*. #gemini
> * **upon event** $\text{Delivery}(\langle \text{sender}, C_{\text{sender}}\rangle)$: **if** $C_{\text{sender}} > C_v$ **then** $C_v = C_{\text{sender}}$. #gemini
> * **upon event** $C_v = kT$ for some $k \in \mathbb{N}^+$: **for all** $\text{dest} \in \text{Neighbours}$ **do** $\text{Send}(\text{dest}, C_v)$. #gemini

### Algorithm 3: Round-Based Failure Detector $\mathcal{P}$ (process $p_i$)
**upon event INIT**:
* $C_{v}$ **note**: synchronizer's clock
* $T$: round length, $T > 2(\text{max\_delay} + \delta)$
* $\text{Corrects}= \{ p_{0},p_{1},\dots,p_{n} \}$
* $\text{RoundAlive} = \text{Corrects}$
* $r=-1$

**upon event** $C_{v} = kT$ for some $k\in \mathbb N^+$:
1. $r=r+1$
2. **for** all $p_{j} \in \text{Corrects} \setminus \text{RoundAlive}$ **do**
	1. $\text{Corrects}= \text{Corrects} \setminus \{ p_{j} \}$
	2. $\text{TRIGGER} \langle\text{Crash}\mid p_{j}\rangle$
3. $\text{RoundAlive} = \{ p_{i} \}$ *(myself)*
4. **for** all $p_{j} \in \text{Corrects}$ **do**:
	1. $\text{SEND}(\langle p_{i}, \text{BEAT}\rangle)$

**upon event** $\text{DELIVERY}(\langle p_{j}, \text{BEAT}\rangle)$:
1. $\text{RoundAlive} = \text{RoundAlive} \cup \{ p_{j} \}$

![[Pasted image 20261111135114.png]]
![[Pasted image 20261111135145.png]]

**FACT 1**: if I send a `BEAT`, I am alive.
**FACT 2**: if I don't send a `BEAT`, I am dead.

**we have to show that**:
* if I send a `BEAT` to $p$ when my round number is $r$,
* then $p$ receives the `BEAT` while its own round number is also $r$.

**proof** (Slide 26):
* My `BEAT` is sent at real time $t$, as soon as my clock enters round $r$.
* Since software clocks are bounded by skew $\delta$:
	* **When does $p$ enter round $r$?** At earliest at $t - \delta$ (if $p$'s clock is faster by $\delta$), and at latest by $t + \delta$ (if $p$'s clock is slower by $\delta$). #gemini
	* **When does $p$ leave round $r$ (enter $r+1$)?** Since a round lasts $T$ and $p$ entered round $r$ no earlier than $t - \delta$, $p$ stays in round $r$ at least until: #gemini
	  $$(t - \delta) + T = t - \delta + 2\delta + 2\cdot\text{max\_delay} = t + \delta + 2\cdot\text{max\_delay} > t + \delta + \text{max\_delay}$$ #gemini
	* **When does my `BEAT` arrive at $p$?** Since $\text{min\_delay} > \delta$, it arrives after $t + \delta$ (when $p$ is already in round $r$), and at latest by $t + \text{max\_delay} < (t - \delta) + T$ (before $p$ leaves round $r$). Thus it arrives in $(t+\delta, t+\text{max\_delay}]$, entirely within $p$'s round $r$. #gemini

> [!warning] Study on your own — Homework (Slide 29): Minimum $T$ for Round-Based $\mathcal{P}$ #gemini
> * **Problem**: Slide 24 sets $T > 2(\text{max\_delay} + \delta)$, which gives a loose upper bound in the proof above. What is the **actual minimum round length $T$** (as a function of $\text{max\_delay}$ and $\delta$) needed so a `BEAT` sent at time $t$ ( arrives $\le t + \text{max\_delay}$) always lands before $p$ exits round $r$ (at $\ge t - \delta + T$)? Also check what happens if $\text{min\_delay} \le \delta$. #gemini
> * **Reference**: *Time 3* slides 24–29. `[INSERT HERE]` #gemini

* **Strong Completeness** (in Round-Based $\mathcal{P}$): if $p$ crashes, it stops sending `BEAT`s, so every correct process will have $p \notin \text{RoundAlive}$ at the next round boundary and permanently trigger $\langle \text{Crash} \mid p \rangle$. #gemini
* **Strong Accuracy** (in Round-Based $\mathcal{P}$): since every `BEAT` sent in round $r$ is guaranteed to arrive during round $r$, if I do not receive $p$'s `BEAT` in round $r$, the only possible reason is that $p$ did not send it $\implies p$ has crashed (no false detections). #gemini


# round based and synch systems
**synchronous systems abstraction (Synchronous = Round-Based)**: time is divided into logical slots called **rounds** (standard measure of time complexity in synchronous algorithms).

**assumptions**:
* **switch time**: all processes switch from round $r$ to $r+1$ at the **exact same time**.
* **messages**: if a correct process $p$ sends a message at the beginning of round $r$, every correct receiver receives it by the end of the **same round $r$**.

![[Pasted image 20261111140535.png]]

**In Round-Based $\mathcal{P}$, is this execution possible (different processes detecting $p_3$ in different rounds $r=3$ vs $r=4$)?** (Slides 31–32)
![[Pasted image 20261111141905.png]]![[Pasted image 20261111141934.png]]
* **YES!** Because the `for all p_j in Corrects do Send(<p_i, BEAT>)` loop is **not atomic**: if $p_3$ crashes at round $r=2$ after sending `BEAT` to $p_1, p_5, p_6$ but before sending it to $p_0, p_2$, then $p_0, p_2$ detect $p_3$ at the start of $r=3$, while $p_1, p_5, p_6$ detect $p_3$ at the start of $r=4$. #gemini

# eventually perfect failure detectors ($\diamond \mathcal{P}$)
**Trade-off in `Exclude on Timeout` (Slide 33)**: what is the advantage/disadvantage of decreasing $\Delta$?
* **Advantage**: faster crash detection (worst-case detection time is $2\Delta$). #gemini
* **Disadvantage**: if $\Delta < 2\cdot\text{max\_delay}$, heartbeats arrive after the timeout $\implies$ **false detections** (violates Strong Accuracy). #gemini
* *(Performance note, Slide 33: in `Exclude on Timeout`, we can avoid sending `HeartbeatRequest` to already `detected` processes).* #gemini

**system model**:
* **Partial synchrony (Eventual synchrony)**: there exists an unknown **Global Stabilization Time (GST)** $t$ after which the system behaves synchronously (message delays and processor speeds become bounded by an unknown $\text{max\_delay}$). #gemini
* **Crash failures** (crash-stop)
* **Perfect point-to-point links**

**behavior in partial synchrony**:
* There is an (unknown) time $t$ after which crashes can be accurately detected.
* **Before $t$** the system behaves as an **asynchronous** one:
	* the failure detector can make **mistakes** (suspect alive processes because delays exceed the current timeout);
	* **the notion of detection becomes suspicion**: instead of permanently declaring a process `Crash`ed, the FD outputs a *reversible* guess (`Suspect`) that can later be withdrawn (`Restore`) if the process replies. #gemini

$\text{EventuallyPerfectFailureDetector}$ ($\diamond \mathcal P$):
* **Events**:
	* **Indication**: $\langle\diamond \mathcal P, \text{Suspect} \mid p\rangle$: notifies that $p$ is suspected to have crashed.
	* **Indication**: $\langle\diamond \mathcal P, \text{Restore} \mid p\rangle$: notifies that $p$ is not suspected anymore.
* **Properties** (together they ensure that the `suspected` set **stabilizes** on every correct process):
	* **EPFD1** (*Strong Completeness*): Eventually, every process that crashes is permanently suspected by every correct process.
	* **EPFD2** (*Eventual Strong Accuracy*): Eventually, no correct process is suspected by any correct process.

**basic construction rules**:
* Use timeouts to suspect processes that did not send expected messages.
* Suspicions may be wrong ($p$ may suspect $q$ because the chosen timeout was too short).
* $\diamond \mathcal P$ is ready to change its judgment (`Restore`) as soon as it receives a message from $q$, also increasing the timeout value.
* If $q$ has actually crashed, $p$ will stop receiving messages from $q$ and will not change its judgment anymore.

# eventually perfect fd $\diamond \mathcal P$ — `Increasing Timeout` (Algorithm 2.7)
**upon event $\langle\diamond \mathcal P, \text{Init}\rangle$ do**:
* $\text{alive} := \Pi$
* $\text{suspected} := \emptyset$
* $\text{delay} := \Delta$
* $\text{starttimer}(\text{delay})$

**upon event** $\langle\text{Timeout}\rangle$ **do**:
1. **if** $\text{alive} \cap \text{suspected} \neq \emptyset$ **then** #gemini
	1. **note**: if a previously `suspected` process replied (is in `alive`), our timeout was too short $\implies$ increment `delay`! *(Note: $\neq \emptyset$, not $= \emptyset$!)* #gemini
	2. $\text{delay} := \text{delay}+\Delta$
2. **forall $p\in\Pi$ do**:
	1. **if $(p \not\in \text{alive}) \land (p \not\in \text{suspected})$ then** *(condition for `Suspect`)*
		1. $\text{suspected} := \text{suspected} \cup \{ p \}$
		2. **trigger** $\langle\diamond \mathcal P, \text{Suspect}\mid p \rangle$
	2. **else if** $(p \in \text{alive}) \land (p \in \text{suspected})$ **then**: *(condition for `Restore`)*
		1. $\text{suspected} := \text{suspected} \setminus \{ p \}$
		2. **trigger** $\langle\diamond \mathcal P, \text{Restore}\mid p \rangle$
	3. **trigger** $\langle pl, \text{Send} \mid p, [\text{HeartbeatReq}]\rangle$
3. $\text{alive} := \emptyset$
	1. **note**: reset and wait for heartbeats in the next period to refill $\text{alive}$
4. $\text{starttimer}(\text{delay})$

**upon event** $\langle pl, \text{Deliver} \mid q, [\text{HeartbeatReq}]\rangle$ **do**:
1. **trigger** $\langle pl, \text{Send} \mid q, [\text{HeartbeatRepl}]\rangle$

**upon event** $\langle pl, \text{Deliver} \mid p, [\text{HeartbeatRepl}]\rangle$ **do**:
1. $\text{alive} := \text{alive} \cup \{p\}$ #gemini


# correctness of `Increasing Timeout`
**Strong Completeness (`EPFD1`)**: if $p$ crashes:
* it stops sending `HeartbeatRepl` messages;
* after all its in-flight messages are delivered, $p$ will never be added to `alive` again, so every correct process will suspect $p$;
* **no process will revise the judgment**: since a crashed $p$ never sends another `HeartbeatRepl`, the `Restore` condition ($p \in \text{alive} \land p \in \text{suspected}$) can never be triggered again, so $p$ remains in `suspected` permanently. #gemini

**Eventual Strong Accuracy (`EPFD2`)**: after unknown stabilization time $t$, the system becomes synchronous:
* any message sent by a correct process $p$ to a correct $q$ is delivered within an (unknown) bounded time $\text{max\_delay}$;
* **what if correct $p$ was wrongly suspected by $q$?**
	* since $p$ is alive, its `HeartbeatRepl` eventually arrives at $q$, so $p \in \text{alive} \cap \text{suspected} \neq \emptyset$: $q$ triggers `Restore` and increases $\text{delay} := \text{delay} + \Delta$;
	* if the new $\text{delay} < 2\cdot\text{max\_delay}$, $q$ may falsely suspect $p$ again, and upon receiving $p$'s reply it will increment $\text{delay}$ again; #gemini
	* after a **finite number of mistakes**, $\text{delay} \ge 2\cdot\text{max\_delay}$, after which $q$ never suspects $p$ again. #gemini

**Lemma (Property of `suspected` — Slide 40)**: let $p_{1},p_{2}$ be two correct processes with sets $\text{suspected}_1$ and $\text{suspected}_2$.
* **Stabilization time**: there exists a time $t$ after which $\text{suspected}_1 = \text{suspected}_2$ permanently (both equal the exact set of crashed processes).

**proof**: by contradiction, suppose after stabilization there exists $p \in \text{suspected}_1$ with $p \notin \text{suspected}_2$:
* if $p$ is **correct**, then $p \in \text{suspected}_1$ violates **Eventual Strong Accuracy (`EPFD2`)**;
* if $p$ is **crashed**, then $p \notin \text{suspected}_2$ violates **Strong Completeness (`EPFD1`)** $\square$.

