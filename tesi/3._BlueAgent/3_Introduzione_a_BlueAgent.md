
Si vuole presentare dunque il nostro Cyber Range: *BlueAgent*. Un servizio *HTTP* che implementa delle *API REST* per la gestione e la verifica delle macchine a partire da file dichiarativi (*IaC*) fornite dagli organizzatori della CTF. Queste API REST potranno poi essere sfruttate ed implementate da un qualsiasi applicativo (denominato CTF Manager) per gestire le challenge, come per esempio, un plugin per CTFd[^1].

Il Cyber Range implementato da BlueAgent e' pensato per scenari di Patch Management da eseguire su un unico nodo con hardware "leggero". Dunque si vuole offrire un'ambiente basato su container (invece di utilizzare delle macchine virtuali pesanti) che offra un meccanismo di verifica completamente nascosto ai giocatori. Tale meccanismo e' basato sulla clonazione sul momento dell'intera infrastruttura interessata, in una rete separata e inaccessibile ai giocatori, su cui verranno poi eseguiti i comandi dell'oracolo definito in fase di dichiarazione.

I membri dei team, potranno connettersi alla rete dei container a loro assegnati utilizzando una VPN, implementata da WireGuard, tenendo presente che ogni membro avra' un peer associato (una coppia di chiavi pubbliche e private).

E' importante puntualizzare che:
1. Gli indirizzi IP dei container, nelle reti dei giocatori, saranno statici e noti a priori (questo scenario si applica alla stragrande maggioranza delle challenge)
2. Il meccanismo di duplicazione avviene sfruttando il meccanismo CoW di ZFS per abbattere il costo in memoria. Inoltre utilizzeremo una SDN per semplificare la gestione e la creazione di router e switch necessari ai container duplicati.
3. BlueAgent non mantiene in memoria lo stato delle challenge (per esempio i punteggi dei vari team). Questo software deve essere inteso come un'orchestratore di container. Blueagent si limita a prendere in input la definzione di una challenge e di istanziare i container richiesti.

A scopo d'esempio mostriamo come creare ed istanziare una challenge con BlueAgent:
1. Il creatore della challenge definisce in modo dichiarativo i container. 
2. Il creatore della challenge, inserisce nel CTF Manager la nuova challenge tenendo in memoria tutte le informazioni necessarie a BlueAgent (inclusi i file dichiarativi)
3. Il giocatore di un determinato team, accede alla challenge e tramite il CTF Manager richiede la creazione dei container
4. Il CTF Manager invia a BlueAgent i file di configurazione della challenge da istanziare
5. BlueAgent si occupa di istanziare i container per il team.

BlueAgent e' basato su *FastAPI*, per gestire in modo semplice ed efficiente le richieste HTTP. 

L'host su cui viene eseguito BlueAgent deve mettere a disposizione dell'architettura le seguenti componenti:
* **Debian 13**: o un qualsiasi distribuzione Linux.
* `nftables`: per filtrare i pacchetti nel Kernel
* **Python 3**: per eseguire BlueAgent.
* **Pool ZFS**: filesystem che supporta il meccanismo `COW`.
* **OVN ed Open vSwitch**: per gestire la rete di verifica dei container.
* **Distrobuilder**: per generare le immagini dei container in modo dichiarativo.
* **WireGuard**: per fornire una VPN come punto d'accesso ai partecipanti
* **Incus**: per la gestione dei container.

Per comprendere passo-passo cosa permette di fare il sistema e come lo fa sono elencati gli attori, gli use cases ed i requisiti di sistema.

[^1]: https://ctfd.io/