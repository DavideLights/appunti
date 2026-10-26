
implementation in fail-stop.

## URB in $\text{FAIL-SILENT}$

**objective**: build a URB in $\text{FAIL-SILENT}$. In order to create the algorithm we have to bound the number of failures.

**quorum**: 
* we have $n$ proc in our set o f total processes $P$
* a quorum is any subset of at least $\frac{n}{2}+1$ processes.
* **note**: two quorums in a system intersect in at least 1 process.
* if the intersection is empty, then the size of the union must by the sum of the sizes of the quorum. (???)

if in the sistem the number of failure is $f < \frac{n}{2}$
* number of correct process: we have always at least $c \geq \frac{n}{2}+1$
* quorum: the number of correct process $c$ is a quorum 

if i take another quorum in the system, they intersect in at least 1 process.

**idea 1**: if $p$ has seen a process, then its safe to deliver it
* assuming $\frac{f}{2}<n$ is a safe number of fails.

**we can modify**  *All-AckUniform Reliable Broadcast alogrithm* to build URB over Fail Silent. (???) into *Majority-Ack Uniform Reliable Broadcast*.

**question**: what if in `candeliver` (inside the algorithm) we have  $\text{return } |\text{ack}(m)| \geq f+1$
* we violate the **validity property**.
* assume 6 processes, with 3 faulty.
* if every running process sees 3 acks, they do not know if they come all from faulty ones.

**takeaway**:
* if you have perfect failure detector: you can tollerate $f<n$ fails
* if you do not have perfect failure detector: you can tollerate $f< \frac{n}{2}$


**notes for excericeses:**
* Reliable is also uniform
* uniform is also best effort
# ordered communications (part 1)

**ordered communications**: define guarantees on the deliveries inside a group of processes.

type:
* FIFO ordering
* Casual orderin
* Total ordering of deliveries

We do we need ordered? client cancels a prenotation before it is booked even if he requested service in a different order.

**FIFO BROADCAST**:
* FRB5 - Fifodelivery, FIFO delivery: ...
* implemented using **counters**.

**FIFO BRD algorithm**:
`upon event <frb, init> do`
* `lsn = 0` its the local sequence number.
* `pending = emptyset`
* $\text{next} := [1]^N$ an array of 1.

`upone event <frb, broadcast | m> do`:
* $\text{lsn} = \text{lsn}+1$
* $\text{trigger } <\text{rb}, \text{Broadcast}, [\text{DATA}, \text{self}, m, \text{lsn}]>$

`upon event <rb, Deliver | p, [DATA, s,m,sn]>`:
* $\text{pending}:= \text{pending} \cup \{ (2,m,sn) \}$
* while exists $(s,m',sn') \in \text{pending}$ s.t. $sn'=\text{next}[s]$ do
	* $\text{next}[s] = \text{[s]}+1$
	* $\text{pending} = \text{pending} \setminus \{ (s,m,sn') \}$
	* trigger $<\text{frb}, \text{Deliver} | s,m'>$

try executing the algorithm to understand how it words

**order**: messages between different senders are not ordered. we ensure only that messages sent from $p_{i}$ are received in an orderered way.

FIFO is **orthogonal** with reliability guarantess

sometimes FIFO is not enough: example in a bank system using broadcast.
* in this system you have to sign transactions
* check the capability for the transaction in your local copy
think about that looking at the example.