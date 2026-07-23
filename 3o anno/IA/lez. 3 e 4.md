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
	* $\text{Result} \equiv \text{Transizione}$
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

| Tipo di astrazione    | Definizione                                                                                                                                                     | Utilità                                                    |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Astrazione Valida** | la soluzione nel nostro modello puo' essere **espansa** in quello reale                                                                                         | l'astrazione e' **corretta** ed applicabile nella **realta |
| **Astrazione Utile**  | la soluzione nel nostro modello e' **piu' semplice computazionalmente rispetto alla realta** **semplificare la ricerca** e ridurre il costo computazionale. le. |                                                            |

**problemi esemplificativi**:
* illustrare/mettere alla prova diversi metodi e algoritmi di risoluzione.
* astratti, semplificati e standardizzati
* giocattoli matematici, di utilità teorica
**problemi** **reali**:
* formulazione specifica e non standard.
* utilità pratica

## esempi

| Elemento                   | Descrizione                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stati**                  | Ogni stato indica la posizione dell’agente e la presenza o assenza di sporco in ogni cella.  <br>In un mondo con `n` celle, ci sono `n × 2ⁿ` stati possibili. |
| **Stato iniziale**         | Può essere qualunque configurazione iniziale di agente e sporco.                                                                                              |
| **Azioni**                 | `Sinistra`, `Destra`, `Aspira` (nel mondo a due celle).                                                                                                       |
| **Modello di transizione** | `Aspira` rimuove lo sporco dalla cella; `Sinistra` e `Destra` spostano l’agente (se non ci sono muri).                                                        |
| **Stati obiettivo**        | Stati in cui **tutte le celle sono pulite**.                                                                                                                  |
| **Costo di azione**        | Tutte le azioni hanno **costo uniforme = 1**.                                                                                                                 |

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

# ricerca non informata

**albero di ricerca**: e' l'insieme degli stati esplorati dall'algoritmo
* **frontiera**: separa i nodi generati (interi) da quelli non ancora espansi (esterni)
* **coda**: implementa l'estrazione dei nodi dalla frontiera, FIFO, LIFO, PRIOR.
* **strategia di scelta**:
	* **FIFO** $\to$ **BFS**
	* **LIFO** $\to$ **DFS**
	* **Coda Priorita** $\to$ Uniform Cost, Greedy, $A^*$.

**nodo**: ha le seguenti informazioni
* stato
* $g(n)$
* padre, azione che lo ha generato

**Analizzare un'algoritmo di ricerca**:
* **completezza**: *trova sempre una soluzione se esiste*?
* **ottimalita**: *trova sempre la soluzione migliore*?
* $b =\text{ branch factor}$
* $d = \text{max depth della soluzione}$
* $m = \text{ lunghezza max della soluzione }$

> [!error] completezza
> Se un'algoritmo esplora tutto lo spazio degli stati senza mancarne uno e' per forza completo.

**(A) Algoritmo di ricerca su albero**:
![[Pasted image 20260717165914.png]]
* **inizializzazione**: vogliamo in frontiera lo stato iniziale.
* **idea**: scegli i nodi dalla frontiera, ed espandili, aggiungi i figli alla frontiera
	* **scegli**: non applichiamo un criterio particolare. scegliere, implica rimuovere dalla frontiera.

**(A) Algoritmo di ricerca** **dettagliato**:
![[Pasted image 20260717170557.png]]
* **inizializzazione**: effettua il `Test-Obiettivo` sul nodo iniziale.
* **frontiera vuota**: se non ho trovato ancora una soluzione allora indica un fallimento
* **iterazione**: per ogni azione possibile su `nodo.stato` genera il figlio corrispondente, effettua `Test-Obiettivo` ed eventualmente metti in frontiera.
* `Test-Obiettivo`: verifica se il lo stato in input e' un'obiettivo

**(A) ricerca su grafo**: rispetto alla ricerca su albero, devo evitare i cicli!
* un grafo ammette cicli a differenza dell'albero.

**(A) BFS**: guarda e tiene in memoria tutti i nodi
* $O(b^d)$
* **completezza**: e' sempre completo
* **ottimo**: se e solo se i nodi hanno costo unitario
* **tempo e spazio**: $O(b^d)$.
	* **tempo**: $T(b,d) = b + b^2 + \dots + b^d = O(b^d)$
	* **spazio**: per visitare i nodi li devo tenere in memoria, $O(b^d)$
* **pesudocodice**: si trova sotto!!!
* **QUAL'E' IL PROBLEMA**? *USA TROPPO SPAZIO*

**(A) UC**: e' BFS generalizzato quando i costi non sono unitari.
* **coda priorita**: scegli di espandere il nodo che minimizza $g(n)$
* **tempo e spazio**: $O(b^{1+ \lfloor   C^*/\epsilon\rfloor})$
	* $C^*$ e' il costo della soluzione ottima
	* $\epsilon$ e' il costo minimo di un'azione.
* e' un'algoritmo di tipo best first

![[Pasted image 20260717171056.png]]

**azioni con costo 0**: in UC potrebbero generare loop!!!!

**(A) DFS**: espando prima il nodo piu profondo della frontiera
* **tempo**: $O(b^{m+1})$
* **spazio**: $O(bm)$
* **depth limited**: limito a $l$ la depth.
* **non ottimo**: se per esempio $C$ e' soluzione ottima ma contiene $C'$ all'interno del suo sottoalbero. Allora DFS vista prima $C'$
* **pesudocodice**:  identico a bfs ma cambia il tipo di coda.

**(A) Backtracking search**: e' DFS ma ogni nodo si ricorda quale deve generare successivamente, richiede solo $O(m)$ memoria.

**diametro**: numero di azioni massime per adare da uno stato all'altro.

**(A) Ricerca Bidirezionale**:
* esplora simultaneamente a partire dallo stato iniziale e a partire dalla fine
* **tempo**: $O(b^{d/2} + b^{d/2})$
* **spazio**: ho due frontiere, e due insiemi di stati raggiunti
* **quando si usa?** posso ragionare all'indietro e generare predecessori.
	*  obiettivo ben definito

**(A) IDS**: Iterative Depth Search. DFS iterata con $l$ incrementale
* genera e guarda $db + (d-1)b^2 + (d-2)b^3 + \dots + b^d$ nodi
* **Rispetto a DFS e BFS**: e' completo ed **OTTIMO**, ed usa **meno spazio di BFS**

**Problema dei cicli**:
1. non tornare nello stato da cui si provivene
2. non andare verso un nodo che e' antenato
3. non generare nodi con stati gia visitati. si fa in costo lineare al numero di nodi visitati.

**(A) Implementare la soluzione del problema dei cicli**:
![[Pasted image 20260717172226.png]]

![[Pasted image 20260717172255.png]]
* **perché eseguo `TestObiettivo` quando estraggo dalla frontiera**? perche' potrei la frontiera mi garantisce l'estrazione del nodo con costo minimo..
# ricerca informata

**Ricerca non informata**: l'agente esplora tutto lo spazio degli stati mentre ricerca, ma non sa quale strada lo "avvicina di piu alla soluzione"
* **obiettivo**: ridurre lo **spazio di ricerca**

**(A) Best first**: e' tree search o graph search dove seleziono i nodi in base a $f(n)$
* **funzione di valutazione**: $f(n)=g(n)$, ossia il path-cost
* **che vuol dire best first**? e' una categoria di algoritmi tra cui rientra Uniform Cost
* **Uniform Cost**: e' best first con $f(n)=g(n)$
* **greedy best first**: e' best first con $f(n)=h(n)$
![[Pasted image 20260717174203.png]]

**(A) greedy best first**: e' best first dove $f(n)=h(n)$, ossia guarda solo l'euristica.
* **IN GENERALE: non e' completo**, **non e' ottimale**
* **euristica**: $f$ incorpora **solo** l'euristica $h$, che stima la distanza dallo stato $n$ al goal.

**euristica**: $h(n)$
* **oracolo**: $h(n) = h^*(n)$
* **teorema dominanza**: se $h_{1}(n) \leq h_{2}(n)$ per ogni nodo $n$
	1. i nodi espansi con $h_{2}$ sono un sottoinsieme di $h_{1}$
	2. $A^*$ con $h_{2}$ e' efficiente almeno quanto $h_{1}$ 
	3. **cosa vuol dire**? piu $h$ approssima l'oracolo, e meno nodi vengono esplorati.
* quando $h(n)$ e' buona?
	* $N+1 = 1+b^* + {b^*}^2 + \dots + {b^*}^d$
	* $b^*$: ad ogni livello espando pochi nodi.

##### Compromesso: costo dell’euristica vs costo della ricerca
- Un’euristica **semplice** è veloce da calcolare ma fa esplorare molti nodi.
- Un’euristica **precisa** riduce la ricerca ma può essere costosa da valutare.

**inventare euristica**:
* **rilassamento**: inventa una versione rilassata per sottostimare la distanza dal goal.
* **massimizza**: se hai piu euristiche valide, prendi quella che massimizza l'euristica
* **sottoproblemi**: pre-calcola i sottoproblemi e usali per l'euristica
* **combinazione lineare**: incorpora piu euristiche pesandole.

**(A)** $A^*$ : usa $f(n) = g(n)+h(n)$
* **completezza**: se e solo se $g(n) \geq d(n) \cdot ε$.
	* **cicli**: e' impossibile incastrarsi in cicli.
* **ottimale**: non e' detto.
* $A \text{ vs} A^*$: $A^*$ e' $A$ dove l'euristica $h$ deve rispettare delle proprieta
	* $h(\text{goal}) = 0$
	* $h(n) \geq 0$
	* **AMMISSIBILITA**: $h(n) \leq h^*(n)$, altrimenti potrebbe scartare la soluzione ottima prematuramente e trovarne un'altra peggiore
	* **monotonia e consistenza**: $h(n) \leq c(n,a,n') + h(n')$. Proprieta piu forte che serve nei grafi.
* $\Delta = h^*-h$
* **tempo**: $O(b^\Delta)$
* **spazio**: $O(b^{\Delta+1})$

```scss
function A* (problem) returns a solution or failure
nodo <- nodo con stato = problem.initialstate
frontiera <- coda di priorità ordinata in base a f(n) con all inizio solo nodo "nodo"
esplorati <- insieme dei nodi esplorati inizialmente vuoto
loop do
    if frontiera is empty? then return failure
    nodo <- POP(frontiera)
    if problem.GOALTEST(nodo.state) then return SOLUTION(nodo)
    add nodo.state to esplorati
    for each action in problem.ACTIONS(nodo.state) do
        child <- CHILD-NODE(problem, nodo, action)
        if child.state non in frontiera or esplorati then
            frontiera <- INSERT(child.state)
        else if child.state is in frontiera con f(n) più alto allora
            replace that frontier node with child
```

**(A)** $SMA^*$: se sto riempiendo la memoria (o comunque ho impostato un limite), allora rimuovo il nodo peggiore dalla frontiera e lo sostituisco con uno migliore trovato.
* **completezza**: se e solo se ho abbastanza memoria per calcolare la soluzione

**(A) Beam Search**
![[Pasted image 20260717183111.png]]
* **completezza**: non lo e'
* **idea**: per tutti i nodi nella `open` list, espandili e mettili nei `Beam-Candidate`
	* **espansione**: espandere un nodo vuol dire spostarlo dalla `open` alla `close` list
	* **scegliere dai candidati**: prendi i migliori $w$ nodi nella lista `Beam-Candidate` e mettili in `open`
* **riassunto semplice**: nella frontiera tengo i migliori $w$ nodi visti fino ad ora.

**(A)** $IDA^*$: e' come Iterative Deep Search
* **come limito la ricerca**? espando i nodi con $f(n) \leq f_{\text{limit}}$
* **come aggiorno** $f_{\text{limit}}$ quando fallisco la ricerca? per esempio, lo aggiorno con il valore $f(n)$ minimo che supera $f_{\text{limit}}$ che ho osservato nell'ultima iterazione di $A^*$.
* **tempo**: come $A^*$
* **spazio**: $O(b \cdot d)$