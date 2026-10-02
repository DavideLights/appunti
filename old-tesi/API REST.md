**API**: meccanismo che permette a un'applicazione/servizio di accedere a risorse all'interno di un'altra applicazione/servizio/database


**API REST**: posso usare questo stile architetturale per implementare la mia API in qualsiasi linguaggio
* **requisito**: limiti di progettazione REST, *vincoli architetturali*

**REST**:
* **interfaccia uniforme**: *le richieste per la stessa risorsa, sono della stessa forma* indipendentemente da chi fa la richiesta.
	* **dunque**: dunque non ci devono essere piu richieste per la stessa risorsa.
* **disaccoppiamento client/server**: in API REST, *il client non sa nulla del server*. conosce solo l'interfaccia, dunque gli URL da usare per fare le richieste. *Il server non modifica il client mandando dati tramite richieste HTTP*
* **memorizzazione in cache**: *bisognerebbe memorizzare le risorse nella cache lato client o server*. Si fa caching lato client solo se autorizzati, vogliamo migliorare le **prestazioni lato cliente** e aumentare la **scalabilita lato server**.
* **architettura a piu livelli**: in presenza di piu nodi tra client e server, il *client non sa se sta comunicando direttamente con il server o con un'intermediario* (e similmente per il server)
* **Codice on-demeand**: Il server può inviare codice eseguibile (come applet) da eseguire sul client solo su richiesta


**HTTP**: le API REST funzionano tramite richieste HTTP. Possiamo usare i metodi, per sempio in questo modo:
* **GET**: recuperare un record
* **POST**: creare un nuovo record
* **PUT**: aggiorna un record
* **DELETE**: rimuovi un record.


**Richardson Maturity Model**:
Suddivisione in livelli secondo Richardson in base all'aderenza ai principi rest.
* **Livello 0**: **Viene usato un unico endpoint** (es. `/appointmentService`) al quale vengono inviate richieste **RPC** solitamente tramite metodo `POST` HTTP. HTTP funge solo da protocollo di trasporto
	* **RPC**: Remote Procedure Call
* **Livello 1**: Viene introdotto il concetto di **risorse individuali**. Il servizio viene suddiviso in molteplici endpoint specifici per risorsa (es. `/doctors/mjones` o `/slots/1234`), ma si continua a usare un metodo HTTP generico per tutte le operazioni
* **Livello 2 (HTTP Verbs)**: Si fa un uso corretto e standardizzato dei **metodi HTTP** e dei **codici di stato**. 
	* `GET`: e' idempotente, dunque considerata una query sicura.
	* `POST, PUT, PATCH, DELETE`: permettono mutazioni nel server.
	* **Risposte**: si risponde con status code HTTP appropriati (es. `201 Created` con header `Location`, o `409 Conflict`) invece di restituire sempre `200 OK` con buste d'errore all'interno del body.
* **Livello 3 (HATEOAS)**: HATEOAS indica i contesti in cui le risposte delle API forniscono url per guidare il client sulle prossime azioni disponibili.


## HTTP e CRUD
|Metodo HTTP|Operazione CRUD|Idempotente?|Descrizione|
|---|---|---|---|
|**GET**|Read (Lettura)|**Sì**|Recupera la rappresentazione di una risorsa o collezione. Non altera lo stato del server.|
|**POST**|Create (Creazione)|**No**|Crea una nuova risorsa subordinata. Esecuzioni multiple creano risorse duplicate.|
|**PUT**|Update/Replace (Sostituzione)|**Sì**|Sovrascrive interamente una risorsa esistente o la crea se l'ID è definito dal client. Chiamate ripetute non variano lo stato finale rispetto alla prima.|
|**PATCH**|Partial Update (Modifica parziale)|**No** (di norma)|Applica una modifica parziale. Può non essere idempotente (es. se incrementa un contatore relativo).|
|**DELETE**|Delete (Cancellazione)|**Sì**|Rimuove una risorsa. Sebbene la prima chiamata restituisca `200`/`204` e le successive `404`, lo stato del server non cambia dopo la prima cancellazione|

## Best Practices
1. **Sostantivi, non verbi, nei percorsi**: Usa `/api/v1/users`, non `/api/v1/getUsers`. Il metodo HTTP esprime l'azione, l'URL identifica la risorsa
2. **Utilizzo di JSON come standard**: JSON è il formato di interscambio predefinito per la sua leggerezza, flessibilità e facilità di parsing nativo nei client JavaScript e linguaggi backend
3. **Inclusione di Idempotency-Key**: Per le richieste `POST` e `PATCH` mutative (specialmente in scenari ad alto traffico o eseguiti da agenti autonomi di AI), accetta un header `Idempotency-Key` (in formato UUIDv4) per memorizzare e restituire la risposta memorizzata in caso di reinvii duplicati causa timeout di rete


## integrazione con CTFd
Architettura di un Plugin in CTFd

I plugin in CTFd risiedono nella cartella `CTFd/plugins/`. Ogni cartella deve contenere un file principale chiamato `__init__.py`. Durante l'inizializzazione del server, CTFd scansiona ogni sottocartella, cerca la funzione `load(app)` e la esegue passando l'istanza principale dell'applicazione Flask (`app`) come parametro.

Questo consente ai plugin di effettuare le seguenti operazioni:

1. Creare nuove **tabelle di database** tramite il motore SQLAlchemy integrato.
2. Registrare **rotte e API REST personalizzate** usando i decoratori Flask standard o Blueprint dedicati.
3. Fornire **interfacce e moduli dinamici** (modali) per sfide personalizzate