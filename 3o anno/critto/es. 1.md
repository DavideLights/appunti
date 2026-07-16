
## attacco a permutazione
* guardo le lettere piu frequenti, i digrammi, i trigrammi piu frequenti e assegno la permutazione in base a cosa mi conviene.
## attacco a vigenere
**Test di kasiski**: nel testo compare spesso il trigramma `HJV`.
* Le distanze tra i trigrammi sono: $18,138,54,12$
* $\text{MCD}(18,138,54,12)=6$

**Sottostringhe**: dunque, ci sono 6 sotto-stringhe $w_{i} \text{ per } 0 \leq i < 6$. Con $y_{i}$, $\text{i-esimo carattere del testo cifrato}$ 
* $w_{i} = y_{i}y_{i+m}y_{i+2m}\dots$ e' la sottostringa $i\text{-esima}$

**Analisi indice incidenza**:
* allora per ogni $w_{i}$ voglio trovare lo shifting $k_{i}$
* Questo $k_{i}$ deve essere quello che si avvicina di piu a $0.065$
* Equivalentemente, Per ogni $w_{i}$ voglio trovare $k$ che massimizza $s_{k} = \sum f_{{i}_{k}} p_{k}$, dato che $\sum p_{i}^2$ e' l'indice di incidenza nella lingua inglese.
	* $p_{k}$: indice incidenza della lettera $k$ nella lingua inglese
	* $f_{{i}_{k}}$: indice incidenza della lettera $k$ nella sottostringa $w_{i}$

**Risultato**: $k=\text{CRYPTO}$
## es probabilita
**input**: Sia $\mathcal P = \{  a,b\}, \mathcal C=\{ 1,2,3,4,5 \}$ ed $\mathcal K = \{ k_{1},k_{2},k_{3},k_{4},k_{5} \}$ ed $\alpha, \beta \text{ t.c }\alpha + \beta =1$
**obiettivo**: far vedere che $P[Y=y]=P[Y=y|X=x]\;\;\; \forall y,x$ 

**Per** $Y=1$:
* $P[Y=1]=P(K_{1})P(X=a) + P(K_{3})P(X=b) = \frac{\alpha}{3} P(X=a) + \frac{\alpha}{3}P(X=b) = \frac{\alpha}{3}$
* $P[Y=1|X=a] = \sum_{k_{i}: e_{K_{i}}(a)=1}P(K=K_{i})P(K=K_{1}) = \frac{\alpha}{3}$
* $P[Y=1|X=b] = \sum_{k_{i}: e_{K_{i}}(b)=1}P(K=K_{i})P(K=K_{3}) = \frac{\alpha}{3}$ 

**Per $Y=2,3$ i calcoli sono simili.z

![[Pasted image 20260412110347.png]]

## es sicurezza semantica
* $\mathcal K = \{ x\in \{ 0,1 \}^L: \text{ x ha parita 0} \}$
* $p_{m}:= \text{ parita di } m$.

**descrizione attacco**:
* **challenger** sceglie $b\in \{ 0,1 \}$, di conseguenza sceglier $m \in \mathcal C$ con parità $p_{m}=b$
* **challenger** invia all'attaccante $y=E(k,m)$ dove $p_{k}=0$ ed $E$ e' OTP.
* **attaccante** riceve $y$  e calcola $p_y$. scrive in output $p_{y}=\hat{b}$ 

**funziona perche'**: fare $k \oplus m$  fissata una chiave con parita 0 non altera la parita del messaggio $m$.