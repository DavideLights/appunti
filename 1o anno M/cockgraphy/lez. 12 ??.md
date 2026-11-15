
# authenticated encryption
**goals**: build a system that ensures secrecy and authenticity.
* **note**: we treated message secrecy and authenticity as separated goals

**note**: SKE is hard???

**def**. 
* **goal**: the definition must **hide** the message and ensure that no one **tampers** with it.
* we used: $c=(c_{1},c_{2}) = (r, F_{k}(r) \oplus m)$


**malleability**: $\tilde c_{2} = c_{2} \oplus 0^{n-1}1 = F_{k}(r) \oplus (m \oplus 0^{n-1}1)$
* flip the last bit
* changing a bit in the cyphertext, changes a bit of the plaintext.

**malleability attack**: we can change cyphertext $c$ to obtain $\tilde{c}$ of message $\tilde m$ related to $m$ in a non-trivial way. Has many real word applications 

**non-malleability encryption**: above attacks are impossible in a *general sense* (= it should be impossible to create an attack for any possible relation)

**def**. CCA Encryption (implies non-malleability), same as CPA security but with different game.

$$
\text{Game}(\Pi,\mathcal A)(\lambda, b)
$$

* $\mathcal C$ chooses the $k \gets \mathcal K$
* $\mathcal A$ does some queries

**gemini**: rephrase in a coincise way the game attack.
* declare what can do $\mathcal A$
* declare phases of the attack, what $\mathcal A$ and $\mathcal C$ does in each phase???

**query 1:**
* $\mathcal A$ sends $m$
* $\mathcal C$ replies with $c$
* $\mathcal A$ can do another query 1 sending $m$ again.
* in this phase $\mathcal A$ can also do decryption queries.
* **goto**: query 2

**query 1 dec**: decryption queries
* $\mathcal A$ sends $\tilde{c} \neq c^*$
* $\mathcal C$ replies with $\tilde{m}=\text{Dec}(\tilde{c})$

**query 2**:
* $\mathcal A$ sends $m_{0}^*,m_{1}^*$
* $\mathcal C$ gets $c^*$

**query 3**: goto query 1.
* so can enc or dec.


**(26:00) exercise**: the above considered SKE $(c_{1}=r; c_{2}=F_{k}(r) \oplus m)$ is not CCA secure.

>[!error] do the ex 

**non malleability of CCA**: is implied. If i can flip an observe relations i can break easily the game.

**construction**: assumes owf, based on 2 properties
* CPA security
* Authenticity property.

> **note**:  CPA sec + Authenticity  $\equiv$ CCA sec


let $\text{Dec}: \mathcal K \times \mathcal C \to \mathcal M \cup \{ 0 \}$
* where $0$ is "**decrytion error**"
* we define: $\text{Game}_{?,\mathcal  A}^\text{auth}(\lambda)$ that is similar to unforgability game we have seen but for encryption
	* $\mathcal A$ can do as queries he want for $m$
	* $\mathcal C$ replies with its $c$
	* $\mathcal A$ must output a valid $c^* \neq c$, 
		* but we do not care actually that $c^*$ must be related to a fixed/chosen $m$.

**thm**: $\text{CPA + AUTH} \implies \text{CCA}$
**intuition**: since $\text{AUTH}$ holds, then decryption queries are useless. Under AUTH mechanism, CPA is just CCA. Actually CPA **reduces** to CCA.

**reduction**: we show an attack involving those entities: $\mathcal A_{cca}$, $\mathcal B_{cpa}$, $\mathcal C_{cpa}$
* $\mathcal A_{cca}$ sends an encryption query with $m$
	* $\mathcal B_{cpa}$ replies with $c$
* $\mathcal B_{cpa}$ sends an encryption query with $m$
	* $\mathcal C$ replies with $c$
	* $\mathcal B_{cpa}$ can do as many queries he wants

**also**:
* $\mathcal A_{cca}$ can send decryption query sending $\tilde c$.
* **48:00**: did not understand
	* $\mathcal B$ replies with 0 or $m$, if $\tilde{c}= \text{old } c$ ????
**then**: 
* $\mathcal A_{cca}$ sends $m_{0}^*, m_{1}^*$ and expected $c^*$ from $\mathcal B_{cpa}$
* $B_{cpa}$ does the same w.r to $\mathcal C_{cpa}$

Let $\text{BAD}$ be the event:
* $\exists \tilde{c}_{i}$ s.t. $\tilde{c}_{i}$ is FRESH and VALID (???)

$$
\text{Pr}[\mathcal A \text{ wins}] \leq \text{Pr}[\mathcal A \text{ wins } \land \text{BAD}] \\ + \text{Pr}[\mathcal A \text{ wins } \land \lnot\text{BAD}] \leq \mathcal E_{cpa}
$$

**How to get 1+2**? Combine SKE with MAC. many ways to do it.
1. **Encrypt-and-auth**: $c \gets \text{Enc}(k_{1},m)$ and $\tau \gets \text{Tag}(k_{2},m)$. Then $c'=(c,\tau)$. Is it CCA secure? **not always**, because of the tag.
	1. consider sending $m[0]|| \tau'$ where $\tau '$ is a valid tag for $m$.
	2. and so what??? the tag could reveal info aboout $m$
2. $c\gets \text{Enc}(k_{1},m||\tau)$ with $\tau = \text{Tag}(k_{2},m)$
	1. used in TLS 1.2, but its not secure. It was believed to be generally secure (???)
	2. exercices: why? 
		1. tag is encrypted so it does not reveal m
3. **the correct way**: 
	1. $c \gets \text{Enc}(k_{1},m)$
	2. $\tau \gets \text{Tag}(k_{2}, c)$
	3. $c'=(c,\tau)$
4. 












