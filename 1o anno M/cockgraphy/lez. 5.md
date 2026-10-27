[4:20] **pseudorandomness**: a deterministic function can create **pseudorandomness**
* from a uniform string 
* we can output bits that look-random

**def. pseudorandomness**: $f$ is pseudorandom iff no $\text{PTT } \mathcal A$ can distinguish it from a random string
	* except for a negligible probability
	* so pseudo.rand. is a property that applies to distributions

**assumptions for def. computationally indistinguishable**
* let $X = \{ X_{\lambda} \}_{\lambda \in \mathbb N}$
* ley $Y = \{ Y_{\lambda} \}_{\lambda \in \mathbb N}$ 
* we have two sets of distributions. 

**def. computationally indistinguishable**: We say that $X$ is computationally indistinguishable from $Y$
$$X \approx_{C} Y$$
if $\forall \text{ PPT } \mathcal A$:
$$
(1) \;\; |\text{Pr}[A(X)=1]-\text{Pr}[A(Y)=1]| \leq \text{negl}(\lambda)
$$
$$
\equiv |\text{Pr}[A(X_{\lambda})=1]-\text{Pr}[A(Y_{\lambda})=1]| \leq \text{negl}(\lambda)
$$

**what the definition says in practice?**
* goal of $A$ is to decide if a "given" $x$ belongs to $X$ or to $Y$
*  we ask if: *pr is not negligible in function of lambda ($\lambda$)*?
	* **note**: $\lambda$ decides how long input and output are
* if $\mathcal A$ can win "often" then $X$ and $Y$ are not computationally indistinguishable
* **note**: we did not point out already how $X$ and $Y$ look like.

**example**:
* $\mathcal A$ receives $z$ that either comes from $X$, or from $Y$
	* if $b=0$, then $z \in X$
	* if $b=1$, then $z \in Y$
* $\mathcal A$ outputs $b'=\{ 0,1 \}$ and wins if $b'=b$.

```mermaid
flowchart
X --b=0--> z
Y --b=1--> z
z --> A
A --> b'
```

In therms of game $(1)$ becomes:
$$
\{ \text{GAME}(\lambda, 0) \}) \approx_{C} \{ \text{GAME}(\lambda, 1) \})
$$
**Pseudorandom Generators**: P.G. extract and **amplify** "recorded random sources". So a **secure** PRG  is a function $G: \{ 0,1 \}^\lambda \to \{ 0,1 \}^{\lambda+l}$ with $l>0$ such that:
1. $\{G(U_{\lambda})\} = \{ X_{\lambda} \}$ 
	- $X_{\lambda}$ is the distribution $G(U_{\lambda})$
	- $U$ stands for Uniform.
	- So i *sample uniformly random strings* and put in $G$
	- The result is $X_{\lambda}$ 
2. $\{G(U_{\lambda})\} \approx_{C} U_{l+\lambda}$
	1. Means that i  want $\{X_{\lambda}\}$  to be *computationally indistinguishable* from $U_{l+\lambda}$.

**Excercise**: no PRG is secure against **unbounded** attackers. Not even if $G: \{ 0,1 \}^\lambda \to \{ 0,1 \}^{\lambda+1}$.
* Adversary can brute force combinations, and find the primitive for $z$.
* **Note**: $X$ is $U$ while $Y$ is $G(U)$
* so given $z\in \{ 0,1 \}^{\lambda+1}$, $\mathcal A$ can find $s \in \{ 0,1 \}^\lambda$ s.t. $z=G(s)$ just by looking at all the combinations, since is unbounded.

**gemini**: what does it mean 
* $\text{Pr}[\mathcal A(z) = 1 : z=G(s); s \gets U_{\lambda}]=1$
* $\text{Pr}[\mathcal A(z) = 1 : z \gets U_{\lambda+1}]=1$

How to construct $G$? its not easy. 

**thm 41:00**: 
* if any **owf** (one way function) exists
* so do PRGs with stretch $l(\lambda)=\text{poly}(\lambda)$ 
	* means that: can stretch of a polynomial factor in $\lambda$.
	* note a polynomial in $\lambda$ is: $a_{n}\lambda^n + \dots a_{1} \lambda + a_{0}$
* The result of the theorem is not something practical, it cannot be easily implemented with code.

> **Note**: often in **crypto** there is difference between theory and practice. something feasible in theory might not be practical

**proof for thm is hard** and so am i. We will discuss main ideas:
1. **thm 1: from $l(\lambda)=1$ to $l(\lambda)=\text{poly}(\lambda)$:** we can design a function that stretchs of 1 bit and produce a function that stratches $\text{poly}(\lambda)$ bits.
 2. **51:50 thm 2: Hard-core bits**.

**thm 1**: 
* assume  $G: \{ 0,1 \}^{\lambda} \to \{ 0,1 \}^{\lambda+1}$ is a PRG
* then there is a $\text{PRG}$: $G^l: \{ 0,1 \}^{\lambda} \to \{ 0,1 \}^{\lambda+l}$ 
* for every $l(\lambda)=\text{poly}(l)$

**construction in excalidraw**:
![[lez. 5 thmconstruction.excalidraw]]
$$
(s_{i}, b_{i}) = G(s_{i-1})
$$

**construction explanation & proof for thm1**:
* **initial seed**: let $s_{0} \in \{ 0,1 \}^\lambda$ an initial seed for $G$
* the first $G$ outputs $s_{1} \in \{ 0,1 \}^\lambda$ and $b_{1} \in \{ 0,1 \}$
	* in total $\lambda+1$ bits.
* then we give again $s_{1}$ in input to $G$ as a seed
* $G$ outputs $s_{2} \in \{ 0,1 \}^\lambda$ and $b_{2} \in \{ 0,1 \}$
* ...
* if we repeat $l$ times we produced bits $b_{1}, \dots, b_{l}$.
	* in total $l$ bits.

**more formarly**:
* let $s_{0} \gets U_{\lambda}$
* for $i \in [l]$, $(s_{i}, b_{i}) = G(s_{i-1})$
	* $s_{i} \in \{ 0,1 \}^\lambda$
	* $b_{i} \in \{ 0,1 \}$
	* were $[l]$ should be $\{ 0,1,\dots,l \}$
* we have gained $l$ bits $(b_{1},\dots,b_{l})$.
* **output**: $(b_{1},\dots,b_{l},s_{l}) \equiv$  $(b_{1},\dots,b_{l}) \text{ concatenated to } s_{l}$

 > **note**: since $s_{0}$ is uniform, then we can assume $G(s_{0})$ also is uniform and so on...

**1:00:0 How to prove thm1?** by reduction. Assume not true. 
* Then there is $PPT$ $\mathcal A$ that breaks $G^l$
* Then we can build a PPT $\mathcal B$ that breaks $G$.
* $\mathcal A$ expects from $\mathcal B$, a value $z' \in \{ 0,1 \}^{\lambda+l}$
* $\mathcal B$ gets $z$ from the **Challenger**.
* ma fare la riduzione da $\mathcal A$ ad $\mathcal B$ e' impossibile ora.

Reducion should look like this:
![[lez. 5 2026-10-27 17.54.26.excalidraw]]
gemini explain what's the difficulty with the reduction:


**There is a problem with the reduction**: what bits should pass $\mathcal B$ to $\mathcal A$?
* $\mathcal B$ breaks $G$ and tells us if $z \in G(U_{\lambda})$ or $U_{\lambda+1}$
* $\mathcal B$  might find or not $x \in \{ 0,1 \}^{\lambda}$ s.t. $G(x) =z$, but then what? 
* then $\mathcal A$ should break $G^l$ using the answer from $\mathcal B$, but they speek different languages and have different goals.
	* $\mathcal A$ takes input $\in \{ 0,1 \}^{ \lambda+\ell}$
	* $\mathcal B$ takes input $\in \{ 0,1 \}^\lambda$

**Solution: the hybrid argument (1:12:00)**: if we need to show $X \approx_{C} Y$ we can do so by finding hybrids $H_{0}, H_{1}, \dots, H_{l}$ such that:
1. $H_{0}\equiv X$ and $H_{l}\equiv Y$.
2. $H_{0} \approx_{C} H_{1}$, ..., $H_{l-1} \approx_{C} H_{l}$
3. by triangle inequality, $H_{0} \approx_{C} H_{l}$ so long as $l(\lambda)=\text{poly}(\lambda)$

How do we find $H_{i}$? idea, lets pretend $s_{1}$ uniform and $b_{1}$ uniform at the first stage in the main idea.
* $H_{1}$: $s_{1},b_{1}$ will be uniform.
* $H_{2}$: $s_{2},b_{2}$ will be uniform. and $s_{1}$ is uniform.
* ...
* $H_{l}: s_{l}, b_{l}$ will be uniform, and $s_{1},\dots,s_{l-1}$ is uniform. 

**formalization** (**critto 5 parte 2 0:00**):
* $H_{0} \equiv G^l(U_{\lambda})$; $H_{l} \equiv U_{l+\lambda}$
* NON CI HO CAPITO NIENTE
* $H_{i}$: $b_{1},\dots,b_{i} \gets \{ 0,1 \}$, $s_{i} \gets U_{\lambda}$, $b_{i+1}, \dots, b_{l}, s_{l} = G^{l-i}(s_{i})$
* $H_{1}$: i pick $b_{1}$ uniformly, $s_{1}$ uniformly and $b_{2},\dots,b_{l}, s_{l} = G^{l-1}(s_{1})$ with $s_{1} \gets U_{\lambda}$.

**now, finally we can do the reduction**: we'll show $H_0 \approx_{C} H_{1}$.
* assume $G$ is secure and $\exists$ PPT $\mathcal A$ that distinguishes $H_{0}$ from $H_{1}$
	* before we wanted to distniguish $H_{0}$ from $H_{l}$, that's why we could not do the reduction.
* we want to find $\mathcal B$ that breaks $G$

* $\mathcal B$ gets $z$ from $\mathcal C$. $\mathcal C$ choses one of the two
	* $z \in G(U_{\lambda})$
	* $z \in U_{\lambda+1}$
* $\mathcal A$ gets from $\mathcal B$ something that does not look like $H_{0}$ and neither like $H_{1}$. The goal is to generating a string containg someway $z$.
	* $z=b_{1} s_{1}$ (concatenation), in $H_{1}$ $s_{1},b_{1}$ are uniform, with $s_{1} \in \{ 0,1 \}^\lambda$ and $b \in \{ 0,1 \}$
	* $(b_{2}, \dots, b_{l}, s_{l})=G^{l-1}(s_{1})$.
	* $\mathcal A$ gets $b_{1},b_{2},\dots,b_{l},s_{l}$

**Observe** if $z \in G(U_{\lambda})$, then $b_{1},\dots,b_{l},s_{l}$ computed by $\mathcal B$ are distribute like $H_{0}$. Else, if $z \gets U_{\lambda+1}$, then it is distrubited like in $H_{1}$.

But by assumption $\mathcal A$, distinguishes $H_{0}$ from $H_{1}$:
$$\text{Pr}[\mathcal A(b_{1},\dots,b_{l},s_{l}): (b_{1},\dots,b_{l}, s_{l}) \gets G^l(U_{\lambda})]- \text{Pr}[\mathcal A(b_{1},\dots,b_{l}, s_{l}): (b_{1}, \dots, b_{l}, s_{l}) \gets H_{1}]  \geq \frac{1}{p(\lambda)}$$
 
* note $G^l(U_{\lambda}) \equiv H_{0}$


And we have shown: 
$$
\text{Pr}[\mathcal B(z)=1: z \gets H_{0}]= \text{Pr}[\mathcal A(b_{1},\dots,b_{l},s_{l})=1:b_{1},\dots, b_{l}, s_{l} \gets H_{0}]
$$
$$
= 
$$


so $\mathcal B$ distinguishes w.p $\geq \frac{1}{p(\lambda)}$, and by **very similar proof**: $H_{i} \approx_{C} H_{i+1}$.

**How do we get (24:00) $G: \{ 0,1 \}^\lambda \to \{ 0,1 \}^{\lambda+1}$ in the first place?** In theory i can do it starting with any ofw, but not very efficiently. Using number theory and other things we can make it more efficient. 

**hard-core bit**: let $f: \{ 0,1 \}^n \to \{ 0,1 \}^n$ be owf. Can we say that a particolar bit of $x$ is hard to compute? Maybe in a owf i can compute some bits of the preimage?

**hard core definition**: $h: \{ 0,1 \}^n \to \{ 0,1 \}$ is hard core if $h(x)$ is hard to compute given $f(x)$.
* alternatively: $(f(x),h(x)) \approx_{C} (f(x),u)$ with $u \in \{ 0,1 \}$.
* given $f(x)$, can i guess $h(x) \in \{ 0,1 \}$
* we want $h(x)$ to be hard to guess. (CHECK THIS)

**Assume** $f: \{ 0,1 \}^n \to \{ 0,1 \}^n$ is a **one-way-permutation**, then look: $G(s) \approx f(s) || h(s)$, with $s \gets U_{n}$. But since $h(s)$ is hardcore, then $b \in \{ 0,1 \}$ is uniform.
$$
f(s) || h(s) \approx_{C} f(s)||b \equiv U_{n+1}
$$

the assumption above works even with $f$ **owf** (and not **owp**). moreover, every $f$ admits hard-core bit $h$.

**Question**: can there be $h: \{ 0,1 \}^n \to \{ 0,1 \}$ for every $f: \{ 0,1 \}^n \to \{ 0,1 \}^n$.