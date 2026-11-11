# perfect failure detection proofs
**Correcteness**: assuming $p_{1}$ crashes at time $t$, then $p_{0}$ detects it at most by time $t+2\Delta$:
1. time $t+\Delta$: $p_{0}$ sends an heartbeat request
2. time $t+2 \Delta$: $p_{0}$ did not receive the heartbeat reply.

**Strong agguracy**: if $2\text{max\_delay} \leq \Delta$
* if $p$ was detected as faulty but its alive, then
1. $\text{heartbeatREQ}$ did not reach $p$ by the timeout.
2. $\text{heartbeatREPL}$ did not reach me by the timeout.
3. both contraddict the assumption  $2 \text{max\_delay}$

> its impossible for $\text{REQ}$ or $\text{REPL}$ to not reach the distance before the timeout if $2text$

**PFD1**: *strong completeness*. **Eventually** every process that crashes is permanently detected by every correct process.

**PFD2**: strong accuracy. If a process $p$ is detected by any process then $p$ has crashed.

**example of PFD1**:
![[Pasted image 20261111112612.png]]

> **note**: PDF1 says eventually. The algorithm specifies the exact latency

## improving $\mathcal P$
> If at time $t$ i do not have process $p$ in my detected set, can i state that $p$ is alive at time $t$? **NO**.

**NO:** Because, there is no algorithm that says what is exactly happening at time $t$. 

**What do we know?** the world of the messages that has a delay $d$, at a time $t$ tells us how te system looks at time $t-d$.

**Can we use silence instead of messages**?![[Pasted image 20261111115330.png]]
*  assume a global skew $\delta$
* and a syncrhonous link with a certain $\text{max\_delay}$ and a $\text{min\_delay} > \delta$

## round-based $\mathcal P$
