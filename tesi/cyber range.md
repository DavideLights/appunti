caso del comune in cui vado a fare una CTF.

**assumiamo**: linux

**obiettivo**: sviluppare una piattaforma per il patching delle vulnerabilita
* step 1: identificare la vulnerabilita
* step 2: patchare
* sistema che verifica che il sistema sia patchato
* voglio solo controllare il tempo massimo per patchare

verificare che la patch non sia stupida:
* verificare servizio sia raggiungibile
* serivizio utilizzabile

**scenario**: 
* macchina controllore: carico gli scenari
	* gli collego le challenge da controllare
	* metodo strutturato per definire degli scenari per la macchina controllore.
	* dashboard!
	* stato: patchato ma non disponibile, patachato e disponibile.

architettura: 
* **controller**: centralizzato
* **macchina**: ogni macchina ha un servizio che comunica con i controller.

https://github.com/ctfd/ctfd
* attacco difesa (?)
* challenge dove devo sia attaccare che difendermi (?)
* due macchine identiche, due team.
* LA BASE PER ESTENDERE

https://github.com/domysh/ctfbox/tree/main/gameserver/checkers
* qui ci sono challenge di tipo attacco e difesa.
* qui si trovano i sistemi che verificano
* assumono che i servizi siano binari e che hai accesso al sorgente
* ma nel nostro caso non e' detto!

cosa devo fare:
* partire da ctfd
* estenderlo per il patching
* ispiriamoci ctfbox


ingegneria software: 
programmazione web: loreti