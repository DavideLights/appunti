**feast or famine**: gli operatori `AND` ed `OR` restringono o allargano troppo lo spazio dei risultati.

**soluzione a feast or famine**: ranked retrieval. Invece di filtrare i documenti vengono ordinati per rilevanza.

**score**: ogni coppia $\text{(query, documento)}$. misura quanto $\text{documento}$ e' rilevante rispetto alla $\text{query}$. restituisco solo i migliori $k$.

**jaccard similarity**: confronto come insiemi. Ma non funziona per il retrieval, non considera:
* quante volte compare una parola.
* quali parole sono frequenti ed altre rare.

## Vector space model
**Vector Space Model**: rappresentare **documenti** e **query** come vettori in uno spazio ad alta dimensionalità.

**cos'e' una dimensione**? ad ogni dimensione corrisponde un termine del vocabolario, ogni termine ha un certo peso, che dipende dalla sua importanza nel documento e nella collezione.

## modelli
**incidence matrix**: ogni documento e' rappresentato da un vettore binario. ma non tiene conto della frequenza.

**count matrix**: indica quante volte compare il termine in ogni documento.

**idea**: piu il termine compare nel documento e piu' il documento e' rilevante per quella parola.

**gemini spiega**: NON VENGONO USATE DAVVERO POI NEL CONCRETO SI USANO LE INCIDENCE MATRIX PER AVERE FREQUENZA O ALTRO

**bag of words**: ignoro l'ordine delle parole. considero quali compaiono e quante volte.

**perdita di contesto**: con bag of words perdiamo l'ordine delle parole ma semplifico il problema.

## term frequency
**term frequency**: $\text{tf}_{t,d} = \text{quante volte } t \text{ occorre in } d$.
**problema**: se un termine compare 10 volte in un documento, allora non e' necessariamente piu rilevante di un documento in cui compare una sola volta.

**soluzione**: introduco il **peso**, non voglio che la crescita dell'importanza del documento si lineare in $\text{tf}_{t,d}$ $$w_{t,d} = \begin{cases} 1 + \log_{10}(tf_{t,d}) & \text{se } tf_{t,d} > 0 \\ 0 & \text{altrimenti} \end{cases}$$

$\text{tg-matching-score}(q,d)=\sum_{t\in q\cap d}(1 + \log \text{tf}_{t,d})$

**problema di** $\text{tf}$:: parole come `the`, `is`, `and` compaiono spesso, ma sono poco informative.

**gemini**: dimmi le conseguenze di sta roba e perche' introduco `idf`.

## idf
**frequenza nella collezione**: considero quanto un termine e' frequente nell'intero set di documenti prima di decidere quanto e' importante un termine.

**regola**: pesi alti per termini rari come `Phenethylamine`

**pesi dei termini frequenti**: hanno comunque pesi positivi ma più leggeri dei termini rari.

**misura della quantità di informazione di un termine**: $\text{idf}_{t} = \log_{10} \frac{N}{\text{df}_{t}}$
* $\text{df}_{t}$: e' il numero di documenti in cui $t$ occorre.
* **ammorbidire** l'effetto di idf: $\frac {\log N}{\text{df}_{t}}$ invece di $\frac{N}{\text{df}_{t}}$

**relazione tra $\text{df}_{t}$ e $\text{idf}_{t}$**: $\text{df}_{t}$ **piccolo** implica un $\text{idf}_{t}$ **alto** e viceversa.
## tf-idf
**peso** $\text{tf-idf}$: e' il **prodotto** dei pesi $\text{tf}$ e $idf$.
* $w_{t,d} = (1 + \log \text{tf}_{t,d}) \log \frac{N}{\text{df}_{t}}$
* all'aumentare di $w_{t,d}$ aumenta il numero di occorrenze nel documento e la rarità nella collezione.

**documento come vettore**: rappresento un documento come un vettore di pesi $\text{tf-idf}$ in $\mathbb R^{|V|}$. 
* **dimensioni**: $|V|$ che e' grande.
* **vettore**: molto sparso, la maggior parte delle componenti valgono 0 se il dizionario e' molto ampio.

**calcolo vettore tf-idf nella query**: devo calcolare $q = [w_{1,q}, w_{2,q},\dots,w_{M,q}]$
* $\text{tf}_{t,q} = \text{numero di volte che il termine compare nella query}$
* $\text{idf}_{t} = \text{importanza del termine sul corpus dei documenti}$
* allora per calcolare ogni componente di $q$: $w_{t,q} = \text{tf}_{t,q} \cdot \text{idf}_{t}$

**ranking per prossimita**: 
* **distanza negativa** $\sim \text{ similarita } \sim \text{prossimita}$
* **ordine inverso**: voglio ordinare in ordine inverso rispetto alla distanza tra vettore documento e vettore della query.
* **definire la distanza**: come definisco la distanza tra due vettori in $|V|$ dimensioni?

**distanza euclidea**: ha diversi problemi.
* **sensibile alla lunghezza**: un documento lungo ha un vettore di lunghezza maggiore, anche se semanticamente e' identico ad uno piu' corto.
* **ES**: sia $D_{1}$ un documento e $D_{2}=D_{1}D_{1}$ ($D_{1}$ concatenato a se stesso). Allora $D_{2}$ ha lo stesso significato semantico di $D_{1}$, ma la distanza tra i due vettori e' grande, dunque dovrebbero avere bassa similarità.
* **documenti lunghi hanno piu significato**: anche se magari, non sono rilevanti di testi con meno parole.

**similarità tra angoli**: meglio della distanza euclidea. ordino i documenti in base all'angolo tra il vettore documento e vettore query.
* **2 documenti sono vettori se**: l'angolo e' di 0 gradi, ossia puntano nella stessa direzione.
* **2 documenti sono ortogonali se**: l'angolo e' di 90 gradi, ossia puntano in direzioni completamente diverse.

**funzione coseno**: e' monotonamente decrescente in $[0,180\degree]$.
*   $\cos(0°) = 1$ (massima similarità)
*   $\cos(90°) = 0$ (nessuna similarità)
*   $\cos(180°) = -1$ (massima dissimilarità, ma non si usa in IR con pesi positivi).
* **gemini**: non ho capito pk!!!

**ranking**:  $\text{angolo decrescente}\equiv \text{coseno crescente }$
* $\text{ coseno grande } \to \text{ angolo piccolo}$
* $\text{ angolo grande } \to \text{ coseno piccolo }$

**calcolare cos su vettori normalizzati** $\cos(\vec{q}, \vec{d})=\vec{q} \times \vec{ d} = \sum_{i} q_{i} d_{i}$
* **normalizzazione**: vale solo se i vettori sono normalizzati.

**applicare cosine similarity**:
* normalizza i vettori
* somma il prodotto delle componenti quando diverse da 0.

**calcolare cos**: $$
\cos(\vec{q}, \vec{d}) = \text{sim}(\vec{q}, \vec{d}) = \frac{\vec{q}}{|\vec{q}|}\frac{\vec{d}}{|\vec{d}|} = \frac{\sum_{i=1}^{|V|} q_{i} d_{i}}{\sqrt{ \sum_{i=1}^{|V|}q_{i}^2 } \sqrt{ \sum_{i=1}^{|V|}d_{i}^2 }}
$$
* **normalizzazione**: $\frac{\vec{q}}{|\vec{q}|}$ divido il vettore per la sua lunghezza
* $L_{2}$: $||x||_{2} = \sqrt{ \sum_{i}x_{i}^2 } = 1$, dunque i vettori vengono proiettati su una sphera di raggio 1. **gemini spiega meglio.**


![[Pasted image 20260407123204.png|400]]

**Coda priorita**: la uso per estrarre i primi $k$ documenti.

**Approccio TAAT**: Term-at-atime. L'algoritmo elabora un termine della query alla volta. Scorrendo la posting list e aggiornando i punteggi dei documenti.

**Ottimizzazioni**:
* **memorizzazione dei pesi**: $w_{t,d}$ e' di solito un numero con la virgola, e richiede più memoria rispetto ad un intero, *dunque non si puo' fare*.
* **memorizzare gli interi**: al posto di $w_{t,d}$ memorizzo $\text{tf}_{t,d}$ nella posting e $\text{idf}_{t}$ nell'header del termine nella posting list.
* **gemini che vuol dire??? pre-filtering**: Per evitare di scorrere tutte le posting list per ogni termine della query, si può applicare un filtro iniziale (ad esempio, un OR di tutti i termini della query) per selezionare un sottoinsieme più piccolo di documenti candidati da valutare in dettaglio.

**siano**:
* $d = \text{un documento}$, $c= \text{una collezione di documenti}$
* $n(t,d) = \text{numero occorrende di } t \text{ in } d$
* $N(d) = \sum_{t}n(t,d)= \text{ lunghezza di } d$.
* $\text{na}(d) = \frac{1}{|d|}\sum_{t}n(t,d) = \text{numero medio di occorrenze in } d$
* $\text{adl}(d,c) = \frac{1}{|c|} \sum_{d \in c} N(d) =  \text{ lunghezza media dei documenti in } c$
* $\text{ndl}(d,c) = \frac{N(d)}{\text{adl}(c)} = \text{lunghezza di } d \text{ normalizzata nella collezione } c$
#### Varianti di tf Weighting
*   **Natural ($\text{TF}_{\text{total}}(t,d) = n(t,d)$):** Semplicemente il conteggio grezzo. Non ha normalizzazione per la lunghezza del documento, favorendo i documenti più lunghi.
*   **Boolean ($\text{TF}_{\text{bool}}(t,d)$):** 1 se il termine è presente, 0 altrimenti.
*   **Sum ($\text{TF}_{\text{sum}}(t,d) = n(t,d)/N(d)$):** Normalizza per la lunghezza del documento. Tutti i documenti con la stessa frazione di occorrenze avrebbero lo stesso punteggio.
*   **Max ($\text{TF}_{\text{max}}(t,d)$):** Normalizza per la frequenza massima del termine nel documento.
*   **Logarithmic ($\text{TF}_{\text{log}}(t,d) = \log(1+n(t,d))$):** Smorza la crescita della frequenza, come già visto.
*   **Fraction ($\text{TF}_{\text{frac}}(t,d; k) = n(t,d) / (n(t,d) + k)$):** Introduce un guadagno marginale decrescente. Mentre il logaritmo cresce all'infinito, queste funzioni tendono a saturare verso 1. Il parametro $k$ influisce sulla pendenza di questa saturazione (come mostrato nel grafico della slide).
*   **BM25:** Una delle funzioni più avanzate e popolari, basata su un **paradigma probabilistico**