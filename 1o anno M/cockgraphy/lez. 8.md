# Block ciphers
**note**: the name is actually misleading, because they are note ciphers on their own. Actually they are pesudorandom permutations.

**examples**: DES, AES, ...

**invertible**: b.c  are used often as an instatiation of a PRF, but they are more, as they are **invertible**. How do we make a PRF invertible?

**feistel network**: design at IBM by feistel and is the inspiration of many block ciphers.

$$\Psi_{F}(x,y) = (y, x \oplus F(y)) = (x',y')$$

![[lez. 8 2026-10-23 16.28.17.excalidraw]]

$$\Psi^{-1}_F(x',y') = (F(x') \oplus y', x')$$

**Q**: is thus a PRP, assuming $F$ a PRF? 
**R**: No, because 1st output half equals 2nd half of the input.

**Stackable**: i can stack $\Psi$ and iterate. So we can solve the problem exposed in $Q$.


![[lez. 8 2026-10-23 16.29.38.excalidraw]]
* $F,F'$ are independent random functions. 
* $F$ has its own key, and $F'$ has a different key.
* **keys**: block ciphers use different keys inside their algorithm.

**Q**: Did we get a PRP?
**R**: No.

**Observation**: 
$$
\Psi_{F,F'}(x,y) \oplus \Psi_{F,F'}(x',y) = \left( x \oplus x', \dots \right)
$$
* we make two different queries.
* it turns out this is the "only problem".

**Fix**: add one more round. We'll get a PRF this time.

$F$, in the real word:
* $F$ is heuristic
* all the keys are derived from single $k$ using an heuristic PRP.

**Lemma**: for every unbounded attacker making $q=\text{poly}(\lambda)$ queries, then the following are undistinguishible:
1. $S: \Psi_{F,F'}(x,y)'; F,F \gets \mathbb R(n,n)$
	1. $F,F'$ are just two random functions
2. $R: R(x,y); R \gets \mathbb R(2n, 2n)$
* **important assumption**: So as long the queries made by $\mathcal A$ are $y\text{-unique}$ ($y$ are all different).

> gemini check this: $\mathbb R(n,n)$ set of functions going from a set of $n$ elements to another set of $n$ elements.

## the proof that i did not understand at all
**proof**: let $H_{i}$ be the experiment were we reply to the first $i$ queries as in  $S$, and all other as in $R$.
* we switch from $S$ (its feistel) and then we switch to $R$ (random).
* $H_{0} \equiv R \text{ and } H_{q} \equiv S$.


Let's look ath $H_{i}$:
* $x_{j} \oplus F(Y_{j}); y_{i} \oplus F'(x_{j} \oplus F(y_{j}))$ for $j=1,\dots,i-1$
* $x_{i} \oplus F(y_{i}); y_{i} \oplus F'(x_{i} \oplus F(y_{i}))$, $\dots$
* we want to show that $H_{i}$ is indistinguishable from $H_{i-1}$.

**since $y_{i}$ are all different** from all $y_{j}$, then $F(y_{i})$ is random (since $F$ is random) and also independent of $F(y_{1}),\dots,F(y_{i-1})$ and everything else. So:

$$
(\dots)_{j=1,\dots, i-1} \to \text{same as before}
$$

$$
x_{i}\oplus r, y_{i} \oplus F'(x_{i} \oplus r)
$$
* with random a $r$
* **essentially**: i can replace $y_{i}$  with $r$ because they are all different by assumption. (???)

**question**: can i replace $F'(x_{i} \oplus r)$ with $F'(r)$? so the input is completly random looking (???)

what's the probability that $x_{i} \oplus r = x_{j} \oplus F(y_{j})$? it is negligible, at most $(i-1) 2^{-n}$
* assuming it does not happen...
* we get $(x_{i} \oplus r, y_{i} \oplus r')$ and they are random!

what happened: i got form $H_{i}$ to $H_{i-1}$. PORCACCIODIDDIOPORCODDIO.

By the hybrid argument: $SD(S;R) \leq \sum_{i} (i-1)2^{-n} \leq q^2 2^{-n} = \text{negl}(\lambda)$.


## feistel proof

**THM**: assuming $\mathcal F$ a PRF family, then 3 rounds of feistel with independent keys is a PRP.

**proof**: consider the following systems (what box the adversary can query).
1. $T: \Psi_{F_{k_{3}}}(\Psi_{F_{k_{2}}}(\Psi_{F_{k_{1}}}(x,y))$
2. $S: \Psi_{F,F'}(\Psi_{F_{F''}}(x,y))$
3. $R: R(x,y); R \gets \mathbb R(2n, 2n)$
	1. $\mathbb R$ is a random function
4. $P: P(x,y); P \gets \mathbb P(2n, 2n)$
	1. $\mathbb P$ is a random permutation

> **note**: a pesudorandom function is indistingushable from a random function.
> * a pseudorandom function cannot be efficiently inverted given the key
> * a random function can be inverted easily.

proof for 1-4.
1. $T \approx_{c} S$. Why? By PRF theorem, $F \approx \text{PRF}$
2. $S \approx_{S} R$. for $\text{poly}(\lambda)$ queries. **IDEA**: 1 round gives you $y\text{-uniques}$,  $\Psi_{F''}(x_i, y_{i})$ satisfies $y\text{-uniques}$
	1. take $(x_{i}, y_{i}) \neq (x_{j}, y_{j})$
	2. we want to compute the $\text{Pr}$ so that the two does not satisfie $y\text{-uniques}$
	3. **case 1**: $y_{i}=y_{j}$, then $x_{i} \neq x_{j}$
		1. $y_{i}'' = x_{i} \oplus F''(y_{i}) = x_{i} \oplus F''(y_{j})$
		2. $\neq x_{j} \oplus F''(y_{j}) = y_{j}''$
		3. so they are always different.
	4. **case 2**: let $y_{i} \neq y_{j}$, then we would need
		1. $x_{i} \oplus F''(y_{i}) = x_{j} \oplus F''(y_{j})$
		2. or $x_{i} \oplus x_{j} = F''(y_{i}) \oplus F''(y_{j})$
		3. this happens with $\text{pr} \leq 2^{-n}$
	5. so: $\text{Pr}[\lnot y\text{-unique}] \leq \binom{q}{2} - 2^{-n} = \text{negl}(\lambda)$, then $S \equiv_{s} R$ by the lemma.
3. $R \approx_{S} P$. A random functions is already is already ... from a random permutation assuming ... ???

But one question remains: we can do SKE beating Shannon assumming any PRF.

$$
C = (r, F_{k}(r) \oplus m), \text{ with } r \text{ random}
$$

What about **very long messages**: $m = m_{1},\dots,m_{t}$ with $m_{i} \in \{ 0,1 \}^n$?

**Mode of operation/Domain Extension**: descrive how do we use cypher $X$ to encrypt a long message? 
* **ECB**: (Elettronic CodeBook), perhaps the simplest idea is to just do 
	* $m_{1} \to F_{k} \to c_{1}$
	* ...
	* $m_{t} \to F_{k} \to c_{t}$.
* Its unsecure, because $F_{k}$ is deterministic
* Nobody uses ECB.

**CBC**:
![[lez. 8 2026-10-23 17.58.08.excalidraw]]


**CFB and OFB**:
![[lez. 8 2026-10-23 18.03.08.excalidraw]]
> think about of decryption works given the encryption.


**note**: in some constructions you can parallelize computation. understand wich one as exercise.

**CTR**: is fully parallelizable.
![[lez. 8 2026-10-23 18.08.17.excalidraw]]

**thm**: CTR is CPA (for variable input length!) secure assuming F is a PRF. 
* Note that adversary can choose input length

> **note**: all modes (expect the first one) are secure.

**Proof**: we need to proof that no adversary can distinguish encryption of $m_{0}$ from $m_{1}$ were they have arbitrary length.

We design a game, it works like this:
* $\mathcal A$ makes a query to $C$ and gets a response.
* $\mathcal A \to m=m_{1},\dots,m_{t} \to \mathcal C$
* $\mathcal A \gets c = c_{0},\dots,c_{t} \gets C$
* **note**: $t$ can be different in every query
* $\mathcal A \to m^*=m_{1}^*,\dots,m^*_{t^*} \to \mathcal C$
* $\mathcal A \gets c = c_{0},\dots,c_{t} \gets C$
* **note**: $\mathcal A$ can make a how many requests he wants.
* $\mathcal A \to b$: outputs $b$.

Let $G_{0}$ be the above game with $b=0$ and using **CTR** for encryption. Same for $G_{1}$ with $b=1$. We need to show $G_{0} \approx_{c} G_{1}$. 
* CTR means that $c_{0} =r, c_{1}=F_{k}(r) \oplus m_{1}, \dots, c_{t} = F_{k}(r + t-1)+m_{t}$

By security of $F$ we can replace $F_{k}$ with $R \gets \mathbb R(n,n)$, let us call this $H_{0}, H_{1}$. So $G_{0} \approx_{c} H_{0}$ and $G_{1} \approx_{c} H_{1}$. We finally introduce $H_{2}$ s.t. $c_{0}^*, c_{1}^*, \dots c_{t}^*$ is uniformly random. We will show that $H_{0} \approx_{S} H_{2}$ and $H_{1} \approx_{S} H_{2}$ assuming $\#$ queries is $q=\text{poly}(\lambda)$.

Look 