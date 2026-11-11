k# pseudorandom 
**note**: we have seen SKE systems that are unsecure with multiple messages encrypted

**def. PRF**: 
$$
\mathcal F \{ F_{k}: \{ 0,1 \}^n \to \{ 0,1 \}^n \}_{K\in \{ 0,1 \}^\lambda}
$$
* for $k \gets U_{\lambda}$
* no efficient $\mathcal A$ can identify if a sample is from $F_{k}(\cdot)$ or from a uniformly random function $R: \{ 0,1 \}^n \to \{ 0,1 \}^n$

> **Note**: $R$ is still deterministic but fixed among all possible maps on $\{ 0,1 \}^n \to \{ 0,1 \}^n$

**def**. $\mathcal F$ is a PRF if:

$$
\text{Game}_{\mathcal F, \mathcal A}^{\text{real}}(\lambda) \approx_{c} \text{Game}_{\mathcal F, \mathcal A}^{\text{ideal}} (\lambda)
$$



$\text{Game}^\text{real}$:
1. $\mathcal A$ does a query for $x\in \{ 0,1 \}^n$.
	1. can do as many as he wants
2. $\mathcal C$ has choosen $k \gets U_{\lambda}$, replies with $y=F_{k}(x)$
3. $\mathcal A$ replies with $b'$
$\text{Game}^\text{ideal}$:
4. $\mathcal A$ does a query for $x\in \{ 0,1 \}^n$.
	1. can do as many as he wants
5. $\mathcal C$ has choosen $R \gets \mathcal R(n,n)$, replies with $R(x)$
6. $\mathcal A$ replies with $b'$

**Excercise**: No $\mathcal F$ is a PRF against unbounded adversaries.

How to create a PRF?
* **practice**: use AES, DES or any blockcipher.
	* **note**: cannot prove AES is a PRF
* **theory**: owf, but they are not practical. or use some assumptions like public-key cryptography based on factoring, discrete log, lattices.

**build practical SKE using PRFs:** 
* **pratical**: one key, short, i can use it to encrypt many messages.


**def**. $\Pi=(\text{Enc, Dec})$ is CPA iff
$$
\text{Game}_{\Pi, \mathcal A}^\text{cpa}(\lambda,0) \approx_{C} \text{Game}_{\Pi, \mathcal A}^\text{cpa}(\lambda,1) 
$$

that is:
$$
\text{Game}_{\Pi, \mathcal A}^\text{cpa}(\lambda,b\in \{ 0,1 \}) 
$$
1. $\mathcal A$ queries as many times he wants $m$
2. $\mathcal C$ replies with $c \gets \text{Enc}_{k}(m)$
3. $\mathcal A$ sends $m_{0}^*,m_{1}^*$ to $\mathcal C$
4. **note**: $\mathcal C$ has choosen an unkown key $k \gets \mathcal K$
5. $\mathcal C$ replies with $c^*\gets \text{Enc}_{k}(m_{b}^*)$
6. $\mathcal A$ queries as many times he wants $m$
7. $\mathcal C$ replies with $c \gets \text{Enc}_{k}(m)$
8. $\mathcal A$ outputs $b'$


**REMARK**: $\text{Enc}_{k}$ is randomized, so $c\gets \text{Enc}_{k}(m) \equiv c=\text{Enc}_{k}(m;r)$ with $r \gets \mathcal R$ (a random space)

How does $\text{Dec}_{k}$ work? Example:
* $\text{Enc}(k,m)=(c_{1},c_{2})$
	* $c_{2} = F_{k}(r) \oplus m$, $r \gets U_{n}$
	* $c_{1}=r$
* $\text{Dec}(k, (c_{1},c_{2}))=F_{k}(c_{1}) \oplus c_{2}=m$

**thm**: assuming $\mathcal F$ is a PRF, then $\Pi = (\text{Enc, Dec})$ as above is CPA-secure

**proof**:
* $G(\lambda,b)\equiv \text{Game}_{\Pi, \mathcal A}(b)$
* **goal**: $G(\lambda,0) \approx_{c} G(\lambda,1)$
* consider $H(\lambda,b)$ the same as $G(\lambda,b)$ except
	* $R \in \mathcal R(n,n)$ instead of $F_{k}$\

**Game attacck** $G(\lambda,b)$:
* **goal**: is to break $F_{k}$ on a random choosen $k$, so being able to understand if $c^*$ is $m_{0}^*$ or $m_{1}^*$
1. $\mathcal A$ queries $m$ as many times to $\mathcal C$
2. $\mathcal C$ replies with $c=(c_{1},c_{2})$
	1. $\mathcal C$ chosen and fixed $k \in U_{\lambda}$
3. $\mathcal A$ queries $m_{0}^*, m_{1}^*$
4. $\mathcal C$ replies with $c^*=(c_{1}^*, c_{2}^*)$
	1. $c_{1}^* = r \gets U_{n}$
	2. $c_{2}^* = F_{k}(r) \oplus m_{b}$
5. $\mathcal A$ queries $m$ as many times to $\mathcal C$
6. $\mathcal C$ replies with $c=(c_{1},c_{2})$
7. $\mathcal A$ outputs $b'$

**Game attacck**:
* **goal**: is to break $R$ on a random choosen one from $\mathcal R(n,n)$, so being able to understand if $c^*$ is $m_{0}^*$ or $m_{1}^*$
1. $\mathcal A$ can ask $m$ queries as many times he wants.
2. $\mathcal C$ replies with $c=(c_{1},c_{2})$
	1. $\mathcal C$ chosen and fixed $R \gets \mathcal R(n,n)$
	2. $c_{1} = r \gets U_{}n$
	3. $c_{2} = R(r) \oplus m$
2. $\mathcal A$ queries $m_{0}^*, m_{1}^*$
3. $\mathcal C$ replies with $c^*=(c_{1}^*, c_{2}^*)$
	1. $c_{1}^* = r^* \gets U_{n}$
	2. $c_{2}^* = R(r^*) \oplus m_{b}^*$
4. $\mathcal A$ queries $m$ as many times to $\mathcal C$
5. $\mathcal C$ replies with $c=(c_{1},c_{2})$
6. $\mathcal A$ outputs $b'$

**lemma**: $G(\lambda, \{ 0,1 \}) \approx_{c} H(\lambda, \{ 0,1 \})$

**proof**: by reduction
1. $\mathcal B$ starts the challenge (???)
2. $\mathcal A$ does as many queries he wants and gets $c=(c_{1},c_{2})$ for each $m$ from $\mathcal B$
	1. $c_{1}=r$
	2. $c_{2}= z \oplus m$
3. $\mathcal B$ sends $r \gets U_{n}$ 
4. $\mathcal C$ replies with $z$
	1. it can be $z = F_{k}(r)$
	2. or $z=R(r)$
5. $\mathcal A$ sends $m_{0}^*,m_{1}^*$
6. $\mathcal B$ sends $r^*$
7. $\mathcal C$ replies with $z^*$
8. $\mathcal B$ repies with $c^*$
	1. $c_{1}^*=r^*$
	2. $c_{2}^*=z^* \oplus m^*_{b}$
9. $\mathcal A$ sends $b'$, then $\mathcal B$ sends $b'$ to $\mathcal C$

**Lemma**:
$$
H(\lambda,0) \approx_{s} H(\lambda,1)
$$
* but, so long the attacker, makes $q(\lambda)=\text{poly}(\lambda)$ queries

**proof**, intuition:
* assume no encrption queries
* 