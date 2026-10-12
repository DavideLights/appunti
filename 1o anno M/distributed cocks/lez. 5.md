**previous lecture**: vector clock, lamport

# lamports algorithm mutual exclusion
**assume**: Request critical section $\to$ grant critical section $\to$ release. And the algorithm
* two grant of critical section cannot overlap in time between grant and release

**asume**: use of a FIFO link. otherwise algorithm doesn't work

**properties**:
* only 1 p gets critical section at a time: its a safety property, once we break this rule algorithm is not safe.
* if p requests critical section, eventually will get it: its a liveness property
* if the request of $p$ happens before $q$, then $q$ does not access: its a fairness property

**lamport algorithm**: assumes 0 crashes, otherwise it can broke forever.

**idea of the lamport algorithm**:
* you can enter the critical section only if you get response from other processes.
* you ask everyone, you wait for everyone and find an order on the grant requests from all the process.

Rivedere il codice per bene, potrebbe esse sbagliato.

`init`:
1. $\text{Requests} = \text{Acks} = \emptyset$. Set of $\text{Acks}$ contains the responses to my grant request.  
2. $\text{scalarClock} = 0$. **Lamport Clock**.
3. $\text{myRequest}= \text{Null (equivalente a Nil o 0)}$
4. $\Pi = \{ p_{0},\dots, p_{n-1}\}$. I need to know the set of processes from wich i expect a response.

`request`:
1. increase my scalar clock: $\text{scalarClock} += 1$
2. $\text{myReq} = (\text{REQ}, <i, \text{scalarClock}>)$, i send a request with my scalar clock
3. $\forall p \in \Pi$ $\text{FIFORequestLink}(p, \text{myReq})$, its sent also to myself.

`deliver_message(m: message)`:
1. $\text{scalarClock} = \text{max}(\text{clock(m)},\text{scalarClock})+1$. devi capire che vordi sta cosa!
2. se $m$ e' $\text{REQ}$:
	1. $\text{ReqSet} = \text{ReqSet} \cup \{ m \}$
	2. $\text{scalarClock} += 1$, because we are going to reply
	3. $\text{send FIFOPerfectLink}(\text{sender}(m), (\text{ACK}, <i, \text{scalarClock}>)$
3. if $m$ is $\text{ACK}$
	1. $\text{AckSet}  = \text{AckSet} \cup \{ m \}$

`critical section test`: (there are some conditions missing here, check slides)
1. if i'm the one with the lowest request, and i got acks with timestamp greather than my
2. we i have to check for acks timestamp? because we never remove acks from the ACK set, so we must be sure that old ack don't allow me to unlock critical section. 
	1. if i receive acks for the first request
	2. then a second request would need new acks.


Running example:
* blue arrow: it's a message exchanged between processes. its not part of the lamport algorithm, but increments the lamport clock.
* $p_{3}$: starts the request message with $(\text{REQ}, <\text{id}:3,\text{timeStamp}:3>)$
	* timestamp was 2, and then incremented
* $p_{1}$: receives the message, and updates  clock from 4 to $5$. send an ACK to $p_{3}$
* same for $p_{2}$
* imagine that you send the ack to yourself.

what if $p_{1}$ wants to access critical section?
* $<\text{REQ}, (t:6, \text{id}:1)>$
* note: everyone reply with an ACK, even if waiting for critical section!

$p_{3}$ and $p_{1}$ both sent a request and both have $\text{ACK} = \{ p_{1},p_{2},p_{3} \}$, who enters the crtical section? 
* recived ACK should have timestamp greater than the timestamp of the message request, $p_{3}$ and $p_{1}$ both satisfy this property
* let's look at the $\text{REQ}$ set
	* $p_{1}.\text{REQ}= \{ (p_{3},3) \}$. 
	* $p_{3}.\text{REQ} = \{ (p_{1},6) \}$
	* $p_{1}$ **gets the request! because he has the lower id** (or the lowest clock??? CHECK THIS!!!)

> why do not remove `ACK`? you can do it but it's an optimization.


# proof dio porco
**idea**: for each process, one has lower `id`

**proof by contraddiction**!

if $p_{1}$ enter in the critical region:
* i've also received the ack from $p_{2}$
* so $p_{2}$ received my request

if $p_{2}$ enters in the critical region, then he sent requests to all the other processes.
* $p_{2}$ request's timestamp is bigger than $p_{1}$ requests' timestamp

in the request sets of $p_{2}$ we have $p_{1}$'s requests with lower timestamp:
* so $p_{2}$ cannot enter the critical seciton even if he senta request to enter critical region

**another scenario for the proof**: what if requests happen with the same clock, at the same time?
* it's not possible that $p_{2}$ send and ack and after the request for critical condition if $p_{2}$ sent the request befor the ack, because the link is FIFO!
* then both $p_{2}$ and $p_{1}$ reply with $\text{ACK}$ and they se the requests of each other!
* $\text{p1.reqSet} = \{ \text{reqp2} \}$ and $\text{p2.reqSet} = \{ \text{reqp1} \}$, but they have the same logical clock! who enters? the one with the lowest $p_{1}$


# fairness property proof (simple)
if $p$ request happens before $q$, then $q$ doesn't enter before $p$. it's true:
* one of the two saw the request
* one of the two requests has higher timestamp
# questions!
in the best case, when a process wants to enter how many messages are sent? 
* $p_{1}$ makes $n$ requests, so $n$ messages
* all the process, reply with an ack, so $n$ messages
* $p_{1}$ releases and tells everyone, so $n$ messages
* so $3n$, $O(n)$ messages for a successful requests.

ho do we compute time?
* assume all the messages for request and ack, take 1 unit of time, image being in a synchronous system.
	* all request are sent in 1 unit
	* all ack are sentn in 1 unit
* so we need 2 unit of time to enter in the request: 1 unit for request, 1 unit for replay.

in the worst case how many unit are needed?
* in the worst cases i have the ACK but i have to wait $n-1$ units, everyone issued a request, and i have to wait all to release (its a chain of releases)

# failure detection
two primitives:
* failure detection
* leader election
* if you can solve one, then you can solve the other one.

**note**: we need to avoid manipulating time in algorithms. because time is complex, and in proof, prone to errors!

**failure detector** and **leader election**: can avoid time manipulation.

**failure detector**: has two property
1. **accuracy**: accuracy in avoiding mistakes when detecting failures 
2. **completeness**: ability to detect failures.
3. based on the idea of **pinging**.

**how to detect a crash**? i ping the other process and wait for a process in a certain time

**system model**:
* synchronous system
* crahs failures
* perfect syncrhonouse p2p
	* perfect p2p with a syncrhonouse property. if i send $m$ at time $t$, its received in $t+\text{maxdelay}$

**idea**: start a timer and send a message to $p_{2}$. $p_{2}$ reply to me,
* if $p_{2}$ doesn't answer me in $2\text{maxDelay}$ where $\text{maxDelay}$ is the max delay in the channel, then its dead. this works in synch.
* what do we do in asynch? we must sure that if $p_{2}$ crasched, then eventually $p_{1}$ knows.

**note, in asynch**: you can't distinguish between slow messages or down processes. you might assume that process 2 is down, but because messages were too slow.

**perfect failure:** 2 properties
* PFD1: **strong completeness**. Eventually every process that crashes is permanently detected by every correct process. it's liveness property!
* PDF2: **strong accuracy**. if $p$ is detected by any process, then $p$ has crashed. It's a safety property!
	* tells us that we cannot detected, but if detected i must be sure.