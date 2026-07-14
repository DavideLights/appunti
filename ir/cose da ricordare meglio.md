
1. Qual è il principale vantaggio prestazionale della compressione dell'indice invertito oltre al risparmio di spazio su disco? aumenta la velocita in lettura e scrittura dell'indice se viene compresso
2. Cosa prevede la Legge di Heaps riguardo al limite superiore del vocabolario in una collezione che continua a crescere? Non esiste un limte superiore a causa di unicode, ed errori di battitura nei documenti
3. i tweet sono memorizzati in segmenti di memoria ordinati in word da 32 bit, in modo da rendere efficiente la lettura per il processore.
4. lettura read-only: una volta che l'indice attivo si riempie viene congelato e tenuto in modalita solo lettura. solo l'indice corrente puo' essere modificato.
5. permuterm index: permette di trasformare tutte le query con `*` in query che hanno sempre la stessa forma: `parola*`, questo tipo di query sono facilmente gestibili, poiche posso cercare meglio nell'albero di ricerca in tempo logaritmico. 
6. lo smoothing di laplace nella correzione degli errori serve ad evitare i casi in cui alcune entry siano 0 nella confusion matrix, azzerando l'intero prodotto.
7. Risposta 1 & 2: Come si processa `se*ate AND fil*er` e la query `*X`. **Cosa mancava nella tua risposta:** Non hai spiegato _come_ si risolvono le wildcard centrali.
    1. In un albero di ricerca standard del dizionario, puoi fare solo ricerche per prefisso (`mon*`). Non puoi risolvere wildcard centrali o finali.
    2. Con il **Permuterm Index**, ruoti le wildcard per spostare l'asterisco alla fine. La query `se*ate` (aggiungendo il terminatore `$`) diventa `se*ate$`, che ruotata diventa **ate$se***. La query `fil*er` diventa **er$fil***. A questo punto esegui due ricerche rapide per prefisso nel B-tree del Permuterm, recuperi i termini reali corrispondenti e solo allora fai l'intersezione delle postings list.
    3. Per la query del tipo ***X**, essa si trasforma ruotando il carattere jolly alla fine, ovvero cercando **X$***.
    4. **Il problema dell'AND:** Se provassimo a risolvere `se*ate` senza Permuterm, dovremmo cercare nel dizionario tutte le parole che iniziano con `se*`, tutte quelle che finiscono con `*ate`, e fare l'intersezione dei termini del dizionario. Questo AND tra insiemi di termini è **estremamente costoso** perché il vocabolario del dizionario è enorme.
8. L'HMM è la cornice teorica che racchiude l'intero processo, ma il calcolo specifico di P(X∣W) (il modello di canale per la frase) si basa sull'**assunzione di indipendenza degli errori delle singole parole**
9. la _document frequency_ (dft​) è una **proprietà globale** del termine t nell'intera collezione
10. **L'errore matematico:** Hai scritto che la F-Measure _"viene massimizzata solo quando Precision=Recall=0.5, altrimenti cala drasticamente"_. **Questo è matematicamente falso.** La F1​ viene massimizzata (raggiungendo il valore ideale di 1.0) solo quando **sia la Precision che la Recall sono pari a** 1.0. Se P=R=0.5, il calcolo della media armonica restituisce 0.5 (il che non è affatto il massimo).
11. La tua intuizione è corretta, ma all'esame la spiegazione tecnica deve basarsi sul **class imbalance** e sul peso dei **True Negatives (**tn**)**:
	- In un archivio reale di 1.000.000 di documenti, i documenti rilevanti per una query sono pochissimi (es. 10).
	- Un sistema "pigro" che restituisce sempre 0 risultati commette 10 falsi negativi, ma indovina ben 999.990 veri negativi (tn).
	- Inserendo questi dati nella formula dell'accuracy (acc=tp+tn+fn+fptp+tn​), il sistema ottiene un'accuratezza quasi perfetta del 99.99% pur essendo totalmente inutile per l'utente. L'accuracy premia l'esclusione di documenti irrilevanti banali, ignorando la capacità di trovare i pochi documenti utili.

12. **La regola corretta:** Puoi stabilire una preferenza relativa (_pairwise_) solo **confrontando un documento cliccato con quelli saltati (non cliccati) che si trovavano sopra di esso**.
	- Se l'utente clicca il documento in posizione 1, salta il 2 e il 3, e poi clicca il 4:
	    - Non sappiamo se 1>4 o 4>1.
	    - Possiamo però dedurre con assoluta certezza che 4>2 e 4>3, perché l'utente ha esaminato la lista, ha volutamente ignorato (saltato) le posizioni 2 e 3, e ha deciso di cliccare la posizione 4 che era più in basso .