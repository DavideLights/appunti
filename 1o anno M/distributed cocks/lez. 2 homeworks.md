# safety or liveness?
**"fairness of an execution"**: it is a liveness property, we cannot find an instant $t$ where the execution is unfair or fair. A system is fair if it will eventually grant a certain attribute or property to a process, so its liveness.

**"An execution E can contain at most $f$ failures"**: its a safety property. If we can identify a process fails, then we can show an exectuion where there is an instant $t$ where we have more than $f$ failures.

**"If a process $p$ experience a $\text{crash}(p)$, then it eventually experiences also a $\text{recovery(p)}$ (an event starting again $p$)"**: it's liveness, because for every istant $t$ where $p$ crashes, there is $t'>t$ s.t. we can have a recovery for that process. it's the definition of a liveness property.

**"If a process $p$ experiences a $\text{recovery}(p)$, then this recovery happens at most $k$ events after its failure"**: it's a safety property. The bad thing is recovering strictly after $k$ events: if $\text{recovery}(p)$ occurs at step $t > \text{crash} + k$, the property is violated on that finite prefix and cannot be cured.
# write 3 safety and 3  liveness prop.
$\text{SAFE1}$: No process delivers the same message more than once (No duplication). #gemini

$\text{SAFE2}$: A process $p$ sends a reply to $q$ only if $p$ previously received a request from $q$ (No reply without request). #gemini

$\text{SAFE3}$: At most one process is granted the critical resource at time $t$ (Mutual Exclusion). #gemini

$\text{LIVENESS1}$: if a process $p$ receives requests from at least $\frac{N}{2}$ processes, then he will eventually reply to all the requests.

$\text{LIVENESS2}$: a process $p$ is a correct process, then he will eventually process all the payments received.

$\text{LIVENESS3}$: if $p$ is correct and everyone else is not correct, then $p$ will eventually shut down.


# does time-bounded recovery imply eventual recovery
If recovery is time-bounded, then a process $p$ that crashed at an instant $t$ will recover before istant $k+t$ where $k$ is the bound. So if $p$ recover befor $k+t$ then we can say also that it eventually recovered.


# improve the writing
If a process $p$ outputs a set of integer $O_{p}$, then any other process $q$ outputs also a set $O_{q}$. For any two processes $z$ and $t$ we have $O_{z}$ subset of $O_{t}$ or $O_{t}$ subset of $O_{z}$.

The problem is that the property combines safety and liveness together, the liveness property should only target correct processes and we should use mathematical notation. #gemini

* **Liveness**: if $p$ outputs a set of integer $O_{p}$, the every correct process $q$ eventually outputs a set $O_{q}$.
* **Safety**: for any two processes $z,t$, if $z$ outputs $O_{z}$ and $t$ outputs $O_{t}$ then $O_z \subseteq O_t \lor O_t \subseteq O_z$.



