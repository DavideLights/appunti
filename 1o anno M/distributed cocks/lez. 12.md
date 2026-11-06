# sequential consistency
Sequential consistency property, Lamport: 
* an exectuion is sequential consistent if the (read and write) operations by all processes on the data store were exectued in some sequential order
	* there is a global order
* and the operations of each indibidual process appear in this sequence in the order specified by its program.

**example slide 1**: the execution is not legal but we could rearrange it.
* the global order could not correspond to the "real time" order
* so we can **rearrange** operations, give a "**fictional**" global order.
* from outside the system you cannot determine the order

**example slide 2**:
* *there exists a global ordering that respects the local ordering seen by each register.*
* it means that we can rearrange order of operations but we have to respect the execution order inside the process $p_{i}$
* we cannot violate the local order seen by the process.

why do you need sequencial consistency? gemini tell me!

differences:
* regular and not sequential consisten
* not regular and sequential consisency 
# atomicity
**Atomicity**: each operation should appear to take effect instantaneusly at some moment between its start and completion.

**or linearizability (synom)**: we can find a moment inside an operation afther wich everyone in the system see the change. the exact point were we read a value, were we write, or when we do something special.

**TODO**: look at the slides and play with linearizability!
* **example**: asdf

if execution is **linearisable** $\to$ **regular**.
* linearisable execution we can find a moment in wich operation are done
* we can fino also a regular exectuion (??)

slide with relations ships.

gemini: explain what regular means and resume using a table differences.

exercise: very hard
* $\text{read}_{2}() \to 2$
	* so $\text{write}(2)$ has been linearised before $\text{read}_2$
	* so $\text{read}_{3}$ cannot return 1
* **note**: $\text{read}_{5}$ can return $\{ 2,3 \}$ if $\text{read}_{3}$ reads $2$
* **note**: $\text{read}_{5}$ can return $\{ 3 \}$ if $\text{read}_{3}$ reads $3$. 
* **note**: $\text{write(3)}$ crashes!

**so**: what a $\text{read}_{i}$ returns depends on what $\text{read}_{j}$ returned with $j<i$.

**tree techinque used by teacher sborz**:
* start from the first $\text{read}_{1}$
* children are the value that this can read
* from the children we apply $\text{read}_{2}$ assuming what $\text{read}_{1}$ read.
* **and so on and so forth**.

gemini: whats the difference between atomic and regular.

## atomic register

$(1,N)$ register specification properties:
1. **termination**: if a correct process invokes an operation ...
2. **validity**: ...
3. **ordering**: if a read returns $v_{2}$ after a read that precedes it has returned $v_{1}$, then $v_{1}$ has not been written after $v_{2}$.
	1. **equivalent** to linearization points.



**gemini**: table differences between regular, atomic, sequential


**atomic register interface**: report it here.


## use regular register to implement atomic register
**fact 1**: read operation cannot be local. This read operation depends from other processes, so it needs to send messages.
* **goal**: understand when a write has been linearized

we want to avoid the fact that:
* $p_{4}$ reads 5 at $t$
* $p_{5}$ reads 7 at $t'>t$

**solution**: a read operation impose a write to everyone else. **read-impose write-all**
* we also must discard old read-impose, write messages using attaching a timestamp to the reader's write messages
* the reader starts a write operations and waits for ACK from everyone else.
* the reader waits 

## read-impose write-all algorithm
1. **reading**: i have to rember if i am the writer or the reader **upon** $\text{correct} \subseteq \text{writeset}$
2. i have to send ACK in anycase in **upon event** $<\text{beb, Deliver} | p \dots>$
3. the write terminates when $\text{correct} \subseteq \text{writeset}$
	1. we set $\text{reading = FALSE}$
	2. it just terminates when at least one correct process sends me an ACK????

**complexity**: $2n$ messages.

**time complexity**: 2
* one broadcast
* then i wait for ack.

## correcteness for read-impose write-all
**termination**: as for regular register (1,N)
**validity**: as for regular register (1,N)

**ordering proof**: it simply look at the slides


## implementation for fail silent
**assumption for n of failures**: $f < \frac{n}{2}$
* $\frac{n}{2}$ then most of the time the implementation uses quorum.

**writer**: waits for a quorum of ack
**reader**: waits for a quorum of ack.


generally, to replace a failure detector, we use a quorum.

gemini: why do we have two fase? 
* ask phase durin read/
* impose phase during write?

gemini: why this algorithm is correct? why do we need a read to help writer to ensure that the algorithm is atomic? diocane?

me so rotto er cazzo della magistrale basta






