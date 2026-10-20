
Si presenta dunque l'architettura di *BlueAgent*, una piattaforma di Cyber Range in esecuzione come servizio *HTTP* che espone *API REST* per il deployment, la gestione del ciclo di vita e la verifica automatizzata delle challenge, a partire da definizioni dichiarative (*Infrastructure as Code*) predisposte dagli organizzatori della gara. Tali API REST possono essere consumate da un qualsiasi applicativo esterno denominato CTF Manager, come ad esempio un plugin per la piattaforma CTFd[^1].

Il Cyber Range implementato da BlueAgent è pensato per scenari di Patch Management da eseguire su un singolo host. Si propone di offrire un ambiente basato su container di sistema, che garantisca un meccanismo di verifica completamente inaccessibile ai concorrenti. Tale meccanismo si fonda sulla clonazione all'occorrenza dell'intera infrastruttura del team in una rete logica separata, sulla quale vengono eseguiti i comandi di verifica definiti dall'oracolo.

I membri di ciascun team possono connettersi alla rete dei container a loro assegnata mediante una VPN WireGuard, dove a ciascun partecipante corrisponde un peer dedicato (ossia, coppia di chiavi pubblica e privata).

È opportuno evidenziare che:
1. Gli indirizzi IP dei container all'interno della rete di produzione di ciascun team sono statici e noti a priori (il che si applica alla maggior parte delle challenge).
2. La duplicazione istantanea sfrutta le proprietà Copy-on-Write (CoW) del filesystem ZFS. Inoltre viene impiegata una rete SDN (Software-Defined Network) per orchestrare router e switch logici dedicati all'ambiente di verifica.
3. BlueAgent non mantiene lo stato della competizione (quali i punteggi o la classifica dei team), delegando tale responsabilità al CTF Manager. BlueAgent opera esclusivamente come un orchestratore specializzato che traduce le specifiche delle challenge in container da eseguire.

A scopo d'esempio, mostriamo ad alto livello come si crea una challenge:
1. Il creatore della challenge definisce tramite un file YAML i container. 
2. Il creatore della challenge, inserisce la nuova challenge tenendo in memoria tutte le informazioni necessarie a BlueAgent (inclusi i file dichiarativi)
3. Il giocatore di un determinato team accede alla challenge e tramite il CTF Manager richiede la creazione dei container.
4. BlueAgent si occupa di istanziare i container per il team.

BlueAgent è basato su *FastAPI*, per gestire in modo semplice ed efficiente le richieste HTTP. 

L'host su cui viene eseguito BlueAgent deve mettere a disposizione dell'architettura le seguenti componenti:
* **Debian 13**: o una qualsiasi distribuzione Linux.
* `nftables`: per filtrare i pacchetti nel kernel
* **Python 3**: per eseguire BlueAgent.
* **Pool ZFS**: filesystem che supporta il meccanismo `COW`.
* **OVN ed Open vSwitch**: per gestire la rete di verifica dei container.
* **Distrobuilder**: per generare le immagini dei container in modo dichiarativo.
* **WireGuard**: per fornire una VPN come punto d'accesso ai partecipanti
* **Incus**: per la gestione dei container.

Per comprendere passo-passo cosa permette di fare il sistema e come lo fa sono elencati gli attori, gli use cases ed i requisiti di sistema.

[^1]: CTFd LLC, *CTFd: Open Source Capture The Flag Framework*, https://ctfd.io/