**definzione di RSV**:
$$
RSV_{d} = \log \prod_{t_{i}: x_{i} = y_{i}} \frac{p(x_{i}=1|R,v_{q})p(x_{i} =0| \bar{R},v_{q})}{p(x_{i}=1|\bar{R},v_{q})p(x_{i} =0| R,v_{q})}
$$
**come detto in [[lez. 9 approccio probabilistico]] approssimiamo**:
* $p(x_{i} =1| \bar{R},v_{q})$ con $p(x_{i}=1)$
* $p(x_{i} =0| \bar{R},v_{q})$ con $p(x_{i}=0)$

**dunque**:
$$
RSV_{d} = \sum_{t_{i}: x_{i}=y_{i}} \log \frac{p(x_{i}=1|R,v_{q})p(x_{i}=0)}{p(x_{i}=1)p(x_{i}=0|R,v_{q})}
$$

**frequenza dei termini**: nella formula di $RSV_{d}$, voglio abbandonare il modello BIM per passare allo studio della variabile $d_{t_{i}} = \# \text{ occ. di } t_{i} \text{ in } d$.
* in BIM: $x_{i} \in \{ 0,1 \}$
* **dunque non analizzo piu** $x_{i}\in \{ 0,1 \}$ ma $d_{t_{i}} \in \{ 0,1,2,3,\dots \}$

**eventi da studiare**:
* $d_{t_{i}} = n_{i}$
* $d_{t_{i}}=0$

**devo studiarli in 2 contesti**:
* contesto dei documenti rilevanti
* baseline distribution, approximated by the whole collection

**riformulo** $RSV_{d}$:
$$
RSV_{d} = \sum_{t_{i}: y_{i} =1} \log \frac{p(d_{t_{i}}=n_{i}|R,v_{q})p(d_{t_{i}}=0)}{p(d_{t_{i}}=n_{i})p(d_{t_{i}}=0|R,v_{q})}
$$

**random var**: $d_{t_{j}} = \text{numero di occorrenze di } t_{j} \text{ nel documento } d$ **a cosa serve**?
* modello probabilistico per il numero di occorrenze dei termini
* **termini rari** $\iff$ $d_{t_{j}}$ e' piccolo
* **termini centrali nel topic** $\iff$ $d_{t_{j}}$ ha valori enormi
* **domanda**: che distribuzione uso?

**distribuzione binomiale**: $p(d_{t_{j}}=k)  = \binom{l}{k}\tilde p^{k}{(1- \tilde p)}^{l-k}$
* $\tilde{p}$: probabilità con cui un termine $t_{j}$ potrebbe occorrere.
* gemini: perche'?
* **praticita**: non e' pratico, meglio poisson

**poisson**:
* **sequenza**: il documento $d$ e' una sequenza di $l$ posizioni
* **occorrenza**: in ogni posizione $t_{j}$ potrebbe occorrere con p. $\tilde{p}$
* dunque $d_{t_{j}} \sim \text{Binomial}(l, \tilde{p})$ con $l$ lunghezza documento e $\tilde{p}$ probabilita che una posizione contiene $t_{j}$

**poisson approssima binomiale**:
* **quando**? se $l$ e' grande e $\tilde{ p}$ e' piccolo
* **dunque**: $\text{Binomial}(l,\tilde{p}) \approx \text{Poisson}(\lambda)$ con $\lambda = l \tilde{p}$
* **che cose' lambda**? $\lambda = \text{numero di occorrenze che mi aspetto}$
* **cosa cambia rispetto alla binomiale**? Poisson e' semplice da calcolare.

$$
p(X=x)=\frac{e^{-\lambda}\lambda ^x}{x!}
$$
![[Pasted image 20260505130649.png]]
* $x$ e' il possibile numero di occorrenze di $t_{j}$ in $d$
* $\lambda$ e' il numero di occorrenze che **mi aspetto**.
* $X = d_{t_{j}}$

**Stimare** $\lambda$: $\lambda_{j} \approx \frac{cf_{t_{j}}}{N}$
* $cf_{t}$ e' la frequenza di $t$ nella collezione.
* $N$ e' il numero totale di documenti
* **andamento**: la distribuzione ha un picco vicino a $\lambda$

**come usiamo poisson**? vogliamo comparare le curve che creano i differenti termini in base al loro parametro $\lambda_{t_{j}}$

dobbiamo studiare due valori, che modellano qualche evento:
* **comportamento dei termini in documenti rilevanti** e' modellato da: $\rho_{j} = \text{ numero che mi aspetto di occorrenze di } t_{j} \text{ in documenti rilevanti per } q$. 
* **comportamento in media nella collezione intera**: $\gamma_{j} = \text{ numero che mi aspetto di  occorrenze di } t_j \text{ nella collezione intera }$

**dunque**:
* $p(d_{t_{j}} = n_{j} | R,v_{q}) = \frac{e^{-p_{j}} \rho_{j}^{n_{j}}}{n_{j}!}$ ossia poisson di parametro solo $p_{j}$
* $p(d_{t_{j}} = 0 | R,v_{q}) = e^{-p_{j}}$
* $p(d_{t_{j}} = n_{j}) = \frac{e^{-\lambda_{j}} \lambda_{j}^{n_{j}}}{n_{j}!}$
* $p(d_{t} = 0) = e^{-\lambda_{j}}$

**Ora sviluppiamo** $RSV$:
![[Pasted image 20260428161325.png]]
**semplicemente**:
$$RSV_d = \sum_{t_i:y_i=1} \log \left( \frac{\rho_i}{\gamma_i} \right)^{n_i} = \sum_{t_i:y_i=1} n_i \log \frac{\rho_i}{\gamma_i}$$

**Interpretazione**: lo score di ogni termine contribuisce come $\log \frac{\rho_{j}}{\gamma_{j}}$ ossia logaritmo del rapporto tra occorrenze attese e occorrenze nella collezione.
* **gestione delle stopwords**: in questo modello ogni occorrenza cresce in modo lineare. *Ma le parole che compaiono **troppo spesso in un documento e sono comuni in tutto il dataset** non contribuiscono più di tanto al punteggio $RSV_{d}$
* **elitness**: *se il termine definisce il **topic** del documento allora compare molto, ed in **modo anomalo** rispetto agli altri documenti*. Dunque ci sono dei termini che sono **elite** per un certo documento $d$ ma non lo sono per un'altro documento.

**problema**: calcolare $\rho_{j}$. (mentre $\gamma_{j}$ puo' essere stimato).
* **con collezione di documenti giudicati**: allora posso stimare $\rho_{j}$
* **a priori come faccio**?
![[Pasted image 20260428161515.png]]

**poisson**:
![[Pasted image 20260428161650.png]]

**eliteness**: e' una hidden binary variable (ossia e' elite oppure non e' elite).
* $d$ e' elite per un termine se: il concetto denotato da quel termine e' argomento centrale del documento
* **proprieta**: il numero di occorrenze dipende dall'eliteness
* **rilevanza**: l'eliteness e' fortemente correlata alla rilevanza, ma non sono la stessa cosa.

**2-poisson**: vogliamo calcolare $p(d_{t_{i}} = n_{i} | R,v_{q})$, ossia probabilita che il termine $t_{i}$ compaia $n_{i}$ volte nel documento sapendo che il documento e' rilevante per la query.
* **si usano 2 poisson**: una per il caso elite, e l'altra per il caso non elite

**ossia**:
$$
p(d_{t_i} = n_i | R, v_q) = p(d_{t_i} = n_i | E_i) p(E_i | R, v_q) + p(d_{t_i} = n_i | \bar{E}_i) p(\bar{E}_i | R, v_q)
$$
* $= p_{i} \text{Poisson}(n_{i}| \mu_{i}) + (1-p_{i})\text{Poisson}(n_{i}|\bar \mu_{i})$
* $= p_i \frac{e^{-\mu_i} \mu_{i}^{n_i}}{n_i!} + (1 - p_i) \frac{e^{-\bar{\mu}_i} \bar{\mu}_{i}^{n_i}}{n_i!}$

dove:
* $\mu_{i}$ media delle occorrenze nei **documenti Elite (alta**)
* $\bar \mu$ media delle occorrenze nei **documenti non-Elite** (bassa)

![[Pasted image 20260428162309.png]]
![[Pasted image 20260428162547.png]]
**vogliamo che il contributo sia non binario rispetto a BIM**: 

## Calcolo del RSV
**obiettivo**: riscriviamo le probabilità necessarie per calcolare l’RSV usando la mistura elite/non-elite ossia lo **score finale assegnato a un documento rispetto a una query**.

Per ogni termine $t_i$, definiamo:  
- $C(n_i)=Poisson(n_i|\mu_i)$: probabilità di osservare $n_i$ occorrenze se il documento è elite;  
- $\bar C(n_i)=Poisson(n_i|\bar\mu_i)$: probabilità di osservare $n_i$ occorrenze se il documento non è elite;  
- $p_i$: probabilità che un documento rilevante sia elite per $t_i$;  
- $\bar p$: probabilità che un documento qualsiasi della collezione sia elite per $t_i$.  

**Nei documenti rilevanti**:  
$$  
p(d_{t_i}=n_i|R,v_q)=C(n_i)p_i+\bar C(n_i)(1-p_i)  
$$
**Nella collezione generale**:  
$$  
p(d_{t_i}=n_i)=C(n_i)\bar p+\bar C(n_i)(1-\bar p)  
$$
**Lo stesso vale per il caso $n_i=0$ quindi con**:
$$p(d_{t_i} = 0 | R, v_q) = C(0)p_i + \bar{C}(0)(1 - p_i)$$
$$p(d_{t_i} = 0) = C(0)\bar{p} + \bar{C}(0)(1 - \bar{p})$$

**a che serve sta cosa**? Questa formalizzazione serve a sostituire le probabilità generiche dell’RSV con probabilità calcolate tramite il modello 2-Poisson.

**costruiamo** $RSV_{d}$: Sostituendo queste scomposizioni nella formula generale dell'RSV, otteniamo l'espressione completa per il punteggio di un documento:
$$RSV_d = \sum_{t_i:y_i=1} \log \frac{(C(n_i)p_i + \bar{C}(n_i)(1 - p_i))(C(0)\bar{p} + \bar{C}(0)(1 - \bar{p}))}{(C(0)p_i + \bar{C}(0)(1 - p_i))(C(n_i)\bar{p} + \bar{C}(n_i)(1 - \bar{p}))}$$

Questa formula, sebbene teoricamente corretta, è **inutilizzabile nella pratica** perché per ogni singolo termine $t_i$ dovremmo stimare ben 4 parametri ignoti (che a priori non conosciamo):
1.  **$\mu_i$**: media delle occorrenze nei documenti elite.
2.  **$\bar{\mu}_i$**: media delle occorrenze nei documenti non-elite.
3.  **$p_i$**: probabilità di eliteness nei documenti rilevanti.
4.  **$\bar{p}$**: probabilità di eliteness nella collezione.

Si cerca una **funzione parametrica semplice** che approssimi il comportamento della curva 2-Poisson.

**caratteristiche della funzione da cercare**:
* Essere pari a $0$ se $n_i=0$.
* Crescere in modo monotono all'aumentare di $n_i$.
	$$\log \frac{p_i(1 - \bar{p})}{(1 - p_i)\bar{p}}$$
* **Saturare**: tendere asintoticamente a un valore massimo (il valore del caso binario).
	- la saturazione è importante perché fa sì che, se un termine compare troppe volte, dopo un po' inizia a non impattare più sulla rilevanza generale

**funzione scelta**:
$$\frac{(k+1)n_i}{k+n_i} \cdot \log(\frac {p_{i}(1-\bar{p})} {(1-p_{i})\bar{p}})$$
- $k$ è una costante (parametro) che decidiamo noi. **VA OTTIMIZZATO TRAMITE BENCHMARK**.

**implementare la funzione**: dobbiamo scegliere dei parametri
 * **feedback rilevanza**: assumo $p_{i}=0.5$
 * **approssimazione logaritmo**: uso IDF come fatto nel BIM

$$RSV_d = \sum_{t_i:y_i=1} \frac{(k+1)n_i}{k+n_i} \log \frac{N}{df_{t_i}}$$

> **Importanza**: Questo è il "primo passo verso il modello BM25". Il fattore $\frac{(k+1)n_i}{k+n_i}$ è ciò che permette di pesare la **Term Frequency** in modo non lineare, introducendo il concetto di **saturazione**.

**staturazione**: il contributo della term frequency **cresce all’inizio**, ma poi **aumenta sempre meno** fino a tendere a un valore massimo.
#### Modello Okapi BM25
**cos'e'?** rappresenta l'evoluzione moderna del BIM. *È un modello probabilistico **non binario*** che risolve le limitazioni dei modelli precedenti. integra:
* **frequenza dei termini** (TF)
* **normalizzazione della lunghezza**

**a che serve**? BM25 è progettato per il **full-text search** moderno. 
* **Sensibilità alla TF**: non si limita a rilevare la presenza di un termine, ma ne pesa l'occorrenza.
* **Sensibilità alla lunghezza**: adatta il peso dei termini in base a quanto è lungo il documento.
* **Robustezza**: è considerato uno dei modelli di ranking più efficaci e utilizzati nello stato dell'arte

**BM25 semplificato**: Il nucleo fondamentale del BM25 è il peso **IDF**. Nella sua forma più semplice, il punteggio di un documento è la somma dei pesi IDF dei termini della query presenti nel documento.
$$RSV_d = \sum_{t \in q} \log \frac{N}{df_t}$$
BM25 con frequenza del termine $tf_{td}$: viene introdotto attraverso una funzione di saturazione. La formula base diventa:
$$RSV_d = \sum_{t \in q} \frac{(k_1 + 1)tf_{td}}{k_1 + tf_{td}} \log \frac{N}{df_t}$$

* **$k_1$**: è un parametro di *tuning* che controlla la scala di saturazione della valenza della TF.
	- solitamente impostato tra **1.2** e **2.0**.
	- Un valore di $k_1$ **basso** porta a una saturazione rapida (già con poche occorrenze il termine raggiunge quasi il suo peso massimo).
    * Un valore di $k_1$ **alto** rende la crescita del punteggio più lenta e "più vicina" a una crescita lineare (tipica del tf-idf classico).
* **Fattore $(k_1 + 1)$**: serve a normalizzare il punteggio in modo che, quando $tf_{td} = 1$, il contributo della componente TF sia pari a 1 (rendendo il punteggio finale pari all'IDF puro).
* **Bounded scores**: a differenza del modello vettoriale (dove la TF può crescere quasi linearmente), qui il punteggio è **limitato superiormente** da un asintoto.
- quanto k fa variare la valenza della TF per un certo termine
> [!note ] aggiungi immagine!!!
###### Ulteriore correzione
**lunghezza dei documenti**: sono un bias importante. documenti lunghi tendono ad avere tf elevato rispetto a documenti corti.

Un documento può essere più lungo per due motivi principali:
1. **Verbosità (Verbosity)**: L'autore utilizza **molte parole per esprimere lo stesso concetto**. In questo caso, **le alte frequenze dei termini sono "artificiali"** e vanno **penalizzate**.
2. **Ampiezza del contenuto (Larger Scope)**: Il documento tratta molti argomenti diversi. In questo caso, le frequenze osservate possono essere corrette.
Poiché una collezione reale contiene entrambi i tipi di documenti, è necessaria una **normalizzazione parziale**.

Definiamo innanzitutto i parametri di calcolo:
* **$L_d$**: lunghezza del documento $d$, calcolata come somma delle frequenze di tutti i termini in esso contenuti $$L_{d} = \sum_{t} tf_{td}$$
* **$L_{ave}$**: Lunghezza media dei documenti nell'intera collezione $D$ $$L_{ave} = \frac 1 {|D|} \sum\limits_{d \in D}L_{d}$$
* **Fattore di normalizzazione $B$**: $$B = (1 - b) + b \frac{L_d}{L_{ave}} \quad \text{con } 0 \leq b \leq 1$$
	**parametro** **$b$**: regola l'intensità della normalizzazione:
	*   **$b = 1$**: Normalizzazione totale (penalizza pesantemente la lunghezza).
	*   **$b = 0$**: Nessuna normalizzazione (modello sordo alla lunghezza).

Il fattore $B$ viene inserito al denominatore della componente TF.

**Valore Standard**: Empiricamente, si è dimostrato che un valore di **$b \approx 0.75$** offre il miglior compromesso tra verbosità e ampiezza di contenuto.

###### Okapi BM25+correzioni varie
$$RSV_d = \sum_{t \in q} \log \left( \frac{N}{df_t} \right) \cdot \frac{(k_1 + 1)tf_{td}}{k_1 \left( (1 - b) + b \frac{L_d}{L_{ave}} \right) + tf_{td}}$$

#### Riepilogo dei Parametri Operativi
1.  **$tf_{td}$**: Frequenza del termine della query nel documento.
2.  **$L_d$ e $L_{ave}$**: Lunghezza del documento corrente e lunghezza media della collezione.
3.  **$k_1$ (TF Saturation)**: Controlla la saturazione della frequenza. 
    *   Se $k_1 = 0$, il modello diventa binario (BIM).
    *   Valori tipici: **1.2 - 2.0**.
4.  **$b$ (Length Normalization)**: Controlla quanto penalizzare i documenti lunghi. 
    *   Valori tipici: **0.75**.
- Per qualcosa di **semplice e basico**: usare Modello Vettoriale con pesatura tf-idf.    
    - Per un **ranking robusto e performante**: usare BM25 (o modelli del linguaggio) con parametri ottimizzati.
    
- **BM25 nella pratica reale:**
    - **Elasticsearch:** utilizza BM25 come modello di default per la similarità.
    - **Apache Solr:** utilizza BM25 come default dalla versione 8.x in poi.