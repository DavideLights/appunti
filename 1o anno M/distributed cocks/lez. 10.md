
implementation in fail-stop.

## URB in $\text{FAIL-SILENT}$

**objective**: build a URB in $\text{FAIL-SILENT}$. In order to create the algorithm we have to bound the number of failures.

**quorum**: 
* we have $n$ proc in our set of total processes $P$
* a quorum is any subset of at least $\lfloor \frac{n}{2} \rfloor + 1$ processes (a majority). #gemini
* **note**: two quorums in a system intersect in at least 1 process.
* if the intersection is empty, then the size of the union must be the sum of the sizes of the two quorums: $|Q_1 \cup Q_2| \geq 2(\lfloor \frac{n}{2} \rfloor + 1) > n = |P|$, contradiction. #gemini

if in the system the number of failures is $f < \frac{n}{2}$
* number of correct processes: we always have $|C| \geq \lfloor \frac{n}{2} \rfloor + 1$ #gemini
* quorum: the set of correct processes $C$ is a quorum 

if i take another quorum in the system, they intersect in at least 1 process.

**idea 1**: if a correct process has seen a message, then it's safe to deliver it #gemini
* assuming $f < \frac{n}{2}$ is a safe number of failures; therefore, if a quorum of processes sees a message, at least one correct process has seen it. #gemini

**we can modify** *All-Ack Uniform Reliable Broadcast algorithm* to build URB over Fail-Silent (remove the `Crash` handler for $\mathcal{P}$ and replace `correct \subseteq ack[m]` with `|ack[m]| > N/2` in `candeliver(m)`) into *Majority-Ack Uniform Reliable Broadcast*. #gemini

**question**: what if $|F| \geq \frac{n}{2}$ and in `candeliver` (inside the algorithm) we require $|\text{ack}[m]| \geq |F|+1$ (or only $|\text{ack}[m]| \geq |F|$)? #gemini
* if we require $|\text{ack}[m]| \geq |F|+1$, we violate **validity** (e.g., with $n=6, |F|=3$, threshold $4$: if all 3 faulty processes crash before acking, correct processes only see $3$ acks and wait forever). #gemini
* conversely, if we only require $|\text{ack}[m]| \geq |F|$ ($=3$), all $3$ acks might come solely from faulty processes that crash before forwarding $m$ to any correct process, violating **uniform agreement**. #gemini

**takeaway**:
* if you have perfect failure detector: you can tollerate $f<n$ fails
* if you do not have perfect failure detector: you can tollerate $f< \frac{n}{2}$


**notes for exercises:**
* **Uniform** reliable is also (regular) reliable (`URB` $\implies$ `RB`, **not** vice versa!) #gemini
* (regular/uniform) reliable is also best effort (`RB` $\implies$ `BEB`) #gemini
# ordered communications (part 1)

**ordered communications**: define guarantees on the deliveries inside a group of processes.

type:
* FIFO ordering
* Causal ordering
* Total ordering of deliveries

We do we need ordered? client cancels a prenotation before it is booked even if he requested service in a different order.

**FIFO BROADCAST**:
* `FRB1–FRB4`: same as `RB1–RB4` (Validity, No duplication, No creation, Agreement). #gemini
* `FRB5 - FIFO delivery`: if some process broadcasts message $m_1$ before it broadcasts message $m_2$, then no correct process delivers $m_2$ unless it has already delivered $m_1$. #gemini
* implemented using **counters**.

**FIFO BRD algorithm** (Algorithm 3.12): #gemini
`upon event <frb, init> do`
* `lsn = 0` it's the local sequence number.
* `pending = emptyset`
* $\text{next} := [1]^N$ an array of $1$.

`upon event <frb, broadcast | m> do`:
* $\text{lsn} = \text{lsn}+1$
* $\text{trigger } <\text{rb}, \text{Broadcast} \mid [\text{DATA}, \text{self}, m, \text{lsn}]>$

`upon event <rb, Deliver | p, [DATA, s, m, sn]>`:
* $\text{pending}:= \text{pending} \cup \{ (s, m, sn) \}$ #gemini
* while exists $(s, m', sn') \in \text{pending}$ s.t. $sn' = \text{next}[s]$ do
	* $\text{next}[s] = \text{next}[s] + 1$ #gemini
	* $\text{pending} = \text{pending} \setminus \{ (s, m', sn') \}$ #gemini
	* trigger $<\text{frb}, \text{Deliver} \mid s, m'>$

try executing the algorithm to understand how it works

**order**: messages between different senders are not ordered. we ensure only that messages sent from $p_{i}$ are delivered in an ordered way.

FIFO is **orthogonal** with reliability guarantees (`URB` vs `RB`). #gemini

sometimes FIFO is not enough: example in a bank system using broadcast.
* in this system you have to sign transactions
* check the balance availability (`SourceAccount - MoneyQuantity >= 0`) in your local copy #gemini
* **Question**: Why can FIFO fail when transfers are causally linked across different senders (e.g., $p_1$ transfers to $p_2$, then $p_2$ reads it and transfers to $p_3$)? * [INSERT HERE] (ref: *Ordered Communications* slides, Main Book Ch. 3.9 `CRB`) #gemini