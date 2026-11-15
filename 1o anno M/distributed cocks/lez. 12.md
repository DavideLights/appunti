# sequential consistency
Sequential consistency property, Lamport: 
* an execution is sequentially consistent if the (read and write) operations by all processes on the data store were executed in some sequential order
	* there is a global order
* and the operations of each individual process appear in this sequence in the order specified by its program.

**example slide 1**: the execution is not legal in real-time order, but we can rearrange it. #gemini
* the global order might not correspond to the "real time" order
* so we can **rearrange** operations, giving a "**fictional**" global order.
* from outside the system you cannot determine the order

**example slide 2**:
* *there exists a global ordering that respects the local ordering seen by each process.* #gemini
* it means that we can rearrange the order of operations, provided we respect the execution order inside each process $p_{i}$ #gemini
* we cannot violate the local order seen by a process.

> **Why Sequential Consistency?** Gives all processes the illusion of a single coherent shared memory preserving each process's program order, without paying the synchronization cost of respecting global real-time order across non-overlapping operations on different processes. #gemini

differences:
* regular and not sequentially consistent
* not regular and sequentially consistent 
# atomicity
**Atomicity**: each operation should appear to take effect instantaneously at some moment between its start and completion.

**or linearizability (synonym)**: we can find a moment inside an operation after which everyone in the system sees the change (the linearization point). #gemini

**TODO**: look at the slides and play with linearizability!
* **example**: * [INSERT HERE] #gemini

if an execution is **linearizable** $\implies$ **regular** (and also **sequentially consistent**). #gemini
* in a linearizable execution we can find a linearization point inside each operation, which induces a valid regular (and sequential) ordering. #gemini

**Regularity & Consistency Comparison** *(ref: Distributed Registers I & II slides)*: #gemini
* **Regular register**: every non-concurrent read returns the latest written value; a read concurrent with writes returns either the latest value written before those writes or any value concurrently being written (can still exhibit new-old inversion across reads). #gemini

| Property | Regular | Sequential Consistency | Atomic (Linearizable) | #gemini |
| :--- | :--- | :--- | :--- | :--- |
| Real-time order | Non-concurrent read sees latest write | Ignored across processes | Preserved (`LP` $\in [\text{inv}, \text{resp}]$) | #gemini |
| Per-process order | Not guaranteed across reads (new-old inversion possible) | Preserved for every process | Preserved | #gemini |
| Cross-reader ordering (`ONAR3`) | Not guaranteed (new-old inversion allowed) | Follows the single global order | Guaranteed (no new-old inversion) | #gemini |
| Implication | Orthogonal to Sequential | Orthogonal to Regular | $\implies$ Regular and $\implies$ Sequential | #gemini |

exercise: very hard
* $\text{read}_{2}() \to 2$
	* so $\text{write}(2)$ has been linearised before $\text{read}_2$
	* so $\text{read}_{3}$ cannot return 1
* **note**: $\text{read}_{5}$ can return $\{ 2,3 \}$ if $\text{read}_{3}$ reads $2$
* **note**: $\text{read}_{5}$ can return $\{ 3 \}$ if $\text{read}_{3}$ reads $3$. 
* **note**: $\text{write(3)}$ crashes!

**so**: what a $\text{read}_{i}$ returns depends on what $\text{read}_{j}$ returned with $j<i$.

**tree technique used by teacher**:
* start from the first $\text{read}_{1}$
* children are the values that it can read
* from the children we apply $\text{read}_{2}$ assuming what $\text{read}_{1}$ read.
* **and so on and so forth**.

> [!warning] Complex Exercise — Study Actively #gemini
> Reconstruct the full linearization-point timeline and possibility tree for this execution on your own (* [INSERT HERE]). Ref: *Distributed Registers II* slides (Linearizability scenarios). #gemini

**Difference between Atomic and Regular**: Atomic = Regular + **Ordering (`ONAR3`)** (if a read returns $v$ and a subsequent read returns $w$, the write of $w$ cannot precede the write of $v$ — forbids new-old inversion; see table above). #gemini

## atomic register

**Module 4.2 — `(1, N)-AtomicRegister` (`onar`)**: #gemini
* **Requests**: `<onar, Read>`, `<onar, Write | v>` #gemini
* **Indications**: `<onar, ReadReturn | v>`, `<onar, WriteReturn>` #gemini

$(1,N)$ register specification properties:
1. **ONAR1 (Termination)**: if a correct process invokes an operation, then the operation eventually completes. #gemini
2. **ONAR2 (Validity)**: a read that is not concurrent with a write returns the last value written; a read concurrent with a write returns the last value written or the value concurrently being written. #gemini
3. **ONAR3 (Ordering)**: if a read returns $v_{1}$ and a subsequent read returns $v_{2}$, then the write of $v_{2}$ does not precede the write of $v_{1}$ (equivalent to linearization points for `(1,N)`). #gemini


## implementing `(1,N)` atomic register (from regular register vs. message passing) #gemini
> [!warning] Missing from notes — `(1,N)-RR` $\to$ `(1,N)-AR` (Without Messages) #gemini
> The slides also show how to build `(1,N)-AR` purely from regular registers in two phases: **Phase 1** (`(1,N)-RR` $\to$ `(1,1)-AR`, Alg. 4.3, reader filters out older timestamps) and **Phase 2** (`N^2` instances of `(1,1)-AR` $\to$ `(1,N)-AR`, Alg. 4.4, readers cross-update each other). Ref: *Distributed Registers II* slides, Main Book Ch. 4.3.1–4.3.2 (* [INSERT HERE]). #gemini

**Direct message-passing approach (modifying `Read-One-Write-All` regular register)**: #gemini
**fact 1**: read operation cannot be local. This read operation depends on other processes, so it needs to send messages.
* **goal**: understand when a write has been linearized

we want to avoid the new-old inversion where (during a concurrent `write(7)` after `write(5)`): #gemini
* $p_{4}$ reads the **new** value $7$ at $t$ #gemini
* $p_{5}$ reads the **old** value $5$ at $t'>t$ #gemini

**solution**: a read operation imposes a write to everyone else: **read-impose write-all**
* we also must discard old read-impose / write messages by attaching a timestamp `ts` to `WRITE` messages #gemini
* the reader starts a write (`[WRITE, ts, val]`) and waits for `ACK` from all non-crashed processes before returning `readval`. #gemini

## read-impose write-all algorithm
```text
Uses: BestEffortBroadcast beb, PerfectPointToPointLinks pl, PerfectFailureDetector P.

upon event <onar, Init> do
    (ts, val) := (0, ⊥); correct := Π; writeset := ∅;
    readval := ⊥; reading := FALSE;

upon event <P, Crash | p> do
    correct := correct \ {p};

upon event <onar, Read> do
    reading := TRUE;
    readval := val;
    trigger <beb, Broadcast | [WRITE, ts, val]>;

upon event <onar, Write | v> do
    trigger <beb, Broadcast | [WRITE, ts + 1, v]>;

upon event <beb, Deliver | p, [WRITE, ts', v']> do
    if ts' > ts then (ts, val) := (ts', v');
    trigger <pl, Send | p, [ACK]>;

upon event <pl, Deliver | p, [ACK]> do
    writeset := writeset ∪ {p};

upon correct ⊆ writeset do
    writeset := ∅;
    if reading = TRUE then
        reading := FALSE;
        trigger <onar, ReadReturn | readval>;
    else
        trigger <onar, WriteReturn>;
```
*(`#gemini`: Algorithm 4.5, Distributed Registers II slides)*

1. **reading**: set `reading := TRUE` on `<onar, Read>` so that inside `upon correct ⊆ writeset`, we distinguish a Read's impose phase (`ReadReturn | readval`) from a Write (`WriteReturn`). #gemini
2. we must send `ACK` in **every** case in `upon event <beb, Deliver | p, [WRITE, ts', v']>` (even if `ts' <= ts`) so a reader imposing an older/equal `ts` or a writer never stalls. #gemini
3. the operation (Write or Read-impose) terminates when **`correct ⊆ writeset`** (i.e., **all** non-crashed processes acked, not just one!): #gemini
	1. reset `writeset := ∅`
	2. if `reading = TRUE`, set `reading := FALSE` and trigger `ReadReturn | readval`; otherwise trigger `WriteReturn`. #gemini

**complexity**: at most $2N$ messages (`Write` and `Read`). #gemini

**time complexity**: 2 steps (`beb` + `ACK`) for both write and read. #gemini

## correctness for read-impose write-all
**termination**: as for `(1,N)` regular register
**validity**: as for `(1,N)` regular register

**ordering proof**:
> [!warning] Study Actively — Ordering Proof #gemini
> Verify why imposing `ts` to all non-crashed processes before returning `readval` ensures `ONAR3` (hint: prove by the timestamp invariant that once `R1` finishes, all correct processes have local `ts >= ts(readval)`). * [INSERT HERE] (ref: *Distributed Registers II* slides, Main Book Ch. 4.3). #gemini


## implementation for fail silent
**assumption for $n$ of failures**: $f < \frac{n}{2}$ (majority of correct processes). #gemini
* $\frac{n}{2}$ threshold: most of the time the implementation uses quorums (`> N/2`).

**writer**: waits for a quorum (`> N/2`) of `ACK`s
**reader**: queries a quorum (`> N/2`) of `VALUE`s, then imposes to a quorum (`> N/2`) of `ACK`s. #gemini

generally, to replace a failure detector, we use a quorum.

**Read-Impose Write-Majority (Algorithm 4.6–4.7)**: #gemini
```text
Uses: BestEffortBroadcast beb, PerfectPointToPointLinks pl.

upon event <onar, Init> do
    (ts, val) := (0, ⊥); wts := 0; acks := 0;
    rid := 0; readlist := [⊥]^N; readval := ⊥; reading := FALSE;

upon event <onar, Read> do
    rid := rid + 1; acks := 0; readlist := [⊥]^N; reading := TRUE;
    trigger <beb, Broadcast | [READ, rid]>;

upon event <beb, Deliver | p, [READ, r]> do
    trigger <pl, Send | p, [VALUE, r, ts, val]>;

upon event <pl, Deliver | q, [VALUE, r, ts', v']> such that r = rid do
    readlist[q] := (ts', v');
    if #(readlist) > N/2 then
        (maxts, readval) := highest(readlist);
        readlist := [⊥]^N;
        trigger <beb, Broadcast | [WRITE, rid, maxts, readval]>;

upon event <onar, Write | v> do
    rid := rid + 1; wts := wts + 1; acks := 0;
    trigger <beb, Broadcast | [WRITE, rid, wts, v]>;

upon event <beb, Deliver | p, [WRITE, r, ts', v']> do
    if ts' > ts then (ts, val) := (ts', v');
    trigger <pl, Send | p, [ACK, r]>;

upon event <pl, Deliver | q, [ACK, r]> such that r = rid do
    acks := acks + 1;
    if acks > N/2 then
        acks := 0;
        if reading = TRUE then
            reading := FALSE;
            trigger <onar, ReadReturn | readval>;
        else
            trigger <onar, WriteReturn>;
```
*(`#gemini`: Algorithm 4.6–4.7, Distributed Registers II slides — Write = 2N msgs / 2 steps, Read = 4N msgs / 4 steps)*

* **Why two phases for Read (and one phase for Write)?** #gemini
	* **Read — Phase 1 (Query/`READ`)**: without $\mathcal{P}$, a reader's local copy might be stale, so it queries a majority quorum (`> N/2`) to find `(maxts, readval)` with the highest timestamp. #gemini
	* **Read — Phase 2 (Impose/`WRITE`)**: before returning `readval`, the reader writes `(maxts, readval)` back to a majority quorum (`> N/2` ACKs). #gemini
	* **Write — One phase (Impose only)**: there is a single writer (`(1,N)`), so it already knows `wts` and just imposes `[WRITE, rid, wts, v]` to a majority. *(Note: in `(N,N)` multi-writer, Write also needs a query phase first!)* #gemini
* **Why is it correct / why must the reader help the writer impose?** #gemini
	* During a concurrent write, `R1` might see the new `(maxts, readval)` from only a few processes (before a full majority has it). If `R1` returned immediately without imposing, a subsequent read `R2` could contact a **different** majority quorum that missed those few processes and return an **older** value (violating `ONAR3`!). #gemini
	* Because `R1` imposes `(maxts, readval)` onto a majority quorum before completing, `R1`'s write-back quorum intersects `R2`'s query quorum in $\geq 1$ process that has timestamp $\geq \text{maxts}$, guaranteeing `R2` never returns an older value. #gemini

me so rotto er cazzo della magistrale basta






