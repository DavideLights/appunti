> registrazione di luca part 1

**Shared memory and registers**: we find a logical variable divided by different processes.
* everyone holds a local copy.

**goal**: create a simulator using messages to create a shared variable.


we will implement:
* **read operation**: $\text{read}() \to v;$ it returns .
* **write operation** ...

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
* 24:00: non ho capito

$(1,N)$ register:
* **termination**: if a correct process invokes an operation, then the operation will terminate even if other processes fail.
* **validity**: a read operation returns eather the **last value written** or the value **concurrently written**.
	* if the write is not concurrent i check the last value on the register.

**example of not regular execution**:
* write 5
* then we read and returns 0 (here is the problem)
* then we read and get 5

**example of regular**:
* write 5
* while writing 5, we read and get 0 (last value written or concurrent write)

**strange example**:
* it is ok to start a read
* we start **AFTER** a write with value 6
* the read is concurrent with the write
* the read returns 6. OK
* we schedule another concurrent read and returns 5
	* ok because (last value written or concurrent write)

> **(29:00) Note**: if the read is not concurrent with any write, it must return the last value written. Else we can return a set of different values.

> if a process crashes while writing 8, then a read can eventually return the value 8!


**how we implement**?
* every process, hold a copy of the value.
* and we have to synch those copy of the same value.
* say $p_{0}$ is the **only writer**, and wants to write $5$
	* he has to write down in its local copy the value
	* he has to broadcast 5 to everyone.
	* everyone holds a variable with the value of the register that can be modified only by $p_{0}$
* a write terminates when i receive an ack from all the other readers.

> look at examples of execution.

$\text{upon event} <\text{onrr}, \text{Init}> \text{do}$:
1. $\text{val} := 0$
2. $\text{correct} = \Pi$
3. $\text{writeset} = \emptyset$

> look at the algorithm on the slides!


**number of messages**:
* a write generates $2n$ messages.
	* n for broadacst
	* n for ACK
* a read generates 0 messages, its local.


**44:30 resiliency (how many failures we can tollerate)**:
 we can tollerate any amount of failures
 * understand what happens if we remove $\text{writeset} := \emptyset$
 * we do not wait for ack at the next write.

**time to complete a write**: 2 steps
**time to complete a read**: 0 


## correctness

**termination**:
* **read**: immediate, its local!
* **write**: if the writer is correct, BEB, will reach other correct processes and we can detect who is not correct.

**validity**;
* **read is not concurrent**: any write started before any read has been completed because hi sent him an ack, so i have a correct copy of the value.
* **read is concurrent**: diocane 

what if a broadcast message is lost?
* the a process $p_{3}$ could always read the old value, example $0$.

**example**:  is it possible to write 5, and then $p_{1}$ reads 5 and then reads 1?

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

> look at the code

> **note**: with $N=4$ i can tollerate at most $1$ failure.

* `wts`: write timestamp
* `rid=0` needed to discard ACKS from an old read request that might arrive later to other processes.

on $<\text{beb}, \text{Deliver} \dots>$:
* we update the value only if the timestamp is greater of the local value.
* then i send the ack with the timestamp
* so the writer knows for what message is the ack.

> IN QUESTO MOMENTO ALFREDO E' USCITO CON LA TIPA ROSCIA

## dim.
**validity**: write waits for $\frac{n}{2}+1$ ACKS, and read too. We have two quorums that intersects in at least one process. The intersection is the set of processes with the latest value for the register.

exrcise 