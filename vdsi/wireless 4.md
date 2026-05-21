**jammer**:
* **broad band**: spacco tutto
* **narrowband**: sacco uno specifica frequenza
* **spot jammer**: spacco uno specifico canale ed ha una durata temporale specifica per tracciarti.

apro il primo file su MATLAB
* bernoulli: generatore di numeri
* **BPSK**: trasforma i simboli in -1/+1
* Trasformazione: in forma d'onda rettangola.
* integrate and dump: fa l'integrale del segnale nel tempo
* **error rate**: prende l'ingresso in trasmissione ed in ricezione e calcola
	* total number of symbols
	* number of errors: errori in assoluto
	* error rate: errori sul totale

![[Pasted image 20260518165505.png]]
* gialla: in fase
* blu: in quadratura
* nel secondo grafico c'e' molto rumore
* nel terzo grafico campiono a pezzi e cerco di ricostruire l'originale
* calcolando l'integrale del segnale decido quanto e' potente e se e' 0 oppure 1.

bassquando SNR o: (es 10)
![[Pasted image 20260518170858.png]]

**quando aumento l'SNR** (es: pari a 40)
![[Pasted image 20260518170753.png]]

**diagramma ad occhio**:
![[Pasted image 20260518171258.png]]
* se l'occhio e' aperto allora tt ok!, riesco a ricostruire il segnale anche se c'e' qualcosa che non va

![[Pasted image 20260518171534.png]]
* occhio chiuso: rapporto segnale rumore

## Domanda 2.1
![[Pasted image 20260518172724.png]]

**la media**: $-0.000414638830\dots$. e' la potenza media del segnale in output dall'Ideal Rectangular pulse filter block. dove $\text{RMS}=1$,


## Lez 4.2!@#!@#%
**due tipi di link**:
 * punto-punto
 * broadcast

**collisione**: avviene quando due persone trasmettono allo stesso tempo sulla stessa frequenza.

**protocollo accesso multiplo**: algoritmo distribuito che determina come i nodi condividono lo stesso canale, senza usare altri canali per la coordinazione.


**idealmente vorrei che**:
1. se un nodo trasmette lo fa a velocita $R$
2. se $m$ nodi trasmettono lo fanno a $\frac{R}{m}$
3. decentralizzato
4. semplice

**tre modi per farlo nella realta**:
* **a turni**
* **random access**: mando i pacchetti e me ne frego delle collisioni
* **partizionamento canale**

**TDMA**: time division multiple access, ossia accesso a turni prestabili, divido il frame di tempo in slot in cui ogni utente puo' trasmettere.
* **problema**: spreco se gli slot non sono tutti utilizzati

**FDMA**: dividi spettro radio in bande di frequenze. ogni stazione radio ha la sua banda, ma spreco bande se rimangono inutilizzate. Funziona bene per le radio

**FDM**: frequency division multiplexing. ho tante piccole bande di frequenze divise da **guard bands**

**OFDM**: Orthogonal FDM.
* **segnale**: ha un massimo e punti di bassa energia dove si arriva a 0
* **sovrapposizione**: posso sovrapporre altri segnali nei punti di 0 dell'altro segnale.
* **guard bands**: qui non servono.


**resource block**: prendo tempo e frequenza ed assegno il quadratone come risorsa per trasmettere.

La base station assegna questi blocchi.

**CDMA**: code division. tutti gli utenti hanno un codice e lo usano per codificare i dati.
* ortogonalita: i codici devono essere ortogonali
* seq. chipping: e' il codice ortogonale.

b**anda alta $\equiv$ bit piu corti** da trasmettere e viceversa
* **banda larga** $\equiv$ mi comporto come rumore, difficile da individuare il mio segnale. copro una banda piu larga del jammer
* banda stretta: usa piu segnale, vengo sgamato e vengo scopato dal jammer.

DS-CDMA: direct seignal, ossia moltiplica il segnale originale per un codice

**FH-CDMA**: frequency hopping, non uso un codice, ma invece di trasmettere sempre alla stessa frequenza, salto di frequenza in frequenza. dunque il jammer l'ho inculato, perche' trasmette ad una frequenza fissa. ho bisogno di un codice che segnala agli altri che sto trasmettendo.
* faccio frequency hopping in base al codice, se sono ortogonali, nel tempo trasmettiamo tutti a frequenze diverse.

TH-CDMA: time hopping in base al codice. ad ogni frame cambio dove trasmetto (???)

## esperimento guidato deppefo
![[Pasted image 20260520150923.png]]
![[Pasted image 20260520151319.png]]
![[Pasted image 20260520151424.png]]![[Pasted image 20260520153129.png]]