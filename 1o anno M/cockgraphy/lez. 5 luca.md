- [Lesson 5 — Pseudorandom Generators and Hard-Core Bits](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#lesson-5-pseudorandom-generators-and-hard-core-bits)
    - [Pseudorandomness](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#pseudorandomness)
        - [Computational indistinguishability](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#computational-indistinguishability)
        - [Clarifying the output bit in the advantage](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#clarifying-the-output-bit-in-the-advantage)
    - [Formal definition of a PRG](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#formal-definition-of-a-prg)
    - [Exercise: why an unbounded adversary can distinguish](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#exercise-why-an-unbounded-adversary-can-distinguish)
    - [How to construct a PRG](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#how-to-construct-a-prg)
        - [Theorem 1 — OWFs imply PRGs](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#theorem-1-owfs-imply-prgs)
        - [Scope of the proof](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#scope-of-the-proof)
        - [Ingredient 1: stretch amplification](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#ingredient-1-stretch-amplification)
            - [Theorem 2 — Statement and assumption](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#theorem-2-statement-and-assumption)
            - [Construction of the amplified generator](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#construction-of-the-amplified-generator)
        - [is it secure?](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#is-it-secure)
            - [1. Proof strategy: Reduction and contradiction](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#1-proof-strategy-reduction-and-contradiction)
            - [2. Understanding the two adversaries](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#2-understanding-the-two-adversaries)
            - [3. The problem with the direct reduction](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#3-the-problem-with-the-direct-reduction)
            - [4. How will we solve this?](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#4-how-will-we-solve-this)
        - [Hybrid Argument](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#hybrid-argument)
            - [1. Goal and intuition](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#1-goal-and-intuition)
            - [2. Constructing the hybrids](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#2-constructing-the-hybrids)
            - [3. General definition of $H_i$](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#3-general-definition-of-h_i)
            - [4. Why are consecutive hybrids indistinguishable?](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#4-why-are-consecutive-hybrids-indistinguishable)
        - [Proving the Hybrid Argument](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#proving-the-hybrid-argument)
            - [Constructing $\mathcal B$ from $\mathcal A$](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#constructing-mathcal-b-from-mathcal-a)
            - [Concrete simulation: $\ell=4$ and $i=2$](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#concrete-simulation-ell4-and-i2)
            - [Why the output probabilities match](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#why-the-output-probabilities-match)
            - [Averaging over the chosen transition](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#averaging-over-the-chosen-transition)
            - [Contradiction and conclusion](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#contradiction-and-conclusion)
    - [Hard-Core Bits](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#hard-core-bits)
        - [Motivation: one-wayness does not hide every input bit](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#motivation-one-wayness-does-not-hide-every-input-bit)
        - [Definition of a hard-core predicate](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#definition-of-a-hard-core-predicate)
        - [Preliminary fact: a permutation preserves uniformity](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#preliminary-fact-a-permutation-preserves-uniformity)
        - [Theorem 3 — A one-bit-stretch PRG from an OWP](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#theorem-3-a-one-bit-stretch-prg-from-an-owp)
            - [Proof of Theorem 3](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#proof-of-theorem-3)
        - [Limitation: replacing the OWP with an arbitrary OWF](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#limitation-replacing-the-owp-with-an-arbitrary-owf)
        - [A separate question: can one predicate work for every OWF?](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#a-separate-question-can-one-predicate-work-for-every-owf)
    - [Sources](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/CR%20LESSON%205.md#sources)

Pick a markdown and code style:  

[Download as HTML](blob:null/7173ff7e-3d10-47de-afe2-51621a52943d)

# Lesson 5 — Pseudorandom Generators and Hard-Core Bits

## Pseudorandomness

The goal is to turn a short uniform seed into a longer string that looks random to an efficient adversary. A deterministic generator expands the number of output bits; it does not create additional genuine randomness. **Pseudorandomness** describes the computational guarantee: an efficient adversary cannot distinguish the generated output from a uniform string of the same length except with negligible advantage.

Consider an adversary $\mathcal A$ that receives a string $z$ generated in one of two worlds:

- **World 0:** $z=G(s)$, where $s\gets U_\lambda$ is a uniformly random seed.
- **World 1:** $z\gets U_{\lambda+\ell}$, a uniform random string of the same length as $G(s)$.

The adversary tries to determine which world produced $z$. If $G$ is a secure pseudorandom generator (PRG), no probabilistic polynomial-time (PPT) adversary has non-negligible distinguishing advantage. Here, advantage measures the difference between the probabilities of outputting $1$ in the two worlds, as defined below.

![[Pasted image 20261111104741.png]]

> [!info]- Recap of a negligible function A nonnegative function $\mu$ is negligible if, for every positive polynomial $p$, there is a sufficiently large $\lambda_0$ such that $\mu(\lambda)<1/p(\lambda)$ for every $\lambda\geq\lambda_0$. It approaches zero faster than the inverse of any polynomial.
> 
> Among $1/\lambda$, $1/\lambda^2$ and $2^{-\lambda}$, only $2^{-\lambda}$ is negligible. The plot illustrates their decay; negligibility is an asymptotic property, not something established by a finite plot. ![[Pasted image 20261111105152.png]]

### Computational indistinguishability

Consider two ensembles of random variables,

$$ X={X_\lambda}_{\lambda\in\mathbb N}, \qquad Y={Y_\lambda}_{\lambda\in\mathbb N}. $$

The ensembles are **indexed by** the security parameter $\lambda$: for each parameter value, $X_\lambda$ and $Y_\lambda$ describe the distributions being compared. The index does not numerically bound the sampled values. Samples must have compatible representations; in our PRG experiment they have the same length, since a difference in length alone would reveal the world.

We say that $X$ and $Y$ are computationally indistinguishable, written $X\approx_c Y$, if, for every PPT adversary $\mathcal A$,

$$ \boxed{\left|\Pr[\mathcal A(X_\lambda)=1] -\Pr[\mathcal A(Y_\lambda)=1]\right| \leq\operatorname{negl}(\lambda)}. $$

The negligible bound may depend on the adversary, and the condition holds for sufficiently large $\lambda$. In $\Pr[\mathcal A(X_\lambda)=1]$, we sample a string according to $X_\lambda$, give it to $\mathcal A$, and measure the probability that $\mathcal A$ outputs $1$. The probability includes the randomness of the sample and of the adversary.

Computational indistinguishability does not require the distributions to be statistically close. They can be far apart while every efficient test has negligible advantage. The definition also applies beyond PRGs: the professor gives encryptions of $0$ and $1$ as another pair of distributions one might want an efficient adversary to be unable to distinguish.

> [!example]- Example of distinguishability If $\Pr[\mathcal A(X_\lambda)=1]=0.80$ and $\Pr[\mathcal A(Y_\lambda)=1]=0.30$, the distinguishing advantage is $|0.80-0.30|=0.50$. These numbers illustrate advantage at a fixed parameter value.

> [!example] Game example of the professor In $\operatorname{GAME}(\lambda,0)$, the challenger samples $z\gets X_\lambda$; in $\operatorname{GAME}(\lambda,1)$, it samples $z\gets Y_\lambda$. The adversary receives $z$ and outputs a bit $b'$.
> 
> ![[CR_L5_indistinguishability_game.svg|700]]
> 
> Redrawing of the supplied game illustration; see lecture-5 slides, PDF p. 2.

For a guessing interpretation, let $b=0$ denote the $X_\lambda$ world and $b=1$ the $Y_\lambda$ world. The adversary wins when $b'=b$. Thus, outputting $1$ means guessing World 1; it does not necessarily mean winning.

### Clarifying the output bit in the advantage

The definition measures how differently the adversary behaves in the two worlds, rather than directly measuring its probability of guessing correctly. If the adversary always outputs $1$, then

$$ \Pr[\mathcal A(X_\lambda)=1]=1, \qquad \Pr[\mathcal A(Y_\lambda)=1]=1, $$

so its distinguishing advantage is $|1-1|=0$. With equally likely worlds, this strategy guesses correctly half the time but learns nothing from its sample.

## Formal definition of a PRG

A pseudorandom generator is a deterministic, polynomial-time computable function

$$ \boxed{G:{0,1}^{\lambda}\rightarrow{0,1}^{\lambda+\ell}}, $$

where $\ell=\ell(\lambda)>0$ is the stretch. A secure PRG satisfies two properties:

1. **Expansion:** $|G(s)|=\lambda+\ell>\lambda$.
2. **Pseudorandomness:** $G(U_\lambda)\approx_c U_{\lambda+\ell}$.

Thus, a uniform seed of only $\lambda$ bits produces a longer string that is computationally indistinguishable from a uniform string of $\lambda+\ell$ bits. In the earlier notation, $X_\lambda=G(U_\lambda)$ and $Y_\lambda=U_{\lambda+\ell}$.

![[CR_L5_prg_worlds.svg|750]]

For every PPT adversary $\mathcal A$, security requires

$$ \left|\Pr[\mathcal A(G(U_\lambda))=1] -\Pr[\mathcal A(U_{\lambda+\ell})=1]\right| \leq\operatorname{negl}(\lambda). $$

## Exercise: why an unbounded adversary can distinguish

**Claim:** no PRG with positive stretch is secure against computationally unbounded adversaries. To see why, consider even a one-bit stretch:

$$ G:{0,1}^{\lambda}\rightarrow{0,1}^{\lambda+1} $$

We have two possible worlds:

- World 0: $z=G(s)$, where $s\gets U_\lambda$.
    
- World 1: $z\gets U_{\lambda+1}$.
    

There are $2^\lambda$ possible seeds and $2^{\lambda+1}$ possible output strings. Thus, the output space is twice as large as the seed space, and $G$ can reach at most half of it.

![[CR_L5_seed_output_spaces.svg|750]]

Some strings of length $\lambda+1$ can therefore never be generated. The attack tests whether its challenge belongs to the image of $G$.

Given $z\in{0,1}^{\lambda+1}$, the adversary performs the following:

1. Enumerate all $2^\lambda$ possible seeds.
2. Compute $G(s)$ for each seed.
3. If any $G(s)=z$, output $1$.
4. Otherwise, output $0$.

Mathematically:

$$ \mathcal A(z)= \begin{cases} 1 & \text{if }\exists s:G(s)=z\ 0 & \text{otherwise} \end{cases} $$

**Generated world:** if $z=G(s)$ for $s\gets U_\lambda$, the search must find at least one matching seed. Therefore,

$$ \boxed{\Pr[\mathcal A(G(U_\lambda))=1]=1} $$

**Uniform world:** if $z\gets U_{\lambda+1}$, at most $2^\lambda$ of the $2^{\lambda+1}$ possible strings pass the test. Therefore,

$$ \boxed{\Pr[\mathcal A(U_{\lambda+1})=1]\leq\frac12} $$

Notice the inequality: different seeds might produce the same output, so the number of distinct outputs could be even smaller.

In this exercise, output $1$ means “the string is in the image of $G$,” rather than “World 1.” A generated sample always passes the test. A uniform sample passes with probability at most $1/2$; if it fails, the adversary knows that it came from the uniform world.

Using the definition of distinguishing advantage:

$$ \begin{aligned} \operatorname{Adv}_{\mathcal A}(\lambda) &=\left|\Pr[\mathcal A(G(U_\lambda))=1]\right.\ &\qquad\left.-\Pr[\mathcal A(U_{\lambda+1})=1]\right|\[4pt] &\geq 1-\frac12\ &=\boxed{\frac12} \end{aligned} $$

An advantage of at least $1/2$ is non-negligible. However, this attack enumerates all $2^\lambda$ seeds, so it does not run in polynomial time. It rules out security against computationally unbounded adversaries while remaining compatible with security against PPT adversaries. The same counting argument applies to any positive stretch.

## How to construct a PRG

The counting attack explains why security must be computational. The next question is how to construct a generator that satisfies it. We return to a **one-way function (OWF)** $f$, which has two properties:

1. Easy to compute: Given $x$, we can compute $f(x)$ in polynomial time.
    
2. Hard to invert: Given $f(x)$, where $x$ was sampled uniformly, no PPT adversary can recover any valid preimage except with negligible probability.
    

The professor introduces the following theorem.

### Theorem 1 — OWFs imply PRGs

If one-way functions exist, then secure pseudorandom generators with polynomial stretch also exist.

$$ \boxed{\text{OWFs exist}\implies\text{PRGs exist}} $$

More precisely, for any positive, efficiently computable, polynomially bounded stretch $\ell(\lambda)$, we can construct a secure PRG:

$$ G:{0,1}^{\lambda}\rightarrow {0,1}^{\lambda+\ell(\lambda)} $$

One-wayness alone does not make a function's output look random: a function may be hard to invert while revealing an easily recognizable pattern. For example, if $f$ is one-way, consider

$$ f'(x)=0\parallel f(x) $$

This function remains one-way, but its output always starts with $0$, whereas a uniform string starts with $0$ only half the time. This gives an efficient distinguishing test.

The theorem therefore promises a construction starting from any OWF; it does not identify every OWF itself as a PRG.

### Scope of the proof

**Proof status: the full proof of Theorem 1 is not given in this lecture.** The professor develops two ingredients instead. First, we assume a secure one-bit-stretch PRG and prove that its stretch can be amplified (Theorem 2). Then we construct a one-bit-stretch PRG under the stronger assumption of a one-way permutation with a hard-core predicate (Theorem 3). These results do not constitute the full proof for arbitrary OWFs.

### Ingredient 1: stretch amplification

> If we already have a secure PRG that generates only one additional bit, can we use it to generate polynomially many additional bits?

#### Theorem 2 — Statement and assumption

Assume we already have a deterministic, polynomial-time computable secure PRG:

$$ G:{0,1}^{\lambda}\rightarrow{0,1}^{\lambda+1} $$

Its security means $G(U_\lambda)\approx_c U_{\lambda+1}$. **This is an assumption of Theorem 2; we do not prove it in the stretch-amplification argument.**

**Conclusion to prove:** for any positive, efficiently computable, polynomially bounded stretch $\ell(\lambda)$, the iterative construction below defines a secure PRG $G^\ell$, satisfying

$$ \boxed{G^\ell(U_\lambda)\approx_c U_{\lambda+\ell}}. $$

#### Construction of the amplified generator

The original generator $G$ receives a $\lambda$-bit seed and produces $\lambda+1$ bits.

We divide its output into two parts:

$$ \boxed{G(s_0)=(s_1,b_1)} $$

Here $s_1$ is a $\lambda$-bit state and $b_1$ is one output bit. We reuse $s_1$ as the input to the next evaluation of $G$.

![[CR_L5_stretch_amplification.svg|700]]

We start with:

$$ s_0\gets U_\lambda $$

Then:

$$ \begin{aligned} G(s_0)&=(s_1,b_1)\ G(s_1)&=(s_2,b_2)\ G(s_2)&=(s_3,b_3)\ &\vdots\ G(s_{\ell-1})&=(s_\ell,b_\ell) \end{aligned} $$

At each step, we obtain one new output bit $b_i$, while keeping a $\lambda$-bit state $s_i$ for the next iteration. After $\ell$ iterations, we output:

$$ \boxed{ G^\ell(s_0)=(b_1,b_2,\ldots,b_\ell,s_\ell) } $$ This defines a new generator:

$$ \boxed{ G^\ell:{0,1}^{\lambda}\rightarrow {0,1}^{\lambda+\ell} } $$ The output contains the $\ell$ generated bits and only the final $\lambda$-bit state:

$$ \underbrace{(b_1,b_2,\ldots,b_\ell)}_{\ell\text{ bits}} \parallel \underbrace{s_\ell}_{\lambda\text{ bits}} $$

Therefore,

$$ \boxed{|G^\ell(s_0)|=\lambda+\ell}. $$

Intermediate states are not included in this output. If an adversary received $s_i$ together with $(s_{i+1},b_{i+1})$, it could evaluate $G(s_i)$ and check the deterministic relation $G(s_i)=(s_{i+1},b_{i+1})$.

The professor also points out a state-compromise limitation: knowing an internal state $s_i$ lets an adversary compute the subsequent states and output bits by continuing to evaluate $G$. The theorem below concerns the specified finite output $(b_1,\ldots,b_\ell,s_\ell)$; it does not promise unpredictability of a future continuation after the final state has been revealed.
### is it secure?

**Proof of Theorem 2 begins here.** We assume that the original one-bit-stretch generator is secure,

$$ G(U_\lambda)\approx_c U_{\lambda+1}, $$

and want to prove security of the amplified construction:

$$ \boxed{G^\ell(U_\lambda)\approx_c U_{\lambda+\ell}}. $$

Here $\ell=\ell(\lambda)>0$ is efficiently computable and polynomially bounded. The security parameter and the construction are public. The proof follows this route: assume an adversary against $G^\ell$, define hybrids, construct an adversary against $G$, calculate its advantage, and derive a contradiction.

#### 1. Proof strategy: Reduction and contradiction

Suppose, for contradiction, that $G^\ell$ is insecure. There is then a PPT adversary $\mathcal A$ whose distinguishing advantage

$$ \varepsilon(\lambda)= \left| \Pr[\mathcal A(G^\ell(U_\lambda))=1] -\Pr[\mathcal A(U_{\lambda+\ell})=1] \right| $$

is non-negligible. This does not mean that $\mathcal A$ always identifies the correct world. It means that its probabilities of outputting $1$ differ by a non-negligible amount between the two worlds.

We will explicitly construct a PPT adversary $\mathcal B$ that uses this same $\mathcal A$ to distinguish $G(U_\lambda)$ from $U_{\lambda+1}$. If $\mathcal B$ also has non-negligible advantage, it contradicts our assumption that $G$ is secure.

#### 2. Understanding the two adversaries

||Adversary $\mathcal A$|Adversary $\mathcal B$|
|---|---|---|
|Goal|Break the amplified generator $G^\ell$|Break the original generator $G$|
|Input length|$\lambda+\ell$ bits|$\lambda+1$ bits|
|Challenge distributions|$G^\ell(U_\lambda)$ or $U_{\lambda+\ell}$|$G(U_\lambda)$ or $U_{\lambda+1}$|
|Role in the proof|Assumed to exist for the contradiction|Constructed using $\mathcal A$|

The existence of $\mathcal A$ alone does not yet establish an attack against $G$: we must show how $\mathcal B$ can use it.

#### 3. The problem with the direct reduction

The challenger gives $\mathcal B$ one string $z\in{0,1}^{\lambda+1}$, sampled either from $G(U_\lambda)$ or from $U_{\lambda+1}$. $\mathcal B$ does not know which distribution produced it. For $\ell>1$, this challenge is shorter than the input expected by $\mathcal A$; as the professor puts it, they “speak different languages.”

Appending arbitrary bits would fix the length but would not ensure the required input distributions. We need an efficient transformation whose output distribution retains the distinction between the two possible origins of $z$.

#### 4. How will we solve this?

We introduce hybrids $H_0,\ldots,H_\ell$ that gradually replace applications of $G$ with uniform sampling. Adjacent hybrids differ in exactly one place: a pair consisting of a state and an output bit is either generated by $G$ or sampled uniformly. This is where $\mathcal B$ can insert its challenge.

![[Pasted image 20261111115528.png]]

### Hybrid Argument

#### 1. Goal and intuition

The endpoints will satisfy

$$ H_0\equiv G^\ell(U_\lambda), \qquad H_\ell\equiv U_{\lambda+\ell}. $$

Here $\equiv$ means identical distributions. Each $H_i$ denotes a distribution of complete output strings, not a pre-existing string whose bits $\mathcal B$ can reuse.

Our assumption concerns $\mathcal A$ distinguishing these endpoints. **We do not assume that it distinguishes every adjacent pair.** The triangle inequality motivates looking at transitions: if $p_i=\Pr[\mathcal A(H_i)=1]$, then

$$ |p_0-p_\ell|\leq\sum_{i=0}^{\ell-1}|p_i-p_{i+1}|. $$

A difference between the endpoints must therefore be reflected in at least some transitions. To handle the polynomially many transitions with one PPT algorithm, we will let $\mathcal B$ choose its transition uniformly at random. Its advantage will be calculated explicitly below.

#### 2. Constructing the hybrids

Take $\ell=4$. The original experiment $H_0$ begins with a uniform seed and performs all four calls to $G$:

$$ \begin{aligned} s_0&\gets U_\lambda,\ (s_1,b_1)&=G(s_0),\ (s_2,b_2)&=G(s_1),\ (s_3,b_3)&=G(s_2),\ (s_4,b_4)&=G(s_3). \end{aligned} $$

It outputs $(b_1,b_2,b_3,b_4,s_4)$. Only $s_0$ is sampled uniformly; the later states and bits are computed deterministically using $G$.

The other hybrids produce an output of the same form, but generate its components differently:

|Hybrid|Uniform values sampled independently|Remaining computation|
|---|---|---|
|$H_0$|$s_0\gets U_\lambda$|Four calls to $G$, starting from $s_0$|
|$H_1$|$(s_1,b_1)\gets U_{\lambda+1}$|Three calls, starting from $s_1$|
|$H_2$|$b_1,b_2\gets U_1$ and $s_2\gets U_\lambda$|Two calls, starting from $s_2$|
|$H_3$|$b_1,b_2,b_3\gets U_1$ and $s_3\gets U_\lambda$|One call, starting from $s_3$|
|$H_4$|$b_1,b_2,b_3,b_4\gets U_1$ and $s_4\gets U_\lambda$|No calls to $G$|

In $H_2$, for example, we sample two uniform output bits and one uniform state; we do not sample two seeds. There is no need to reconstruct earlier states $s_0,s_1$, because the experiment continues directly from the freshly sampled $s_2$.

The notation $U_n$ means a uniform distribution on $n$-bit strings. Thus, $b_j\gets U_1$ samples one bit, while $s_i\gets U_\lambda$ samples a $\lambda$-bit state. Sampling $b_1,b_2$ independently from $U_1$ is equivalent to sampling $(b_1,b_2)\gets U_2$; each pair $00,01,10,11$ has probability $1/4$. Independent fair coin flips describe exactly this sampling.

> [!example]- Earlier illustration with three iterations The same replacement pattern for $\ell=3$ is shown below. Its final output has $\lambda+3$ bits; the four-iteration example above has $\lambda+4$ bits.
> 
> ![[Pasted image 20261111121314.png]]

#### 3. General definition of $H_i$

For any $0\leq i\leq\ell$, generate a sample from $H_i$ as follows:

1. Sample $b_1,\ldots,b_i$ independently from $U_1$.
2. Sample $s_i\gets U_\lambda$, independently of those bits.
3. For $j=i+1,\ldots,\ell$, compute $(s_j,b_j)=G(s_{j-1})$.
4. Output $(b_1,\ldots,b_\ell,s_\ell)$.

When $i=0$, the prefix is empty and every pair is generated using $G$, reproducing $G^\ell(U_\lambda)$. When $i=\ell$, no calls to $G$ remain. The output consists of $\ell$ independent uniform bits and an independent uniform $\lambda$-bit state, so it is exactly uniform on $\lambda+\ell$ bits. Consequently,

$$ \boxed{H_0\equiv G^\ell(U_\lambda),\qquad H_\ell\equiv U_{\lambda+\ell}}. $$

#### 4. Why are consecutive hybrids indistinguishable?

Fix a transition index $i\in{0,\ldots,\ell-1}$. The first $i$ output bits are uniform in both $H_i$ and $H_{i+1}$. The difference is the next pair:

$$ \begin{array}{c|c} H_i & (s_{i+1},b_{i+1})=G(s_i),\quad s_i\gets U_\lambda\ H_{i+1} & (s_{i+1},b_{i+1})\gets U_{\lambda+1}. \end{array} $$

After this pair, both experiments continue by applying $G$ from $s_{i+1}$. Thus, each transition replaces $G(U_\lambda)$ with $U_{\lambda+1}$ and otherwise uses the same efficient procedure. An efficient adversary distinguishing the resulting adjacent hybrids could therefore distinguish the original challenge distributions. The next section constructs that reduction and then combines all transitions.

### Proving the Hybrid Argument

#### Constructing $\mathcal B$ from $\mathcal A$

The challenger gives $\mathcal B$ a single string $z$ sampled from $G(U_\lambda)$ or $U_{\lambda+1}$. Using the same endpoint adversary $\mathcal A$ assumed above, $\mathcal B$ does the following:

1. Choose an index $I$ uniformly from ${0,\ldots,\ell-1}$, independently of $z$. Write $i$ for its selected value.
2. Sample fresh prefix bits $b_1,\ldots,b_i$ independently from $U_1$, also independently of $z$.
3. Split the received string as $z=(s_{i+1},b_{i+1})$, with a $\lambda$-bit state and a one-bit output. This step labels parts of $z$; it generates no new randomness.
4. For $j=i+2,\ldots,\ell$, compute $(s_j,b_j)=G(s_{j-1})$.
5. Form $z'=(b_1,\ldots,b_\ell,s_\ell)$, give this complete string to $\mathcal A$, and return its output: $\mathcal B(z)=\mathcal A(z')$.

The prefix bits are newly generated by $\mathcal B$; they are not taken from $z$ or from a previously existing hybrid sample. They are called a prefix because they occupy the beginning of $z'$. The final string has $\lambda+\ell$ bits: $\ell$ output bits and one final $\lambda$-bit state.

The general procedure for a selected transition is also shown in the existing illustration:

![[Pasted image 20261111124422.png]]

#### Concrete simulation: $\ell=4$ and $i=2$

Suppose $\mathcal B$ chooses $i=2$. It samples $b_1,b_2$ independently, interprets its challenge as $z=(s_3,b_3)$, and computes $(s_4,b_4)=G(s_3)$. It gives $\mathcal A$

$$ z'=\left( \underbrace{b_1,b_2}_{\text{fresh uniform bits}}, \underbrace{b_3}_{\text{from the challenge}}, \underbrace{b_4,s_4}_{\text{computed using }G} \right). $$

For instance, if the prefix sampling yields $(b_1,b_2)=(0,1)$, the actual input is $(0,1,b_3,b_4,s_4)$. The prefix remains independent of the challenge whether sampled before or after the remaining computation.

If $z\gets G(U_\lambda)$, the pair $(s_3,b_3)$ is generated by $G$ on a hidden uniform state $s_2$. Together with the fresh prefix and the final call to $G$, this is exactly $H_2$. $\mathcal B$ does not need to recover $s_2$.

If $z\gets U_{\lambda+1}$, splitting it yields a uniform $s_3$ and an independent uniform $b_3$. Together with $b_1,b_2$ and the final call to $G$, this is exactly $H_3$. A “uniform state” means that each of the $2^\lambda$ possible state strings has probability $2^{-\lambda}$; we make that claim here only in the uniform-challenge case.

The same boundary reasoning handles $i=0$: a generated challenge has already performed the first call $G(s_0)$ on a hidden uniform seed and leads to $H_0$, whereas a uniform challenge replaces the first pair and leads to $H_1$. For $i=\ell-1$, no further call to $G$ is needed; a uniform challenge gives $H_\ell$.

> [!example]- Earlier first-transition illustration with $\ell=3$ For $i=0$, the prefix is empty. Split $z=(s_1,b_1)$, compute $(s_2,b_2)=G(s_1)$ and $(s_3,b_3)=G(s_2)$, and pass $(b_1,b_2,b_3,s_3)$ to $\mathcal A$. Generated and uniform challenges produce $H_0$ and $H_1$, respectively.
> 
> ![[CR_L5_first_hybrid_reduction.svg|700]]

#### Why the output probabilities match

For every selected index $i$, the simulation is exact:

$$ \boxed{ \begin{aligned} z\gets G(U_\lambda)&\implies z'\text{ is distributed as }H_i,\ z\gets U_{\lambda+1}&\implies z'\text{ is distributed as }H_{i+1}. \end{aligned}} $$

$\mathcal B$ knows which index it selected, but does not know which challenge world it is in. It uses the same procedure in both worlds. The enlargement preserves the effect of the challenge's origin: an algorithm distinguishing the resulting long samples would also distinguish the original short challenges by returning the same bit.

Define $p_i=p_i(\lambda)=\Pr[\mathcal A(H_i)=1]$. The notation “$=1$” inside the probability specifies the event that $\mathcal A$ outputs the bit $1$; it does not say that the probability itself is $1$. All probabilities include the sample randomness and the adversary's random coins.

Conditioned on $I=i$, exact simulation and $\mathcal B$ returning $\mathcal A$'s bit give

$$ \begin{aligned} \Pr[\mathcal B(G(U_\lambda))=1\mid I=i]&=p_i,\ \Pr[\mathcal B(U_{\lambda+1})=1\mid I=i]&=p_{i+1}. \end{aligned} $$

For example, if $\mathcal A$ outputs $1$ with probability $0.3$ on $H_i$, then $\mathcal B$ outputs $1$ with probability $0.3$ in the generated-challenge world for that selected index. The probabilities are equal because the input distribution is identical and the output bit is passed on unchanged. No assumption that $\mathcal A$ always guesses correctly is needed.

#### Averaging over the chosen transition

With $\ell=4$, there are four possible transitions. $\mathcal B$ chooses one row of the following table, each with probability $1/4$, and sends exactly one string to $\mathcal A$:

|Selected index|If $z\gets G(U_\lambda)$|If $z\gets U_{\lambda+1}$|
|---|---|---|
|$i=0$|An $H_0$ sample|An $H_1$ sample|
|$i=1$|An $H_1$ sample|An $H_2$ sample|
|$i=2$|An $H_2$ sample|An $H_3$ sample|
|$i=3$|An $H_3$ sample|An $H_4$ sample|

The factor $1/4$ describes the choice of row, not $\mathcal A$'s success probability. Averaging the conditional output probabilities gives

$$ \begin{aligned} \Pr[\mathcal B(G(U_\lambda))=1] &=\frac{p_0+p_1+p_2+p_3}{4},\ \Pr[\mathcal B(U_{\lambda+1})=1] &=\frac{p_1+p_2+p_3+p_4}{4}. \end{aligned} $$

For instance, the term $p_2/4$ in the first expression comes from choosing row $i=2$ with probability $1/4$ and then obtaining output $1$ with conditional probability $p_2$. Taking the absolute difference of the two averages gives

$$ \begin{aligned} \operatorname{Adv}_{\mathcal B}^{G}(\lambda) &=\left|\frac{p_0+p_1+p_2+p_3}{4} -\frac{p_1+p_2+p_3+p_4}{4}\right|\ &=\frac{|p_0-p_4|}{4}. \end{aligned} $$

The intermediate terms cancel, leaving only the endpoint difference. For general $\ell=\ell(\lambda)$, the same calculation is

$$ \begin{aligned} \operatorname{Adv}_{\mathcal B}^{G}(\lambda) &=\left|\frac1\ell\sum_{i=0}^{\ell-1}p_i -\frac1\ell\sum_{i=0}^{\ell-1}p_{i+1}\right|\ &=\frac1\ell\left|\sum_{i=0}^{\ell-1}(p_i-p_{i+1})\right|\ &=\frac{|p_0-p_\ell|}{\ell}. \end{aligned} $$

The denominator comes from the uniform choice among $\ell$ transitions: each conditional probability is weighted by $1/\ell$. The notation $\ell(\lambda)$ records that the number of iterations, and hence transitions, can depend on the security parameter, for example $\ell(\lambda)=\lambda^2$.

By our contradiction assumption and the definitions of the endpoints,

$$ |p_0-p_\ell| =\left|\Pr[\mathcal A(G^\ell(U_\lambda))=1] -\Pr[\mathcal A(U_{\lambda+\ell})=1]\right| =\varepsilon(\lambda). $$

Substituting this name for the endpoint difference yields

$$ \boxed{\operatorname{Adv}_{\mathcal B}^{G}(\lambda) =\frac{\varepsilon(\lambda)}{\ell(\lambda)}}. $$

This calculation keeps the sign of each difference until after summing, which is why the terms telescope. It does not assume that $\mathcal A$ distinguishes every adjacent pair or that all transition differences have the same sign. Choosing the index inside one algorithm also handles the polynomial-length hybrid issue directly, rather than relying on a separate asymptotic claim for each fixed index.

#### Contradiction and conclusion

$\mathcal B$ is PPT: it samples at most $\ell-1$ prefix bits, performs at most $\ell-1$ evaluations of the efficient generator $G$, and runs the PPT adversary $\mathcal A$. These operations take polynomial time because $\ell(\lambda)$ is polynomially bounded.

By assumption, $\varepsilon(\lambda)$ is non-negligible. Dividing it by the positive polynomially bounded $\ell(\lambda)$ still gives a non-negligible function. Therefore, $\mathcal B$ would distinguish $G(U_\lambda)$ from $U_{\lambda+1}$ with non-negligible advantage, contradicting the security assumption on $G$.

Our temporary assumption that $G^\ell$ is insecure must be false. Hence

$$ \boxed{G^\ell(U_\lambda)\approx_c U_{\lambda+\ell}}. $$

**End of the proof of Theorem 2.** Security of the original one-bit-stretch $G$ was assumed; security of the constructed $G^\ell$ has been proved. This establishes stretch amplification, the first ingredient of the general OWF-to-PRG result stated on PDF p. 4. The adjacent-hybrid simulation follows PDF pp. 7–11; the random-index averaging above makes its endpoint-advantage calculation explicit.

## Hard-Core Bits

> [!warning] Review before lesson 6 I need to study this final part more carefully before starting lesson 6.

### Motivation: one-wayness does not hide every input bit

Theorem 2 assumed a secure one-bit-stretch generator. We now ask how to obtain that starting generator. Let

$$ f:{0,1}^{n}\rightarrow{0,1}^{n} $$

be a one-way function: evaluating $f(x)$ is efficient, while finding a valid preimage of $f(x)$ for uniform $x$ is computationally hard. Here $n$ plays the role of the security parameter $\lambda$ used earlier.

The professor asks whether the hardness of finding a valid preimage also means that each input bit is hard to predict. Not necessarily: imagine an input consisting of two parts,

$$ x=(b,t) $$

where $b$ is a single bit and $t$ is a longer binary string.

Suppose $g$ is a one-way function, and we construct:

$$ f(b,t)=(b,g(t)) $$

![[Pasted image 20261111125011.png]]

The first output bit reveals $b$ immediately. However, finding a valid preimage still requires inverting $g$, so $f$ remains one-way. This separates two tasks: learning one input bit can be easy even when finding a complete valid preimage is hard.

### Definition of a hard-core predicate

A hard-core predicate for $f$ is an efficiently computable function

$$ \boxed{h:{0,1}^{n}\rightarrow{0,1}} $$

with the following property: **given $f(x)$, no PPT adversary can predict the bit $h(x)$ with probability non-negligibly better than $1/2$, when $x$ is sampled uniformly.**

The adversary knows the functions $f$ and $h$, but does not receive $x$. The function $h$ is public, not a secret key. Knowing how to compute $h$ from an input does not necessarily allow the adversary to compute $h(x)$ from $f(x)$.

A random guess of one bit already succeeds with probability $1/2$. The requirement is therefore not that prediction must always fail, but that no PPT adversary gains a non-negligible improvement over that baseline. Formally, for every PPT adversary $\mathcal A$,

$$ \boxed{\Pr_{x\gets U_n}[\mathcal A(f(x))=h(x)] \leq\frac12+\operatorname{negl}(n)}. $$

The probability includes the uniform choice of $x$ and the adversary's random coins. The negligible bound may depend on $\mathcal A$.

This requirement is **one-directional**: the adversary receives $f(x)$ and tries to predict $h(x)$. It places no reverse requirement on predicting $f(x)$ from $h(x)$. The two security properties concern different tasks:

- **One-wayness of $f$:** given $f(x)$, finding a valid preimage is hard.
- **Hard-core property of $h$ for $f$:** given $f(x)$, predicting $h(x)$ better than chance by a non-negligible amount is hard.

When $x$ is known, both $f(x)$ and $h(x)$ can be computed efficiently. Thus, an example that reveals $h(x)$ can violate the hard-core property while $f$ remains one-way.

The professor gives an equivalent distributional formulation: the left-hand pair uses one shared sample $x\gets U_n$, while the comparison bit $u\gets U_1$ on the right is independent of $x$:

$$ \boxed{ (f(x),h(x))_{x\gets U_n} \approx_c (f(x),u)_{x\gets U_n,,u\gets U_1} } $$

Thus, even when given $f(x)$, an efficient adversary cannot distinguish the real bit $h(x)$ from an independent uniform bit with non-negligible advantage. This is the form we will use to prove pseudorandomness of the new generator.

### Preliminary fact: a permutation preserves uniformity

The hard-core property will supply one pseudorandom bit. We also need the other $n$ output bits to look uniform. For the simple construction in this lecture, we assume a **one-way permutation (OWP)**: a one-way function that is also a bijection. Consider

$$ f:{0,1}^{n}\rightarrow{0,1}^{n} $$

Every $n$-bit output has exactly one corresponding input. A permutation therefore rearranges the uniform distribution without changing it:

$$ \boxed{f(U_n)\equiv U_n}. $$

The output distribution is exactly uniform even though finding the corresponding input remains computationally hard.

### Theorem 3 — A one-bit-stretch PRG from an OWP

**Assumptions:** $f$ is a one-way permutation, and $h$ is a hard-core predicate for this $f$.

**Construction:** the professor defines

$$ \boxed{G(s)=f(s)\parallel h(s)} $$

For a uniform seed $s\gets U_n$, the two functions use the same $s$. The function $h$ produces one bit; it is not a second independent seed.

![[Pasted image 20261111125200.png]]

This satisfies the expansion requirement:

$$ G:{0,1}^{n}\rightarrow{0,1}^{n+1} $$

**Conclusion to prove:** $G(U_n)\approx_c U_{n+1}$. Here $n$ plays the same role as $\lambda$ in the earlier sections.

#### Proof of Theorem 3

The proof on PDF p. 13 has two steps. **First, use the hard-core property:** the bit $h(s)$ can be replaced by an independent uniform bit $u$ without an efficient adversary gaining non-negligible distinguishing advantage:

$$ (f(s),h(s))_{s\gets U_n} \approx_c (f(s),u)_{s\gets U_n,,u\gets U_1} $$

**Second, use the permutation property:** $f(U_n)\equiv U_n$. Since $u$ was sampled independently of $s$, it is also independent of $f(s)$. Therefore,

$$ (f(s),u)_{s\gets U_n,,u\gets U_1}\equiv(U_n,U_1) $$

The two components on the right are independent and uniform, so their concatenation is a uniform $(n+1)$-bit string:

$$ (U_n,U_1)\equiv U_{n+1} $$

Putting these statements together:

$$ \boxed{ \underbrace{(f(s),h(s))_{s\gets U_n}}_{G(U_n)} \approx_c \underbrace{(f(s),u)_{s\gets U_n,,u\gets U_1}}_{\text{Hard-core property}} \equiv \underbrace{U_{n+1}}_{\text{Uniform}} } $$

Hence:

$$ \boxed{G(U_n)\approx_c U_{n+1}} $$

This gives a secure one-bit-stretch PRG.

**End of the proof of Theorem 3.** This supplies the kind of starting generator assumed in Theorem 2, under the OWP and hard-core assumptions above.

### Limitation: replacing the OWP with an arbitrary OWF

The second step of this proof is the reason for assuming a permutation. For an arbitrary OWF, we cannot necessarily write

$$ f(U_n)\equiv U_n $$

Some outputs may occur more frequently than others or never occur at all. Therefore, the simple construction

$$ G(s)=f(s)\parallel h(s) $$

does not necessarily produce pseudorandom output.

The general OWF-to-PRG result stated earlier still holds, but handling this non-uniformity requires additional techniques. The simple proof above establishes the OWP case; it does not supply the full construction from an arbitrary OWF.

PDF p. 14 also announces an existence result for hard-core bits in the general OWF setting, without developing the construction. The precise role of function transformations and auxiliary randomness is outside the proof supplied here.

### A separate question: can one predicate work for every OWF?

The professor then asks whether we can choose one fixed efficient predicate $h$ that is hard-core for every OWF. The following examples explain why the answer is no. This discussion follows the proof of Theorem 3; it is not another step in that proof.

**Example: the first input bit.** Suppose we propose
$$ h(x)=x_1 $$

where $x_1$ is the first bit of $x$.

To test whether this choice works for every OWF, recall the example

$$ f(b,t)=(b,g(t)) $$

where $g$ is a one-way function.

The function remains one-way, but it explicitly reveals $b$. Hence, for

$$ h(b,t)=b $$

an adversary receiving $f(b,t)$ can recover $h(b,t)$ immediately.

$$ \Pr[\mathcal A(f(x))=h(x)]=1 $$

The adversary succeeds at predicting $h(b,t)$, without inverting $f$. Thus, this $h$ is not hard-core for this particular OWF, although $f$ remains one-way. This does not rule out the predicate being hard-core for another function; it rules out treating it as a universal choice.

The professor's broader idea is to take a proposed fixed predicate and build a one-way function that reveals its value.

**Supplementary illustration of the idea.** For a candidate efficient predicate $h$ and an OWF $g$, consider

$$ \boxed{f_{\mathrm{bad}}(x)=(g(x),h(x))} $$

![[Pasted image 20261111125344.png]]

This function remains one-way if $g$ is one-way and $h$ is an efficiently computable single-bit predicate.

To see why, suppose an efficient inverter for $f_{\mathrm{bad}}$ succeeded with non-negligible probability. Given $g(x)$, an inverter for $g$ could guess a uniform bit $c$, run that inverter on $(g(x),c)$, and check the returned preimage. With probability $1/2$, $c=h(x)$, so this preserves at least half of the inverter's success probability. It would contradict one-wayness of $g$.

But an adversary trying to predict $h(x)$ from $f_{\mathrm{bad}}(x)$ has a trivial strategy: read the last bit.

Therefore:

$$ \Pr[\mathcal A(f_{\mathrm{bad}}(x))=h(x)]=1 $$
So $h$ is not hard-core for $f_{\mathrm{bad}}$.

This supplementary example has output one bit longer than $g$'s. It illustrates the prediction-versus-inversion distinction, but is not the complete length-preserving construction suggested on PDF p. 14. The supplied slide gives the idea and an auxiliary-OWF premise; the transcript ends during the discussion, so its remaining steps cannot be reconstructed reliably from these materials.

The question is therefore about a fixed predicate working for every unchanged OWF. Transforming a function to obtain a hard-core predicate is a different construction.

> [!info]- Supplementary preview: Goldreich–Levin Goldreich–Levin provides a hard-core predicate for a transformed function using an additional random string. This name and construction are supplementary context, not a theorem stated or proved in the supplied lesson-5 material. See the [Stanford notes, Goldreich–Levin method](https://crypto.stanford.edu/pbc/notes/crypto/hardcore.html) for that preview; its proof is outside this note.

## Sources
- [Lecture-5 slides, 2026/27](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/Assets/SLIDES/crypto_lecture05_2627.pdf): PDF pp. 1–3, indistinguishability/PRGs and the unbounded attack; pp. 4–11, stretch amplification and hybrids; pp. 12–14, hard-core bits and one-way permutations.
- [Lecture-5 transcript](https://raw.githubusercontent.com/likingaxis/UNIVE/refs/heads/v4/content/UNI/Magistrale/ANNO1%20M/CRYPTOGRAPHY/Assets/TRANSCRIPTION/CR%20LESSON%205%20Transcripted.md): secondary support for the explanations; heavily duplicated and sometimes garbled. It ends mid-discussion of the universal-predicate question, so it does not independently establish the complete classroom stopping point.
- [The Joy of Cryptography, §4.3.1](https://joyofcryptography.com/comp/): supplementary reference for handling polynomially many hybrid transitions; the proof of Theorem 2 above makes the random-index reduction explicit. This formalization is separate from the professor's adjacent-hybrid presentation.
- The game, PRG-world and counting diagrams redraw the supplied illustrations; the stretch and first-hybrid diagrams are converted from the supplied inline SVGs. Original screenshot files are retained.

The theorem numbers in this note organize the results for study; they are not numbering printed on the professor's slides. The explicit random-index reduction and the two clearly labeled supplementary discussions are explanatory additions rather than a verbatim transcript.