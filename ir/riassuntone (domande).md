k
# Lez. 1
1. Che cos'e IR? che assunzioni si fanno inizialmente? cosa si cerca nell'information retrieval
2. Differenza tra Information Need e query.
3. Differenze tra Precision e Recall, cosa misurano e come si comportano
4. Differenza tra notazione sparsa e densa.
5. Cosa e' la Term-Document Incidence matrix e quando e' sconveniente
6. A cosa serve l'inverted Index? puo' essere di lungezza fissa?
7. Come memorizzo l'inverted index in memoria principale e su disco?
8. Descrivere il preprocessing dei documenti (Lemmatizzazione, Stemming, Normalizzazione, Stop words)
9. Accenna alcuni problemi che possono comparire con il preprocessing
10. Come si costruisce l'inverted index? (Indexer)
11. differenza tra posting e postings list.

![[Pasted image 20260627155426.png]]

![[Pasted image 20260627160614.png]]
![[Pasted image 20260420180804.png]]



![[Pasted image 20260306124936.png]]



![[Pasted image 20260318094400.png]]


**Merge algorithm** $\text{Intersect}(p_{1},p_{2})$:
1. $\text{answer} \gets \emptyset$
2. **while** $p_{1} \neq \text{NIL}$ and $p_{2} \neq \text{NIL}$:
3. **do if** $\text{docID}(p_{1}) = \text{docID}(p_{2})$
	1. **then**: $\text{Add}(\text{answer}, \text{docID}(p_{1}))$
	2. **else if** $\text{docID}(p_{1}) < \text{docID(p2)}$
		1. **then** $p_{1} \gets \text{next}(p_{1})$
		2. **else** $p_{2} \gets \text{next}(p_{2})$

# Lez. 2

1. cosa voglio minimizzare quando salvo in memoria su disco le posting lists? (`seek`)
2. che cos'e' `WEST LAW`? (precision, boolean retrieval)
3. Come implementeresti `Brutus AND NOT Caesar` ed  `Brutus OR NOT Caesar`
4. Come ottimizzo le query? Che informazione devo tenere in memoria per fare queste ottimizzazioni? Perche' ho una riduzione in complessita?
5. ![[Pasted image 20260627173541.png]]
6. Come ottimizzeresti una query del tipo: $(t_{1} \text{ OR } t_{2}) \text{ AND} (t_{3} \text{ OR } t_{4})$
7. Come viene effettuata la tokenizzazione? Che porblemi potrebbe comportare?
8. Come effettuo la normalizzazione?
9. **Differenza tra stemming e lemmatization.** La lemmatizzazione fa analisi del contesto per ridurre correttamente il termine (verbi coniugati, maschili e femminili) alla sua forma canonica,
10. Descrivi Biword Index, Phrase index e Positional index. Che problema di spazio ha il positional index?
11. In che modo biword index puo' essere usato per le entita nominali?

## lez. 3 
1. quanto costa ordinare le coppie $(\text{term}, \text{docID})$?
2. che cos'e' RCV1?
3. che problema ha il sort-based index? (scalabilita, fault tollerant, blocchi su disco)
4. che differenza c'e' tra termine e token?
5. perche' in RCV1 ho **avg. # bytes per term = 7.5** mentre **avg. # bytes per token 4.5**?
6. **Come funziona BSBI**? come sono fatte le coppie $\text{(\_, docID)}$? cosa e' un blocco e come viene effettuato il merge
	1. ATTENZIONE: termID contro docID
7. Descrivi lo pseudocodice di BSBI.
8. Come viene usato l'AVL per il merge dei blocchi? Come avviene la procedura di merge di un blocco?
9. Che cosa e' il multiway merge? perche' utilizza una coda con priorita?
	1. ATTENZIONE: la coda con priorita deve tenere conto del range di docID riguardanti ogni blocco. 
10. Come funziona SPIMI? in che modo evita il sort di tutte le coppie? Quale condizione triggera la scrittura su disco?
11. Qual'e' la complessita di SPIMI, e come differisce da BSBI?

## lez. 4
1. Cosa sono `master`, `splits`, `split` e `pool`
2. differenza tra document partitioned e term partitioned
3. come vengono distribuite le operazioni dell'inverter dal master?
4. cosa e' il dynamic indexing? come gestisco modifica e rimozione dei documenti
5. descrivi l'approccio che prevede l'uso di un main index e di indici ausiliari e il problema della reindicizzazione.
6. perche' l'approccio scemo con 1 indice ausiliario e 1 indice principale costa $\Theta\left( \frac{T^2}{n} \right)$?
7. spiega il logarithmic merge. Perche' costa $\Theta\left( T \log \frac{T}{n} \right)$
8. che problema introduce l'uso di piu indici riguardo al calcolo delle frequenze dei termini, e come si risolve?
9. che assunzione usa twitter per le posting dei tweet? che cosa sono gli indici read-only
![[Pasted image 20260318121849.png]]
## lez. 5
1. perche' togliere i numeri da RCV1 riduce di poco la grandezza?
2. perche togliere le stopword cambia poco il dizionario ma di tanto il positional index?
3. perche' case folding e stemming non cambiano la grandezza del positional index, ma riducono il dizionario?
4. quali sono i due tipi di compressione? (lossy, lossless)
5. che cosa dice la Heaps Law? $M=kT^b$
6. che cosa dice la legge di Zipfs? $cf_{i} = ci^k$
7. che relazione c'e' in logaritmo tra $cf_{i}$ ed $i$?
8. che struttura viene usata per cercare nel dizionario?
9.  come comprimo la grandezza del dizionario? a cosa serve la struttura blocking?
10. perche' e' meglio usare il puntatore nella stringa rispetto a salvare 20 byte?
11. che cos'e' il frontcoding?
12. quando mi conviene immagazzinare il gap, invece del doc id grezzo?
13. in cosa consiste l'unary code?
14. in cosa consiste il gamma code?
15. che problema hanno unary code e gamma code sui byte?
16. in cosa consiste VB codes?
17. come funziona la codifica usata da google?
![[Pasted image 20260702143546.png]]

## lez. 6

1. come processo la query `se*ate AND fil*er`? come funziona la ricerca binaria e qual'e' il problema dell'AND?
2. descrivi il permuterm index, come si usa e come si trasforma la query `*X`
3. che problema ha il permuterm? descrivi il $\text{k-gram}$ index e perche' e' una soluzione migliore, e quale problema introduce.
4. descrivi i 3 tipi di errore (`non-word`, `tipografico` e `cognitivo`)
5. come si rimedia ad `non-word` error? perche' correggo con parole che minimizzano l'edit distance?
6. che cos'e' il candidate set? che parole contiene?
7. che opzioni posso navigare per scegliere il candidato migliore?
8. che  cosa vuol dire $\hat{w} = \text{argmax}_{w \in V}P(w|x)$?
9. che modello viene usato per calcolare $P(x|w)$
10. che modello e' $P(w) = \frac{C(w)}{T}$
11. come genero l'insieme dei candidati?
12. a cosa serve lo smoothing di la place? scrivi la formula
13. Nel noisy channel model, per context-sensitive spell correction, cosa vogliamo fare? cosa sono $X$ e $W$?
14. che modello uso per calcolare $P(X|W)$ per context sensitive? qual'e' la formula?
15. che modello uso per calcolare $P(W)$? qual'e' la formula?
16. cosa descrive l'hidden markov  model? cosa sono transizioni ed emissioni?
17. perche' non si usa l'algoritmo di viterbi per risolvere hidden markov model?
18. come si risolve in caso la mia parola e' corretta ma e' molto rara?


## lez. 7
1. che cosa e' feast or famine? come si risolve?
2. differenza tra incidence matrix e count metrix.
3. che cos'e' il modello bag of words? e cosa comporta? perche' e' utile?
4. che cos'e' la term frequency? in che modo viene usata per calcolare il peso di un termine per un documento
5. perche $\text{tf-matching-score}$ non va bene come metrica? perche $\text{tf}_{t,d}$ non puo' essere usato cosi?
6. Che cosa e' $\text{idf}_{t}$ e perche' non scriviamo $\text{idf}_{t,d}$?  che relazione ha con $\text{df}_{t}$? Come si comporta $\frac{N}{df_{t}}$ rispetto a $\log \frac{N}{df_{t}}$?
7. Che cosa e' $\text{tf}_{d,f} \cdot \text{idf}_{t}$?
8. In che modo rappresentiamo un documento come vettore?
9. Perche non possiamo usare distanza euclidea per misurare la similarita tra vettori? che cosa succede con documenti lunghi?
10. che proporzione c'e' tra la funzione coseno e la similarita?
11. come si calcola il coseno di due vettori? come si calcola la norma $L_{2}$ di un vettore?
12. Nello pseudocodice cosa facciamo per pesare lo score in modo corretto per tutti i documenti?]
13. Che differenza c'e' tra TAAT e DAAT?
14. Perche non posso memorizzare $w_{t,d}$? in cosa e' sconveniente?

![[Pasted image 20260704161026.png]]
![[Pasted image 20260704162743.png]]

## lez. 8
1. cosa e' un benchmark e a che ci serve banalmente?
2. cosa e' un proxy?
3. cosa e' il gold standard? che cosa e' il ground truth?
4. descrivi precision e recall e a che serve la media armonica
5. perche l'accuracy e' una metrica inutile e di merda?
6. in che senso precision e recall sono metriche globali?
7. cosa sono $\text{Precision}@K$ ed $\text{Recall}@K$? come si comporta il grafico
8. cosa e' MAP? che cosa massimizzo quando miglioro questa metrica?
9. cosa e' il DCG? su quale assunzione lavora?
10. cosa e' il reciprocal rank? e cosa e' l'MRR?
11. come abbiamo definito il bais umano? che conseguenze ha sulla rilevanza dei click? (valutazioni pairwise, confronto interleaving e click, ed A/B testing)
12. che cosa dice l'ipotesi distribuzionale? come posso di conseguenza rappresentare il termine $x$?
13. che tipi di relazioni ci sono tra termini? (topiche, sintagmatiche e paradigmatiche)
14. come faccio a catturare il topic di una parola? come catturo le co-occorrenze? come catture le co-occrenze guardando la sintassi?
15. che cosa e' verb net?
16. che cosa misura PMI? scrivimi la formula scemo
17. la matrice di cooccorrenza dei termini e' sparsa, cosa faccio?

![[Pasted image 20260705215046.png]]

![[Pasted image 20260705221804.png]]
![[Pasted image 20260705230820.png]]
## lez. 9 e 10
1. **quali sono gli eventi incerti che ci portano all'approccio probabilistico**? (utenti, contesto, rappresentazione, approssimazione)
2. $P(\text{relevant|d,q})$ che cosa descrive?
3. perche' vector space model non va bene rispetto all'approccio probabilistico? (somiglianza, contesto, normalizzazione)
4. che cosa descrive $O(R|d,q)$? quand'e' che un documento e' piu probabile che sia rilevante?
5. calcolare $p(R|d,q)$ con bayes e' difficile, che assunzioni vengono fatte?
6. che cosa dice il PRP? come deve essere la funzione di costo dell'errore? che assunzione viene fatta?
7. che cosa descrive la formula? cosa sono $C, C'$?~~$$R(D(q)) = \sum_{d\in D} C'(d,q)p(\bar{R}|d,q) + \sum_{d \not \in D} C(d,q) p(R|d,q)$$
8. che assunzione fa il Binary Independence Model? chi partecipa all'indipendenza nel BIM? cosa vuol dire indipendenza delle feature?
9. in BIM perche' $O(R|v_{d}, v_{q})=\prod_{i=1}^M \frac{p(x_{i}|R,v_{q})}{p(x_{i}|\bar{R},v_{q})}$ che assunzione viene fatta per semplificare il calcolo riguardo ai termini che non compaiono nella query?
10. cosa vuol dire la formula? che cazzo sono $p_{i}$ ed $u_{i}$?
 $$O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=y_{i}} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})}
$$
11. come approssimiamo $p_{i}$ ed $u_{i}$, di conseguenza come definiamo  $RSV_{d}$?
12. che problema ha **BIM**? perche' studiamo la poisson?
13. a differenza di BIM, che variabili studiamo?
14. perche nella formula non compare $\bar R$? a che assunzione faccio riferimento? $$RSV_{d} = \sum_{t_{i}: y_{i} =1} \log \frac{p(d_{t_{i}}=n_{i}|R,v_{q})p(d_{t_{i}}=0)}{p(d_{t_{i}}=n_{i})p(d_{t_{i}}=0|R,v_{q})}$$
15. che cosa descrive il parmametro $\lambda$ della poisson? come approssiamo $\lambda_{j} \approx \frac{cf_{t_{j}}}{N}$ 
16. dove avviene il picco in una poisson di parametro $\lambda$? e come si comporta al variare del parametro k?
17. perche' dobbiamo sdoppiare lambda  usando due poisson differenti di parametro $\rho_{j}$ e $\gamma_{j}$. che decrivono?
18. come si ottiene la formula? cosa descrive il rapporto? $$RSV_d = \sum_{t_i:y_i=1} \log \left( \frac{\rho_i}{\gamma_i} \right)^{n_i} = \sum_{t_i:y_i=1} n_i \log \frac{\rho_i}{\gamma_i}$$
19. cosa descrive $= p_i \frac{e^{-\mu_i} \mu_{i}^{n_i}}{n_i!} + (1 - p_i) \frac{e^{-\bar{\mu}_i} \bar{\mu}_{i}^{n_i}}{n_i!}$? cosa sono $\mu_{i}$, $\bar{\mu}$ ed $p_{i}$?
20. con quale funzione approssimiamo il comportamento della 2poisson?
21. $RSV_d = \sum_{t_i:y_i=1} \frac{(k+1)n_i}{k+n_i} \log \frac{N}{df_{t_i}}$ come si ottiene?
22. descrivi okapiBM25. c

## lez. 11
