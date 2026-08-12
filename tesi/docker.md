**proprieta dei container**:
* self-contained: ogni container ha tutto cio che gli serve per funzionare. Non dipende dalle dipendenze della macchina host.
* **isolate**: interferenza minima col sistema operativo.
* indipendenza: tra container su stesso host
* portabilita: eseguono ovunque allo stesso modo
## eseguire i container
**isolated containers**: eseguono i processi.

**cosa e' un container**? un processo in esecuzione su un host locale o remoto. Il processo nel container esegue con il suo file system, la sua rete e il suo process tree

**strutturalmente, cosa e' un container**? Un Docker container e' un immagine leggera, standalone, che contiene un pacchetto software con tutto il necessario per la sua esecuzione.
* **per "necessario" si intende**: codice, runtime, tool di sistema, librerie, impostazioni specifiche
* **da immagine a container**: l'esecuzione di un immagine genera il container.

**a che serve?** il container permette di creare ambienti riproducibili, indipendentemente dall'infrastruttura.

**Tipi di docker engine**:
* **standard**
* **lightweight**: i container condividono tutti lo stesso kernel.Non c'e' bisogno di un sistema operativo per container.
* **Secure**: piu isolazione del container

![docker containerized appliction blue border 2](https://www.docker.com/app/uploads/2021/11/docker-containerized-appliction-blue-border_2-376x300.png "- docker containerized appliction blue border 2")![container vm whatcontainer 2](https://www.docker.com/app/uploads/2021/11/container-vm-whatcontainer_2-376x300.png "- container vm whatcontainer 2")

**Container**: astrazioni a livello applicativo, forniscono codice pacchettizzato e dipendenze insieme.
* **condivisione os kernel**: piu container condividono lo stesso kernel. i processi dei container sono isolati in userspace. **VELOCE**
* **Struttura**: Docker parla con il sistema oeprativo host

**VM**:
* **ogni macchina un kernel**: una VM include una copia completa di un sistema operativo, di cui bisogna fare il boot. **LENTO**
* **struttura**: Le macchine virtuali parlano con l'hypervisor, "bypassando" il sistema operativo.

## immagini

**proprieta**:
* **immutabili**: l'immagine non cambia
* **layer**: le immagini dei container sono fatte di layer. Ogni layer aggiunge, rimuove o modifica file


## docker compose 
**best practice**: tanti container che fanno una cosa bene

**problema**: anche se non seguo la best practice... come gestisco tanti container?
* come eseguo rapidamente un sistema fatto di piu container?


**docker compose**: definisco le caratteristiche dei container in un file YAML e poi con un solo comando posso eseguire e collegare i container!

**tool dichiarativo**: docker compose e' dichiarativo. Non devo fare nulla da 0, piuttosto, faccio modifiche ed eseguo ` docker compose up`

**docker file**: da istruzioni per costruire un singolo container a partire dall'immagine.

**compose file**: definisce i container in esecuzione.

## system container
**cosa sono**? simili alle vm, ma la struttura rimane quella di un container.

**LXC**: e' l'implementazione di un system container, basato su linux.
* genera sia system container che container applicativi
* **infatti**: docker era basato su LXC

**conseguenza del system container**: eseguo un'intero sistema operativo condividendo il kernel dell'host. I processi eseguono 

**LXD**: gestore di system container e macchine virtuali che esegue sopra LXC.
* implementa REST API
* supporta container E MACCHINE VIRTUALI
