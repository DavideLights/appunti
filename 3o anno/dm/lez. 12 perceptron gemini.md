## 1. Il Modello del Neurone (Classificatore Lineare)

**Obiettivo:** Classificare un input $x$ in due classi possibili: $+1$ oppure $-1$.
- **Input:** Un vettore $x = (x_1, \dots, x_d) \in \mathbb{R}^d$.
- **Pesi (Weights):** Un vettore $w = (w_1, \dots, w_d)$ che "pesa" l'importanza di ogni input.
- **Funzione lineare:** La combinazione lineare di input e pesi è data da $x_1w_1 + \dots + x_dw_d$.
- **Soglia di decisione ($\Theta$):** Se la somma pesata supera una certa soglia $\Theta$, classifichiamo come $+1$, altrimenti $-1$.
### Il trucco del Bias (L'unità di polarizzazione)
Invece di portarci dietro la disuguaglianza con $\Theta$, spostiamo tutto a sinistra:

$$ x_1w_1 + \dots + x_dw_d - \Theta \geq 0 $$

Per semplificare la matematica, definiamo:
- **bias**: $w_0 = -\Theta$
- **input fittizio**: $x_0 = 1$, e' sempre acceso

Ora la disequazione diventa il **prodotto di due vettori** di dimensione $d+1$:
$$ w \cdot x = x_0w_0 + x_1w_1 + \dots + x_dw_d \geq 0 $$

> **Nota di intuizione sui vettori:**
> Immagina il **prodotto scalare** $w \cdot x$ come un "rilevatore di somiglianza". Se l'input $x$ punta nella stessa direzione generale del vettore dei pesi $w$, il prodotto scalare sarà positivo (classe $+1$). Se puntano in direzioni opposte, sarà negativo (classe $-1$). Il bias $w_0$ serve solo a traslare questo confine di decisione lontano dall'origine degli assi.

**Funzione di attivazione (Notazione):**
$$ \phi(w \cdot x) = \begin{cases} 1 & \text{se } w \cdot x \geq 0 \\ -1 & \text{altrimenti} \end{cases} $$

## 2. Geometria dell'Iperpiano e Preliminari sui Vettori

**iperpiano**:  e' $H$ insieme dei punti $x$ in cui la nostra rete è "indecisa", ovvero dove l'input di rete è esattamente zero.
$$ H: w \cdot x = 0 $$
- **Modulo (o norma):** È la lunghezza geometrica di un vettore. $\|a\| = \sqrt{a_1^2 + \dots + a_d^2}$.
- **Proprietà 1 (Prodotto scalare e angoli):** Dati due vettori $a$ e $b$, e chiamato $\beta$ l'angolo tra loro, vale la relazione:
$$ a \cdot b = \|a\| \|b\| \cos(\beta) $$
- **Vettori perpendicolari:** Due vettori sono perpendicolari se e solo se l'angolo $\beta$ è $90^\circ$. Poiché $\cos(90^\circ) = 0$, la condizione di perpendicolarità è semplicemente $a \cdot b = 0$.

**Proprietà 2:** Il vettore dei pesi $w = (w_1, \dots, w_d)$ è **sempre perpendicolare** all'iperpiano $H$.

**dim prop. 2**:  sia $H'$ l'iperpiano
$$
H': w_{1} x_{1} + \dots + w_{d}x_{d} = 0
$$
* $H'$ e' parallelo ad $H$
* sia il punto $p \in H'$, **allora il vettore direzione che dall'origine va in $p$ e' vettore direzione per $H'$, ma lo e' anche per** $H$.
* dato che $p\in H'$, allora vale  $w \cdot p = 0$. 
* sia $\beta$ l'angolo tra $p$ e $w$
$$
||w||\; ||p|| \cos(\beta) = 0
$$
* **soluzione**: deve essere che $\cos(\beta)=0 \iff \beta=\pm 90$.
_

**Proprietà 3 (Distanza di un punto dall'iperpiano):**

La distanza geometrica $d_{pH}$ di un punto generico $p$ dall'iperpiano $H$ è data da:

$$ d_{pH} = \frac{w \cdot p + w_0}{\|w\|} $$

**Dim.** 
* sia $u \in H$
* $w \cdot u = -w_{0}$
* sia $\beta$ angolo tra $H$ e $p-u$

Allora, la distanza $d_{pH}$ da $p$ a $H$ è
$$

d_{pH} = \|p-u\| \sin(\beta).

$$

Applichiamo la Proprietà 1 ai vettori $p-u$ e $w$ (il vettore perpendicolare ad $H$, Proprietà 2):
$$

\cos(90-\beta) = \frac{w\cdot (p-u)}{\|w\| \|p-u\|} = \frac{||w||  \;||(p-u)||}{\|w\| \|p-u\|} \sin (\beta) = \sin(\beta)

$$
* $a \cdot b= ||a||\; ||b|| \cos(\beta) \to \frac{a \cdot b}{||a||\; ||b||}=  \cos(\beta)$
* $90-\beta$: il vettore $(p-u)$ e' "sollevato" di $\beta$ rispetto al  piano $H$, ma sappiamo anche che $w$ e' perpendicolare ad $H$

Sostituendo $\sin(\beta)$ nella formula per $d_{pH}$:
$$

d_{pH} = \frac{w\cdot (p-u)}{\|w\|} = \frac{w\cdot p - w\cdot u}{\|w\|} =

\frac{w\cdot p + w_0}{\|w\|}

$$

## 3. Addestramento: Algoritmo Perceptron

**Scopo:** Trovare il vettore $w$ (l'iperpiano) che separa correttamente tutti gli esempi di training. _Assunzione:_ Il dataset deve essere linearmente separabile.

**Inizializzazione:** Imposta $w = (0, \dots, 0)$.

**Ciclo di Addestramento (Epoche):**

Per ogni esempio $(x^{(i)}, y^{(i)})$ nel dataset:

1. **Test:** L'esempio è classificato correttamente se e solo se il segno della previsione coincide con il target reale $y^{(i)}$. Matematicamente: $y^{(i)} (w \cdot x^{(i)}) > 0$.
    
2. **Aggiornamento (solo se c'è un errore):** Se l'esempio è classificato male, si corregge il vettore $w$:
    
    $$ w = w + \eta y^{(i)} x^{(i)} $$
    
    _(Dove $\eta$ è il tasso di apprendimento, solitamente impostato a 1 nelle dimostrazioni base)._
    

> **Perché questo aggiornamento funziona?**
> 
> Se il modello sbaglia dicendo $-1$ quando doveva essere $+1$, significa che $w \cdot x$ era troppo negativo. Aggiungendo $x$ a $w$, al giro successivo il prodotto scalare $(w+x) \cdot x = (w \cdot x) + \|x\|^2$ sarà un numero più grande, spingendo la decisione verso il $+1$ corretto.

## 4. Teorema di Convergenza (Analisi dell'Algoritmo di Novikoff)

Questa è la parte matematicamente più densa. Lo scopo è dimostrare che il Perceptron non ciclerà all'infinito, ma troverà la soluzione in un numero massimo garantito di passi $k$.

**Assunzioni:**

- Esiste un iperpiano ottimo $w^*$ (con $\|w^*\|=1$) che separa perfettamente i dati.
    
- **Margine ($\gamma$):** È la distanza del punto più vicino all'iperpiano $w^*$. Poiché abbiamo normalizzato $\|w^*\|=1$, il margine è $\gamma = \min_i (y^{(i)} (w^* \cdot x^{(i)}))$. Il margine è strettamente $>0$.
    
- **Limite superiore norma ($U$):** È la lunghezza del vettore di input più lungo nel dataset. $U \geq \max_i \|x^{(i)}\|$.
    

L'idea della dimostrazione è studiare l'angolo $\beta$ tra il vettore corrente $w^{(k)}$ e quello ottimo $w^*$. Al crescere degli aggiornamenti, questo angolo si restringe.

$$ \cos(\beta) = \frac{w^* \cdot w^{(k)}}{\|w^*\| \|w^{(k)}\|} = \frac{w^* \cdot w^{(k)}}{\|w^{(k)}\|} $$

### Fattore 1: Il numeratore (L'allineamento cresce)

Vogliamo dimostrare che ad ogni errore, $w^{(k)}$ si allinea sempre di più con $w^*$.

$$ w^* \cdot w^{(k)} = w^* \cdot (w^{(k-1)} + \eta y^{(i)} x^{(i)}) $$

$$ = w^* \cdot w^{(k-1)} + \eta y^{(i)} (w^* \cdot x^{(i)}) $$

Poiché l'iperpiano ottimo separa bene con margine $\gamma$, sappiamo che $y^{(i)} (w^* \cdot x^{(i)}) \geq \gamma$. Quindi:

$$ w^* \cdot w^{(k)} \geq w^* \cdot w^{(k-1)} + \eta \gamma $$

Applicando questo ragionamento per $k$ passi (partendo da $w^{(0)} = 0$):

$$ w^* \cdot w^{(k)} \geq k \eta \gamma $$

### Fattore 2: Il denominatore (La lunghezza non cresce troppo)

Vogliamo limitare quanto si "allunga" il vettore $w^{(k)}$ ad ogni passo. Usiamo la regola del quadrato di un binomio per i vettori ($\|a+b\|^2 = \|a\|^2 + 2a\cdot b + \|b\|^2$):

$$ \|w^{(k)}\|^2 = \|w^{(k-1)} + \eta y^{(i)} x^{(i)}\|^2 $$

$$ = \|w^{(k-1)}\|^2 + 2\eta y^{(i)}(w^{(k-1)} \cdot x^{(i)}) + \eta^2 \|x^{(i)}\|^2 $$

- Il termine di mezzo è $\leq 0$ perché stiamo facendo un aggiornamento _solo_ se c'è stato un errore su quell'esempio!
    
- L'ultimo termine è limitato dalla massima lunghezza al quadrato $\eta^2 U^2$.
    

Quindi, dopo $k$ passi, la lunghezza massima accumulata è:

$$ \|w^{(k)}\|^2 \leq k \eta^2 U^2 \implies \|w^{(k)}\| \leq \eta U \sqrt{k} $$

### Conclusione: Il limite dei passi $k$

Unendo i due fattori nel coseno dell'angolo iniziale:

$$ \cos(\beta) = \frac{w^* \cdot w^{(k)}}{\|w^{(k)}\|} \geq \frac{k \eta \gamma}{\eta U \sqrt{k}} = \frac{\gamma \sqrt{k}}{U} $$

Sappiamo dalla trigonometria che il coseno di un angolo non può mai superare $1$. Quindi:

$$ 1 \geq \frac{\gamma \sqrt{k}}{U} $$

Risolvendo per $k$, otteniamo il numero massimo di errori (e quindi di aggiornamenti) prima che l'algoritmo si fermi:

$$ k \leq \frac{U^2}{\gamma^2} $$

L'algoritmo **deve convergere** in un numero finito di passi, proporzionale al raggio dei dati ($U$) e inversamente proporzionale alla nettezza della separazione ($\gamma$).