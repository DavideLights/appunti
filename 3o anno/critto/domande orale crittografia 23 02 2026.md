## Povero Iannitti: steccandi
* **D**: definizione di campo finito
* **D**: **prodotto, inverso e somma** su $F_{p} \times F_{p}$
* $\mathbb F_{p}$ non e' necessariamente i numeri da $0$ a $p-1$.
* **D**: sia $p$ dispari in $\mathbb F_{p}$, $a=\frac{p+3}{2}$ ed $b=p-5$. Quanto vale *ab*?

## Orale 2: voto 26/30
* **D su esercizio**: come costruire $\mathbb F_{3^4}$ usando polinomi.
	* coefficienti in modulo 3 e polinomi in mod 4.
	* verificare $f(i)\neq_{0}$ per $i=0,1,2$ perche' mod 3.
	* sceglie polinomio $f(x)$ della forma $ax^4 + x +b$, dove tocca trovare $a,b$

> [!nota] svolgimento $F_{3^4}$
> Il **tizio** ha costruito il sistema per trovare $a,b$ tali che mi danno $\mathbb F_{3^4}$:
> * $b \neq 0$ ossia: ($f(0) \neq 0$)
> * $a+1+b \neq 0$ ossia: ($f(1) \neq 0$) 
> * $16a + 2 + b \neq 0$ ossia: $(f(2) \neq 0)$

**Nota**: se $p(x) = (x-r)q(x)$, se $x=r$ allora fa $0$!

* **D**: in $\mathbb Z_{12}$ valgono somma, prodotto e inverso? (ossia e' un campo?).
* **D**: **diffie-hellman** su curve ellittiche, come fuziona
* **D**: e' vero che per ogni curva ellittica, per ogni $Q,P$ esiste $k$ tale che $Q=kP$. 
	* **R**: se $E(\mathbb F_{p})$ e' ciclica esiste $k$. (????)
* **D**: come calcolo $k P$ in modo efficiente? (**exponentation**) + pseudocodice.
## Orale 3 (steccato)
* **D**: definizione di **sicurezza perfetta**.
	* **R**: c'ha fatto la dimostrazione.
* **D**: perche' **OTP** fa cagare e non si usa come cifrario a blocchi?  E definizione di sicurezza "che preferiamo" (ossia i **giochi d'attacco**).
	* **R**: OTP ha chiavi lunghe se ho un messaggio lungo (non l'ha detto bene)
	* **R**: vogliamo giochi d'attacco con bassa probabilità di successo. (non l'ha detto)
* **D (su esercizio)**: sia $E: y^2 = x^3+x$ e $\mathbb F_{5}$, $i=2$ e $\phi: (y,x)\to (iy,-x)$ una mappa sui punti della curva. Dimostrare che va da se in se stessa, la mappa e' razional, rispetta la struttura di gruppo ed e' invertibile.
	* **R**: un po' na merda
	* **D**: dimostrare che $\phi(P_{1}) + \phi(P_{2}) = \phi(P_{1} + P_{2})$.
		* **R**: ha risposto bene.
* **D (su esercizio)**: data $H$ hash function, trovare una collisione in $O(\sqrt{ n })$. (algoritmo simile a **Pollard Rho**).
	* **R**: per trovare la collisione prima devo trovare il ciclo in $H$, poi trovo, (non lo sa fare).

## Mirko:
* **D**: spiega **AES**.
* **R**: chill
	* **D**: come si converte lo stato di AES in un polinomio in $F_{2^7}$?
	* **R**:Esiste una mappa $B$ che manda ogni byte  in un polinomio di $\mathbb F_{128}$
	* **D**: provare a definire $B$.
	* **R**: ad ogni bit acceso corrisponde una potenza di $x$ nel polinomio. (???)
*  **D**: algoritmo di shanks.
* altre cose non segnate
