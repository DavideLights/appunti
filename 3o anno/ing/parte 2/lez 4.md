**documento wsdl**: e' un documento XML che descrive **l'interfaccia pubblica** di un WebService e le **modalita di invocazione**. E' un **istanza** di un **metamodello WSDL** che descrive tutti i port *type e i loro binding*.

**port type**: e' **l'interfaccia**, in*sieme di operazioni raggruppate e fornite su un end-point di rete*. Simile ad un modulo.

**bindings**: *lega il port-type ad un particolare protocollo con il suo formato di dati*, per erogare il servizio in rete attraverso un **URI**. E' un oggetto vero e proprio o una relazione.

**Q-WSDL**: *lightweight **extension** per QoS su WSDL*. Aggiunge informazioni riguardo la qualità del servizio, arricchisce WSDL negli aspetti che di base non copre senza modificare la struttura base di un documento WSDL.

**meta modello**: viene usato per descrivere un documento WSDL. E' un modello che descrive altri modelli.

**qos profile**: un profilo e' un **meccanismo di estensione standard** di un modello, in questo caso orientato alla **qualita del profilo**.

**qos charatteristic**: ogni caratteristica raggruppa delle **qos dimension** che vanno misurate.

**XMI**: standard per scambiare informazione di metadati. Trasforma un modello/diagramma a classi in una rappresentazione XML.

**applicazione di q-wsdl**: 
* specificare qos requirements
* specifica service level agreements in ambito di rete (cosa riesco garantire secondo quanto descritto)

## REST
**rest**: Representational state transfer. **Descrive uno stile architetturale** di rete.

**restful api**: una api basata su risorse che usa HTTP.

**caratteristica**:
* client-server
* **interfaccia uniforme**: faccio accesso a tutte le risorse usando le operazioni base di HTTP.
* **nomi delle risorse**: identificata dall'URL
* **cache**: posso fare caching delle risposte

**risorsa**: qualsiasi entita' e' una risorsa (dai servizi, alle pagine, ai documenti). Rappresentazione basata su **XML**. Accedo alla risorsa usando il suo **URI** e con una richiesta HTTP.

**collection**: insieme di item.
**item**: oggetto in una collezione.

**POST e GET**: per ottenere lista di item o creare nuovi item.

**es compagnia aerea**:
* **cosa voglio fare**: offrire diversi tipi di servizio a seconda del tipo di utente
* **approccio 1**: un'unico URL per accedere al servizio
* **approccio 2 con rest**: ho 3 risorse differenti per i 3 tipi di membri della compagnia aerea.

**single apporach (sbagliato)**: 
* **unico** URL. 
* **arriva una richiesta**: il server deve capire da che tipo di utente arriva la richiesta e reindirizzarla al servizio giusto.
* **single point of failure**
* **assioma 0**: violato

**approccio rest**:
* **ogni tipo di client ha il suo url**
* **single point of failure**: non c'e'!
* **assioma 0**: consistente.
* **url autoesplicativo**: guardando l'url so che servizio ho richiesto.

# pattern di transazione 
**transaction pattern**: e' una richiesta client to service che e' costituita di una sequenza di operazioni che devono essere tutte eseguite in ordine.

**ACID**: Atomicita, Consistenza, Isolazione e Durabilita.

**two phase commit protocol**: *amtbio dei bonifici*. 3 entita:
* **first bank service**: da chi trasferisco i soldi
* **second bank service**: dove trasferisco i soldi
* **coordinator**: arbitro centralizzato

**prima fase**: 
1. **invia** `prepareTo commit`: arbitro manda il segnale ai service
2. **ricevo**: ogni servizio fa il `lock` dei dati
3.  **invia** `readyTo commit`: ogni servizio invia il messaggio all'arbitro

**seconda fase**:
1. **invia** `commit`: arbitro manda il segnale ai service
2. **ricevo** `commit`: i servizi fanno `unlock`
3. **invia**: `commit completed` i servizi mandano  al coordinatore.

**compound transaction pattern**: 
* **sottotransazioni**: una transazione divisa in piu sottotransazioni.
* ***errore**: in caso di errore devo fare un **rollback parziale**, perche' le sotto transazioni sono indipendenti tra loro.

**long living transaction**: split della transazioni in modo tale da considerare l'**human loop**. Devo attendere l'intervento umano, dunque la *transazione puo' durare molto tempo*.
* **esempio**: transazione per riservare un posto fino a quando non acquisto l'oggetto.

**negotiation pattern**: il cliente fa una proposta, deve essere valutata ed eventualmente negoziata per arrivare al successo.
* **client agent**:
	* **propose service**: propone un servizio al service. ed e' negoziabile
	* **request service**: richiede un servizio specifico
	* **reject service**
* **service agent**:
	* **offer service**
	* **reject/accept request/proposal**.

**cosa e' un servizio**? può essere un volo dove non posso negoziare la data. oppure posso negoziare la destinazione.

**orchestrazione servizi**: un controller **centralizzato** coordina più servizi
**coreografo**: come orchestrazione ma **decentralizzato**. 