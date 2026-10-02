![[Pasted image 20260807001314.png]]# 1. introduzione
**problemi superabili con progresso tecnologico**:
* **sono accidentali**
* teaming
* specifica e progetto
* manutezione
* attitudine

**ciclo di vita del software**:
* sviluppo:
	* requisiti
	* specifiche
	* pianificazione
	* progettazione
	* codifica
	* integrazione
* manutenzione
* dismissione

**verifica e validazione**:
* verifica = stiamo costruendo il prodotto nel modo giusto?
* validazione = stiamo costruendo il prodotto giusto?

**problemi non superabili col progresso tecnlogico**:
* **aspetti essenziali**
* complessita
* conformita: non risponde a **leggi fisiche universali**
* cambiabilita
* invisibilita

**Affidabilita**:
* informale
* formale: in termini di probabilita

**catena malfunzionamenti**:
* errore
* difetto
* guasto

# 2 processo software
**processo software**: attivita necessarie allo sviluppo entro i tempi previsti e caratteristiche di qualita.

**sviluppo**: due tipi di fasi
* fasi di definizione: "cosa"
* fasi di produzione: "come"

**manutenzione**:
* correttiva
* adattiva
* perfettiva
* preventiva

**build and fix**:
![[Pasted image 20260827180048.png]]

**waterfall**:
![[Pasted image 20260827180109.png]]
* $V\&V$: verifica e validazione 

![[Pasted image 20260827180140.png]] 
* **verifica**: riguarda consistenza interna
* **validazione**: conformita rispetto utente.

**rapid prototyping**: 
![[Pasted image 20260827180257.png]]
* come waterfall,ma inizio con prototipo rapido.

**prototipo**: riduce rischi sui requisiti.
* **vantaggi**: rilevamento precoce di incomprensioni, sistema funzionante in breve tempo, training utente e testing.
* **svantaggi**:
	* sicurezza e peculiarita
	* valore legale
	* prestazioni e affidabilita

![[Pasted image 20260827180432.png]]


**Throw-away prototyping**:
* sviluppa -> scarta
* **a che serve?** impressione del prodotto finito.
* **caratteristiche**:
	* non documentato
	* struttura degrada
	* bassa qualita

![[Pasted image 20260827180819.png]]
* **struttura**
	* prototipazione in alto
	* sviluppo in basso

**Programmazione visuale**:
* **prototipazione rapida**
* **problemi**:
	* coordinamento
	* architettura assente
	* dipendenze complesse

**iterazione/build**: serve per fornteggiare vari problemi
* **richiede**: architettura globale
* sperimentare
* prototipi

**iterazione con overall architecture**:
* requisiti - specifiche - design architetturale
* iterazione della build i-esima.
* puo' essere **parallelo/senza overall**

**costo dei build e di integrazione**: piu build $\equiv$ costo di entegrazione alto.

**modello incrementale vs cascata**: 
* continuo feedback
* parallelo
* + tema, di piccole dimensioni

**modello a spirale**:
* **analisi del rischio** -> step -> verifica
* **rapid prototype**: all'inizio

**il modello a spirale riduce il rischio**:
* **determinare** obitivi e alternative
* **valutare alternative**
* **pianificare** la prossima fase 

**metriche**: 
* **asse verticale** -> costo cumulativo
* **rotazione**: progresso nei vari step.