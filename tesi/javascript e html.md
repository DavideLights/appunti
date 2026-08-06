
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

`getElementById()`:
