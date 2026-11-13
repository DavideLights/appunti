# alg. uniform hierarchical consensus 

**Module 5.2 — `UniformConsensus` (`uc`)**: #gemini
* **Events**: `<uc, Propose | v>`, `<uc, Decide | v>` #gemini
* **UC1–UC3**: same as `C1–C3` in Regular Consensus (Termination, Validity, Integrity). #gemini
* **UC4 (Uniform agreement)**: no two processes decide differently. #gemini

**Algorithm 5.4 — Hierarchical Uniform Consensus**: #gemini
```text
Implements: UniformConsensus uc.
Uses: PerfectPointToPointLinks pl, BestEffortBroadcast beb, ReliableBroadcast rb, PerfectFailureDetector P.

upon event <uc, Init> do
    detectedranks := ∅; ackranks := ∅;
    round := 1; proposal := ⊥; decision := ⊥; proposed := [⊥]^N;

upon event <P, Crash | p> do
    detectedranks := detectedranks ∪ {rank(p)};

upon event <uc, Propose | v> such that proposal = ⊥ do
    proposal := v;

upon round = rank(self) ∧ proposal != ⊥ ∧ decision = ⊥ do
    trigger <beb, Broadcast | [PROPOSAL, proposal]>;

upon event <beb, Deliver | p, [PROPOSAL, v]> do
    proposed[rank(p)] := v;
    if rank(p) ≥ round then
        trigger <pl, Send | p, [ACK]>;

upon round ∈ detectedranks do
    if proposed[round] != ⊥ then
        proposal := proposed[round];
    round := round + 1;

upon event <pl, Deliver | q, [ACK]> do
    ackranks := ackranks ∪ {rank(q)};

upon detectedranks ∪ ackranks = {1, ..., N} do
    trigger <rb, Broadcast | [DECIDED, proposal]>;

upon event <rb, Deliver | p, [DECIDED, v]> such that decision = ⊥ do
    decision := v;
    trigger <uc, Decide | decision>;
```
*(`#gemini`: Synchronous Consensus 1 slides / Alg. 5.4)*

* **Message complexity**: $(1\,\text{Beb} + 1\,\text{Rb}) \cdot (f + 1)$ (plus up to $N$ ACKs per round). #gemini
* **Step complexity**: $2$ delays per failed leader, $3$ delays for the leader that succeeds $\implies O(f)$. #gemini

# alg. proofs

> [!warning] Complex Proofs — Study Actively #gemini
> Complete the four correctness proofs for **Algorithm 5.4** on your own before checking the slides. Ref: *Synchronous Consensus 1* slides, Main Book Ch. 5.1 (Alg. 5.4). #gemini
* **Integrity & Validity**: (same reasoning as non-uniform Hierarchical Consensus) * [INSERT HERE] #gemini
* **Termination**: (proof by strong induction on process rank / ID from $1$ to $N$ using `beb`, `rb`, and $\mathcal{P}$ completeness) * [INSERT HERE] #gemini
* **Uniform Agreement**: (let $p_i$ be the first process to decide $v$; consider both cases: $p_i$ is correct vs. $p_i$ crashes after collecting ACKs) * [INSERT HERE] #gemini

# modify the algorithm.
**beb instead of reliable (`rb`)**: integrity, validity, and other properties can fail?
* **does integrity fail**? No: if a process receives `DECIDED` twice, the `decision = ⊥` guard prevents the handler from triggering `<uc, Decide>` twice. #gemini
* **does validity fail**? No, the validity is still correct (no changes in logic; `beb` has no-creation). #gemini
* **does uniform agreement fail**? (=two processes decide something different). No: before broadcasting `DECIDED`, $p_i$ collected ACKs from all correct processes so everyone advancing to round $i+1$ sets `proposal := proposed[i] = v`. #gemini
* **(25:00) does termination fail?** Yes: if the last leader $p_k$ to collect ACKs crashes mid-`beb` of `DECIDED` (sending only to a subset of processes, otherwise it acts like reliable), a correct process with rank $< k$ that missed `DECIDED` advances past its own turn and waits forever. #gemini
	* if one process received `DECIDED` under `beb`, that does not imply the others did too!
	* that's why termination does not hold anymore.

# ex. hierarchical
**R**:
* integrity is not violated
* termination is not violated
* **validity**: * [INSERT HERE] #gemini

> [!warning] Exercise check #gemini
> Specify which modification to Hierarchical Consensus (`Alg. 5.2`) is being tested here (e.g., removing `if r < rank(self) ∧ r > proposer` in Alg. 5.2 violates **Agreement**). Complete **validity** and **agreement** on your own (* [INSERT HERE]). Ref: *Synchronous Consensus 1* slides, Main Book Ch. 5.1. #gemini
