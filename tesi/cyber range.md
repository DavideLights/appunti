**assunzione**: linux

**obiettivo**: sviluppare una piattaforma per il patching delle vulnerabilita. L'utente deve:
* **step 1**: identificare la vulnerabilita
* **step 2**: patchare la vulnerabilita tramite binary patching, gestione file di configurazione, ecc...
* **flag**: non esiste una flag da trovare. Si vince la sfida quando il servizio/sistema e' stato patchato.
* **caso esempio**: voglio controllare che l'utente esegua il patch di una macchina entro un certo limite e che lo faccia correttamente

**quali patch vanno bene**? non deve essere una patch scema, es:
* rimuovo il servizio
* blocco tramite firewall il servizio
* ecc...

**architettura**:
* macchina controllore: nodo centrale, su questa carico le configurazioni delle macchine challenge. E' fondamentale
	* **formato strutturato**: definire un formato JSON, o un linguaggio per definire le challenge
	* **dashboard**: su questa compare lo **stato** della challenge
		* **patchato ma non disponibile**
		* oppure, **patchato e disponibile**, e' il goal dello sfidante.
	* **verifica patch**: esegue l'exploit
* **macchina challenge**: ogni macchina ha un servizio che comunica con il controller


**ctfd**: e' il software per le CTF. Non supporta nativamente le ctf su patch.
* **Plugin CTFd**: dobbiamo inserire tramite python il supporto alle patch
* *"Verifica PATCH"*: dovra comparire nella pagina web il pulsante per verificare se la patch e' stata applicata correttamente.
* **Assegnazione del punteggio**: solo se il servizio viene patchato correttamente.


## CTFd
**REST API**: https://docs.ctfd.io/tutorials/api/using-ctfd-api