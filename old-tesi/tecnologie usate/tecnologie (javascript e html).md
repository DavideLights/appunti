
```html
<script async src="scripts/main.js"></script>
```

```js
// Store a reference to the <h1> in a variable
const myHeading = document.querySelector("h1");
// Update the text content of the <h1>
myHeading.textContent = "Hello world!";
```


**HTML DOM API**: interfacce che definiscono le funzionalita degli elementi in HTML
* **DOM**: descrive la struttura di un `documento
* `Document`: interfaccia che descrive una qualsiasi pagina caricata nel browser
	* `HTMLDocument`: e' l'API specifica per i documenti HTML
	* `XMLDocument`: e' l'API specifica per gli XML]
* `Node`: un documento e' fatto di Nodi, organizzati gerarchicamente. E' l'interfaccia base per i nodi, ma non rappresentano l'informazione mostrata su schermo.
* `Element`: eredita da `Node`. E' la classe più generale da quale tutti gli oggetti (che rappresentano "elementi") ereditano.

**Documento HTML**: e' un `HTMLDocument` dove tutti gli elementi sono `HTMLElement`:
* `<a>` e' un `HTMLAnchorElement`, che eredita da `HTMLElement`

**EventTarget**: `Nodo` eredita da `EventTarget`, ossia l'oggetto che raccoglie e gestisce gli eventi.


## Perche' si ritorna `success` booleano nelle API REST?
Nel file  ~api.py~ il valore booleano `"success": True` viene restituito per le seguenti ragioni principali:

### 1. Convenzione Standard dell'Architettura REST di CTFd
Tutti gli endpoint REST nativi di CTFd (e dei relativi plugin) seguono una struttura di risposta JSON standard:
- **In caso di successo:** `{"success": true, "data": {...}}` oppure `{"success": true, "message": "..."}`
- **In caso di errore:** `{"success": false, "errors": [...]}` oppure `{"success": false, "message": "..."}`

### 2. Gestione Semplificata nel Frontend (JavaScript)
Il client frontend di CTFd (tramite `CTFd.fetch` o gli handler AJAX in jQuery) si aspetta questa struttura standard.

### 3. Disaccoppiamento tra Stato HTTP ed Esito Logico
- **HTTP Status Code (es. 200 OK):** Conferma che la trasmissione della richiesta web è andata a buon fine.
- **`success` (booleano):** Indica l'esito logico a livello applicativo (ad esempio se il _Verification Agent_ è riuscito concretamente ad avviare, fermare o verificare il container Docker della challenge).