# attack games

# MAC (Message Authentication Code)
**mac**: symmetric primitive that corrispo
* alice and bob share the same $k$
* alice sends $m$ unencrypted, with a tag.
* alice sends $t\in\mathcal T$
* bob uses gets $m$ and $k$ and calculates $\text{Tag}$
	* is $\tau \in \mathcal T$ the same alice sent?

* $\text{Tag}: \mathcal K \times \mathcal M \to \mathcal T$, the tag is deterministic

**what's the definition of security here**? adversary should be albe to write down $m,t$ to fool bob.
* goal for eve: produce some $m', \tau'$ without knowing $k$ so that $\tau'=\text{Tag}(k,m')$
* **forgery definition**: given pairs of $(m,\tau)$, can Eve forge another valid pair?

**definition**: let $\text{Tag}$ be a MAC over $\mathcal K, \mathcal A, \mathcal T$ is $\epsilon \text{-statistically}$ secure if for every $m,m' \in \mathcal M \text{ and } \tau, \tau' \in \mathcal T \text{ with } m \neq m'$, we want $\text{Pr}[\tau' = \text{Tag(k,m')}|\tau=\text{Tag}(k,m)] \leq \epsilon$
* **one-time definition**: applies only in case given $k$, we forge only one message. if we forge more messages the definition does not apply.
* where $\epsilon$ is $2^{-80}$ or $2^{-128}$ for example...
* where the adversary computes $\tau'$ and $m'$ valid
* we don't care how, we want that it's almost impossible

**exercise 1**: $\epsilon \text{-security}$ is impossible for every $\epsilon=0$
**exercise 2**: OTP for MAC is insecure
**exercise 3**: consider this game
* $\mathcal A$ sends $m\in \mathcal M$
* $\mathcal C$ replies with $\tau = \text{Tag}(m,k)$
	* $k$ is unkown, or eventually chosen by $\mathcal A$
* $\mathcal A$ send $m', \tau'$
	* wins if $m' \neq m$
	* and $\text{Tag}(k,m')=\tau$

then for every attacker, $\text{Pr}[\tau' = \text{Tag(k,m')}|\tau=\text{Tag}(k,m)] \leq \epsilon$. (???)


**definition**: a family $\mathcal H = \{  h_{k}: \mathcal M \to \mathcal T \}_{k\in \mathcal K}$ is **pairwise independent** if for very $m \neq m'$ then $(h(K,m), h(K,m'))$ with $K$ uniform over $\mathcal K$, is also uniform over $\mathcal T^2 = \mathcal T \times \mathcal T$.
* if not uniform, it means that two pair $h_{k}$ and $h_{k'}$ are the same $\text{Tag}$ function?

**note**: $\text{Tag}(k,m)=h(k,m)=h_{k}(m)$.


**example**: $h_{a,b}(m)=a \cdot m + b \mod p$ with $p$ a large prime
* $(a,b) \in \mathbb Z_{p}^2 = \mathcal K$
* $m \in \mathbb Z_{p} = \mathcal M = \mathcal T$





