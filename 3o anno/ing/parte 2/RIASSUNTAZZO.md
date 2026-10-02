# design patterns
**design patterns**: sono metodi e modelli collaudati e ben funzionanti. Si applicano in base condizioni, utilita, e benefici e problematiche che possono apportare al sistema.
* sono classificati in: design patterns su classi/oggetti ed creazionali, comportamentali e strutturali.
* un pattern ha sempre: nome, motivazione, condizioni di applicabilita, documentazione, esempi di codice, ecc...

**abstract factory**: e' basato su oggetti. creazionale. 
* abstract factory: interfaccia per la creazione di oggetti
* concrete factory: implementazione della factory
* abastract/concrete product
* **funzionamento**: la abstract fornisce un'interfaccia con metodi per creare ogni tipo di oggetto. il software deve decidere quale tipo di metodo creare.

**factory method**: basato su classi.
* creator/concrete creator
* product/concrete product
* il costrutture ritorna il tipo giusto.

adapter: classe o oggetto
* adapter: eredita l'oggetto da adattare, e implementa l'interfaccia dell'oggetto adaptee
* a livello di implementazione, l'adattatore e' un adaptee
* **oggetti**: allora l'adaptee e' un riferimento all'interno di una classe.

**decorator**: 
* UI look and feel
* incapsula al suo interno un'altro oggetto evitando l'overhad dell'ereditarieta in caso
* decorator: mantiene un riferimento all'oggetto da decorare, e ne incapsula e richiama il comportamento

**observer**:
* subject: e' l'oggetto da osservare
* observer: e' un'oggetto che osserva 
* **funzionamento**: gli observer si registrano presso il subject. quando avviene un cambiamento gli observer sono notificati dal subject scatenando eventi negli observer che possono poi richiedere lo stato dell'oggetto.

**composite**: uniformare gerarchie di oggetti
* component: oggetto che puo contenere piu 

**requisiti**:
# misure
**misure**: dobbiamo misurare la complessita del codice
* fase preliminare di OOD: quanto e' buona la soluzione?
* misure inter-modulari e intra-modulari in fase avanzata di design

**modulo**: e' una porzione di software con un inizio ed una fine, delimitato logicamente.

relazione progetto/software:
* moduli del modello -> moduli nel codice
* connessioni tra moduli -> riferimenti a moduli nel codice
* interfacce tra moduli -> scambio di dati

structure chart: modella la gerarchia delle chiamate dei moduli
* depth
* numero di nodi
* width massima
* rapport e/n

attributi dei moduli:
* coesione interna
* accoppiamento
* morfologia
* flusso di informazioni: come passano i flussi dati nella moroflogia

impurita: server per misurare quanto si avvicina lo structure chart allo spanning tree
* $m(G) = \frac{2(e-n+1)}{(n-1)(n-2)}$
* $m(G)=1$ albero impuro
* $m(G)=0$ albero puro

**metriche per il flusso di informazioni**
* flusso locale/globale: 
	* diretto: procedure
	* indiretto: ritorno di procedure
	* globale: uso di strutture dati condivise globalmente nel codice

**fan-in**: numero di flussi locali+indiretti+globali in entrata

**fan-out**: numero di flussi ... in uscita