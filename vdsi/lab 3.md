**frequency offset**: quando converto tra banda base e portante devo farla perfetta. ma questa conversione non viene fatta sempre in modo precisa

**sincronizzazione**: ci vuole dunque una sincronizzazione perfetta tra emittente e ricevente. idealmente abbiamo considerato che la conversione e' fatta con una sincronizzazione perfetta.
* devo sapere quando iniziano i simboli
* lo sfasamento della fase di chi trasmette
* questo crea problemi quando

**riassumendo**: devo conoscere perfettamente $f_{c}$ e $t$ nella modulazione/demodulazione

**trasmissione coerente**: richiede
* **synchronization** sulla portante
* devo conoscere il **timing** dei simboli (quanto dura la trasmissione di un bit)
* questi valori possono essere recuperati

**trasmissioni non coerenti**: per comunicare non richiedono la sincronizzazione porcaccio gesu

**differential phase-shift keying**: e' una tecnica non coerente.

**guarda la tabella**:
* $k$ istanti di tempo
* in sequenza i bit da trasmettere.
* $b_{k}$ e' lo stream da trasmettere
* $d_{k}$ e' la sequenza effettivamente trasmessa
* **come funziona**? ogni volta che in $b_{k}$ compare un 1 cambio il bit trasmesso in $d_{k}$ 

sia $z(t)=Am(t)$ un segnale BPSK:
* $R\{ z(t)\exp(j 2 \pi f_{c}t) \}$ 
* ...
* questa roba e' la codifica del messaggio in base al segnale
* codifico in +1 o -1


shifting in frequenza: se la $f_{c}$ non e' perfetta? ossia nella formula ho $f_{c} - \Delta t$
* uso l'**esponenziale** sulla slide per calcolare il coseno
* moltiplico questo esponenziale per il coseno

**shift in phase**: fa ruotare la costellazione
**shift sia in phase che in frequenza**: ottengo punti della costellazione distribuiti su un anello.

**oss**: 2 bit consecutivi hanno lo stesso $\Delta f$. riesco a ricostruire il segnale anche se i punti sono distribuiti ad anello sulla costellazione.

## laboratorio
se guardo lo spettro:
* e' simmetrico
* spostato dopo lo 0
* la costellazione e' strana

**offset 2500**:
![[Pasted image 20260603151958.png]]

**offset 3500**:
![[Pasted image 20260603152232.png]]

**offset 4500**:
![[Pasted image 20260603152254.png]]


![[Pasted image 20260603152021.png]]