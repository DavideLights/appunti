# Collision-resistant hash
**very important primitive**:  an hash function is a **deterministic function** $H: \{ 0,1 \}^* \to \{ 0,1 \}^n$ ($n=128, 256, \dots$) and we'd like $H$ to work for arbitrary input length.

**otherwise**: $H: \{ 0,1 \}^N \to \{ 0,1 \}^n$ with $N\gg n$ is a **compression function**.

**what security do we want**? 
* main issue are collision, an its a problem by design of what we are trying to do.
* **hard**: collisions should be hard. they always exists but should be hard to **find**.

**def**. let $\mathcal H = \{H_{S}: \{ 0,1 \}^* \to \{ 0,1 \}^n\}_{s\in \{ 0,1 \}^\lambda}$ be a family of hash functions.
* $\mathcal H$ is collision resistance if no $\mathcal A$ wins the following game.

**attack game**:
* $\mathcal A$ gets $s$ from $\mathcal C$ with $s \gets \{ 0,1 \}^\lambda$
* $\mathcal A$ sends $x,x'$ and wins if $x\neq x'$ but $H_{s}(x)=H_{s}(x')$

**why seed**? in practice there is no seed, we need it that for the definition. (gemini explain what the teacher means)

**otherwise**: there is only one function.
* we said that attacker A must find a collision.
* but if we had only one hash function, then $\mathcal A$ could know the hard coded collision of that hash function (??? gemini check this. )

# constructions
we will cover one of the main desings: Merkle Damgaarr.

**basic idea**: recipe to build $\mathcal H$. two steps:
1. design a compression function.
2. **domain extension**: make it collision resistance.

**note**: sha 1,2, md5 follow step 1 heuristically and step 2 as is.

**start with step 2**:
* assume we have $\text{cmps}: \{ 0,1 \}^{2n} \to \{ 0,1 \}^n$ (compression function)
* we have $x_{1},x_{2},\dots,x_{d}$ blocks of size $n$, and we compress block by block
* we compute $y_{1} = \text{cmps}$ using $x_{1}$ and $0^n$ as input
* then we compute $y_{2}= \text{cmps}$ using $x_{2}$ and $y_{1}$ as input
* then we compute $y_{3}= \text{cmps}$ using $x_{3}$ and $y_{2}$ as input
* and so on...

> **note**: compute $y_{1}$ using $x$ and $y$ as input means concatenating $x$ and y and give as inmput to $\text{cmps}$

**gemini**: write the mermaid diagram showing merkle daamgard construction.

**thm**: assuming $\text{cmps}_{S}$ (note that it has a seed!) $\{ 0,1 \}^{2n} \to \{ 0,1 \}^n$ to be collision resistance. The MD $H_{s}$ : $\{ 0,1 \}^{nd} \to \{ 0,1 \}^n$ is collision resistance for every fixed choice of $d \in \text{poly}(\lambda)$

**proof**: consider any collision $x=x_{1},\dots,x_{d}$ and $x'=x_{1}',\dots,x_{d}'$ s.t.
* $x\neq x'$ but $H_{s}(x) = H_{s}(x')$
* running backwards Markle Daamgard
* there must be a largest index $j$ s.t. $(x_{j};y_{j-1}) \neq (x_{j}';y_{j-1})'$ 
* such this is the largest, then we also know $\text{cmps}_{s}(x_{j}, y_{j-1}) = \text{cmps}_{s}(x_{j}', y_{j-1}')$


**gemini**: visualize this proof for $d=3$ for example using mermaid diagram. dio cane bastardo

so given a machine braking collision resistance of $\text{H}_{s}$ we can break collision resistance for $\text{cmps}$.