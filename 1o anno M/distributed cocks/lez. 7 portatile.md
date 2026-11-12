# alg. **round-based** $\mathcal P$


**upon event INIT**:
* $C_{v}$ **note**: synchronizer's clock
* $T$: how long is a round? $T>2(\text{max\_delay} + \delta)$
* $\text{Correct}= \{ p_{0},p_{1},\dots,p_{n} \}$
* $\text{RoundAlive} = \text{Correct}$
* $r=-1$

**upon event** $C_{v} = kT$ for some $k\in \mathbb N^+$:
1. $r=r+1$
2. **for** all $p_{j} \in \text{Corrects} \setminus \text{RoundAlive}$ **do**
	1. $\text{Corrects}= \text{Corrects} \setminus \{ p_{j} \}$
	2. $\text{TRIGGER} <\text{Crash}|p_{j}>$
3. $\text{RoundAlive} = \{ p_{i} \}$
4. for all $p_{j} \in \text{Corrects}$ do:
	1. $\text{SEND}(<p_{i}, \text{BEAT}>)$

**upon event** $DELIVERY(<p_{j}, \text{BEAT}>)$
1. $\text{RoundAlive} = \text{RoundAlive} \cup \{ p_{j} \}$

![[Pasted image 20261111135114.png]]
![[Pasted image 20261111135145.png]]

**FACT 1**: if i send a BEAT, i am alive
**FACT 2**: if i don't send a BEAT, i am dead.

**we have to show that**:
* if i send a BEAT to $p$
* and my round number is $r$
* then $p$ gets the BEAT in round $r$

**proof**:
* my BEAT is sent at round $r$
* since clocks are bounded by the skew:
	* if i send BEAT at time $t$, when i'm in round $r$
	* then $p$'s clock will be at most at time $t$
	* $t-\delta + T = t- \delta + 2\delta + 2\text{max\_delay} > t+\delta+\text{max\_delay}$
	* gemin explain formula
	* by the delay: my beat reaches $p$ in the interval $(t+\delta, t+\text{max\_delay})$


gemini: what does it mean strong completeness and strong accuracy.

**strong completeness**: if $p$ dies i will not receive the beat and signal it trought CRASH.

**stron accuracy**: if i do not receive the BEAT from $p$ its only because $p$ did not sent it, and so it's dead.


# round based and synch systems
**syncrhonous systems abstraction**: time is divided in logical slots called rounds

**assumptions**:
* **switch time**: all $p$ switch from a round to another at the **same time**
* **messages**: if $p$ sends a message avery receiver seed the message at the same round

![[Pasted image 20261111140535.png]]

can we design a round based $\mathcal P$?
![[Pasted image 20261111141905.png]]![[Pasted image 20261111141934.png]]

# eventually perfect failure detectors
**Take Exclude on timeout algorithm**: what if we decrease $\Delta$?

**system model**:
* partial synchrony: gemini what does this mean.
* crash failures
* perfect point-to-point links

**in a synch model**:
* there is a (unkown) time $t$ after that crashes can be accurately detected.
* before $t$ the systems behaves as an asynchronous one
	* the failure detector makes mistakes
	* the notion of detection becomes suspicios (gemin what does this mean)

$\text{EventuallyPerfectFailureDetector} \diamond \mathcal P$:
* **Events**:
	* **Indication**: $<\diamond \mathcal P, \text{Suspect} | p>$: notifies that $p$ is suspected to have crashed
	* **Indication**: $<\diamond \mathcal P, \text{Restore} | p>$: notifies that $p$ is not suspected anymore
* **Properties**: they ansure that a set of supsected processes **stabilises** on a correct process.
	*  **EPFD1**: *strong completeness*. Eventually, every process that crashes is perma-nently suspected by every correct process.
	* **EPFD2**: Eventual strong accuracy: Eventually, no correct process is suspected by any correct process.

what we will use?
* timeouts to suspect processes
* suspects may be wrong
	* $p$ may suspect $q$ because timeout was too short
* $\diamond \mathcal P$ adjust timeout when we receive a message from $q$
* if $q$ REALLY crashed, $p$ will not change its judgement.

# eventually perfect fd $\diamond \mathcal P$
**upon event $<\diamond \mathcal P, \text{Init}>$ do**:
* $\text{alive} = \Pi$
* $\text{suspected} = \emptyset$
* $\text{delay} = \Delta$
* $\text{starttimer}(\Delta)$

**upon event** $<\text{Timeout}>$ **do**:
1. **if** $\text{alive} \cap \text{suspected} = \emptyset$ **then**
	1. **note**: if we did not suspect anyone, then we can increment the delay
	2. $\text{delay} := \text{delay}+\Delta$
2. **forall $p\in\Pi$ do**:
	1. **note**: update $\text{alive}$ and $\text{suspected}$
	2. **if $(p \not\in \text{alive}) \land (p \not\in \text{suspected})$ then** (condition for *Suspect*)
		1. $\text{suspected} = \text{suspected} \cup \{ p \}$
			1. **note**: because its not alive but not in suspected.
		2. **trigger** $<\diamond \mathcal P, \text{Suspect}|p >$
	3. **else if** $(p \in \text{alive}) \land (p \in \text{suspected})$ **then**: (condition for *Restore*)
		1. $\text{suspected} = \text{suspected} \setminus \{ p \}$
			1. **note**: its alive but still in suspected.
		2. **trigger** $<\diamond \mathcal P, \text{Restore}|p >$
	4. **trigger** $<pl, \text{Send} | p, [\text{HeartbeatReq}]>$
3. $\text{alive} = \emptyset$
	1. **note**: we will wait for hartbeats and fill $\text{alive}$
4. $\text{starttimer}(\text{dalay})$

upon event $<pl, \text{Delive} | q, [\text{HeartbeatReq}]>$ do:
1. trigger $<\text{pl}, Send | q, [\text{HeartbeatRepl}]>$

upon event $<pl, \text{Delive} | q, [\text{HeartbeatRepl}]>$ do:
1. $\text{alive} = \text{alive} \cup {p}$


# correcteness
**strong completeness**: if $p$ cashes
* it will stop sending messages
* it will be suspected by any correct $p$
* no process will revise the judgement. (gemini: what does this mean)

**eventual strong accuracy**: after a time $t$ the system becomes syncrhonous.
* so, $p$ sent to $q$ will be delivered in a bounded time
* the max delay is unknow to us
* what if $p$  **was wrongly suspected**?
	* during the execution $q$ may increases its delay
	* then we'll be synchronous forever
	* if $\text{delay}< \text{max\_delay}$ eventually $q$ suspects it and increase $\text{delay}$
	* since we are syncrhonous and $\text{delay}$ will reach $2 \text{max\_delay}$ in a finite number of errors.

**lemma**: let $p_{1},p_{2}$ be correct processes.
* let $\text{suspected1 and suspected2}$ their sets.
* **stabilization time**: there is $t$ after wich $\text{suspected1=suspected2}$

**proof**: by contraddiction
* $\exists p \in \text{suspected1}$ and $\notin \text{suspected2}$
* if $p$ is **correct**, then violates strong accuracy.
* otherwise it violates strong completeness.

# alive - leader election
how to know who is alive?

**leader election spec.**:
* **Events**:
	* Indication: $<le, \text{Leader}|p>$ indicates that $p$ is the leader
* **Properties**:
	* **LE1**: *Eventual detection*: Either there is no correct process, or some correct process is **EVENTUALLY**Z elected as the leader.
	* **LE2**: *Accuracy*: If a process is leader, then all previously elected leaders have crashed.

**stabilized**: when a leader is determined and does not change.


![[Pasted image 20261111184934.png]]

gemini what does this mean:
![[Pasted image 20261111222412.png]]

# leader election alg.
**how it works**? we can do leader election just my electing a correct process with highest rank (process id)

**upon event** $<le, \text{Init}>$ **do**:
* $\text{suspected} = \emptyset$
* $\text{leader} = 0$

**upon event** $<\mathcal P, \text{Crash}|p>$ **do**:
* $\text{suspected = suspected} \cup \{ p \}$

**upon** $\text{leader} \neq \text{maxrank}(\Pi \setminus \text{suspected})$ **do**:
* $\text{leader} = \text{maxrank}(\Pi \setminus \text{suspected})$
* **trigger** $<le, \text{Leader} | leader>$

**correcteness**:
* **eventual detection**: come from the completeness of $\mathcal P$
* **accuracy**: from the strong accuracy of $\mathcal P$ and the fact that id's of process form a total order when ranking.
