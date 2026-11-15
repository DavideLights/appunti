> [!info] References #gemini
> * **Course Slides**: Daniele Venturi, [Lecture 8 — Constructing PRFs from OWFs (GGM)](https://dventuri83.github.io/assets/pdf/crypto_lecture08_2627.pdf) #gemini
> * **Reference Notes**: Simone Bianco, [Cryptography.pdf](https://github.com/Exyss/university-notes/raw/main/Master/Cryptography/Cryptography.pdf), Section 4.2.1 (*The GGM Tree*, pp. 35–38) #gemini
> * **Textbook**: Katz & Lindell, *Introduction to Modern Cryptography* — 3rd ed. Section 8.5 (Theorem 8.21) / 2nd ed. Section 7.5 #gemini

How to build a PRF?
* from any OWF
* from any PRG *(today)* 

**GGM**: 
* assume $G: \{ 0,1 \}^\lambda \to \{ 0,1 \}^{2\lambda}$
* we want to build $F_{k}: \{ 0,1 \}^n \to \{ 0,1 \}^\lambda$
* think of $G(k)=(G_{0}(k), G_{1}(k))$ 
	* $G_{0}$ outputs first $\lambda$ bits of $G(k)$ 
	* $G_{1}$ outputs last $\lambda$ bits of $G(k)$
	* $|G_{0}(k)|=|G_{1}(k)|=|k|=\lambda$ 

Then we can define (for $n=2$): 
* $F_{k}(00)=G_{0}(G_{0}(k))$
* $F_{k}(01)=G_{1}(G_{0}(k))$
* $F_{k}(10)=G_{0}(G_{1}(k))$
* $F_{k}(11)=G_{1}(G_{1}(k))$

these four strings are pseudorandom, even when viewed together:
* **intuition**: $G_{0}(k)||G_{1}(k)$ is pseudorandom and indistinguishable from $k_{0}||k_{1}$ (two independent uniform keys) 
* and so is $F_{k}(00)||F_{k}(01)||F_{k}(10)||F_{k}(11)$ 
* since $G$ is a PRG (applying $G$ independently to pseudorandom seeds $k_0, k_1$ keeps the outputs pseudorandom). 

**GGM Tree (Fig. 7.2, $n=3$)**: 
* Each input bit $x_i$ chooses whether to take the left branch ($0 \to G_0$) or the right branch ($1 \to G_1$) starting from the root key $k$. 
* Evaluating $F_k(x)$ only traverses **one root-to-leaf path** (equals to $n$ calls to $G$)
* So it runs in poly-time without ever materializing all $2^n$ leaves (
* below, green highlights $F_k(011) = G_1(G_1(G_0(k)))$. 

```mermaid
flowchart TD
    K(["k"]) -->|0: G_0| N0(["G_0(k)"])
    K -->|1: G_1| N1(["G_1(k)"])
    N0 -->|0: G_0| N00(["G_0(G_0(k))"])
    N0 -->|1: G_1| N01(["G_1(G_0(k))"])
    N1 -->|0: G_0| N10(["G_0(G_1(k))"])
    N1 -->|1: G_1| N11(["G_1(G_1(k))"])
    N00 -->|0| L000["F_k(000)"]
    N00 -->|1| L001["F_k(001)"]
    N01 -->|0| L010["F_k(010)"]
    N01 -->|1| L011["F_k(011) = G_1(G_1(G_0(k)))"]
    N10 -->|0| L100["F_k(100)"]
    N10 -->|1| L101["F_k(101)"]
    N11 -->|0| L110["F_k(110)"]
    N11 -->|1| L111["F_k(111)"]
    style K stroke:#2ecc71,stroke-width:2px
    style N0 stroke:#2ecc71,stroke-width:2px
    style N01 stroke:#2ecc71,stroke-width:2px
    style L011 stroke:#2ecc71,stroke-width:2px
```

$$
F_{k}(x) = G_{x_{n}}(G_{x_{n-1}}(\dots G_{x_{1}}(k)\dots))
$$
$$
x=x_{1}\dots x_{n} \in \{ 0,1 \}^n
$$
**what we are doing**: constructing a PRF on $n$-bit inputs using only a length-doubling PRG $G$ (and $n$ sequential evaluations of $G$).

> [!note] question for venturi
> why we cannot use a PRG as a PRF?

**Thm**: assuming $G$ is a PRG 
* with expansion factor $\ell(\lambda)=2\lambda$ (in Katz & Lindell notation: $\ell(n)=2n$) 
* so $G_{0},G_{1}: \{0,1\}^\lambda \to \{0,1\}^\lambda$ 
$$
\mathcal F = \{ F_{k}: \{ 0,1 \}^n \to \{ 0,1 \}^\lambda\} \text{ is a PRF.}
$$
**intuition (Slides 3–4)**:
* $k$ is random
* so $(G_{0}(k), G_{1}(k)) \approx_{C} (U_{\lambda}, U_{\lambda})$, and ideally we could replace all $2^n$ leaves of the tree with uniform strings. 
* **goal of the proof**: to show that $\mathcal F$ is a PRF we have to show that all the levaves of the GGM tree look truly like independent uniform strings.
* **Why that naive idea fails**: replacing all $2^n$ leaves one by one requires **exponentially many hybrids** ($2^n$) 
* So we would need to build $H_{0},H_{1},\dots,H_{T}$ hybrids with $T=2^n$
* But to use hybrids, and to have a polinomial attacker we don't want an exponential number of hybrids! So we need another idea.

**lemma**: for any $t(\lambda)=\text{poly}(\lambda)$ 
$$
(G(k_{1}),\dots,G(k_{t})) \approx_{C} (U_{2\lambda}, \dots, U_{2\lambda})
$$
* where $k_{i} \gets U_{\lambda}$

**proof**: requires hybrids (Slides 4–5, Bianco Lemma 4.1). 
* $H_0 \equiv (G(k_1), G(k_2), \dots, G(k_t))$
* $H_1 \equiv (U_{2\lambda}, G(k_2), \dots, G(k_t))$ 
* $H_i \equiv (\underbrace{U_{2\lambda}, \dots, U_{2\lambda}}_{i}, G(k_{i+1}), \dots, G(k_t))$ 
* $H_t \equiv (U_{2\lambda}, U_{2\lambda}, \dots, U_{2\lambda})$ 


**we want to prove that**: 
$$
H_{0} \approx_{C} H_{1} \approx_{C} \dots \approx_{C} H_{t-1} \approx_{C} H_{t} \implies H_{0} \approx_{C} H_{t}
$$
> **means**: it's impossible to distinguish in polynomial time between $t$ random strings of size $2\lambda$ from $t$ pseudorandom strings of size $2\lambda$


**let's see $H_{0} \approx_{C} H_{1}$ (Slides 5–6)**
```mermaid
sequenceDiagram
    participant A as PPT Adversary A
    participant B as Reduction B
    participant C as PRG Challenger C
    Note over C: Samples z_1 ← G(U_λ) or z_1 ← U_{2λ}
    C->>B: z_1 ∈ {0,1}^{2λ}
    Note over B: Samples k_2, ..., k_t ← U_λ
    B->>A: (z_1, G(k_2), ..., G(k_t))
    A->>B: b' ∈ {0,1}
    B->>C: b'
```
* **Goal of $\mathcal{A}$**: distinguish $H_0$ from $H_1$
	* understand whether the first $2\lambda$-bit block is $G(k_1)$ 
	* or uniform $U_{2\lambda}$ 
* **Goal of $\mathcal{B}$**: break the PRG security of $G$
	* understand whether $\mathcal{C}$ gave $z_1 = G(k_1)$ or $z_1 \gets U_{2\lambda}$)
* **Algorithm of $\mathcal{B}$**: on input $z_1 \in \{0,1\}^{2\lambda}$ from $\mathcal{C}$, $\mathcal{B}$ samples $k_2, \dots, k_t \gets U_\lambda$, 
	* computes $(z_1, G(k_2), \dots, G(k_t))$, 
		* so $\mathcal B$ knows $G$ that $\mathcal C$ is using.
	* calls $\mathcal{A}$ **once** on this tuple, 
	* and outputs $\mathcal{A}$'s bit $b'$ to $\mathcal{C}$. 
	* (For a general step $H_{i-1} \approx_C H_i$, $\mathcal{B}$ puts $i-1$ uniform $U_{2\lambda}$ blocks before $z_i$ and $G(k_{i+1}), \dots, G(k_t)$ after it.) 
* **contraddiction**: $\mathcal A$ can break $C$ by reduction, but $PRG$ by definition is unbreakable. so $\not \exists A\square$

now we still have to prove the following:
**Thm**: assuming $G$ is a PRG 
* with expansion factor $\ell(\lambda)=2\lambda$ 
* so $G_{0},G_{1}: \{0,1\}^\lambda \to \{0,1\}^\lambda$ 
$$
\mathcal F = \{ F_{k}: \{ 0,1 \}^n \to \{ 0,1 \}^\lambda\} \text{ is a PRF.}
$$

**proof**: induction on $n(\lambda)=\text{poly}(\lambda)$ *(in Slides 6–12 written with $m(\lambda) = \text{poly}(\lambda)$)* 
* let $F'_{k}: \{ 0,1 \}^{n-1} \to \{ 0,1 \}^{\lambda}$
* let $F_{k}: \{ 0,1 \}^{n} \to \{ 0,1 \}^{\lambda}$ 
* $F_{k}(x,y)=G_{x}(F'_{k}(y))$
	* *this just a way to build $F_{k}$ using $F'_{k}$ that takes $n-1$ bits instead of $n$*
	* $x \in \{ 0,1 \}$ and $y \in \{ 0,1 \}^{n-1}$

* **Base case ($n = 1$, Slide 7)**: 
	* $F_k(0) = G_0(k)$ so it calls just $G_{0}$,
	* $F_k(1) = G_1(k)$ is the same
	* all of this $\implies (G_{0}(k), G_{1}(k)) \approx_{C} (U_{\lambda}, U_{\lambda})$ 
		* why? b.c. **G is PRG**.
* **Inductive step (Slides 8–9)**: 
	* Assume $F'_k$ is a PRF for length $n-1$. 
	* **goal**: show $F_{k}$ is a PRF for length $n$
	* Define three games for $\mathcal{A}$ querying $(x, y)$: 
		* $\text{Game}_0(\lambda)$: oracle returns $F_k(x,y) = G_x(F'_k(y))$
		* $\text{Game}_1(\lambda)$: oracle returns $H(x,y) = G_x(R'(y))$, where $R' \gets \mathcal{R}(n-1, \lambda)$ 
		* $\text{Game}_2(\lambda)$: oracle returns $R(x,y)$, where $R \gets \mathcal{R}(n, \lambda)$

```mermaid
sequenceDiagram
    participant A as PPT Adversary A
    participant C as Challenger C
    Note over C: Game_0: k ← U_λ (F_k)<br/>Game_1: R' ← R(n-1, λ)<br/>Game_2: R ← R(n, λ)
    loop poly(λ) queries
        A->>C: (x, y) ∈ {0,1} × {0,1}^{n-1}
        alt Game_0(λ)
            C->>A: F_k(x, y) = G_x(F'_k(y))
        else Game_1(λ)
            C->>A: H(x, y) = G_x(R'(y))
        else Game_2(λ)
            C->>A: R(x, y)
        end
    end
    A->>C: b' ∈ {0,1}
```

* **Lemma 1 ($\text{Game}_0(\lambda) \approx_C \text{Game}_1(\lambda)$, Slides 9–10, Bianco Claim 1)**: 
	* $\mathcal A$ wants to distinguish $\text{Game}_0(\lambda)$ from $\text{Game}_1(\lambda)$ 
		* **goal**: distinguish $G_x(F'_k(y))$ from $G_x(R'(y))$ 
	* $\mathcal B$ wants to break the PRF security of $F'$ 
		* **goal**: distinguish $F'_k$ from $R'$ 
	* **how the reduction works (for each query $(x, y)$ from $\mathcal{A}$)**: 
		* $\mathcal{B}$ forwards **$y \in \{0,1\}^{n-1}$** to $\mathcal{C}$, who returns $w = F'_k(y)$ or $w = R'(y)$ 
			* (note: $\mathcal{C}$ evaluates on query $y$, NOT on $k$) 
		* **$\mathcal B$ sends $G_{x}(w)$ to $\mathcal A$** 
			* if $w = F'_k(y)$: $\mathcal{A}$ receives $G_x(F'_k(y)) = F_k(x,y)$ ($\text{Game}_0(\lambda)$) 
			* if $w = R'(y)$: $\mathcal{A}$ receives $G_x(R'(y)) = H(x,y)$ ($\text{Game}_1(\lambda)$) 
		* when $\mathcal{A}$ outputs $b'$, $\mathcal{B}$ forwards $b'$ to $\mathcal{C}$ (perfect reduction)

```mermaid
sequenceDiagram
    participant A as PPT Adversary A
    participant B as Reduction B
    participant C as PRF Challenger C (for F')
    Note over C: Picks F'_k (k←U_λ) or R'←R(n-1,λ)
    loop poly(λ) queries
        A->>B: (x, y) ∈ {0,1} × {0,1}^{n-1}
        B->>C: y
        C->>B: w (F'_k(y) or R'(y))
        B->>A: G_x(w)
    end
    A->>B: b' ∈ {0,1}
    B->>C: b'
```
* **Lemma 2 ($\text{Game}_1(\lambda) \approx_C \text{Game}_2(\lambda)$, Slides 10–12, Bianco Claim 2)**: #gemini