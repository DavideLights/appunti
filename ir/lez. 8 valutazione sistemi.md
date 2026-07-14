**obiettivo**: voglio restituire all'utente qualcosa che lo soddisfi. 
**soggettivita**: questa metrica e' soggettiva, devo introdurre un metodo standard e replicabile.

**benchmark**: un'ambiente di valutazione controllato. Nel nostro caso e' composto da
* **collezione di documenti**: definisce il contesto in cui lavoriamo.
* **insieme di query**: realistiche.
* **insieme di giudizi di rilevanza**: per ogni documento stabilisco se e' rilevante oppure no.
* **valutazione e' riproducibile**: perche' abbiamo definito query, documenti e cosa ci aspettiamo dal sistema.

**proxy**: e' una misura indiretta che approssima qualcosa. non potendo misurare la felicita dell'utente usiamo come proxy la **rilevanza dei documenti**. e' un'**assunzione**:
* se il documento e' rilevante $\to$ utente soffisfatto.

**valutazione empirica**: il benchmark ci permette di confrontare sistemi diversi
* in modo **equo**
* scegliere chi performa meglio
* migliorare i modelli in modo sistematico

**non posso isolare le componenti del sistema IR**:
* ossia: ranking, pesi, stemming, ecc...
* devo valutare l'intero sistema IR

## gold standar
**gold standard**: processo di costruzione dei dati etichettati, ossia il dataset per la valutazione. rappresenta la **ground truth**
* **equivalente a**: dataset oracolo e dataset annotato

**idea**: voglio costruire un dataset conoscendo già per ogni query, cosa e' rilevante e cosa non lo e'.
* **step 1, query rappresentative**: devo preparare query non casuali che riflettono bisogni informativi reali.
* **step 2, recuperare i documenti candidati**: uso un sistema IR "di base" che include molti falsi positivi (alta recall)
* **step 3, identificare la rilevanza dei documenti**: un umano identifica quali sono rilevanti.

## Precision e recall
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


**precision e recall**:
* **alta precision**: non sbaglio quasi mai ad identificare i positivi, ma inevitabilmente molti positivi li classifico come falsi. Ma viceversa, i falsi non li classifico quasi mai come positivi.
* **alta recall**: recupero tutti i positivi, ma sbaglio spesso a classificarli, molti falsi sono classificati come positivi. Ma viceversa i positivi non li classifico quasi mai come negativi.

**media armonica**:
$$
F_{1}=\frac{2PR}{P+R}
$$
* **massimizzare** $F_{1}$: se e solo se $P,R$ sono bilanciati.

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


## Rank based measures
**P ed R sono metriche globali**: non penalizzano se metto i documenti rilevanti in fondo al rank.
* sistema $A$ mette tutti i documenti rilevanti in cima
* sistema $B$ mette tutti i documenti rilevanti in fondo
* $A$ e $B$ potrebbero avere stessa precision e recall sugli stessi dati.


**Problema**: precision e recall sono metriche globali, non guardano come il sistema effettua il ranking. Dobbiamo definire delle nuove metriche

$\text{Precision@}K$: la precision sui primi $K$ documenti ritornati
* $\text{Recall@}K$: similmente
* **grafico**: posso disegnare il grafico. E' a forma di sega.
	* documento $i\text{-esimo}$ e' rilevante: aumentano la precision e la recall
	* documento $\text{i-esimo}$ non rilevante: la precision diminuisce, ma la recall rimane uguale
![[Pasted image 20260705215046.png]]**Interpolation**:
$$
P(R) = \max \{ P': R' \geq R \land (R) \}
$$
* produce un grafico a scalini.

**MAP** (Mean Average Precision):
* per ogni documento rilevante, calcola $\text{Precision@}K$
* **average precision** e' la media dei $P@K$.
* **MAP** e' l'average precision **su più** **query**.
* **macro**: e' un sistema che pesa allo stesso modo i risultati delle query (che possono ritornare pochi documenti rilevanti, oppure tanti)
$$
\text{MAP}= \frac{1}{|Q|} \sum _{q \in Q} \text{AP}(q)
$$
![[Pasted image 20260705221804.png]]
* **sistemi che massimizzano recall**: map e' ideale in contesti dove voglio alta recall. MAP penalizza sistemi che mettono i documenti rilevanti in fondo alla classifica.
## Discounted Cumulative Gain
**assunzioni**: 
* **distinzione** tra documenti **altamente rilevanti**, e documenti rilevanti in modo **marginale**.
* documenti rilevanti in bassa posizione non vengono mai visti dall'utente

**misuro**:
* **gain**: quanto e' rilevante un documento con rilevanza $r_{i}$?
	* **scala**: per esempio in $[0,3]$
* **discount**: di solito si misura come $\frac{1}{\log i}$, con $i=\text{rank}$
* **cumulative gain**: $CG = r_{1} + r_{2} + \dots + r_{n}$
* **discount cumulative gain**: $DCG_{p} = r_{1} + \sum_{i=2}^p \frac{r_{i}}{\log i}$
	* **a che serve?** penalizza documenti rilevanti in posizioni dopo la 1.


**ideal ranking**: ho i documenti con rilevanza 3 in alto, poi 2, ecc...
**normalizzazione per DCG**:
$$
\text{NDCG} = \frac{\text{DCG}}{\text{IDCG}}
$$
* $\text{IDCG}$ e' il DCG calcolato sul risultato ideale.

**reciprocal rank ed mrr**
* **scenario**: voglio misurare il modello in scenari in cui ho solo un risultato corretto
* $\text{RR} = \frac{1}{K}$ con $K$ posizione del primo documento rielvante.
* $\text{MRR}$ e' la media degli RR **su piu query**


## giudizio umano
**bias umano**: si tende a guardare sempre i primi due risultati
* **primi risultati**: sono i piu cliccati e guardati. Magari i risultati dopo manco vengono letti.
* Quindi i click sono molto informativi, ma soggetti ad un bias utente.

**sequenze di click**: 
![[Pasted image 20260705230820.png]]
* l'unica cosa che posso dedurre e' che il terzo risultato e' migliore del secondo

**valutazioni pairwise**: per ridurre il bias, faccio paragonare all'utente due documenti
**confronto interleaving e click**: intervallo nel risultato mostrato due ranking diversi e vedo chi ottiene piu click dei due.
**A/B testing**: due gruppi di utenti con due sistemi differenti per il ranking. Misuro e vedo chi e' meglio.

## lexical semantics

**Ipotesi Distribuzionale**: parole con significati simili tendono ad apparire in contesti simili, dunque il significato di una parola e' descritto dall'insieme del contesto testuale.

**idea**: $x$ puo' essere rappresentata considerando la distribuzione delle parole insieme a cui occorre.
* **parole che condividono le stesso co-occurrences**: rappresentazione simile
* parole mappate in vettori

**contesto**: finestra di $n$ parole su una finestra nel documento.

**relazioni**:
* **topiche**: due parole che si riferiscono ad un topic comune come `calcio, stadio, squafra`
* **sintagmatiche**: dipende dalla posizione della parola e dalle entita coinvolte nel testo. `il lupo e' affamato`, allora tra `lupo` ed `affamato` c'e' una relazione sintagmatica.
* **paradigmatiche**: parole che possono essere scambiate, nello stesso contesto `il lupo e' [affamato | assetato]`

**spazi vettoriali di parole**:
* **topic space**: per catturare il topic, il contesto e' l'intero documento
* **co--occurrence**: uso una finestra di ampiezza $n$
* **co-occ. syntaxt based**: guardo l'albero sintattico nella finetra e decido per esempio? chi e' soggetto?, chi e' oggetto? ecc...

**verb net**: lessico verbale online.
* **classi di levin**: migliora l'organizzazione in classi del lavoro di levin.
* ogni verbo ha:
	* I **ruoli tematici** (es. Agente, Paziente, Destinatario).
	- Le **restrizioni di selezione** imposte sugli argomenti del verbo (es. se l'oggetto deve essere necessariamente [+animato] o [+concreto]).
	- I **frame**, i quali consistono in una descrizione strettamente sintattica associata a predicati semantici dotati di una funzione temporale.

**POS Tagging**: fase nell'elaborazione del linguaggio naturale in cui assegno ad ogni parola la sua categoria (es. sostantivo, verbo, aggettivo, pronome), in base al contesto.

![[Pasted image 20260706001020.png]]![[Pasted image 20260706001131.png]]

**matrice di co-occorrenza**:
* **righe**: scegli parole target con occorrenza maggiore di $t$ threshold, di cui si vuole calcolare il significato
* **colonne**: le $C$ piu frequenti word-context sono selezionate
* per ogni parola target, con la matrice di incidenza calcolo una lista che descrive quante volte i termini in colonna compaiono vicino alla target.

**PMI**: Pointwise Mutual Information
$$
\text{PMI}(x,y) = \log \frac{P(x,y)}{P(x)P(y)}
$$
- P ( x ) → probabilità di vedere x
- P ( y ) → probabilità di vedere y
- P ( x , y ) → probabilità che compaiano insieme
    - parole molto frequenti → penalizzate
    - parole rare ma significative → valorizzate
- se $PMI > 0$ allora  le due parole tendono a comparire insieme, piuttosto che da sole
- se $PMI = 0$ allora le due parole compaiono insieme per caso.
- se $PMI < 0$ allora le due parole tendono a non comparire mai insieme 

![[Pasted image 20260706002005.png]]

![[Pasted image 20260706101519.png]]


**Problema, la matrice e' molto sparsa**, posso decomporla a valori singolari (**SVD**):
$$
M = U \cdot S \cdot V^T
$$
![[Pasted image 20260706101845.png]]
* $k$: la matrice viene troncata in $k$ dimensioni con $k \ll N$
* $S$ e' $k\times k$, ossia mantengo $k$ concetti da questa matrice.
* - **Minimizza l'errore globale di ricostruzione:** Offre la migliore approssimazione a basso rango possibile della matrice originaria.
- **Riduce il rumore (_Noise reduction_):** Eliminando le dimensioni minori (i concetti meno frequenti), taglia via le variazioni casuali del linguaggio e gli errori di co-occorrenza statistica.
- **Fa emergere i "Pseudo-Concetti":** Le nuove componenti principali individuate dalla SVD non corrispondono più a singole parole, ma sono combinazioni lineari delle dimensioni originali. Diventano veri e propri concetti astratti (es. una dimensione latente potrebbe rappresentare implicitamente il concetto di "Medicina" fondendo insieme gli effetti di _ospedale_, _dottore_, _paziente_).
- **Cattura relazioni di secondo ordine:** Questo è l'effetto più importante. Se la parola $A$ compare spesso con $B$, e la parola $B$ compare spesso con $C$, la LSA capirà che $A$ e $C$ sono semanticamente correlate, **anche se $A$ e $C$ non sono mai comparse insieme nello stesso documento**