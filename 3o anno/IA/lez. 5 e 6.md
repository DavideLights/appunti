**assunzioni**:
* azioni non deterministiche
* ambiente parzialmente osservabile
* ad un'azione piu stati possibili 
* **conseguenza**: ho troppi stati da esplorare.
* **soluzione**: un'insieme dei cammini verso la soluzione.

**come funziona la ricerca locale**?
* **non e' sistematico**: non garantisce di esplorare tutte le possibilita, non c'e' un'ordine fissato con cui guardare i nodi.
* **un solo stato in memoria**: non tengo in memoria l'intera frontiera di nodi, genero solo i prossimi stati a partire da quello corrente.
	* **memoria**: efficiente
	* **mi muovo solo tra nodi adiacenti**, non pianifico sequenze di azioni.
* **ottimizzazione**: e' utile in problemi di ottimizzazione dove devo esplorare per trovare la funzione obiettivo che minimizza il costo.
* **path**: non c'e' bisogno di tenerlo in memoria, mi interessa solo trovare la soluzione.
* **conesto**: ambiente completamente osservabile, noto, statico, deterministico.

**(A) hill climbing**: genera e valuta i successori. scegli quello che migliora la valutazione rispetto allo stato attuale.
* **greedy**: scegli quello che sembra migliore in quel momento
* **varianti**:
	* **salita rapida**: sceglie sempre il migliore. *Problema: potrebbe incastrarsi in massimi locali.*
	* **a caso**: sceglie a caso tra i vicini migliori. *Vantaggio*: *evita facilmente i massimi locali*
	* **prima scelta**: genera i vicini casualmente e sceglie il migliore. *Vantaggio: evita di calcolare tutti i vicini, potrebbero essere troppi*
	* **mosse laterali**: ammetti mosse con passi uguali al valore corrente. *Vantaggio*: esci dai plateau.
	* **riavvio casuale**: se mi blocco, ricomincia a caso
* **iniettare randomicita**: e' la soluzione migliore per evitare vari problemi.
* **completo**: non lo e'! Potrebbe incastrarsi.

**problemi di hill climbing**:
* **massimi locali**
* **altipiani, ossia i plateau**: area piatta, non so dove muovermi per migliorare lo stato.
* **crinali**: ho una serie di massimi locali separati da discese, l'agente si blocca continuamente.

**(A) Simulated annealing**: ogni tanto accetta percorsi negativi
* **scegli uno stato random**
	* **migliora lo stato corrente**? allora lo prendo
	* **peggiora**? lo prendo con $P<1$.
* $P$ **decresce esponenzialmente** tanto quanto fa schifo lo stato da scegliere.
* $T$ **temperatura**: influenza $P$
	* **alto**: scelte casuali
	* **comportamento**: la temperatura decresce col tempo, in base allo schedule al variare del tempo $t$
$$
p=e^{-\Delta E/T}
$$
![[Pasted image 20260717192455.png]]

**(A) Local beam search**: tieni traccia dei $k$ nodi piu' promettenti usando $k$ ricerche collaborative
* **collaborativo**: ho $k$ ricerche indipendenti sull'istanza del problema
* **espansione e beam**: espando le $k$ ricerche, e seleziono i $k$ nodi piu promettenti
* **problema diversita**: tutti i nodi si incontrano nello stesso punto se si comportano in modo simile

**(A) alberi and-or**:
* **contesto**: ambiente non deterministico
	* **conseguenza**: l'albero di ricerca classico non va piu bene
* **foglia**: e' un'obiettivo oppure uno stato gia visto
* **cicli**: li posso gestire rieseguendo all'infinito finche non riesce
	* **es**: il robot vuole andare a destra ma con una certa probabilita fallisce, ma per perseguire l'obiettivo devo andare per forza a destra.
* **come funziona l'algoritmo in pratica?** nella fase di **PIANIFICAZIONE**...
	1. **stato credenza radice** e' un nodo OR. Da qui comincio a provare tutte le azioni
	2. Per ogni azione viene generato un'albero AND con uno o piu stati possibili. Devo risolvere ognuno di questi trattandolo come un nodo OR
		1. Se uno stato e' obiettivo allora l'ho risolto
		2. Se non e' obiettivo devo risolverlo cercando la sequenza di azioni che lo risolve.

![[Pasted image 20260718011458.png]]

**codice ricerca-or**: per ogni azione effettua una **ricerca-and**
* se la ricerca-and ritorna successo allora ritorna la sequenza per quel successo e concatena l'azione.

**codice ricerca-and**: per ogni stato possibile nel nodo and, fai una ricerca OR
* se un solo stato fallisce, allora ritorna il fallimento
* altrimenti ritorna il piano di contingenza per ogni stato possibile

**ricerca in ambiente parzialmente osservabile**: gestire l'incertezza riguardo a cosa non riesco a percepire. L'obiettivo e' agire, eseguire azioni per capire com'e' il mondo anche se non posso osservarlo.

**ricerca sensor-less**:
* **stati-credenza**: rappresenta tutte le situazioni fisiche in cui l'agente potrebbe trovarsi
	* **ossia**: e' un'insieme di stati.

| Elemento           | Descrizione                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- |
| **Stati**          | Ogni belief state è un sottoinsieme degli stati fisici possibili (fino a 2ⁿ).           |
| **Stato iniziale** | Insieme di tutti gli stati compatibili con le informazioni note.                        |
| **Azioni**         | Ammissibili se sicure in tutti gli stati del belief state.                              |
| **Transizioni**    | Il nuovo belief state è l’unione dei risultati dell’azione su ciascuno stato possibile. |
| **Test obiettivo** | È raggiunto se almeno uno stato del belief state soddisfa l’obiettivo.                  |
| **Costo**          | Può essere medio o prudente (es. il massimo).                                           |
![[Pasted image 20260718005015.png]]


**ricerca con stati credenza in ambiente parzialmente osservabile**:
1. **predizione**: calcola lo stato-credenza $C'$ risultante da un'azione $A$ su $C$
	1. per ogni stato $c\in C$ nello stato-credenza applica l'azione $A$
	2. ottengo $C'$
2. **percezioni possibili**: determina quali percezioni potrei ricevere in quello stato
3. **filtra in base alle percezioni effettivamente ricevute**: in base alle percezioni ricevute, determina lo stato credenza contenente gli stati compatibili con quanto percepito.

**ricerca online**:
* **contesto**: ambienti reali, dinamici o ignoti, non deterministici.
* **alterna**: $\text{azione} \to \text{osservazione} \to \text{decisione}$

**ambienti sconosciuti**: l'agente deve sperimentare un modello dell'ambiente. Agisce per imparare com'e' fatto il modello del mondo
* **stato**: conosce solo quello attuale
* **costo e risultato**: conosce $c(s,a,s')$ e $\text{Risultato}(s,a)$ solo dopo aver agito
* **euristica**: puo' usare un'euristica.
* **vicoli ciechi**: potrebbero esistere stati in cui una volta entrati non si riesce piu ad eseguire alcuna azione!
	* **conseguenza**: l'agente deve essere in grado di esplorare in sicurezza

**(A) ricerca locale online**:
1. l'agente conosce $h(s)$ solo dopo aver esplorato $s$
2. mantiene un solo stato in memoria
3. **contesto**: ambienti ignoti/dinamici
4. **Strategia Random Walk**: scegli casualmente un'azione per uscire da massimi locali
5. **LRTA$^*$**: impara mentre ricerca aggiornando l'euristica 

![[Pasted image 20260718013859.png]]
* $s,a$: stato e azione precedenti
* $s'$: percezione dello stato corrente
* $\text{result}[s,a] \gets s'$ devo ricordare cosa succede applicando $a$ ad $s$, imparo il modello del mondo
* $H[s] \gets \min_{b \in \text{Actions}(s)} \text{LRTA}^*\text{-Cost}(s,b,\text{result}[s,b], H)$
* $a \gets$ azione che minimizza $\text{LRTA}^*\text{-Cost}$

## agenti basati su conoscenza
**(A) basato su conoscenza**:
* $KB$: Knowledge Base, e' insieme di fatti e regole.
* **assioma**: fatto vero, non derivato da altre regole o fatti.
* $\text{TELL}(KB, \phi)$: inserisce nel KB il nuovo fatto o regola
* $\text{ASK}(KB,a)$: $a$ e' conseguenza logica di $KB$
* $\text{RETRACT}(KB,a)$: elimina $a$ dal $KB$

![[Pasted image 20260718014727.png]]
1. Inserisci nel $KB$ la percezione
2. Fai una query al $KB$ per ottenere l'azione
3. Inserisci nel $KB$  l'azione eseguita

| Componente    | Descrizione                                                                             |
| ------------- | --------------------------------------------------------------------------------------- |
| **Sintassi**  | Definisce i simboli e le regole per costruire frasi logiche.                            |
| **Semantica** | Stabilisce la corrispondenza tra formule e fatti del mondo (quando una formula è vera). |
| **Inferenza** | Insieme di regole che permettono di derivare nuove formule vere da quelle note.         |

**grounding**: descrive il legame tra rappresentazione logica ed il mondo reale di riferimento
* **sensori**: creano connessione con il mondo
* l'agente ha una **credenza del mondo** data dalle percezioni
* **apprendimento**: puo' essere fallibile, e creare dunque **FATTI ERRATI**

![[Pasted image 20260718020043.png]]

**conseguenza logica**: $A$ e' conseguenza logica di $KB$ se 
$$
KB⊨ A \ \text{⇔}\ M(KB) ⊆ M(A)
$$
* $M(KB) =$ modelli che rendono vero $KB$
* $M(A)$ = modelli che rendono vero $A$
* **modello**: mondo in cui $X$ e' vero
	* se $X$ e' composto da tante formule
	* allora pochi modelli soddisfano $X$

**ragionamento non monotono**: Nella **logica classica** vale la **monotonia**: se $KB ⊨ α$, allora anche $KB ∪ \{β\} ⊨ α$ 
- Se aggiungo una nuova informazione non modifico ciò che prima era vero
- Nel ragionamento umano, invece, **nuove informazioni possono invalidare** conclusioni precedenti → **ragionamento non monotòno**.
