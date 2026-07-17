**agenti risolutori di problemi**
* **architettura**: goal
* **come si raggiunge il goal**? algoritmo di ricerca
	* **alg. informato**: greedy search ed A* misurano quanto sono vicino al goal
	* **alg. non informato**: l'agente non conosce la distanza dal goal e deve esplorare tutte le soluzioni possibili con BFS, DFS, Uniform Cost.
* **rappresentazione stato**: atomica
	* **agente pianificatore**: usa stati strutturati
* **cosa fa nel codice**? pianifica e poi esegue, modello **open-loop** (anello aperto)

**in che tipo di problemi operano**?
- Episodici
- A singolo agente
- **Completamente osservabili**
- **Deterministici**
- **Statici** (non cambiano mentre l’agente pensa)
- **Discreti** (stati e azioni finite)
- **Noti** (modello di transizione conosciuto)

**agente risolutore in ambiente noto e deterministico**: devo pianificare e poi eseguo
* **se noto de deterministico** $\to$ so per ogni azione come sara' il mondo successivamente.
* **percezioni**: non mi servono mentre eseguo, devo solo conoscere la configurazione iniziale del mondo.
* **modello closed-loop** (anello chiuso): l'agente monitora le percezioni e si riadatta di continuo.

**quattro frasi per la risoluzione**:
* **formulare obiettivo**: cosa devo raggiungere?
* **formulazione problema**: modello stati, azioni, transizioni e costi.
* **ricerca**: calcola la sequenza di azioni
* **esecuzione**: esegui

## definizione formale
$$
\text{problema di ricerca } = <S,S_{0}, A, \text{Result}, \text{Goal, C}>
$$
* $S_{0}$: stato iniziale.
* $\text{Result}$: f. transizione $\text{Stato} \times \text{Azione} \to \text{Stato}$
* $\text{Goal}: \text{Stato} \to \{ \text{T,F} \}$:
* $\text{C}(s,a,s')$: costo per passare da s ad $s'$ usando l'azione $a$.

| #       | Componente                     | Descrizione                                                                                                                                                                                                                  |
| ------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1️⃣** | **Stato iniziale**             |                                                                                                                                                                                                                              |
| **2️⃣** | **Azioni possibili**           | La funzione **Azioni(s)** restituisce l’insieme finito di azioni eseguibili nello stato `s`.                                                                                                                                 |
| **3️⃣** | **Modello di transizione**     | Descrive come le azioni modificano lo stato del mondo.  <br>Formalmente: `Risultato(s, a) = s′` indica lo stato successivo ottenuto eseguendo l’azione `a` nello stato `s`.  <br>Es: `Risultato(Arad, VersoZerind) = Zerind` |
| **4️⃣** | **Insieme di stati obiettivo** | Contiene uno o più stati che soddisfano il goal dell’agente (le condizioni di successo).                                                                                                                                     |
| **5️⃣** | **Funzione di costo**          | La funzione `CostoAzione(s, a, s′)` (o `c(s, a, s′)`) assegna un valore numerico positivo al costo di eseguire `a` in `s` per raggiungere `s′`.  <br>Serve per confrontare soluzioni e trovare quella più economica.         |
* **sequenza azioni**: e' il cammino (path) che attraversa gli stati
* **soluzione**: e' un cammino che fa dallo stato iniziale ad uno stato obiettivo
* **soluzione ottima**: minimizza il costo totale delle transizioni
* **spazio degli stati**: e' un grafo
* **astrazione**: e' il modo in cui rappresentiamo la realtà nel nostro modello

| Tipo di astrazione    | Definizione                                                                                   | Utilità                                                         |
| --------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Astrazione Valida** | la soluzione nel nostro modello puo' essere **espansa** in quello reale                       | l'astrazione e' **corretta** ed applicabile nella **realta      |
| **Astrazione Utile**  | la soluzione nel nostro modello e' **piu' semplice computazionalmente rispetto alla realta** **semplificare la ricerca** e ridurre il costo computazionale. le. |

**problemi esemplificativi**:
* illustrare/mettere alla prova diversi metodi e algoritmi di risoluzione.
* astratti, semplificati e standardizzati
* giocattoli matematici, di utilità teorica
**problemi** **reali**:
* formulazione specifica e non standard.
* utilità pratica

## esempi

|Elemento|Descrizione|
|---|---|
|**Stati**|Ogni stato indica la posizione dell’agente e la presenza o assenza di sporco in ogni cella.  <br>In un mondo con `n` celle, ci sono `n × 2ⁿ` stati possibili.|
|**Stato iniziale**|Può essere qualunque configurazione iniziale di agente e sporco.|
|**Azioni**|`Sinistra`, `Destra`, `Aspira` (nel mondo a due celle).|
|**Modello di transizione**|`Aspira` rimuove lo sporco dalla cella; `Sinistra` e `Destra` spostano l’agente (se non ci sono muri).|
|**Stati obiettivo**|Stati in cui **tutte le celle sono pulite**.|
|**Costo di azione**|Tutte le azioni hanno **costo uniforme = 1**.|

|Elemento|Descrizione|
|---|---|
|**Stati**|Tutte le possibili configurazioni della scacchiera 3×3 con i numeri da 1 a 8 e una casella vuota.|
|**Stato iniziale**|Una configurazione specifica del puzzle.|
|**Obiettivo**|Configurazione ordinata (numeri da 1 a 8, casella vuota in basso a destra).|
|**Azioni**|Spostare la casella vuota **su, giù, destra, sinistra**.|
|**Goal test**|Verificare se la configurazione corrente corrisponde allo stato obiettivo.|
|**Costo del cammino**|Costo uniforme (ogni mossa = 1).|
|**Spazio degli stati**|Molto ampio, può contenere cicli; adatto a testare efficienza degli algoritmi.|

|Formulazione|Descrizione|Spazio di ricerca|
|---|---|---|
|**Incrementale 1 (base)**|Si aggiungono regine una per volta su qualunque casella.|~1.8 × 10¹⁴ sequenze (molto grande).|
|**Incrementale 2 (migliorata)**|Si aggiunge una regina per colonna, assicurandosi che non minacci le precedenti.|Solo 2057 stati (molto più efficiente).|
|**A stato completo**|La scacchiera contiene 8 regine (una per colonna) e si spostano finché non sono tutte non minacciate.|Usata in algoritmi di ricerca locale (es. _Hill Climbing_).|

| Elemento                   | Descrizione                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Stati**                  | Includono posizione (aeroporto), ora corrente e altre informazioni storiche (es. tratte, tariffe, voli precedenti). |
| **Stato iniziale**         | L’aeroporto di partenza dell’utente.                                                                                |
| **Azioni**                 | Prendere un volo disponibile dopo l’ora corrente, rispettando i tempi di trasferimento.                             |
| **Modello di transizione** | Lo stato successivo aggiorna la posizione e l’orario di arrivo del volo.                                            |
| **Stato obiettivo**        | Aeroporto di destinazione desiderato.                                                                               |
| **Costo dell’azione**      | Combinazione di fattori: costo del biglietto, tempo, durata, coincidenze, dogane, qualità del posto, ecc.           |

## algoritmi di ricerca

**albero di ricerca**: e' l'insieme degli stati esplorati dall'algoritmo
* **frontiera**: separa i nodi generati (interi) da quelli non ancora espansi (esterni)
* **coda**: implementa l'estrazione dei nodi dalla frontiera, FIFO, LIFO, PRIOR.
* **strategia di scelta**:
	* **FIFO** $\to$ **BFS**
	* **LIFO** $\to$ **DFS**
	* **Coda Priorita** $\to$ Uniform Cost, Greedy, $A^*$.

**Algoritmi informati**:
* **funzione euristica** : $h(c)$.
* **esempi**: greedy search ed $A^*$.

**Analizzare un'algoritmo di ricerca**:
* **completezza**: trova sempre una soluzione se esiste?
* **ottimalita**: trova sempre la soluzione migliore?


**fattori**:
* $b =\text{ branch factor}$
* $d = \text{max depth della soluzione}$
* $m = \text{ lunghezza max della soluzione }$

**BFS**: guarda e tiene in memoria tutti i nodi
* $O(b^d)$
* **completezza**: e' sempre completo
* **ottimo**: se e solo se i nodi hanno costo unitario
* **tempo e spazio**: $O(b^d)$.
	* **tempo**: $T(b,d) = b + b^2 + \dots + b^d = O(b^d)$
	* **spazio**: per visitare i nodi li devo tenere in memoria, $O(b^d)$

**UC**: e' BFS generalizzato quando i costi non sono unitari.
* **coda priorita**: scegli di espandere il nodo che minimizza $g(n)$
* **tempo e spazio**: $O(b^{1+ \lfloor   C^*/\epsilon\rfloor})$
	* $C^*$ e' il costo della soluzione ottima
	* $\epsilon$ e' il costo minimo di un'azione.

**azioni con costo 0**: in UC potrebbero generare loop!!!!

**DFS**: espando prima il nodo piu profondo della frontiera
* **tempo**: $O(b^{m+1})$
* **spazio**: $O(bm)$
* **depth limited**: limito a $l$ la depth.
* **non ottimo**: se per esempio $C$ e' soluzione ottima ma contiene $C'$ all'interno del suo sottoalbero. Allora DFS vista prima $C'$

**Backtracking search**: e' DFS ma ogni nodo si ricorda quale deve generare successivamente, richiede solo $O(m)$ memoria.

**diametro**: nomero di azioni massime per adare da uno stato all'altro.

**Ricerca Bidirezionale**:
* esplora simultaneamente a partire dallo stato iniziale e a partire dalla fine
* **tempo**: $O(b^{d/2} + b^{d/2})$
* **spazio**: ho due frontiere, e due insiemi di stati raggiunt
* **quando si usa?** posso ragionare all'indietro e generare predecessori.
	*  obiettivo ben definito

**IDS**: Iterative Depth Search
* genera e guarda $db + (d-1)b^2 + (d-2)b^3 + \dots + b^d$ nodi

**Problema dei cicli**:
1. non tornare nello stato da cui si provivene
2. non andare verso un nodo che e' antenato
3. non generare nodi con stati gia visitati. si fa in costo lineare al numero di nodi visitati.

