## es 7, punto B
**D:** Consideriamo il numero primo p = 101527 e sia E la curva ellittica su $F_{p}$ definita dall'equazione $y^2 = x^3 + x$. Dedurre che $E(\mathbb F_{}p)$ e' isomorfo a Z/(p + 1)Z

**R1:** dimostrare che $\# E(\mathbb F_{p})$ ha $p+1$ elementi.
* **simbolo di legendre**: $\left( \frac{f(x)}{p} \right)$. Sia $y^2 = f(x) = z$, con $x$ fissato
	* $\left( \frac{f(x)}{p} \right) = 1$ se  $z$ e' un quadrato, ossia due soluzioni per $y^2$.
	* $\left( \frac{f(x)}{p} \right) = -1$ se $z$ non e' un quadrato, ossia nessuna sol per $y^2$
	* $\left( \frac{f(x)}{p} \right) = 0$ se $z \equiv 0 \mod p$.  
* **Teorema Hasse**: $\# E(\mathbb F_p) = p + 1 - a_p$, dove $a_p = - \sum_{0 \leq i \leq p} (\frac{f(x)}{p})$ .
* **Numero di soluzioni**L $1+\left( \frac{f(x)}{p} \right)$ e' il numero di soluzioni in $f(x)$ per una $x$ fissata.
* **Applicare Teorema Hasse** (chiedi a gemini/alfredo): $\# E(\mathbb F_{p})= 1 + \sum_{x \in \mathbb F_{p}} \left(1 + \left( \frac{f(x)}{p} \right)\right)$
* $= 1 + p + \sum_{x \in \mathbb F_{p}} \left( \frac{f(x)}{p} \right)$
* **Analizziamo la sommatoria**: 
	* **criterio di eulero**: dato che $p \equiv 3 \mod 4$, allora $-1$ non e' residuo quadratico.
	*  $f(x)$ **e' simmetrica**: $f(-x) = -f(x)$.
	* $\sum_{x\in \mathbb F_{x}} \left( \frac{f(x)}{p} \right) = \sum_{x \in \mathbb F_{x}} \frac{f(x)}{p}+\frac{f(-x)}{p}$ (tutto in simboli legendre)
	* $\left( \frac{f(-x)}{p} \right) = \left( -\frac{1}{p} \right) \left( \frac{f(x)}{p} \right) = -\left( \frac{f(x)}{p} \right)$
	* dove $\left( -\frac{1}{p} \right) = -1$ poiche non e' residuo quadratico in $\mod p$.
* **Si conclude che** $\sum_{x \in \mathbb F_{p}} \left( \frac{f(x)}{p} \right) = \sum \left( \frac{f(x)}{p} \right) - \left( \frac{f(x)}{p} \right) = 0$
* $\# E(\mathbb F_p) = 1+p$.

**R2**: dimostrare $\#E(\mathbb F_{p}) \sim \mathbb Z_{1} \oplus \mathbb Z_{p+1} \sim \mathbb Z_{p+1}$, ossia che $\# E(\mathbb F_{p})$ e' ciclico ed isomorfo a $\mathbb Z_{p+1}$
* Dalla teoria (specifica il teorema): $\# E(\mathbb F_{p})$ **e' sempre isomorfo al prodotto di due gruppi ciclici**.
* **Dunque**: $\# E(\mathbb F_{p}) \sim \mathbb Z_{n_{1}} \oplus \mathbb Z_{n_{2}}$ dove $n_{1} | n_{2}$.
* **Obiettivo**: far vedere che  $n_{1}=1$, dunque il gruppo si riduce alla componente $\mathbb Z_{n_{2}}$, che deve avere $n_{2}=p+1$ (lo abbiamo stabilito in **R1**).
* **Per Accoppiamento di Weil**: se $\# E(\mathbb F_{p})$ contiene un sottogruppo isomorfo a $\mathbb Z_{n_{1}} \oplus \mathbb Z_{n_{2}}$ allora $\mathbb F_{p}$ contiene le radici $n_{1}$ esime, ossia $n_{1}$ deve dividere l'ordine del gruppo $\mathbb F_{p}^*$.
* (1) **Piu semplicemente, Per Accoppiamento di Weil**: $n_{1}|p-1$
* (2) **Inoltre**: $n_{1} \cdot n_{2} = p+1$
* **Per (1) e (2)**, $n_{1}$ divide $(p-1)$ e $(p+1)$. 
* **Necessariamente $n_{1}$ ne divide la differenza**, ossia $n_{1}|2$. 
* **obiettivo**: escludere $n_{1}=2$.
	* **(3)** se $n_{1}=2$, allora $\# E(\mathbb F_{p})$ conterrebbe un sottogruppo isomorfo a $\mathbb Z_2 \oplus \mathbb Z_{2}$
	* Quindi devono esserci necessariamente 3 punti di ordine 2 
	* **I punti di ordine 2 si trovano sull'asse delle ascisse**: ossia con $y=0$.
	* **Sostituendo**: $0 = x^3 + x$ ed ho 3  casi. $x=0, x^2 = -1$.
	* **Residui quadratici**: $-1$ non e' residuo quadratico (gia visto in R1).
	* **Dunque**: Avendo un solo punto di ordine 2, il sottogruppo di 2-torsione è isomorfo a $\mathbb Z_{2}$ e _non_ a $\mathbb Z_{2} \oplus \mathbb Z_{2}$. (gemini, che vuol dire).
* allora $n_{1} = 1$ ed $n_{2} = p+1$.
* **(3)**: se $n_{1} = 2$, allora il gruppo ha la forma $\mathbb Z_{2} \oplus \mathbb Z_{n_{2}}$, con condizione $2|n_{2}$, ossia $n_{2}$ e' pari.
# Es 7
## A: controlla se $P \in E$
Lo script python risolve l'esercizio:
* per verificare $P\in E$ devo verificare $50342^2 \equiv (-2)^3-2\mod p$
* per verificare l'ordine basta vedere se $\min \{ n: [n]*P=0 \} = p+1$
```python
def calcola_ordine(P):
    n = 1
    Q = P
    # finche' Q non e' il punto all'infinito
    while Q != E(0):
        Q = Q+P
        n+=1
    return n

p = 101527
F = GF(p)  # Campo finito F_p

# Definisco la curva ellittica E: y^2 = x^3 + x
E = EllipticCurve(F, [1, 0])

P = E(-2, 50342)

if P in E:
    print("Il punto P appartiene alla curva E.")
    if calcola_ordine(P) == p+1:
        print("L'ordine di P e' p+1, ossia: ", p+1)
else:
    print("Il punto P non appartiene alla curva E.")
```

## C: calcolare logaritmo discreto di $Q=(56355,4891)$ in base $P$. Ossia $n$ tale che $n\cdot P = Q$
```python
import math

def bsgs(N,P,Q):
    m = math.isqrt(N)
    L = {}
    for j in range(m):
        L[j*P] = j
    for i in range(m):
        R = Q-((i*m)*P)
        if R in L:
            return (L[R] + m*i) % N
    return -1

p = 101527
F = GF(p)
E = EllipticCurve(F, [1,0])
P = E(-2, 50342)
Q = E(56355, 4891)
print(bsgs(p, P, Q))
```

![[Pasted image 20260414124336.png]]
# Es 3
![[Pasted image 20260414124355.png]]