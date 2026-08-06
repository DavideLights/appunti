`@app.router("/")`: decoratore, indica che URL triggera l'azione

**Debug Mode**: `--debug`

**view**: In **Flask**, una **view** (o _view function_, funzione di vista) è semplicemente una funzione Python che gestisce una specifica richiesta HTTP inviata al tuo server

**Variable Rules** ed `escape`: per passare come parametro una parte dell'URL
```python
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'
    
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'
```

`url_for`: costruisce un URL per una funzione specifica.

**Static Files**: si trovano dentro la cartella `static` e usano l'endpoint `static`.
* `url_for("static", filename="style.css")`

**Jinja**: e' un motore di template. Posso incorporare dentro HTML statici , dati dinamici che provengono dal codice python.
* **template**: e' il file HTML, che contiene la struttura fissa con dei placeholder/tag speciali, da sostituire con dati reali.
* **render**: e' la fase in cui il template viene renderizzato.
* - `{% ... %}` for [Statements](https://jinja.palletsprojects.com/en/stable/templates/#list-of-control-structures)
- `{{ ... }}` for [Expressions](https://jinja.palletsprojects.com/en/stable/templates/#expressions) to print to the template output
- `{# ... #}` for [Comments](https://jinja.palletsprojects.com/en/stable/templates/#comments) not included in the template output


**context locals**: alcuni oggetti in flask sono dei proxy verso un'area di memoria relativa ad un contesto locale.

**redirect**: `redirect` interrompe una richiesta lato cliente e lo ridireziona ad un'altro url correttamente.

`@app.errorhandler(404)`: gestione degli errori

`make_response`: If you want to get hold of the resulting response object inside the view you can use the [`make_response()`](https://flask.palletsprojects.com/en/stable/api/#flask.make_response "flask.make_response") function.

**logging**: `app.logger.[debug,warning,error]("text", format)`


##  blueprint
**Blueprint**: serve ad organizzare un gruppo di Views e di codice
* **es**: `Blueprint('auth', __name__, url_pfrefix="/auth")`
	* blueprint di nome `auth`, definito in `__name__` e con prefisso `/auth`


# SQL Alchemy
**a che serve**? in modo dichiarativo, definisco le classi (tabelle) con i loro attributi (colonne).

**classe**: deve ereditare dalla struttura base, che in `CTFd` e' `db.Model`

**aggiungere al database**: uso il paradigma del commit. devo aggiungerli alla `sessione` e poi faccio il `commit` dei cambiamenti.

## Salvataggio JSON su disco vs attributo su DB

| Criterio                        | Opzione A: JSON come Attributo DB (Raccomandata)                                                                    | Opzione B: File JSON caricato su Server                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Portabilità & Export/Import** | 🟢 **Eccellente**: Il JSON fa parte del backup nativo di CTFd (zip export/import). Niente file persi in migrazione. | 🔴 **Complesso**: Richiede gestione dei file allegati e del mapping dei path durante backup/restore.                  |
| **Atomicità & Transazioni**     | 🟢 **Garantita**: Salvataggio, update e rollback avvengono in un'unica transazione SQL.                             | 🟡 **Rischio Disallineamento**: Il record su DB potrebbe essere creato/modificato anche se il file fallisce l'upload. |
| **Performance**                 | 🟢 **Ottima**: Accesso diretto in memoria via query ORM (senza I/O su file system).                                 | 🟡 **I/O Extra**: Lettura del file da disco/S3 ad ogni richiesta di check.                                            |
| **Manutenibilità**              | 🟢 **Semplice**: Nessuna pulizia di file orfani necessaria alla cancellazione della challenge.                      | 🔴 **Manutenzione**: Bisogna gestire l'eliminazione dei file su disco ed i permessi di lettura/scrittura.             |

### Decisione d'Architettura

**Scelta adottata: Opzione A (Salvataggio diretto nel Database)**. Nel modello SQLAlchemy `PatchChallenge`, aggiungeremo un campo `patch_config = db.Column(db.Text)` (o `db.JSON`). Quando l'amministratore carica il file `.json` nel form di creazione/modifica, il contenuto viene letto, validato e memorizzato nel database.