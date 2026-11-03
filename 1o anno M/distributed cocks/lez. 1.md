
**D1**: cosa descrive $\Pi$? come si comporta $n$?: (system, fixed)
* **R1**: describes a distributed system. $n$ is fixed and $\Pi=\{ p_{0},. ..,p_{n-1} \}$. a process could be anything: thread, host, pearson.
**D2**: cosa decsrive $G:(\Pi,E)$? (assume complete)
* **R2**: describes a communication graph, where $E$ represents all the possible links between processes. we assume it to be complete, otherwise messages might have to travel between more nodes.
**D3**: how do you model a process? (input, output, state)
* **R3**: a process is made of input and output related to the real word and a state representing its memory. It is an **infinite** state machine
**D4**: what does the state represent and what it's made of? (memory,buffer)
* **R4**: the state represents the memory of the process, including the input buffer (what i've received from other processes) and the output buffer (what's scheduled to be sent to other processes) 
**D5**: why do you need an output buffer? 
* **R5**: because sending a message ($\text{Exec}$) only puts it in $\text{OutBuf}$ (in-flight); delivering it to $\text{InBuf}$ is a separate asynchronous event ($\text{Del}$) scheduled by the adversary. #gemini
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

# intro
**distributed system**: set of **separate entities**, each with **computational power**, that **communicate** and **coordinate** to achieve a **common goal**. #gemini

> "A distributed system is one in which the failure of a computer you did not even know existed can render  your own computer unusable" Leslie Lamport.

**distributed systems are complex**: coordinating entities is hard due to: #gemini
* **asynchrony**: no global clock, message delays are unbounded, non-constant. #gemini
* **failures**: uncertain; requires failure detection, masking, tolerance, or recovery. #gemini
* **local view**: each process only sees its own local state and messages. #gemini

# model: system and concepts
**system**: $n$ processes (qualsiasi cosa, computer, thread, una persona) in $\Pi : \{ p_{0},p_{1},\dots,p_{n-1}  \}$
* $n$ e' fissato (static network), non cambia
* $p_{i}$ e' il processo che ha come identita $i$ (distinta). $i$ puo' essere un IP o un MAC addr per esempio.

**modellazione**: $G: (\Pi, E)$, communication graph.
* $E$: **communication links**, tipo internet o qualsiasi altra cosa.
* **complete**: tutti i nodi sono collegati agli altri.
* **se non fosse complete**: per mandare messaggi avrei bisogno di inoltrare i messaggi tra piu processi.

**process**: 
* every process is a (possibly infinite) state machine (I/O Automaton). #gemini
* **input**: e' il modo in cui il processo prende informazioni dall'esterno (upper layer).
* **output**: e' il modo in cui il processo comunica con l'esterno (upper layer).
* **ha uno stato**: la sua memoria interna e il contenuto del buffer input e buffer output
	* **buffer input** ($\text{InBuf}$): e' il buffer in cui i processi ricevono messaggi dal link
	* **buffer otuput** ($\text{OutBuf}$): contains "in-flight" messages. Those that are created and sent but still not delivered. 
		* **adversary**: the scheduler acts as an adversary. He chooses when to deliver to the input buffer of the receiver.
	* **link**: it's where processes messages travel
* **Layer**: il processo e' visto a layer IO <-> PROCESS <-> BUFFER IO

![[Pasted image 20260928195503.png]]

**formalizzazione processo**:
* $Q$: **insieme di stati interni**
* $Q_{\text{in}} \subseteq Q$: insieme stati iniziali possibili
* $M$: insieme di messaggi possibili $<\text{sender, receiver, payload}>$
* $\text{InBuf}_{j}$: multinsieme di messaggi ricevuti, consumati nel prossimo local step ($\text{InBuf}_{j} = \emptyset$ dopo lo step)
* $\text{OutBuf}_{j}$: multinsieme di messaggi "in-flight" (inviati ma non consegnati).
* **transizione**: $P_j(q \in Q, \text{InBuf}_j) = (q' \in Q, \text{Send\_msg} \subset M)$, con $\text{OutBuf}_j = \text{OutBuf}_j \cup \text{Send\_msg}$ e $\text{InBuf}_j = \emptyset$. #gemini

> non esistono processi con stato iniziale identico, almeno differiscono in identità (IP addr, MAC addr, e altre cose).

# model: asynch executions
* **no concept of time**, non ci sono bound sul ritardo dei messaggi o sul tempo di esecuzione. #gemini
* an action executes in an unpredictable amount of time.
* unpredictable does not mean slow.

**Evento**: un avversario, ossia lo **scheduler**, decide cosa succede sui processi schedulando eventi:
* $\text{Del}(i,j,m)$: muovi il messaggio $m$ da $\text{OutBuf}_{i}$ in $\text{InBuf}_{j}$
* $\text{Exec}(i)$: il processo $i$ esegue uno step del suo automa (consuma $\text{InBuf}_{i}$, aggiorna lo stato $q \to q'$, aggiunge eventuali messaggi inviati a $\text{OutBuf}_{i}$). #gemini

![[Pasted image 20260928195612.png]]

**configuration** ($C_t$): e' un vettore di $n$ componenti che rappresenta lo stato globale del sistema allo step $t$. Il componente $j$ rappresenta lo stato del processo $j$: $C_t[j] = (q_j, \text{InBuf}_j, \text{OutBuf}_j)$. 

$$
C_{0} = (<q_{0}, \{  \}, \{  \}>, <q_{1}, \{ m \}, \{  \}>, <q_{2}, \{  \}, \{  \}>)
$$

**abilitazione degli eventi**: $e$ e' abilitato nella configurazione $C$, se in quella configurazione può accadere:
* $\text{Del}(i,j,m)$ e' abilitato in $C$ solo se $m \in \text{OutBuf}_i$ (e' impossibile consegnare qualcosa se i buffer in output sono tutti vuoti).
* $\text{Exec}(i)$ (local execution) e' sempre abilitato.

![[Pasted image 20261103113532.png]]
**execution** ($\mathcal{E}$): e' un'infinita sequenza alternata di configurazioni ed eventi $(C_0, e_0, C_1, e_1, C_2, e_2, \dots)$ dove $e_{t}$ e' abilitato in $C_{t}$ e $C_{t}$ si ottiene applicando $e_{t-1}$ su $C_{t-1}$.
* $e_{0} = \text{Exec}(1)$, for example, move $m$ in process 1 from InBuffer to OutBuffer
* $e_{1} = \text{Del}(1,2,m')$
* **scheduler**: decides $e_{i}$

**space time diagram**:
* una riga orizzontale per ogni processo
* una riga verticale tratteggiata per ogni configuration $C_t$
* **asincronia**: i messaggi hanno ritardi arbitrari e possono arrivare fuori ordine (nella slide $m''$ inviato in $e_{2}$ viene consegnato in $e_{9}$, dopo il messaggio inviato in $e_7$). #gemini

![[Pasted image 20260928195705.png]]

* we apply $e_{0}$ to $C_{0}$: send $m'$ from $p_{1}$ to $p_{2}$
* we apply $e_{1}$ to $C_{1}$: deliver $m'$, now $p_{2}$ received $m'$
* apply $e_{2}$ to $C_{2}$: send $m''$ from $p_{2}$ to $p_{0}$
* $m''$ is delivered only with $e_{9}$, decided from the scheduler.

**fair execution**: if every process $p_{i}$ exectues an infinitely many amount of local steps and every message is eventually delivered using $\text{Del}(i,j,m)$.
* **infinitely many local steps**: every processes are always exectued by the scheduler. its not possible that after a certain point in the exectuion the process is never exectuted.
* **eventually**: it will happend, but we don't know when

**fairness**: senza fairness lo scheduler può impedire il progresso isolando processi o non consegnando mai messaggi.
* **example**: does exists a process holding a 1?
	* if the only process holding a 1 is nevere scheduled
	* then we cannot solve the problem correctly

**local execution (local view)**: $\mathcal{E}|p_{j}$ e' la sotto-sequenza di **eventi** in $\mathcal{E}$ che riguardano $p_{j}$ (nel loro ordine originale). #gemini
* $\mathcal{E}|p_{1}= (\text{Del}(0,1,m),\dots)$


![[Pasted image 20261103114909.png]]

**indistinguishability**: #gemini
* esecuzioni globali diverse possono produrre la stessa local execution per un processo: se $\mathcal{E}|p_1 = \mathcal{E}'|p_1$, allora $p_1$ **non può distinguere** $\mathcal{E}$ da $\mathcal{E}'$ (anche se il timing globale degli eventi è diverso, localmente vede la stessa sequenza). #gemini
* $\mathcal{E}$ ed $\mathcal{E}'$ sono **indistinguibili** se $\forall p_j \in \Pi, \; \mathcal{E}|p_j = \mathcal{E}'|p_j$. #gemini
* **Theorem**: in un sistema asincrono è impossibile ricostruire l'esatta esecuzione globale. #gemini

