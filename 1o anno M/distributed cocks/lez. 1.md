
**D1**: cosa descrive $\Pi$? come si comporta $n$?: (system, fixed)
* **R1**: describes a distributed system. $n$ is fixed and $\Pi=\{ p_{0},. ..,p_{n-1} \}$. a process could be anything: thread, host, pearson.
**D2**: cosa decsrive $G:(\Pi,E)$? (assume complete)
* **R2**: describes a communication graph, where $E$ represents all the possible links between processes. we assume it to be complete, otherwise messages might have to travel between more nodes.
**D3**: how do you model a process? (input, output, state)
* **R3**: a process is made of input and output related to the real word and a state representing its memory. It is an **infinite** state machine
**D4**: what does the state represent and what it's made of? (memory,buffer)
* **R4**: the state represents the memory of the process, including the input buffer (what i've received from other processes) and the output buffer (what's scheduled to be sent to other processes) 
**D5**: why do you need an output buffer? 
* **R5**: because sending a message does not mean to deliver it. (**why???**)
**D6**: how do you formalize a process?( $<Q,Q_{\_{}}, M>$)
**D7**: describe $\text{InBuf}_{j}$ and $\text{OutBuf}_{j}$. (step $j$)
**D8**: can two process have the same identical state? (id)
**D9**: characteristics of async execution. (time, unpredictable time)
**D10**: descrive the role of the scheduler. ($\text{Del}, \text{Exec}$, adversary)
**D11**: what is the configuration? (entire system)
**D12**: what's an execution? what does it mean for an event to be enabled? (infinite, sequence, scheduler)
**D13**: what's impossible to happen if output buffers are empty?
**D14**: describe the space time diagram
**D15**: what does it mean for a process to execute infinitely many local steps and for each $m$ to be delivered? (fair, always scheduled, it has to happen)
**D16**: why fairness is crucial? give an example (1's example)
**D17**: what is local execution? what it implies? (local execution, extend)
# model: system and concepts
**system**: $n$ processes (qualsiasi cosa, computer, thread, una persona)in $\Pi : \{ p_{0},p_{1},\dots,p_{n-1}  \}$
* $n$ e' fissato, non cambia
* $p_{i}$ e' il processo che ha come identita $i$. $i$ puo' essere un IP o un MAC addr per esempio.

**modellazione**: $G: (\Pi, E)$, communication graph.
* $E$: **communication links**, tipo internet o qualsiasi altra cosa.
* **complete**: tutti i nodi sono collegati agli altri.
* **se non fosse complete**: per mandare messaggi avrei bisogno di inoltrare i messaggi tra piu processi.

**process**: infinite state machine.
* **input**: e' il modo in cui il processo prende informazioni dall'esterno.
* **output**: e' il modo in cui il processo comunica con l'esterno
* **ha uno stato**: la sua memoria interna e il contenuto del buffer input e buffer output
	* **buffer input**: e' il buffer in cui i processi ricevono messaggi dal link
	* **buffer output**: a che serve? potrebbe essere che il messaggio venga inviato ma non posso inviarlo subito, quindi lo metto in coda nel buffer output
		* qualcun'altro preleva il messaggio dal buffer e lo mette nel link.
	* **link**: it's were processes travel
* **Layer**: il processo e' visto a layer IO <-> PROCESS <-> BUFFER IO

![[Pasted image 20260928195503.png]]

**formalizzazione processo**: robba inuile
* $Q$ **insieme di stati interni**, e' un'insieme che conosciamo a priori
* $Q_{\text{\_}}$ insieme stati iniziali possibili
* **Messages**: insieme di messaggi possibili $<\text{sender, receiver, payload}>$
* $\text{InBuf}_{j}$: multinsieme di messaggi ricevuti consumati nel prossimo local step
* $\text{OutBuf}_{j}$: multinsieme di messaggi inviati ma non consegnati.

> non esistono processi con stato iniziale identico, almeno differiscono in identità (IP addr, MAC addr, e altre cose).

# model: asynch executions
* **no concept of time**
* un'azione richiede un tempo **non prevedibile** per eseguire.
* non previdible non vuol dire lento.

**execution**: e' una storia del sistema che esegue un algoritmo.
* la storia include la memoria e i messaggi ricevuti ed inviati

**Evento**: un avversario, ossia lo scheduler decide cosa succede sui processi, scatenando eventi ??? Tipi di eventi:
* $\text{Del}(i,j,m)$: muovi il messaggio m da $\text{OutBuff}_{i}$ in $\text{InBuff}_{j}$
* $\text{Exec}(i)$: il processo i esegue uno step nella sua macchina a stati finiti.

![[Pasted image 20260928195612.png]]

> **tempo e' discreto**: che cazzo vordi???

**configuration**: e' un vettore di $n$ componenti che rappresenta lo stato del sistema. il componente $j$ rappresenta lo stato del processo $j$. 

$$
C_{0} = (<q_{0}, \{  \}, \{  \}>, <q_{1}, \{ m \}, \{  \}>, <q_{2}, \{  \}, \{  \}>)
$$

**abilitazione degli eventi**: $e$ e' abilitato nella configurazione $C$, se in quella configurazione potrebbe accadere.

> e' impossibile ricevere qualcosa se i buffer in output sono tutti vuoti

* local execution e' sempre abilitata

**execution**: e' un infinita sequenza di configurazioni ed eventi dove $e_{t}$ e' abilitato in $C_{t}$ e $C_{t}$ si ottiene applicando $e_{t-1}$ su $C_{t-1}$.
* $e_{0} = Exec(1)$
* $e_{1}=Del(1,2,m')$
* ecc...
* **scheduler**: decide gli eventi $e_{i}$

**space time diagram**:
* una riga per ogni processo
* una riga verticale per ogni configuration
* $e_{0}$ avviene dopo $C_{0}$
* $e_{0} \to e_{1}$ e' il tempo per eseguire $e_{1}$
* **asincronia**: i messaggi arrivano a cazzo di cane e possibilmente fuori ordine. nella slide $e_{2}$ arriva molto dopo, scatenando $e_{9}$.

![[Pasted image 20260928195705.png]]

**fair execution**: se ogni processo esegue infinitely many local steps ed ogni messaggio viene eventualmente consegnato con $\text{Del}(i,j,m)$
* **infinitely many local steps**: vuol dire che tutti i processi devono essere schedulati, sempre. non e' possibile che un processo dopo un po di tempo non venga più schedulato.
* **eventualmente**: vuol dire che succederà, ma non so quando.

**fairness**: se isolo i processi e non li schedulo mai, potrebbe succedere che messaggi importanti non vengano mai consegnati dallo scheduler. Quindi lo scheduler deve essere fair.
* **esempio**: esiste un processo con un 1? se l'unico processo con un 1 non viene schedulato, allora gli altri processi non possono conoscerne lo stato.

> **Local execution**: $E|p_{j}$ e' la sotto sequenza di eventi in $E$ che interferiscono con $p_{k}$
 * $\epsilon|p_{1}= (\text{Del(0,1,m),...})$

Quando arriva un evento $\text{Del(i,j,m)}$ allora $j$ conosce potenzialmente lo stato di $i$ fino al momento in cui $i$ ha inviato il messaggio.

> guarda l'esempio e giocaci con il cervelletto.

per local execution si intende il fatto che lo stato degli altri processi deve essere propagato porcaccio cristo.

guarda nella slide dopo le differenze tra i messaggi: quando arrivano, quando sono inviati.
* $p_{1}$ non puo' distinguere le due differenti esecuzioni, perche anche se il timing e' diverso vede le stesse cose.
* nemmeno $p_{2}$ puo' distinguere le due differenti esecuzioni
* scheduling diverso ma i processi vedono la stessa cosa.
* localmente non puoi capire cosa succede globalmente nello scheduling delle esecuzioni



