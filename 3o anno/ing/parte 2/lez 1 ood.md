# Object Oriented Design
**OOD**: e' una fase che consiste di
* **preliminary OOD**: definisce la strategia per costruire la soluzione al problema.
* **detailed OOD**: definire le classi e le associazioni da implementare. Classi, strutture dati e metodi.

**Sviluppo incrementale**: il modello **OOA** (Obj Oriented Analysis) viene trasformato in **OOD** aggiungendo dettagli su come si implementa il software.

## Architettura di sistema
**architettura di sistema**: definisce la struttura dei componenti software e le loro relazioni.

**Evoluzione delle architetture**:
* Mainframe-based
* **File sharing**: non distribuisce l'esecuzione ma mette a disposizione dispositivi alla rete.
* Client Server
* Distributed Objetcs
* Component-Based
* Service-oriented

**sistema software distribuito**: Client Server, Distributed Objects, Component-Based, Service-oriented. Il calcolo e' distribuito su piu macchine.

## sistemi software distribuiti
**sistema software distribuito**: esecuzione distribuita su insieme di host indipendenti.

**Set di independent execution hosts**: appare all'utente come un'unica risorsa di esecuzione.

**Middleware**: livello che nasconde la complessita del calcolo distribuito. Funziona come **interfaccia** *tra livello applicativo e livello del sistema operativo*, fondamentale nella transizione verso il calcolo distirbuito. 

**Controllo del traffico su strada**: esempio di sistema distribuito su macchine remote. Comunicano tra di loro con un'interfaccia middleware.

**Feature dei sistemi distribuiti**:
* **condivisione risorse**: *non sono piu associate ad una singola macchina ma a disposizione di tutti*. Anche tra sistemi operativi differenti, faccio interagire tra loro **sistemi eterogenei**.
* **Concorrenza**: 
* **Bilanciamento del carico**: distribuisco il carico su piu host, evito i colli di bottigla.
* **Tolleranza ai guasti**: se va giu un host ne ho altri disponibili.
* **Scalabilita**: posso aggiungere nodi di esecuzione, per gestire sovraccarichi
* **Trasparenza**: la trasparenza e' rispetto a come funziona il sistema distribuito e cosa vede l'utente di questo sistema.

**Fattori critici**:
* **sicurezza**: troppi messaggi su rete vulnerabili.
* **qualita del servizio**: se la richiesta viene consumata da un servizio remoto e' difficile predire l'affidabilità e il tempo di esecuzione, ci sono molti fattori in mezzo.

## Client/Server
**client**: processo con interfaccia utente che raccoglie le sue richieste, e manda le richieste al server.

**server**: *oppure insieme di server*, che esaudisce le richieste.

**Stratificazione dell'applicazione in layer**:
* ***Presentation Layer**: mostra risultati e raccoglie input.
* ***Application processing Layer**: logica applicativa.
* ***Data Management Layer**: gestisce accesso ai dati.

**Due Architetture C/S**:
* **thin-client**: il server fa tutti e 3 i layer.
* **fat-client**: il client fa Presentation e Application Processing. Il server fa Data Management.
* **three-tier**: client fa Presentation, un Server fa Application Processing (intermedio tra client e altro server) e un'altro Server fa Data Management. **Piu' scalabile**.

**Internet Banking a three-tier**:
* **client**: tramite HTTP fanno richieste al Web Server utilizzando una pagina web.
* **Web Server**: fa application processing e gestisce l'accesso al conto corrente (la logica)
* **Database Server**: contiene i database con i conti correnti.

## Distributed Object Architectures
**Client e Server**: nessuna distinzione.
**DO (Distributed Objects)**: sono sia client che server.
**Comunicazione tra DO**: comunicazione remota tramite middleware attraverso un **bus software**, ossia **object request broker**:
* **bus astratto**: specifica dell'interfaccia per comunicazione e data exchange services.
* **implementazione del bus**: implementazione del bus in base a software e hardware. es: **corba**

**Applicazioni basate su DO**: oggetti che eseguono su piattaforme eterogenee e comunica tramite **invocazione di metodi remota**.

**Oggetti**: hanno dei metodi che possono essere chiamati remotamente. Questi oggetti si trovano su client differenti e definiti su **linguaggi differenti** ma *possono comunicare usando il bus*.


## Component Based Architectures
**CBA**: definisci prodotti software assemblati da componenti software che lavorano insieme come un **component framework**.

**Component Framework**: usa architetture software generiche per realizzare applicazioni. E' una collezione di software preesistente arrangiato per risolvere un problema.

**Black-Box reuse software**: voglio usare i componenti del framework conoscendone solo le specifiche. Do un input e ottengo risultato.

**plugs**: posso collegare i componenti attraverso le operazioni e le interfacce che mettono a disposizione.

**variabilita e adattabilita**: per comunicare i componenti devono essere variabili e adattabili nei parametri che posso fornire in input.

**Object vs Component**: 
* **Componente**: generalizzazione dell'oggetto, ma viene usato gia in fase di progettazione, dunque **prima del run time**. Non ha stato ma ha un'interfaccia per l'utilizzo. **E' generalemente software gia testato e che funziona bene.**
* **Oggetto**: ha stato e comportamento, definito da un linguaggio di progrmamazione ed **esiste solo a run time** quando istanziato.

**Come si sviluppa app con component framework**:
* Il framework mette a disposizione una Domain Knowledge ed un **Requirements Model**
* Devo mappare le richieste del problema al Requirement Model del framework.
* Il componente guida l'operazione di assemblaggio del sistema.



