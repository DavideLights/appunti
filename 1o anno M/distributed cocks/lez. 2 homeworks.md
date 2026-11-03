# safety or liveness?
**"fairness of an execution"**: it is a liveness property, we cannot find an instant $t$ where the execution is unfair or fair. A system is fair if it will eventually grant a certain attribute or property to a process, so its liveness.

**"An execution E can contain at most $f$ failures"**: its a safety property. If we can identify a process fails, then we can show an exectuion where there is an instant $t$ where we have more than $f$ failures.

**"If a process $p$ experience a $\text{crash}(p)$, then it eventually experiences also a $\text{recovery(p)}$ (an event starting again $p$)"**: it's liveness, because for every istant $t$ where $p$ crashes, there is $t'>t$ s.t. we can have a recovery for that process. it's the definition of a liveness property.

**"If a process $p$ experiences a $\text{recovery}(p)$, then this recovery happens at most $k$ events after its failure"**: it's a safety property. The bad thing is recovering strictly after $k$ events: if $\text{recovery}(p)$ occurs at step $t > \text{crash} + k$, the property is violated on that finite prefix and cannot be cured. (Note: crashing and never recovering does NOT violate it!). #gemini

# write 3 safety and 3  liveness prop.
$\text{SAFE1}$: No process delivers the same message more than once (No duplication). #gemini

$\text{SAFE2}$: A process $p$ sends a reply to $q$ only if $p$ previously received a request from $q$ (No reply without request). #gemini

$\text{SAFE3}$: At most one process is granted the critical resource at time $t$ (Mutual Exclusion). #gemini

$\text{LIVENESS1}$: if a process $p$ receives requests from at least $\frac{N}{2}$ processes, then he will eventually reply to all the requests.

$\text{LIVENESS2}$: a process $p$ is a correct process, then he will eventually process all the payments received.

$\text{LIVENESS3}$: if $p$ is correct and everyone else is not correct, then $p$ will eventually shut down.


# does time-bounded recovery imply eventual recovery
**No**. The property states: *"If $p$ experiences a recovery, then it happens in $\leq k$ events"*. If $p$ crashes and **never** recovers, the premise is false, so the implication is vacuously true. Thus an execution where $p$ stays dead forever satisfies time-bounded recovery but violates eventual recovery. #gemini

# improve the writing
**Decompose into safety and liveness** (badly written because it mixes both): #gemini
* **Liveness** (eventual progress): If a correct process $p$ outputs $O_p$, then every correct process $q$ eventually outputs a set $O_q$. #gemini
* **Safety** (containment / consistency): For any two processes $z, t$, if $z$ outputs $O_z$ and $t$ outputs $O_t$, then either $O_z \subseteq O_t$ or $O_t \subseteq O_z$ (incomparable sets can never be output). #gemini
