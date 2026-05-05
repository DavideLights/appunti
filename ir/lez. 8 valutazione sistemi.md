**obiettivo**: voglio restituire all'utente qualcosa che lo soddisfi. 
**soggettivita**: questa metrica e' soggettiva, devo introdurre un metodo standard e replicabile.

**benchmark**: un'ambiente di valutazione controllato. Nel nostro caso e' compost da
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
* **step 2, recuperare i documenti candidati**: uso un sistema IR "di base" che include molti falsi positivi
* **step 3, identificare la rilevanza dei documenti**: si h
