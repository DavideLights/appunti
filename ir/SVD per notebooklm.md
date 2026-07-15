Ecco una versione riscritta, ripulita e strutturata dei tuoi appunti. Ho corretto le imprecisioni matematiche (come la confusione tra diagonalizzazione e SVD, o la regola di inversione di $U$) e riorganizzato i concetti in modo logico.

Questo formato è perfetto per essere caricato su **NotebookLM**: i concetti sono definiti in modo netto, le formule sono precise e la struttura gerarchica aiuterà l'IA a generare domande e risposte estremamente coerenti.

# Latent Semantic Indexing (LSI) e Decomposizione a Valori Singolari (SVD)

## 1. Prerequisiti di Algebra Lineare

### Autovalori e Autovettori

- **Definizione:** Sia $S$ una matrice quadrata. Se vale la relazione $S v = \lambda v$ (con $v \neq 0$), allora:
    
    - $v$ è un **autovettore** di $S$.
        
    - $\lambda$ è l'**autovalore** associato a $v$.
        
- **Significato geometrico:** Applicare la trasformazione lineare $S$ al vettore $v$ non ne cambia la direzione, ma ne modifica solo la lunghezza (la scala) di un fattore $\lambda$.
    
- **Normalizzazione:** Un vettore si dice normalizzato (ha lunghezza unitaria, pari a $1$) quando viene diviso per la sua norma euclidea ($L_2$):
    
    $$\Vert{}v\Vert{} = \sqrt{v_1^2 + v_2^2 + \dots + v_n^2}$$
    

### Proprietà delle Matrici

- **Matrice Simmetrica:** Una matrice quadrata $S$ è simmetrica se è uguale alla sua trasposta ($S = S^T$). I valori speculari rispetto alla diagonale principale sono identici.
    
- **Ortogonalità:** Due vettori sono ortogonali se il loro prodotto scalare è nullo ($v_1 \cdot v_2 = 0$). Geometricamente sono perpendicolari, il che significa che sono linearmente indipendenti e non hanno "sovrapposizioni".
    
- **Matrice Ortogonale ($Q$):** Una matrice le cui colonne sono vettori ortonormali (ortogonali tra loro e di lunghezza unitaria). Per queste matrici, l'inversa coincide semplicemente con la trasposta:
    
    $$Q^T = Q^{-1} \implies Q Q^T = I$$
    
- **Matrice Positiva Semidefinita:** Una matrice simmetrica i cui autovalori sono tutti non-negativi ($\lambda \geq 0$).
    
- **Proprietà di $A A^T$ e $A^T A$:** Per qualunque matrice $A$ (anche non quadrata), le matrici quadrate $A A^T$ e $A^T A$ sono sempre **simmetriche** e **positive semidefinite** (quindi i loro autovalori sono sempre $\lambda \geq 0$).
    

### Diagonalizzazione (Decomposizione Spettrale)

Ogni matrice simmetrica $S$ può essere diagonalizzata (decomposta) sfruttando i suoi autovettori e autovalori:

$$S = Q \Lambda Q^T$$

- $Q$ è la matrice ortonormale degli autovettori (quindi $Q^T = Q^{-1}$).
    
- $\Lambda$ è la matrice diagonale contenente gli autovalori sulla diagonale principale.
    

_(Nota di correzione: Se in un esercizio specifico gli autovettori non sono normalizzati, vanno divisi per la loro norma, che spesso è $\sqrt{2}$ nei sistemi 2x2, per rendere la matrice $U$ ortogonale e poter fare $U^{-1} = U^T$. In generale, per invertire una matrice ortogonale basta trasporla, senza dividere per due)._

## 2. Latent Semantic Indexing (LSI)

### Obiettivo di LSI

LSI (Latent Semantic Indexing) mira a superare i limiti del modello a spazio vettoriale classico (dove i documenti sono indicizzati solo per parole chiave esatte). LSI costruisce una matrice iniziale $A$ di dimensioni $m \times n$ (**Termini $\times$ Documenti**), dove:

- **Righe ($m$):** Rappresentano i termini unici del vocabolario.
    
- **Colonne ($n$):** Rappresentano i singoli documenti della collezione.
    
- **Celle $A_{i,j}$:** Contengono il peso (es. TF-IDF o frequenza) del termine $i$ nel documento $j$.
    

### Applicazione di SVD (Singular Value Decomposition)

Poiché la matrice $A$ ($m \times n$) è rettangolare, non possiamo usare la semplice diagonalizzazione spettrale (riservata alle matrici quadrate). Usiamo quindi la **SVD**:

$$A = U \Sigma V^T$$

La scomposizione mappa la matrice originale in uno spazio di **concetti (o dimensioni) latenti**:

1. **Matrice $U$ ($m \times m$):** Matrice ortogonale delle colonne. Rappresenta lo **spazio dei termini**.
    
    - Le colonne di $U$ sono gli autovettori di $A A^T$ (matrice di co-occorrenza dei termini).
        
    - Associa ciascun termine del dizionario alle dimensioni latenti.
        
2. **Matrice $\Sigma$ ($m \times n$):** Matrice diagonale rettangolare.
    
    - Contiene sulla diagonale i **valori singolari** $\sigma_i = \sqrt{\lambda_i}$ ordinati in modo decrescente ($\sigma_1 \ge \sigma_2 \ge \dots \ge 0$).
        
    - Ciascun $\sigma_i$ indica quanta informazione (varianza) cattura quella specifica dimensione latente.
        
3. **Matrice $V^T$ ($n \times n$):** Trasposta della matrice ortogonale $V$. Rappresenta lo **spazio dei documenti**.
    
    - Le colonne di $V$ (righe di $V^T$) sono gli autovettori di $A^T A$ (matrice di similarità dei documenti).
        
    - Associa ciascun documento alle dimensioni latenti.
        

## 3. Approssimazione a Basso Rango (Low-Rank Approximation)

LSI riduce il rumore del linguaggio troncando la scomposizione SVD. Invece di usare tutte le dimensioni, si mantengono solo le prime $k$ dimensioni latenti (tipicamente $100 < k < 300$).

$$A \approx A_k = U_k \Sigma_k V_k^T$$

- **Teorema di Eckart-Young:** La matrice $A_k$ di rango $k$ è la migliore approssimazione possibile della matrice originale $A$. È la matrice $X$ di rango $k$ che minimizza la **Norma di Frobenius** dell'errore di ricostruzione:
    
    $$\min_{X: \text{rank}(X)=k} \Vert{}A - X\Vert{}_F$$
    
    - La _Norma di Frobenius_ misura la discrepanza complessiva (l'errore) tra la matrice originale e quella approssimata.
        
- **Fattore di informazione conservata:** La quantità di informazione (energia) catturata dalle prime $k$ dimensioni rispetto all'originale si calcola come:
    
    $$\text{Info}_k = \frac{\sum_{i=1}^{k}\sigma_i^2}{\sum_{i=1}^{\min(m,n)} \sigma_i^2}$$
    

### Effetti della scelta di $k$:

- **$k$ troppo piccolo:** Perdita eccessiva di dettagli e informazioni fondamentali.
    
- **$k$ troppo grande:** Si mantiene il rumore di fondo del testo e ci si riavvicina alla matrice sparsa originale (perdendo il vantaggio semantico).
    
- **$k$ ottimale:** Rimuove il rumore e fa emergere le relazioni semantiche profonde. Ad esempio, nella matrice ricostruita $A_2$, celle che prima erano $0$ possono assumere valori positivi. LSI ha "capito" una relazione indiretta (es. due parole sono correlate anche se non compaiono mai nello stesso documento, perché compaiono in documenti simili).
    

## 4. Rappresentazione nello Spazio Latente e Query Projection

Nello spazio latente a $k$ dimensioni, possiamo rappresentare termini e documenti in modo omogeneo per confrontarli.

### Convenzione di Rappresentazione Simmetrica

Per poter visualizzare o confrontare termini e documenti direttamente (sfruttando le proprietà geometriche), si distribuisce l'effetto dei valori singolari $\Sigma_k$ equamente (elevando a $1/2$) su entrambe le componenti:

$$A_k = (U_k \Sigma_k^{1/2}) (\Sigma_k^{1/2} V_k^T) = T_k D_k$$

- **Coordinate dei Termini ($T_k$):** $T_k = U_k \Sigma_k^{1/2}$ (dimensione $m \times k$)
    
- **Coordinate dei Documenti ($D_k$):** $D_k = \Sigma_k^{1/2} V_k^T$ (dimensione $k \times n$)
    

In questa forma simmetrica, la ricostruzione di un elemento della matrice $A_k(t, d)$ è semplicemente il prodotto scalare tra il vettore del termine $t$ e il vettore del documento $d$ nello spazio ridotto:

$$A_k(t,d) \approx \langle T_k(t), D_k(d) \rangle$$

### Proiezione di una Nuova Query ($q$)

Una query di ricerca originaria $q$ (vettore colonna $m \times 1$, o riga $q^T$ di dimensione $1 \times m$) deve essere proiettata nello stesso spazio semantico ridotto per poter essere confrontata con i documenti indicizzati in $V_k^T$:

$$q_k = q^T U_k \Sigma_k^{-1}$$

- **Perché si fa così?**
    
    1. $q^T U_k$ proietta la query sulle $k$ direzioni semantiche principali definite dallo spazio dei termini.
        
    2. Moltiplicare per $\Sigma_k^{-1}$ normalizza le coordinate dividendo per l'importanza (valore singolare) di ciascuna dimensione semantica.
        
- Una volta ottenuto il vettore coordinato della query $q_k$, si calcola la **Cosine Similarity** tra $q_k$ e i vettori colonna di $V_k^T$ (o $D_k$) per trovare i documenti più rilevanti.
    

## 5. Impatto Linguistico e Performance

### Soluzione ai Problemi del Linguaggio

1. **Sinonimia:** Parole diverse con lo stesso significato (es. _PC_ e _computer_). Nella matrice originale $A$ sono trattate come indipendenti. Nello spazio LSI, poiché co-occorrono con gli stessi termini di contorno, vengono proiettate vicine nello spazio dei concetti latenti.
    
2. **Polisemia:** Una parola con più significati (es. _banca_). LSI riduce l'ambiguità perché la rappresentazione del documento tiene conto del contesto semantico globale (le altre parole presenti nel documento forzano la proiezione verso la dimensione latente corretta).
    

### Effetto sulle metriche di Information Retrieval (IR)

- **Recall (Richiamo) $\uparrow$ Aumenta:** LSI trova documenti rilevanti anche se non contengono le parole esatte della query, grazie alle relazioni semantiche trovate nello spazio latente.
    
- **Precision (Precisione) $\downarrow$ Invariata o Peggiora:** A causa dell'approssimazione (specialmente se $k$ non è impostato in modo ottimale), LSI può creare associazioni semantiche errate o "forzate", portando a galla documenti non pertinenti (falsi positivi).
    
- **Dizionari Piccoli:** Applicare LSI su collezioni di testo troppo piccole o con poche parole uniche è sconsigliato, poiché l'approssimazione rischia di tagliare via termini rari ma cruciali, degradando le performance.