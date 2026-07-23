## formulazione esempi AIMA

**vacumm world**:
* **Stati**: l'agente deve sapere: posizione dell'agente, posizione dello sporco. L'agente si trova in una delle due stanze e ognuna di queste potrebbe contenere o non contenere lo sporco.
	* **Numero di stati**: $2^2 \times 2$, ossia due celle, che possono essere sporche o pulite, ed l'agente si trova solo su una di queste due
* **Stati iniziale**: qualsiasi configurazione e' un possibile stato iniziale.
* **Azioni**: Movimento: `Left`, `Right`. `Suck` per aspirare.
* **Modello delle transizioni**:
	* **Movimento**: Muoversi a sinistra vuol dire spostare l'agente sulla casella più a sinistra, e similmente per destra. 
	* **Suck**: vuol dire passare allo stato in cui la stanza su cui e' posizionato l'agente non e' sporca. **Suck** su una stanza pulita non ha nessun effetto.
* **Goal Test**: controlla se le stanze sono pulite.
* **Path Cost**: ogni azione costa 1.

**8-puzzle**:
* **Stati**: una particolare configurazione della griglia $3\times 3$
	* **Numero di stati**: $\frac{9!}{2}$, ossia devo posizionare in modo sequenziale $8$ numeri avendo a disposizione inizialmente 9 caselle. Divido per 2 perche' ho solo 8 numeri.
* **Stato iniziale**: qualsiasi configurazione e' un possibile stato iniziale.
* **Azione**: Left, Right, Up, Down e corrisponde a fare uno slide di tutte le caselle verso una certa direzione (seguendo le regole della griglia)
*  **Transition Model**: applicare per esempio `Left` vuol dire spostare sequenzialmente, tutte le caselle che ammettono quello spostamento. 
* **Goal Test**: controlla se i numeri sono ordinati
* **Path Cost**: pari ad  1 per ogni azione.

**8-regine**: posizionare 8 regine sulla scacchiera in modo che nessuna faccia scacco verso le altre.
* **formulazione 1**: incrementale vuol dire che comincio dalla scacchiera vuota e le posiziono 1 per 1.
* **formulazione 2**: complete-state, ossia ho 8 regine sulla scacchiera e le devo muovere per raggiungere il goal
	* **Hill-Climbing**: risolvei l problema.

1. **Formulazione Stati 1**: un qualsiasi posizionamento delle 8 regine. 
	1. **Numero di stati**: $64 \cdot 63 \cdot \dots \cdot 57$
2. **Formulazione Stati 2**: una qualsiasi configurazione dove per $i=1,\dots,8$ nella colonna $i$ ho una regina posizionata in modo che le 8 regine non si facciano scacco a vicenda
	1. Numero di stati: $2057$???

## esempi euristiche

> [!error] sottostimare/sovrastimare
> * **l'euristica non deve mai sovrastimare**, altrimenti l'algoritmo potrebbe scartare il percorso migliore e perdere la garanzia di ottimalita.
> * **l'euristica non deve mai troppo sottostimare**, al caso peggiore $A^*$ si comporta come UC

**8-puzzle**:
* $h_{1}$: numero di pezzi fuori posto
* **Manhattan Distance**: $h_{2}$: $\sum_{i}^8 c_{i}$ con $c_{i} = \text{\# mosse per portare il pezzo }i \text{ alla configurazione finale}$
* **qual'e meglio?** $h_{2}$ ha $b^*$ piu basso in generale (vedi lezione).
* $h_{2}$ e' sempre meglio di $h_{1}$? per ogni nodo $h_{2}(n) \geq h_{1}(n)$, dunque $h_{2}$ domina $h_{1}$ ed e' più vicino all'ottimo