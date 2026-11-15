> registrazione di luca part 1

**Shared memory and registers**: we find a logical variable divided by different processes.
* everyone holds a local copy.

**goal**: create a simulator using messages to create a shared variable.


we will implement:
* **read operation**: $\text{read}() \to v;$ returns the value $v$ stored in the register. #gemini
* **write operation**: $\text{write}(v) \to \text{WriteReturn};$ updates the register value to $v$ and returns confirmation. #gemini

these operations will take a certain amount of time to complete:
* **invocation**: a certain operations starts a write operation at a certain time.
* **return**: the operation just return the status, when its completed, in this task `null`.
	* the `read` operation returns the actual value.
* there will be multiple types of registers.

**atomic**: an operation is a single atomic action, and cannot be interrupted or divided.
* the operation itself is not atomic, we need to do some work to make operations atomic

**assumptions**: 
* **register**: stores positive integers, initialized to 0.
* each written value is univocally identified (so we write down a value only one time)
	* to solve this problem, we attach the timestamp to the value to write.
* its not possible for the same processes to invoke operations on the same register at the same time.

**failed operation**: an invoked operation that carashes before completing.

**crashed operation**: an operation that crashes is concurrent with any other operations starting after.
* because the operation that crashed did not return.


## register semantics
**strictly serialised semantic**: we imagine that operations are serialized trough a lock. Operations are strictly exectued when the lock is released
* **assume**: no failures
* **liveness**: each operation eventually terminates
* **safety**: each read returns the last value written
* we cannot implement it witout losing performances, we have to take the lock, and stop other processes!
	* serializing costs a lot in distributed systems.

**concurrency semantic**: what happens if we read while a write an operation is executing? what happens if we have write while someone is writing?
* several process can access the register
* concurretn access
* no failures

**failure semantic**: what happens if a write fails and the we read?

**goal**: find a set of useful semantics to have a working concurrent system.
* we will define the semantics focusing on the read operation.
* we will restrict what read can do.

## (19:00) regular consistency

$(X,Y)$ register: 
* $X$ number of processes that can write
* $Y$ number of processes that can read
* $(1,1)$: one can write and one can read
	* **exam trap**: you can have $(1,1)$ in a system with 1000 processes for example
* $(N,N)$: $N$ can write and $N$ can read
* *24:00 (`#gemini`)*: in $(1,1)$ and $(1,N)$ registers, it is **known a priori** which process(es) can write and which can read (and in $(1,N)$, the writer is also included among the $N$ readers). #gemini

**Module 4.1 — `(1, N)-RegularRegister` (`onrr`)**: #gemini
* **Events**: Requests `<onrr, Read>`, `<onrr, Write | v>`; Indications `<onrr, ReadReturn | v>`, `<onrr, WriteReturn>`. #gemini
* **ONRR1 (Termination)**: if a correct process invokes an operation, then the operation eventually completes (even if other processes fail). #gemini
* **ONRR2 (Validity)**: a read that is not concurrent with a write returns the **last value written**; a read concurrent with a write returns either the **last value written** or the value **concurrently being written**. #gemini

**example of not regular execution**:
* write 5 (completes)
* then we read and returns 0 (here is the problem)
* then we read and get 5

**example of regular**:
* write 5
* while writing 5, we read and get 0 (last value written or concurrent write)

**strange example**:
* it is ok to start a read
* we start **AFTER** a write with value 6 (after 5 was written)
* the read is concurrent with the write
* the read returns 6. OK
* we schedule another concurrent read and returns 5
	* ok because (last value written or concurrent write)

> **(29:00) Note**: if the read is not concurrent with any write, it must return the last value written. Else we can return a set of different values.

> if a process crashes while writing 8 (after 5), `write(8)` never returns, so it is **concurrent with every subsequent read forever**: any future read can legally return either $5$ or $8$ (and even alternate between them)! #gemini


**how we implement**?
* every process, hold a copy of the value.
* and we have to synch those copy of the same value.
* say $p_{0}$ is the **only writer**, and wants to write $5$
	* he has to write down in its local copy the value
	* he has to broadcast 5 to everyone.
	* everyone holds a variable with the value of the register that can be modified only by $p_{0}$
* a write terminates when i receive an ack from all the other readers.

> look at examples of execution.

**Read-One-Write-All `(1,N)` Regular Register (Algorithm 4.1)**: #gemini
```text
Uses: BestEffortBroadcast beb, PerfectPointToPointLinks pl, PerfectFailureDetector P.

upon event <onrr, Init> do
    val := ⊥; correct := Π; writeset := ∅;

upon event <P, Crash | p> do
    correct := correct \ {p};

upon event <onrr, Read> do
    trigger <onrr, ReadReturn | val>;

upon event <onrr, Write | v> do
    trigger <beb, Broadcast | [WRITE, v]>;

upon event <beb, Deliver | q, [WRITE, v]> do
    val := v;
    trigger <pl, Send | q, ACK>;

upon event <pl, Deliver | p, ACK> do
    writeset := writeset ∪ {p};

upon correct ⊆ writeset do
    writeset := ∅;
    trigger <onrr, WriteReturn>;
```
*(`#gemini`: algorithm from Distributed Registers I slides / Alg. 4.1)*

**number of messages**:
* a write generates at most $2n$ point-to-point messages: #gemini
	* $n$ for broadcast (`beb`)
	* at most $n$ for `ACK` #gemini
* a read generates 0 messages, it's local.


**44:30 resiliency (how many failures we can tolerate)**:
 we can tolerate any amount of failures ($f < n$) #gemini
 * understand what happens if we remove $\text{writeset} := \emptyset$
 * we do not wait for acks at the next write (`correct \subseteq writeset` triggers immediately on stale ACKs from the previous write, returning before processes update `val`, violating Validity). #gemini

**time to complete a write**: 2 steps
**time to complete a read**: 0 


## correctness

**termination**:
* **read**: immediate, it's local!
* **write**: if the writer is correct, BEB will reach other correct processes and $\mathcal{P}$ completeness detects crashed ones. #gemini

**validity**:
* **read is not concurrent**: any write preceding the read has completed, meaning every correct process (including the reader) updated its copy and sent an `ACK`. #gemini
* **read is concurrent**: by the no-creation property of the channels, the returned value is either the last value written or the one concurrently being written. #gemini

what if a broadcast message is lost? (Impossible with reliable `pl` + `beb` unless sender crashes; if `p3` never receives `WRITE`, it keeps the old value, e.g., $0$). #gemini

**example**: is it possible to write 5 (after 1), and then $p_{1}$ reads 5 and then reads 1?
* **Answer**: * [INSERT HERE] (check if `(1,N)`-regular allows new-old inversion during a concurrent `write(5)`). #gemini

> registrazione luca perte 2 da ora in poi

**assume**: now we have a not perfect failure detector. so we can see $p_{2}$ crashed but in reality its working.
* we return from write witout waiting $p_{2}$ ACK
* and $p_{2}$ can read an invalid value because he might start a read before receiving the broadcast, but at the same time the write was completed.


## fail silent variant
can we adapt the algorithm to be fail-silent?
* (4:50) means that we don't need a fail detector


**assumptions**:
* $N$ processes: 1 writer and $N$ readers
* at least $\frac{n}{2}+1$ correct processes, and $f < \frac{n}{2}$

**write**:
* do BEBCast
* wait for $\frac{n}{2}+1$ ACKS
* so $p_{1}$ send in broadcast the value to all processes
* the faster $\frac{n}{2}+1$ reply ACK, and $p_{1}$ terminates the write.
* we know that a quorum contains the last value

**read**:
* what if we read locally? it would not work because processes not in the quorum would read an old value while the operation concluded.
* we have to read using messages, we ask the register value to $\frac{n}{2}+1$ processes (another quorum)
* because two quorums intersect, we will eventually get the right value.

**what happens when**:
* half of the quorum says the value is 1 and the other half is 2? we do not have a majority
* we need to attach a timestamp to the value.
* the highest timestamp is the latest value.

**Majority Voting `(1,N)` Regular Register (Algorithm 4.2)**: #gemini
```text
Uses: BestEffortBroadcast beb, PerfectPointToPointLinks pl.

upon event <onrr, Init> do
    (ts, val) := (0, ⊥); wts := 0; acks := 0;
    rid := 0; readlist := [⊥]^N;

upon event <onrr, Write | v> do
    wts := wts + 1;
    acks := 0;
    trigger <beb, Broadcast | [WRITE, wts, v]>;

upon event <beb, Deliver | p, [WRITE, ts', v']> do
    if ts' > ts then (ts, val) := (ts', v');
    trigger <pl, Send | p, [ACK, ts']>;

upon event <pl, Deliver | q, [ACK, ts']> such that ts' = wts do
    acks := acks + 1;
    if acks > N/2 then
        acks := 0;
        trigger <onrr, WriteReturn>;

upon event <onrr, Read> do
    rid := rid + 1;
    readlist := [⊥]^N;
    trigger <beb, Broadcast | [READ, rid]>;

upon event <beb, Deliver | p, [READ, r]> do
    trigger <pl, Send | p, [VALUE, r, ts, val]>;

upon event <pl, Deliver | q, [VALUE, r, ts', v']> such that r = rid do
    readlist[q] := (ts', v');
    if #(readlist) > N/2 then
        v := highestval(readlist);
        readlist := [⊥]^N;
        trigger <onrr, ReadReturn | v>;
```
*(`#gemini`: algorithm from Distributed Registers I slides / Alg. 4.2)*

> **note**: with $N=4$ i can tolerate at most $1$ failure ($f < N/2$). #gemini

* `wts`: write timestamp (to distinguish newer writes and match `[ACK, ts']` on the writer). #gemini
* `rid=0`: read identifier, needed to discard stale `[VALUE, r, ts', v']` messages from an old read request when they arrive late. #gemini

on $<\text{beb}, \text{Deliver} \mid p, [\text{WRITE}, ts', v']>$: #gemini
* we update `(ts, val)` only if `ts' > ts` (avoids overwriting a newer value with a delayed out-of-order write). #gemini
* then i send `[ACK, ts']` in any case so the writer knows which write is acknowledged. #gemini

> IN QUESTO MOMENTO ALFREDO E' USCITO CON LA TIPA ROSCIA

## dim.
**termination**: from properties of `pl`/`beb` and majority of correct processes ($> N/2$ respond). #gemini
**validity**: write waits for $> N/2$ ACKs, and read waits for $> N/2$ `VALUE` replies. Any two quorums intersect in at least one process, which holds a timestamp $\geq$ the timestamp of the latest completed write; `highestval(readlist)` thus returns either the latest completed value or a concurrently written one. #gemini

> [!warning] Exercise & Complexity #gemini
> Trace the `(1,3)` regular register execution scenario and verify: #gemini
> * **Message complexity**: write = * [INSERT HERE], read = * [INSERT HERE] #gemini
> * **Communication steps**: write = * [INSERT HERE], read = * [INSERT HERE] #gemini
> * **Resiliency**: how many faults $f$ can be tolerated? * [INSERT HERE] (ref: *Distributed Registers I* slides) #gemini