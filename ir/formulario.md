# compressione e dizionario
**heaps law**: $M = kT^b$
* $M = \text{termini dizionario}$
* $T = \text{token}$
* $30 \leq k \leq 500, b \sim 0.5$
* **a che serve?** stimare il numero di parole del dizionario a partire dal numero di token totali osservati.

**zipf's law**: $cf_{i}= \frac{1}{i^{th}}$
* $cf_{i} = \text{collection frequency}$
* **forma completa**: $cf_{i} = ci^k$, dove abbiamo scelto $k=-1$ ed $c=1$.
* **a che serve**? permette di stimare la frequenza con cui compaiono le parole in un testo dato che è inversamente proporzionale al loro **rango**

**unary code**:
* **ottimale**: se $P(n) = 2^{-n}$ 

**spazio gamma code**: $2 \log G + 1$ bit.
* **ottimale**: se $P(n) \approx \frac{1}{2n^2}$

# Noisy channel model
## Non-words
**nosy channel model**: 
$$
\hat{w} = \text{argmax}_{w\in V}P(x|w)P(w)
$$

**unigram model**:
$$P(w) := \text{quanto e' comune la parola } w = \frac{C(w)}{T}$$
* $C(w) = \text{numero occorrenze}$
* $T$ numero totale di termini nel corpus.

**channel model probability**:
$$
P(x|w) = \text{edit distance in base alla confusion matrix}
$$

**smoothing la place** per channel model probability:
$$P(x|w)=\frac{\text{sub}[x,w]+1}{\text{count}[w]+A}$$
* **a che serve**? 
* **perche serve lo smoothing**? se $P(x|w)$ valesse 0 ma $P(w)$ ha valore alto allora il prodotto ha valore 0

## Real-word errors
**Hidden Markov Model**:
$$
P(X|W)=  \prod_{i=1} P(x_{i}|w_{i})
$$
* **a che serve?** guardo per ogni coppia di parole in $X$ e $W$ la probabilità di voler scrivere $x_{i}$ avendo osservato $w_{i}$.

**Bigram Model**:
$$
P(W)= P(w_{1}, \dots, w_{n})=P(w_{1})P(w_{2}|w_{1})\dots P(w_{n}|w_{n-1})
$$
* **a che serve**? vedo quanto e' corente una parola con la precedente 

**smoothing per Bigram Model**:
$$P(w_{i}|w_{i-1})=(1-\lambda)P_{\text{bigram}}(w_{i}|w_{i-1}) + \lambda P_{\text{unigram}}(w_{i})$$
* $P_{\text{bigram}}(w_{k}|w_{k-1})=\frac{C(w_{k-1},w_{k})}{C(w_{k-1})}$
* $P_{\text{unigram}}(w_{i})= \frac{C(w_{i})}{C(W)}$
* **a che serve**? Bilanciare le due metriche mi serve per non penalizzare troppo combinazioni di parole troppo rare.
 
**log sul bigram model**:
$$\log P (w_{1} \dots w_{n}) = \log P(w_{1})  +\log P(w_{2}|w_{1}) + \dots$$
* **a che serve**? la formula originale potrebbe avere troppi prodotti e far esplodere il valore del risultato.

**Markov Model**:
* **transizioni**: $P(w_{i}|w_{i-1})$, ossia le successioni possibili di parole.
* **emissioni**: $P(x_{i} |w_{i})$, le parole possibili da scegliere.

**peso** $\beta$: $P(W)^\beta$ e' il peso da applicare a $P(W) = \text{probabilita che la parola osservata sia corretta}$ nella formula 
$$
\hat{w} = \text{argmax}_{w\in V}P(x|w)P(w)^{\beta}
$$
* **a che serve**? se $w$ e' corretta ma molto rara? allora introduco $\beta$ per dare una spinta a queste parole. 

# ranked retrieval

**term frequency**: $$\text{tf}_{t,d} = \text{quante volte } t \text{ occorre in } d$$
**peso del termine $t$ per il documento $d$:**
$$w_{t,d} = \begin{cases} 1 + \log_{10}(tf_{t,d}) & \text{se } tf_{t,d} > 0 \\ 0 & \text{altrimenti} \end{cases}$$
* **perche'**? voglio smorzare la crescita lineare di $\text{tf}_{t,d}$. il logaritmo e' piu rappresentativo del fenomeno.

**score per la coppia query documento**:
$$\text{tf-matching-score}(q,d)=\sum_{t\in q\cap d}w_{t,d}$$

**misura della quantità di informazione (OSSIA DELLA RARITA) di un termine**: $$\text{idf}_{t} = \log_{10} \frac{N}{\text{df}_{t}}$$
* **perche**? descrive quanto e' informato un termine.
* $\text{df}_{t}$ **basso**  $\to \text{idf}_{t}$ **alto**
* $\text{df}_{t}$ **alto**  $\to \text{idf}_{t}$ **basso**

**peso** $\text{tf-idf}$: 
$$w_{t,d} = (1 + \log \text{tf}_{t,d}) \log \frac{N}{\text{df}_{t}}$$
**cosine similarity**:
$$
\cos(\vec{q}, \vec{d}) = \text{sim}(\vec{q}, \vec{d}) = \frac{\vec{q}}{|\vec{q}|}\frac{\vec{d}}{|\vec{d}|} = \frac{\sum_{i=1}^{|V|} q_{i} d_{i}}{\sqrt{ \sum_{i=1}^{|V|}q_{i}^2 } \sqrt{ \sum_{i=1}^{|V|}d_{i}^2 }}
$$
* $L_{2}$: $||x||_{2} = \sqrt{ \sum_{i}x_{i}^2 }$, dunque i vettori vengono proiettati su una sfera di raggio 1.


## valutazione dei sistemi
**precision**:
$$
\frac{tp}{tp+fp}
$$
> *Su tutti i documenti che ho etichettato come positivi, quanti effettivamente lo erano, ossia, quanto sono stato preciso?*

**recall**:
$$
\frac{tp}{tp+fn}
$$
> *Quanti documenti ho ritornato all'utente sul totale dei positivi? Ossia, ho preso tutti i documenti che dovevo prendere?* 


**media armonica**:
$$
F_{1}=\frac{2PR}{P+R}
$$

**accuracy**:
$$
\frac{TP + TN}{TP + FP + FN + TN}
$$
* **[ATTENZIONE] su una collezione di 1.000.000 di documenti non serve ad un cazzo**!
	* ritorno correttamente 10 positivi, ma ho milioni di true negative.
	* allora l'accuracy e' altissima

**error**:
$$
\text{error} = 1-\text{accuracy}
$$

## metriche

$\text{Precision@}K$: la precision sui primi $K$ documenti ritornati
* $\text{Recall@}K$: similmente

**MAP** (Mean Average Precision):
* **average precision**: per ogni documento rilevante, calcola e fai media degli $\text{Precision@}K$
* **MAP** e' **AP** **su più** **query**.
* **perche**? si usa in sistemi che massimizzano la recall

**Discounted Cumulative Gain**:
$$DCG_{p} = r_{1} + \sum_{i=2}^p \frac{r_{i}}{\log i}$$
* $r_{i} \in [0,3]$
* **perche'?** penalizza documenti con $r_{i}$ alto ma in posizioni troppo basse.

## lexical semantics
**PMI**: 
$$
\text{PMI}(x,y) = \log \frac{P(x,y)}{P(x)P(y)}
$$


???


## probabilita a manetta
$P(R|d,q)$ e':
> probabilità che il documento osservato sia rilevante per $q$ rispetto al giudizio di un qualsiasi utente.


**Che cos'è' $P(R|d,q)$?**
$$p(R|d,q) = \sum_{u\in U} p(R|d,q,u)p(u)$$
* $p(u)$ **non cambia l'ordinamento**, se lo si assume costante 

**Proviamo invece ad usare bayes su** $P(R|d,q)$
$$
p(R|d,q) = \frac{p(d|R,q)p(R|q)}{p(d|q)} = \frac{p(d|R,q)p(R|q)}{p(d)}
$$
* $p(d|R,q) = \text{p. che } d \text{ venga scelto u.a.r dai documenti rilevanti per } q$.
* $p(R|q) = \text{p. che un documento scelto dalla collezione sia rilevante per } q$, ed e' **costante per tutti i documenti che vengono confrontati con la query** $q$.
* $p(d|q) = p(d) = \text{la probabilita che } d \text{ sia pescato dalla collezione}$, si assumono $d,q$  indipendenti $\forall d,q$.

## rischio
**Rischio**: vogliamo trovare una formula che calcoli un rischio, da minimizzare per risolvere il problema.
$$R(D(q)) = \sum_{d\in D} C'(d,q)p(\bar{R}|d,q) + \sum_{d \not \in D} C(d,q) p(R|d,q)$$
* $C(d,q) = \text{ costo quando }d \text{ e' rilevante rispetto a } q \text{ e non e' stato recuperato}$
* $C'(d,q) = \text{ costo quando }d \text{ non e' rilevante rispetto a } q \text{ ed e' stato recuperato}$
* $D = D(q)$ insieme di documenti ritornati dal sistema

$$
R(D(q)) =|D(q)| + \sum_{d \notin D(q)} p(R|d,q) - \sum_{d \in D(q)} p(R|d,q)
$$
**equivalente per il ranking ad**:
$$
R(D(q)) =_{\text{rank}} \sum_{d \in D(q)} p(R|d,q) - \sum_{d \notin D(q)} p(R|d,q)
$$
* **a che serve**? ho trovato una metrica per l'ordinamento, che pero' e' inutilizzabile, in pratica. Bisogna fare molte assunzioni.

**PRP e 0/1 Loss**:
* assumendo 0/1 loss, allora per **PRP**, il sistema e' ottimo e minimizza gli errori.

> [!note] PRP (Probability Ranking Principle)
>  *If the retrieved documents (w.r.t a query) are ranked decreasingly on their probability of relevance, then the effectiveness of the system will be the best that is obtainable.*

## BIM
**assunzione features indipendenti**:
$$p(f_{1},\dots,f_{n}|R,q) = \prod_{i} p(f_{i}|R,q)$$

**Passiamo da $p(R|d,q)$ ad...**
$$p(R|v_{d},v_{q}) = \frac{p(v_{d}|R,v_{q})p(R|v_{q})}{p(v_{d}|v_{q})} =_{rank} p(v_{d}|R,v_{q})$$


**[PROCEDIMENTI ALGEBRICI STRANI DA NON SAPERE NECESSARIAMENTE] Odds**: e' una misura compatta della rilevanza di $v_{d}$ rispetto a $v_{q}$.
$$
O(R|v_{d}, v_{q}) = \frac{p (R|v_{d}, v_{q})}{p(\bar{R}|v_{d},v_{q})} =_{\text{rank}} \frac{p(v_{d}|R,v_{q})}{p(v_{d}| \bar{R}, v_{q})}
$$
$$
\prod_{i=1}^M \frac{p(x_{i}|R,v_{q})}{p(x_{i}|\bar{R}, v_{q})} =\prod_{t_{i}: x_{i}=y_{i}=1} \frac{p(x_{i}=1|R,v_{q})}{p(x_{i}=1|\bar{R}, v_{q})} \cdot \prod_{t_{i}: x_{i}=0, y_{i}=1} \frac{p(x_{i}=0|R,v_{q})}{p(x_{i}=0|\bar{R}, v_{q})}  
$$
**Importante**:

| LOL         | $R$       | $\bar{R}$ |
| ----------- | --------- | --------- |
| $x_{t} = 1$ | $p_{t}$   | $u_{t}$   |
| $x_{t} = 0$ | $1-p_{t}$ | $1-u_{t}$ |

**[PROCEDIMENTI ALGEBRICI STRANI DA NON SAPERE NECESSARIAMENTE]  varie manipolazioni...**
$$
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=y_{i}} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})}
$$
**Retrieval Status Value**:
$$
RSV_{d} = \sum_{t_{i}:x_{i}=y_{i}=1} \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} = \sum_{t_{i}:x_{i}=y_{i}=1} c_{i}
$$

$$
c_{i} = \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} = \log \frac{p_{i}}{1-p_{i}} - \log \frac{u_{i}}{1-u_{i}}
$$
* **a che serve?** $RSV$ e' il logaritmo di ODDS che abbiamo sviluppato fino ad ora, ed non e' altro che la somma dei pesi per ogni termine

**$p_{i}$ e $u_{i}$**:
$$p_i=\frac{r_i}{R} = 0.5 \text{ (assunzione)}$$

$$u_i=\frac{df_i-r_i}{N-R} = \frac{df_{i}}{N} \text{ (assunzione)}$$
- ($N$): numero totale di documenti nella collezione;
- ($R$): numero di documenti rilevanti;
- ($r_i$): numero di documenti rilevanti che contengono il termine ($t_i$);
- ($df_i$): numero totale di documenti che contengono ($t_i$). 
- **assunzione**: *i documenti rilevanti sono pochi rispetto ai non rilevanti!*

## poisson

**distribuzione binomiale**: $$p(d_{t_{j}}=k)  = \binom{l}{k}\tilde p^{k}{(1- \tilde p)}^{l-k}$$
* **a che serve**? binomiale di parametro $l$ lunghezza del documento ed $p$ probabilita che una posizione contiene il termine, descrive

**poisson**: $p(X=x)=\frac{e^{-\lambda}\lambda ^x}{x!}$ approssima binomiale con $\lambda= kl$ con $k$ piccolo ed $l$ grande.

$$
\lambda_{j} \approx \frac{cf_{t_{j}}}{N}
$$
* **cosa vuol dire**? il parametro della poisson descrive il numero di occorrenze che mi aspetto.
* **ATTENZIONE**: non va bene, viola PRP

$$d_{t_{j}} = \text{Binom} \approx \text{Poisson}$$
* **cosa vuol dire**? Poisson/Binomaile mi dice qual'e' la probabilita di osservare $x$ occorrenze nel documento. 

**Retrieval Status Value**:
$$
(\star) RSV_{d} = \sum_{t_{j}: y_{j}=1}\frac{ p(d_{t_{j}}=n_{j}|R,v_{q})p(d_{t_{j}}=0)}{p(d_{t_{j}} = n_{j})p(d_{t_{j}}=0|R,v_{q})} 
$$
$$RSV_d = \sum_{t_i:y_i=1} \log \left( \frac{\rho_i}{\gamma_i} \right)^{n_i} = \sum_{t_i:y_i=1} n_i \log \frac{\rho_i}{\gamma_i}$$

* $\rho_{j} = \text{ numero che mi aspetto di occorrenze di } t_{j} \text{ in documenti rilevanti per } q$. 
	* **ossia**: occorrenze medie per $t_{i}$ nei documenti rilevanti
* $\gamma_{j} = \text{ numero che mi aspetto di  occorrenze di } t_j \text{ nella collezione intera }$
	* **ossia**: numero di occrenze medie nella collezione generale.
* $p(d_{t_{j}} = n_{j} | R,v_{q}) = \frac{e^{-p_{j}} \rho_{j}^{n_{j}}}{n_{j}!}$ ossia poisson di parametro solo $p_{j}$ (RHO)
* $p(d_{t_{j}} = 0 | R,v_{q}) = e^{-p_{j}}$ (RHO)
* $p(d_{t_{j}} = n_{j}) = \frac{e^{-\gamma{j}} \gamma{j}^{n_{j}}}{n_{j}!}$
* $p(d_{t} = 0) = e^{-\gamma_{j}}$


## 2-poisson
**2-poisson**
$$
p(d_{t_i} = n_i | R, v_q) = p(d_{t_i} = n_i | E_i) p(E_i | R, v_q) + p(d_{t_i} = n_i | \bar{E}_i) p(\bar{E}_i | R, v_q)
$$
$$= p_{i} \text{Poisson}(n_{i}| \mu_{i}) + (1-p_{i})\text{Poisson}(n_{i}|\bar \mu_{i})$$
$$= p_i \frac{e^{-\mu_i} \mu_{i}^{n_i}}{n_i!} + (1 - p_i) \frac{e^{-\bar{\mu}_i} \bar{\mu}_{i}^{n_i}}{n_i!}$$
* $p_i$: probabilità che un documento rilevante sia elite per $t_i$
* $\mu_{i}$ media delle occorrenze nei **documenti Elite (alta**)
* $\bar \mu$ media delle occorrenze nei **documenti non-Elite** (**bassa**)
* **DIFFICILE DA CALCOLARE**!

**cercare una funzione simile a poisson in funzione di $p_{i}$ e $p$:**
$$\frac{(k+1)n_i}{k+n_i} \cdot \log(\frac {p_{i}(1-\bar{p})} {(1-p_{i})\bar{p}})$$
-  $p_i$: probabilità che un documento rilevante sia elite per $t_i$
* $\bar{ p}$: probabilità che un documento qualsiasi della collezione sia elite per $t_i$
- $k$ è una costante (parametro) che decidiamo noi. **VA OTTIMIZZATO TRAMITE BENCHMARK**.

**apporssimazione ed assunzione**
$$\log \frac{p_i(1 - \bar{p})}{(1 - p_i)\bar{p}} \approx \log \frac{N}{df_{t_{i}}}$$
* **assumendo** $p_{i} =0.5$

**Retrieval Status Value**:
$$RSV_d = \sum_{t_i:y_i=1} \frac{(k+1)n_i}{k+n_i} \log \frac{N}{df_{t_i}}$$

**BM25 Semplificato:**
$$RSV_d = \sum_{t \in q} \log \frac{N}{df_t}$$

**BM25**:
$$RSV_d = \sum_{t \in q} \frac{(k_1 + 1)tf_{td}}{k_1 + tf_{td}} \log \frac{N}{df_t}$$
* $k_{1} \in [1.2, 2.0]$, tuning.
	* **basso**: saturazione rapida
	* **alto**: crescita piu bassa
* $\frac{N}{df_{t}}$ **fattore IDF**
	* **basso**: il termine e' comune
	* alto: il termine e' raro.
* **apporx. 2poisson**: tende a $(k_{1}+1)$


**Okapi BM25**:
$$RSV_d = \sum_{t \in q} \log \left( \frac{N}{df_t} \right) \cdot \frac{(k_1 + 1)tf_{td}}{k_1 \left( (1 - b) + b \frac{L_d}{L_{ave}} \right) + tf_{td}}$$
1.  **$tf_{td}$**: frequenza del termine della query nel documento.
2.  **$L_d$ e $L_{ave}$**: lunghezza di $d$ e lunghezza media nella collezione
	1. $\frac{L_{d}}{L_{avg}}$ e' la lunghezza di $d$ **normalizzata**
3.  **$k_1$ (TF Saturation)**: controlla la saturazione della frequenza. 
    *   Se $k_1 = 0$, il modello diventa binario (BIM).
    *   Valori tipici: **1.2 - 2.0**.
4.  **$b \approx 0.75$ (Length Normalization)**: controlla quanto penalizzare i documenti lunghi. 

# modelli linguistici

**modello unigram**:
$$
\hat p_{i} = \hat{p}(t_{i}|M_{d}) = \frac{tf_{t,d}}{|d|}
$$

