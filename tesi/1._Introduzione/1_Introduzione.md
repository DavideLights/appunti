Nel lavoro di tesi vogliamo gestire una competizione CTF (Capture The Flag).

Di solito in una competizione CTF, uno o più utenti (eventualmente organizzati in team) si sfidano per risolvere un insieme di challenge, ossia recuperare una **flag**: una stringa del tipo `{hai_trovato_la_flag}`.

Le CTF hanno lo scopo di migliorare la formazione degli specialisti del settore, tramite la simulazione di scenari realistici, complessi o quantomeno molto specifici. In particolare è essenziale formare studenti e risorse aziendali per la gestione e mitigazione di sistemi vulnerabili, in modo da prevenire perdite dovute ad attacchi informatici in scenari reali. La simulazione di questi scenari avviene all'interno di un ambiente denominato Cyber Range.

Ci concentreremo nel lavoro in un tipo di competizione CTF, basato sulla gestione di uno o più sistemi vulnerabili da mitigare, dunque una competizione di Difesa dove la flag si ottiene unicamente difendendo il sistema, ossia *"patchando"* la vulnerabilità. Nel lavoro si tiene conto di due requisiti da soddisfare:
* Il sistema vulnerabile spesso potrebbe essere costituito da uno o più host/nodi che comunicano tra di loro. 
* Il Cyber Range dovrebbe essere in grado di determinare in autonomia e senza interferire con i giocatori, lo stato della macchina.

Per soddisfare tali requisiti abbiamo sviluppato *BlueAgent*, un orchestratore basato sulla tecnologia dei container che implementa il Cyber Range di cui abbiamo bisogno per gestire competizioni di Difesa. BlueAgent si occupa di verificare che le vulnerabilità presenti sui container siano state corrette, tramite un sistema di verifica che avviene completamente all'oscuro dei giocatori, ossia la clonazione dei container in un ambiente separato.

Per valutare l'efficacia della soluzione proposta, l'architettura è stata validata misurando i tempi di esecuzione e assorbimento delle risorse (CPU e memoria RAM) al crescere del numero dei team e dei container istanziati.