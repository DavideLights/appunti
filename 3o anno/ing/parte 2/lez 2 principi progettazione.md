* stepwise refinement
* astrazione
* decomposizione modulare
* modularita
* information hiding
* riusabilita
* gay

## stepwise refinement
**raffinamenti successivi**: strategia usata nell'ambito della programmazione strutturata.

**raffinamento**: ad ogni passo aggiungo un livello di dettaglio maggiore. Corrisponde al processo di **astrazione**.

**Legge di Miller**: Se un modulo ha troppe responsabilità, supera i 7±2 elementi della Legge di Miller e diventa difficile da manutenere.
## astrazione
**astrazione**: Ignorare i dettagli.
**step**: *ogni passo rappresenta un raffinamento del livello di astrazione della soluzione*.
**entita**: permette di identificare cosa e' e cosa fa ogni entita del progetto.

**astrazione procedurale**: *corrisponde alla funzioni in C*. Do un nome ad una funzione per poter richiamare del codice senza conoscerne i dettagli implementativi.

**astrazione dei dati**: *incapsulazione dei dati*. Una struttura dati che contiene un insieme di campi.

**classi astratte**: identifica tipo di dato insieme alle azioni
eseguite sulle istanze del tipo di dato. Migliora e riusabilità e manutenibilità 

## Modularita
**moduli**: *suddivido il progetto in segmenti piu piccoli*.
**modificare moduli**: la modifica di un modulo ha impatto minimale sugli altri. (def. IEEE)

**architettura dei moduli**: *risultato della suddivisione in moduli di un sistema software*. Descrive **come interagiscono** e la **struttura dei dati manipolati**

![[Pasted image 20260302122406.png]]

**buona suddivisione in moduli**:
* **massimizza coesione**: interna ai moduli, il modulo fa una cosa sola e fatta bene.
* **minimizzare coupling**: esterna tra i moduli, moduli più indipendenti possibili.

**legge di miller**: *la modularita serve a gestire la complessita cognitiva*.

![[Pasted image 20260302122624.png]]

## coesione
**funzione**: per eseguire necessita di azioni
**azioni**: si trovano tutte in un modulo o sono sparse tra moduli.

**coesione del modulo**: *Misura in cui il modulo*
*espleta internamente tutte le azioni necessarie a*
*espletare una data funzione (cioè senza interagire*
*con le azioni interne ad altri moduli).*

**interazione interna**: la coesione misura il grado di interazione
interna al modulo tra le azioni di una funzione

## Livelli coesione (dal peggiore al migliore)
1. **Coincidental** (Elementi messi insieme per puro caso o per risparmiare spazio).
2. **Logical** (Il modulo esegue azioni diverse ma correlate logicamente)
3. **Temporal** (Le azioni sono unite solo perché avvengono nello stesso momento).
4. **Procedural** (elementi correlati in base ad una sequenza predefinita di passi da eseguire).
5. **Communicational** (elementi correlati in base ad una sequenza predefinita di passi che vengono eseguiti **sulla stessa struttura dati**).
6. **Informational** ossia il concetto base della **OOP**(ogni elemento ha una porzione di codice indipendente e un proprio punto di ingresso ed uscita; tutti gli elementi agiscono sulla stessa struttura dati).
7. **Functional** (tutti gli elementi sono correlati dal fatto di svolgere una singola funzione)

---
## copuling (dal peggiore al migliore)
1. **Content** (un modulo fa diretto riferimento al contenuto
di un altro modulo). 
2. **Common** (due moduli che accedono alla stessa
struttura dati)
3. **Control** (un modulo controlla esplicitamente
l'esecuzione di un altro modulo).
4. **Stamp** (due moduli che si passano come argomento
una struttura dati, della quale si usano solo alcuni
elementi).
5. **Data** (due moduli che si passano argomenti omogenei,
ovvero argomenti semplici o strutture dati delle quali si
usano tutti gli elementi).

**Strength**: la forza del coupling tra due moduli dipende da:
* numero **riferimenti** tra l'uno e l'altro
* numero **dati condivisi**
* **complessità interfaccia** tra moduli
* **quantita di controllo** che un modulo ha sull'altro.

**information hiding**: introdotto da Parnas. Definisco e progetto moduli in modo che i dettagli implementativi non siano accessibili ad altri moduli.

**nota**: altri moduli non devono conoscere i dettagli.

## riusabilita
**riusabilità**: fa riferimento all'utilizzo di componenti
sviluppati per un prodotto all'interno di un prodotto
differente.



