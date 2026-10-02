# creazione team
**requisiti**: una cartella locale nel server che contiene le configurazioni wireguard

**Azioni**:
1. crea l'interfaccia wireguard `wg-k`, e metti a disposizione la configurazione per il download
	1. genera la configurazione e mettila in una cartella
2. crea l'interfaccia bridge `br-team-k`
# creazione container patch
**Azioni**:
1. identifica quale sia il bridge di rete del team `k-esimo`
2. aggancia a questo bridge i container specificati nello `yaml` in input.
	1. per ogni `container` nello `yaml`:
		1. verifica se esiste l'immagine, altrimenti creala prendendo il file da `distrobuilder[container]`
		2. crea il containery
		3. esegui il container imponendo i `limits` specificati nel file `yaml`

# verifica

**Azioni**:
1. cattura  `POST /teams/{id}/challenges`
2. duplica configurazione dentro bridge di verifica
	1. snapshot dei container
	2. duplicazione
	3. **se neessario**: aggiungi interfaccia `eth1` ai container.
		1. nello `yaml`, `internet-access=True`?
	4. **se fornito**: crea il container `verify` a partire dalla configurazione `distrobuilder`
	5. restore/esegui i container
		1. blueagent deve aspettare che i container siano **ready**
			1. per ogni comando nello `yaml`, leggi e aspetta che esegua con successo entro un certo `timeout`
		2. bleuagent esegui **comandi di verifica** via incus exec sui vari host
			1. per ogni comando nello `yaml`, eseguilo. se esiste un comando che fallisce nell'esecuzione, allora la verifica fa caca.
	6. distruggi i container ed il container `verify` se era richiesto
3. distruggi il bridge di verifica 

**perche il container `verify` non e' obbligatorio**?
* **scenario 1**: e' già disponibile un macchina nella challenge da utilizzare come verifier (es: un client vulnerabile)
* **scenario 2**: la challenge mette a disposizione un server vulnerabile, ma non un client ed e' necessario un client esterno al server per l'exploit.

## esecuzione comandi di verifica/readyness
**Azioni**:
1. per ogni comando specificato dall'utente
	1. esegui il comando sul container specificato: potrebbe essere eseguito su verify, oppure no


