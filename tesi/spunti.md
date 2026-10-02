* [containerlab](https://github.com/srl-labs/containerlab)




# esempi di cyber range
kCTF

CyberPatrion (Air Force Association): i concorrenti ricevono un'immagine virtuale completa, compromessa su piu livelli. Un servizio interno alla macchina esegue ciclicamente controlli di stato confrontando la configurazione locale con delle specifiche crittografate.

Seth e WASC

EDURange: formazione, topologie complesse che richiedono analisi del traffico di rete. Il suo scopo sfora l'ambito della gestione di vulnerabilita.

KYPO Cyber range Platform

DARPA: la piattaforma di testing misurava l'efficacia delle patch binarie proposte tramite l'iniezione mirata di _Proof of Vulnerability_ (PoV) formali. L'oracolo verificava l'annullamento della vulnerabilità inviando contemporaneamente migliaia di _polls_ applicativi con transazioni lecite, penalizzando severamente qualsiasi patch che introducesse rallentamenti o un consumo di memoria ingiustificato

# architettura
1. casi d'uso
	1. creazione di una challenge
	2. gestione team
	3. gestione container
	4. gestione interfacce di rete
2. requisiti di sistema 
3. architettura agente produzione
4. architettura agente verifica

# argomenti di difesa
1. spiegare perche la combo wireguard + bridge L2 e' necessaria
2. spiegare perche l'approccio ibrido e' un ottimo compromesso
3. spiegare in quali ambienti e' ottimo blueagent

# limitazioni
* l'uso del bridge L2  limita la capacita di catturare il traffico all'interno della rete.
* massimo 254 team
* il meccanismo di verifica sotto carico potrebbe triggerare OOM
* cow snapshot inconsistenti in alcuni casi

# architetture alternative
1. shadow bridge per la verifica
2. shadow bridge con doppia interfaccia eth
3. network namespace separato per la verifica
4. pid namespace separato
5. libprocesshider
6. Esecuzione In-Memory con Mascheramento di `/proc`
7. verifica statica
8. verifica out of band

altre cose alternative
1. docker compose: does not support CoW on running container, does not integrate with ovn
2. virtual machine: too much memory

# todo
* controlla periodicamente se il servizio e' disponibile
	* controllo healt
	* invio di transazioni lecite al servizio
* ansible per configurare ancora meglio le challenge
* implementare docker come backend per gestire i container
* implement a cleaner utility (remove profiles, interfaces, containers ecc...)