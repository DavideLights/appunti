
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
6. 