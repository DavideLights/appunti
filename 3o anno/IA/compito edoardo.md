## PEAS
* **Performance Measure**: l'agente deve recuperare un pacco e portarlo all'uscita minimizzando il **costo totale**.
	* **movimento**: -1
	* **zona rallentata**: -2
	* **raccogliere il pacco**: +100
	* **portare il pacco all'uscita**: +1000
* **Environment**: magazzino modellato come una griglia 7x7. L'agente inizia in posizione $(0,0)$, il pacco sta in $(2,4)$ ed l'uscita e' in $(5,6)$. In $(5,4)$ e $(3,6)$ troviamo delle celle scivolose
* **Attuatori**: il robot ha braccia e gambe che gli permettono di spostarsi nella griglia nelle 4 direzioni $\{ N,S,E,O \}$.
* **Sensore**: la vista gli consente di percepire l'ambiente circostante, percepire la posizione e cosa lo circonda.

**Caratteristiche ambiente**: completamente osservabile, deterministico, episodico (sequenziale), discreto, statico, noto.

Il nostro agente dovrà perseguire un'obiettivo, ed opererà da pianificatore. L'ambiente e' statico, completamente osservabile e deterministico, dunque dovrà: pianificare ed eseguire.

**Stati**: lo **stato** e' una fotografia del nostro ambiente in un dato momento ed e' rappresentato dalla tupla: $$<P_{\text{robot}},  P_{\text{pacco}}, P_{\text{uscita}}, \text{Ostacoli}, \text{LP}_{\text{olio}}, \text{B}_{\text{raccolto}}>$$
**stato di ricerca**: $S_{\text{RIC}}: <P_{\text{robot}}, B_{\text{raccolto}}>$, con $P_\text{raccolto} \in [0\dots {6}]^2$ ed $B_{\text{raccolto}} \in \{ T,F \}$
* **Stato iniziale** di ricerca: $S_{\text{start}}:<(0,0), \text{false}>$
* **Stato goal 1**: $S_{\text{goal}1}: <(2,4), \text{True}>$
* **Stato goal 2**: $S_{\text{goal}}: <(5,6), \text{True}>$

**abbiamo 2 tipi di azioni**:
1. $a \in \{ N,S,E,O \}$
2. $a \in \text{racco}$