**algoritmo di derivazione**:
* **truth preserving**: non devo derivare cazzate
* **completezza**: posso derivare tutto il derivabile.

**espressivita**: introduce incertezza, concetti vaghi e imprecisi. Con linguaggi espressivi determino cosa puo' essere lasciato di non detto.

**complessita della derivazione**:
* PROP: decidibile ma intrattabile
* FOL: semidecidibile.

**da cosa e' composta la conoscenza?**
* fatti specifici, es: "socrate e' un uomo"
* regole generali, le regole
* **inferire**: se nel $KB$ ho: "gli uomini sono mortali", allora posso inferire che "socrate e' mortale"

**assunzione ontologica**: nel linguagio che sto usando, come e' fatto il mondo

**Ontologia: PROP VS FOL**.
- **In PROP hai solo:**
    - **Simboli proposizionali** (es. $P, Q, R$).
    - **Connettivi logici** ($\neg, \wedge, \vee, \to, \leftrightarrow$).
- **In FOL hai in più:**
    - **Costanti** (per gli oggetti, es. $A, B$) e **Variabili** (es. $x, y$).
    - **Predicati** (per proprietà e relazioni, es. $Studente(x)$, $Fratello(x, y)$).
    - **Funzioni** (es. $madre(x)$).
    - **Quantificatori:** Il quantificatore universale ($\forall$, "per ogni") e quello esistenziale ($\exists$, "esiste almeno uno").

**Calcolo Proposizionale**:
* **equivalenza logica**: $A \equiv B$ iff. $A ⊨ B$ ed $B ⊨ A$
* **tautologia**:  $A$ e' tautologia se tutti i modelli $M$ soddisfano $A$.
* **soddisfacibilita**: se $\exists M: M(A)$ e' vera.


**~~Regole di inferenza~~**:
![[Pasted image 20260719013230.png]]

**SAT**: ho una formula in CNF e voglio trovare una combinazione di letterali che la renda vera.

**Metodo locale per SAT**:
* **euristica**: numero di  clausole soddisfatte.
* **problema**: ci sono molti minimi locali dunque si usa HC con riavvio casuale oppure SA. 

**probabilita di soddisfacibilita**: sia $\frac{n}{m}$ il rapporto tra il numero di simboli e il numero di clausole.
* $\frac{n}{m} \in [3,6]$ la probabilita di soddisfare cala
* $\frac{n}{m} > 6$ cala drasticamente vicino allo 0


**TEOREMA deduzione**: $A ⊨ B$ iff $A \to B$ tautologia
**TEOREMA refutazione**: $A ⊨ B \text{ iff } A \land \lnot B$ insoddisfacibile

La dimostrazione di $A ⊨ B$ e' NP-Completo ma decidibile.

Regoal di risoluzione