
## laboratorio
**offset**: e' un valore che viene sommato alla portante.
**dbpsk**: e' un sistema di comunicazione non coerente, dunque non richiede sincronizzazione tra chi trasmette e chi riceve. per decodificare, interpreto il segnale comparando il simbolo corrente con il precedente.

**obiettivo laboratorio**: ascoltare e decodificare del testo inviato come ascii utilizzando dbpsk.

**offset 2500**:
![[Pasted image 20260603151958.png]]
* e' simmetrico
* me e' spostato dopo lo 0
* e la costellazione e' strana

**offset 3500**:
![[Pasted image 20260603152232.png]]

**offset 4500**:
![[Pasted image 20260603152254.png]]

**costellazione**:
![[Pasted image 20260603152021.png]]

## decodifica del messaggio ricevuto
### `recover_text_Part1_V2.m`

**CODICE: ottenere la fase dei campioni**:
* `sig = yout.signals.values(1:600,1,20)` estrae i primi 600 campioni.
* `phase = angle(sig(1:200));` calcola la fase dei primi 200 campioni
* **grafico 1**: viene mostrata la fase in radianti campione per campione. lavorando con DBPSK mi aspetto valori vicini a $\pi$ e $-\pi$, tutta via le imperfezioni del canale disturbano la fase che campiono. 
![[Pasted image 20260619010904.png]]


**complex envelope** $z(t)$: e' la rappresentazione del segnale in due parti
* $I(t)$ in fase
* $jQ(t)$ in quadratura

**dbpsk**:
$$
z(t)= A(t) \cdot m(t)
$$
* $A(t)$ ampiezza del segnale
* $m(t) \in \{+1,-1  \}$ e' il messaggio modulato in banda base

**estrarre la parte real del segnale**:
$$
s(t) = \mathrm{Re} \{ z(t) \cdot \exp(j_{2}\pi f_{c} t) \} = \mathrm{Re} \{ A(t) \cdot m(t) \cdot \exp(j_{2}\pi f_{c} t) \} 
$$
$$
s(t)=A \cdot m(t) \cdot \cos(2 \pi f_{c} t)
$$
**significa che**:
* se $m(t)=1$, allora $s(t)=A \cos(2\pi f_{c}t)$, ossia corrisponde alla portante con ampiezza positiva
* se $m(t)=-1$, allora corrisponde alla portante con ampiezza negativa.
* Inoltre, moltiplicare il segnale con $-1$ equivale ad effettuare un salto di $180\degree$ in fase.

**errore di fase costante**: 
* **quando avviene**? se l'oscillatore locale e' sfasato di $\phi$ rispetto al trasmettitore
* **cosa comporta**? sulla costellazione i punti ruotano, ma guardando entrambe le componenti (I e Q), posso determinare che simbolo ho ricevuto.

**errore di frequenza**:
* **quando avviene**? se sono sfasato anche in frequenza
* **cosa comporta**? sulla costellazione ottengo un anello completo e non distinguo piu i simboli $\pm 1$

**dbpsk e gli errori**: e' vantaggioso utilizzare dbpsk perche'
* moltiplicare due simboli **cancella la differenza di fase**
* la differenza di fase tra due simboli consecutivi $\sim 0$

**CODICE: calcolare la differenza di fase**
* `phase_diff = sig(2:end) .* conj(sig(1:end-1));` per ottenere la differenza di fase tra un campione ed il precedente.
* se la differenza di fase e' positiva vuol dire che il simbolo trasmesso non e' cambiato
* se la differenza e' negativa vuol dire che ho cambiato simbolo.
![[Pasted image 20260619014604.png]]

**CODICE: decodificare**
* se `rxBits = real(phase_diff) < 0;` vuol dire che ho un bit 1, altrimenti e' 0.
### `recover_text_Part2_V2.m`

**cross correlation**
* `xcorr(rxBits, pre);` calcola la `cross correlation` tra il vettore dei bit ricevuti e il preambolo.
* ossia: faccio scorrere il preambolo su tutti i bit, e vedo quanti di questi coincidono
* **picco**: la funzione restituisce un picco quando molti bit coincidono

il resto del codice si occupa dell'estrarre 32 caratteri dopo il preambolo identificato al passo sopra, e di convertirli in testo ascii.

![[Pasted image 20260619020708.png]]

# esperimenti
**Devo fare**: analisi spettro, costellazione, fase raw, bit ricevuti, ricerca preambolo sugli esperimenti, decodifica testo.

**Nota**: A causa di un qualche problema con l'antenna non ho registrato bene il segnale, nonostante fossi vicino al trasmettitore. ho ottenuto segnali e costellazioni molto diverse dai miei compagni.

**Nota**: durante il laboratorio, per confusione, ho provato a decifrare il messaggio utilizzando uno script scritto da Gemini.
## esp 1
![[Pasted image 20260608162341.png]]
![[Pasted image 20260608162400.png]]
![[Pasted image 20260608164131.png]]

**Tuttavia**: avrei dovuto ricevere un segnale molto disturbato e con una costellazione a cerchio. E' possibile che qualcuno stesse attuando un'attacco di tipo **overshadowing** dato il preambolo era leggibile.
## esp 2
![[Pasted image 20260608164402.png]]
![[Pasted image 20260608164516.png]]
![[Pasted image 20260608164654.png]]

**tuttavia**: il segnale dovrebbe essere molto più disturbato di prima, ed e' impossibile captare tutti i preamboli.
## esp 3
![[Pasted image 20260608165545.png]]
![[Pasted image 20260608165626.png]]

**Tuttavia**: in questo esperimento, l'attaccante e' riuscito a sincronizzarsi sul preambolo di chi trasmetteva, e ha trasmesso a potenza maggiore un messaggio contraffatto. L'obiettivo dell'attaccante e' dunque quello di fare overshadowing.