
# PDF 1 — Vettori, coordinate, rette/piani, primi sistemi lineari

## 2. Concetti da sapere
### introduzione
**spazi affini**, insieme di vettori.
* $\mathcal A^2$: piano, corrisponde al piano cartesiano.
* $\mathcal A^3$: spazio, coordinate x,y,z
* $\mathcal A^1$: retta

$V^2_{O}$: e' l'insieme dei vettori $\vec{OA} \text{ per ogni } A \in R^2$
 
[DEFINIZIONE] **Vettore applicato in $O$**  
Nel piano o nello spazio, un vettore è pensato come un segmento orientato, con un primo estremo e un secondo estremo. Esempio: $\overrightarrow{OP}$.

[DEFINIZIONE] **Somma di due vettori**  
Dati due vettori applicati $\overrightarrow{OA}$ e $\overrightarrow{OB}$, la somma si ottiene con la regola del parallelogramma:

$$ \overrightarrow{OA}+\overrightarrow{OB}=\overrightarrow{OC} $$

dove $C$ è il **quarto vertice del parallelogramma**.

[TEOREMA] **L’insieme dei vettori è un gruppo commutativo rispetto alla somma**  
Bisogna ricordare che la somma di vettori è associativa, ha elemento neutro, ogni vettore ha opposto e vale la commutatività.

**~~Proprietà~~**:
* **associativa**: $(a+b)+c = a + (b+c)$. Si dimostra facendo vedere che in entrambi i modi si costruisce lo stesso parallelogramma.
* **esistenza elemento nullo**: $a+a_{0} = a_{0}+a = a$, ossia $\overrightarrow{OO}$
* **esistenza opposto**: $a + a'= a' + a = a_{0}$, $-\overrightarrow{OA}$
* **commutativa**: $a +b = b +a$

[DEFINIZIONE] **Prodotto di un vettore per uno scalare**  
Dato $t \in \mathbb{R}$ e un vettore $\overrightarrow{OA}$, il vettore $t\overrightarrow{OA}$:
- ha lunghezza moltiplicata per $|t|$;
- ha **stesso verso** se $t>0$;
- ha **verso opposto** se $t<0$;
- è il vettore nullo se $t=0$.

[FORMULA] Proprietà del prodotto per scalare:
* $\lambda(\overrightarrow{OA}+\overrightarrow{OB})= \lambda \overrightarrow{OA}+\lambda \overrightarrow{OB}$
* $(\lambda+\mu)\overrightarrow{OA} =\lambda\overrightarrow{OA}+\mu\overrightarrow{OA}$
* $(\lambda\mu)\overrightarrow{OA} = \lambda(\mu\overrightarrow{OA})$
* $1\cdot \overrightarrow{OA}=\overrightarrow{OA}$ ed $0 \cdot \overrightarrow{OA} = \overrightarrow{OO}$

> [!nota] esempi scemi
> * $3 \overrightarrow{OA} = \overrightarrow{OA} + \overrightarrow{OA} + \overrightarrow{OA}$
> * $-2 \overrightarrow{OA} = (-\overrightarrow{OA}) + (-\overrightarrow{OA})$

### vettori e piani 
[DEFINIZIONE] **Coordinate rispetto a due vettori non paralleli**  
Se $\vec i,\vec j$ sono due vettori **non paralleli** nel piano, ogni vettore $\overrightarrow{OP}$ si scrive in **modo unico** come:

$$ \overrightarrow{OP}=x_1\vec i+x_2\vec j$$
**~~dimostrazione~~**: con le intersezioni delle due rette passanti per $\vec{i}$ e $\vec{j}$ posso rappresentare tutti i vettori $\overrightarrow{OP}$ .

**coordinate**: La coppia $(x_1,x_2)$ sono le coordinate del vettore ed $(x_{1},x_{2}) \in R^2$, dunque siamo passati da $V^2_{O}$ in $R^2$


[DEFINIZIONE] **Rappresentare un Vettore, notazione rispetto alle leezioni!**
$\overrightarrow{OP} = \begin{vmatrix} x_{1}\\ x_{2}  \end{vmatrix}$ con $x_{1},x_{2}$ coordinate rispetto ai vettori $\vec{i}, \vec{j}$

 [ESEMPIO]: siano $\vec{i} = \begin{vmatrix} 1 \\ 0  \end{vmatrix}$ e $\vec{j} = \begin{vmatrix} 0 \\ 1  \end{vmatrix}$, allora
$$
\overrightarrow{OP} = \begin{vmatrix} 1 \\ \frac{1}{2}
	
\end{vmatrix} = 1 \vec{i} + \frac{1}{2}\vec{j} = 1 \begin{vmatrix} 1 \\ 0  \end{vmatrix} + \frac{1}{2}\begin{vmatrix} 0 \\ 1  \end{vmatrix}
$$
[DEFINIZIONE] Regole sui Vettori
* $0= \begin{vmatrix} 0\\0 \end{vmatrix}$
* $\lambda \begin{vmatrix} x_{1} \\ x_{2} \end{vmatrix} = \begin{vmatrix} \lambda x_{1} \\ \lambda x_{2} \end{vmatrix}$
* $\begin{vmatrix} x_{1}\\ x_{2} \end{vmatrix} + \begin{vmatrix} y_{1}\\ y_{2} \end{vmatrix} = \begin{vmatrix} x_{1}+y_{1} \\ x_{2}+y_{2} \end{vmatrix}$

[METODO] **Descrivere una retta nel piano**  
*Una retta si descrive scegliendo*:
- un punto $P_0$ della retta;
- un vettore direttore $\overrightarrow{OQ}$, parallelo alla retta.
* allora: $\overrightarrow{OP} = \overrightarrow{OP_0}+t\overrightarrow{OQ}$, con $t\in\mathbb{R}$.

![[Pasted image 20260605152628.png]]
~~**Spiegazione**~~:
* sia $r_{0}$ la retta parallela ad $r$, passante per $O$
* sia $P_{0} \in r$
* **allora**: $P \in r \iff \overrightarrow{OP}-\overrightarrow{OP}_{0} \in r$
* sia $Q \in r_{0}$
* **allora**: $\overrightarrow{OP} - \overrightarrow{OP_{0}}$ e' parallelo ad $\overrightarrow{OQ}$ 
* **quindi**: $\overrightarrow{OP} - \overrightarrow{OP_{0}} = t\overrightarrow{OQ}$ per qualche $t$.
*  *e da questa formula si ricava quella esposta sopra*.

[ESEMPIO] **Trova la linea attraverso $\begin{vmatrix} 0 \\ 1 \end{vmatrix}$ ed $\begin{vmatrix} 1 \\ 2 \end{vmatrix}$**
![[Pasted image 20260605153629.png]]
scelgo: 
* $P_{0} = \begin{vmatrix} 0\\1 \end{vmatrix} \in r$ , ed $Q = \begin{vmatrix} 1 \\ 1   \end{vmatrix} \in r_{0}$, con $r_{0}$ parallela ad $r$ che passa per l'origine
* allora $\overrightarrow{OP} = \begin{vmatrix} 0\\1 \end{vmatrix} + t \begin{vmatrix} 1\\1 \end{vmatrix} = \begin{vmatrix} t\\1+t \end{vmatrix}$

[DEFINIZIONE] **equazione vettoriale di una retta** 
* se $P_{0} = \begin{vmatrix} x_0\\x_1 \end{vmatrix}$, $Q = \begin{vmatrix} l\\m \end{vmatrix}$ ed $P = \begin{vmatrix} x\\ y \end{vmatrix}$
$$(*): \overrightarrow{OP} = \overrightarrow{OP_{0}} + t\overrightarrow{OQ} \iff \begin{vmatrix} x\\ y \end{vmatrix} = \begin{vmatrix} x_{0}\\ y_{0} \end{vmatrix} + t \begin{vmatrix} l\\m \end{vmatrix}$$
[DEFINIZIONE] **vettore direzione** $\overrightarrow{OQ}$
$\overrightarrow{OQ}$ e' il vettore direzione dell'equazione parametrica $(*)$

[DEFINIZIONE] **Equazioni Parametriche per** $(*)$
* $x = x_{0} + tl$
* $y = y_{0} + tm$

[METODO] **Retta passante per due punti**  
Se la retta passa per $P_1$ e $P_2$, un vettore direttore è:
$$ \overrightarrow{OQ} = \overrightarrow{OP_2}-\overrightarrow{OP_1} $$
quindi:
$$ \overrightarrow{OP} = \overrightarrow{OP_1} + t(\overrightarrow{OP_2}-\overrightarrow{OP_1}) $$

[METODO] **Piano nello spazio**  
Un piano $\pi$ si descrive scegliendo:
- un punto $P_0$;
- $\pi_{0}$ parallelo a $\pi$ passante per $O$
- due vettori non paralleli tra loro $\vec i,\vec j$ .
- $\vec{i}, \vec{j}$ contenti in $\pi_{0}$

Allora:
$$ \overrightarrow{OP} = \overrightarrow{OP_0} + t_1\vec i + t_2\vec j $$

con $t_1,t_2\in\mathbb{R}$.

[METODO] **Piano a partire da tre punti allineati**
Siano $P_{1},P_{2},P_{3}$ dei punti allineati:
* $\vec{i} = \overrightarrow{OP_{2}} - \overrightarrow{OP_{1}}$
* $\vec{j} = \overrightarrow{OP_{3}} - \overrightarrow{OP_{1}}$
$$
\overrightarrow{OP} = \overrightarrow{OP_{1}} + t_{1}(\overrightarrow{OP_{2}} - \overrightarrow{OP_{1}}) + t_{2}(\overrightarrow{OP_{3}} - \overrightarrow{OP_{1}})
$$

[METODO] **Intersezione tra rette**
Due rette si intersecano se $\exists t_{1},t_{2} \in R$ tali che:
$$
\overrightarrow{OP_{0}} + t_{1} \overrightarrow{OQ}
 = \overrightarrow{OP_{0}'} + t_{2}\overrightarrow{OQ}
 \iff \overrightarrow{OP_{0}'} -\overrightarrow{OP_{0}}
 =  t_{1} \overrightarrow{OQ} - t_{2}\overrightarrow{OQ'}
$$
**ossia**: due rette si intersecano se $\overrightarrow{OP_{0}'} -\overrightarrow{OP_{0}}$ appartiene al piano generato da $t_{1} \overrightarrow{OQ} - t_{2}\overrightarrow{OQ}$.

**in equazioni parametriche**:
* $x_{0}' - x_0 = t_{1} l-t_{2}l'$
* $y_{0}' -y_{0} = t_{1} m -t_{2} m'$

con $(t_{1},t_{2})$ la soluzione del sistema, allora il punto d'intersezione e':
$$
\begin{vmatrix}
	x_{0}+lt_{1} \\ y_{0} + mt_{1}
\end{vmatrix}
$$

[ESEMPIO] **trova intersezione fra la retta passante per $\begin{vmatrix} 1\\ 1\end{vmatrix}$ e vettore direzione $\begin{vmatrix}2 \\ 1\end{vmatrix}$ e la retta $r'$ passante per $\begin{vmatrix}2 \\0\end{vmatrix}$ ed vettore direttore** $\begin{vmatrix}0 \\ 1\end{vmatrix}$

**svolgimento**...

>[!note] Esercizi da vedere da carrara (tutoraggio a.a. 2023)
> 2.8, 2.2, 2.3, 2.4, 2.8, 2.9, 2.7, 2.11, 2.14

[CARRARA 2.8]  **vettore ortogonale**
il vettore ortogonale ad un piano in si ottiene prendendo i coefficienti $(a,b,c)$ del piano in forma $ax + by + cz = v$

[CARRARA 2.2] **la retta passante per AB e'** $A + t(\overrightarrow{AB})$

### Equazioni e matrici
[ESEMPIO] **equazione di una sola incognita**
$ax+b=0$ ha:
* una soluzione se $a \neq 0$: ossia $x = -\frac{a}{b}$
* nessuna soluzione se: $a=0, b \neq 0$
* infinite se: $a=b=0$ 

[ESEMPIO 3.2]  tre equazioni in tre incognite
da provare a risolvere a mano.

[DEFINIZIONE] **Sistema lineare**  
Un sistema lineare di $m$ equazioni in $n$ incognite (ossia **ordine** $n$) ha forma:
$$
\begin{cases}  
a_{11}x_1+\dots+a_{1n}x_n=b_1 \\  
\quad\quad\quad\quad \vdots \\  
a_{m1}x_1+\dots+a_{mn}x_n=b_m  
\end{cases}  
$$
**Si scrive in forma matriciale**:
$$ Ax=b $$

dove:
- $A$ è la matrice dei coefficienti;
- $x$ è il vettore delle incognite;
- $b$ è il vettore dei termini noti.
[ATTENZIONE] $a_{ij}$ dove $i := \text{riga}$ e $j := \text{colonna}$

[DEFINIZIONE] **Sistema compatibile**  
Un sistema $Ax=b$ è compatibile se esiste almeno una soluzione $x\in\mathbb{R}^n$.

[DEFINIZIONE] **Matrice triangolare superiore**  
Una matrice è triangolare superiore se tutti gli elementi **sotto la diagonale** sono nulli.
$$
\left(\begin{matrix}
\textcolor{red}1 \ 7 \ 3 \\
0 \ \textcolor{red}2 \ 0  \\
0 \ 0\ \textcolor{red}1
\end{matrix}\right)
$$
* e se $n=m$
[TEOREMA] **Soluzione** **Sistema triangolare superiore quadrato**  
Un sistema triangolare superiore quadrato e' compatibile  se e solo se tutti gli elementi della diagonale sono non nulli, ossia ho **soluzione unica**

**Dimostrazione** $\rightarrow$: sostituendo a ritroso, a partire dall'equazione $n$-esima, si vede facilmente che la soluzione e' unica.
**Dimostrazione** $\leftarrow$: e' piu complicata.
## 3. Teoremi / risultati importanti
[TEOREMA] **Vettori come gruppo commutativo**  
* Idea: la somma di vettori si comporta come una somma “ben fatta”.  
* Ipotesi: vettori applicati nello stesso spazio.  
* Tesi: valgono associatività, elemento neutro, opposto e commutatività. 
* A cosa serve: giustifica il calcolo algebrico con i vettori.  
* Dimostrazione: presente in forma geometrica; da sapere almeno l’idea.

[TEOREMA] **Coordinate uniche nel piano**  
* Idea: se scelgo due direzioni non parallele, ogni vettore del piano si decompone lungo quelle due direzioni.  
* Ipotesi: $\vec i,\vec j$ non paralleli.  
* Tesi: ogni $\overrightarrow{OP}$ si scrive in modo unico come $x_1\vec i+x_2\vec j$.  
* A cosa serve: permette di passare dai vettori alle coordinate.  
* Dimostrazione: geometrica; da sapere l’idea.

[TEOREMA] **Sistemi triangolari superiori**  
* Idea: in un sistema triangolare superiore si risolve dal basso verso l’alto.  
* Ipotesi: sistema quadrato triangolare superiore.  
* Tesi: soluzione unica se e solo se gli elementi diagonali sono tutti diversi da zero.  
* A cosa serve: è la base del metodo di eliminazione di Gauss.  
* Dimostrazione: presente; da sapere almeno il ragionamento operativo.
## 4. Metodi operativi per esercizi
### Scrivere la retta passante per un punto e parallela a un vettore
1. Prendi il punto $P_0=(x_0,y_0)$.
2. Prendi il vettore direttore $\vec q=(\ell,m)$.
3. Scrivi:
$$ \begin{pmatrix}x\\ y\end{pmatrix} =  \begin{pmatrix}x_0\\y_0\end{pmatrix} + t \begin{pmatrix}\ell \\ m\end{pmatrix} $$
4. Passa alle equazioni parametriche:
* $x=x_0+t\ell$
* $y=y_0+tm$
---
### Scrivere la retta passante per due punti

1. Hai $P_1=(x_1,y_1)$ e $P_2=(x_2,y_2)$.
2. Calcola il vettore direttore:
$$
\vec q=P_2-P_1=  
\begin{pmatrix}  
x_2-x_1\\  
y_2-y_1  
\end{pmatrix}  
$$
3. Scrivi:
$$
\begin{pmatrix}x\\y\end{pmatrix} =\begin{pmatrix}x_1\\y_1\end{pmatrix} + t \begin{pmatrix} x_2-x_1\\ y_2-y_1 \end{pmatrix}  
$$
---
### Trovare l’intersezione di due rette nel piano
1. Scrivi le due rette in forma parametrica:
$$ P=P_0+t\vec q $$
$$ P=P'_0+s\vec q' $$
2. Uguaglia le coordinate.
3. Ottieni un sistema in $(t,s)$.
4. Risolvi il sistema.
5. Sostituisci il parametro trovato in una delle due rette.
6. Il punto ottenuto è il punto di intersezione.

---
### Scrivere il piano passante per un punto e parallelo a due vettori

1. Prendi un punto $P_0$.
2. Prendi due vettori non paralleli $\vec i,\vec j$.
3. Scrivi:
$$ \overrightarrow{OP}= \overrightarrow{OP_0} + t_1\vec i + t_2\vec j $$
4. Se richiesto, passa alle coordinate.

---

### Risolvere un sistema triangolare superiore
1. Parti dall’ultima equazione.
2. **Ricava l’ultima incognita**.
3. Sostituiscila nell’equazione precedente.
4. **Procedi dal basso verso l’alto**.
5. Se trovi un coefficiente diagonale nullo, controlla compatibilità e unicità.
## 5. Formule da ricordare
Coordinate di un vettore rispetto a due direzioni non parallele:
$$ \overrightarrow{OP}=x_1\vec i+x_2\vec j $$

Equazione vettoriale di una retta:
$$ \overrightarrow{OP} = \overrightarrow{OP_0}+t\vec q $$

Equazioni parametriche di una retta nel piano:
$$ x=x_0+t\ell,\qquad y=y_0+tm $$

Equazione vettoriale di un piano nello spazio:
$$ \overrightarrow{OP} =\overrightarrow{OP_0} + t_1\vec i + t_2\vec j $$

Forma matriciale di un sistema lineare:
$$ Ax=b $$

## 6. Note del professore
[NOTA PROF]  
Il vettore direttore di una retta **non è unico**: qualunque multiplo non nullo dello stesso vettore descrive la stessa direzione.

[NOTA PROF]  
Per costruire coordinate nel piano servono due vettori **non paralleli**. Se sono paralleli, non riescono a descrivere tutto il piano.

[NOTA PROF]  
L’intersezione tra rette viene trasformata in un problema algebrico: si uguagliano le due forme parametriche e si risolve un sistema.

## 7. Mini-checklist del PDF
Dopo questo PDF devo saper:
- definire vettore, somma di vettori e prodotto per scalare;
- usare la regola del parallelogramma;
- scrivere coordinate rispetto a due vettori non paralleli;
- scrivere l’equazione parametrica di una retta;
- scrivere la retta passante per due punti;
- trovare l’intersezione tra due rette tramite sistema;
- scrivere l’equazione vettoriale di un piano;
- riconoscere un sistema lineare in forma $Ax=b$;
- sapere quando un sistema è compatibile;
- risolvere un sistema triangolare superiore.
---
# PDF 2 — Eliminazione di Gauss, spazi vettoriali, sottospazi, span, basi
## 2. Concetti da sapere
[DEFINIZIONE] **Sistemi equivalenti**  
Due sistemi lineari sono equivalenti se hanno le stesse soluzioni.

[DEFINIZIONE] **Combinazione lineare di equazioni**  
Date due equazioni, posso sostituire una di esse con una combinazione lineare delle due:
$$ h\cdot(a)+k\cdot(b) $$
* con $h,k\in\mathbb{R}$, facendo attenzione alle condizioni indicate nel metodo.
* $a = a_{1}x_{1} + \dots a_{n}x_{n}$ ed $b = b_{1}x_{1} + \dots b_{n}x_{n}$

[METODO] **Eliminazione di Gauss**  
Serve a trasformare un sistema lineare in un sistema triangolare superiore equivalente.

[DEFINIZIONE] **Pivot**  
Il pivot è l’elemento non nullo usato per eliminare gli elementi sotto di lui nella stessa colonna.

[TEOREMA] **Sistema quadrato e pivot**  
Un sistema lineare quadrato ammette un’unica soluzione se e solo se ogni pivot è non nullo.

[DEFINIZIONE] **Matrice non singolare**  
Una matrice quadrata è detta non singolare se tutti i suoi pivot sono non nulli.

[DEFINIZIONE] **$\mathbb{R}^n$**  
$\mathbb{R}^n$ è l’insieme dei vettori colonna con $n$ componenti reali:

$$ \mathbb{R}^n= \left\{ \begin{pmatrix} v_1 \\ \vdots \\ v_n \end{pmatrix} : v_i\in\mathbb{R} \right\} $$

[DEFINIZIONE] **Spazio vettoriale su $\mathbb{R}$**  
Un insieme $V$, con somma e prodotto per scalare, è uno spazio vettoriale se soddisfa le proprietà usuali: associatività, commutatività della somma, elemento neutro, opposto, distributività, compatibilità del prodotto per scalare e $1v=v$.

[DEFINIZIONE] **Sottospazio vettoriale**  
Un sottoinsieme $W\subseteq V$ è un sottospazio se:
1. per ogni $w_1,w_2\in W$, $w_1+w_2\in W$;
2. per ogni $\lambda\in\mathbb{R}$ e $w\in W$, $\lambda w\in W$.
3. 
Da queste proprietà segue che:
* $0\in W$.
* $\forall w \in W \to -w \in W$

**Esempi**:
* sia $V = \mathbb R^2$, allora $W = \text{punti della retta passante per origine}$
* $W = \{ 0 \}$ e' sottospazio di ogni spazio vettoriale.

[TEOREMA] **Soluzioni di un sistema omogeneo**  
L’insieme delle soluzioni di un sistema lineare con termini noti tutti nulli è un sottospazio vettoriale.

> **infatti**: la somma di due soluzioni e' anch'essa una soluzione, ossia $a_{m_{1}}(v_{1}+w_{1}) + \dots + a_{mn})(v_{n}+ w_{n}) = 0$

[DEFINIZIONE] **Combinazione lineare di vettori**  
Dati $v_1,\dots,v_k\in V$, una combinazione lineare è un vettore del tipo:

$$ \alpha_1v_1+\dots+\alpha_kv_k $$

con $\alpha_1,\dots,\alpha_k\in\mathbb{R}$.

[DEFINIZIONE] **Span**  
Lo span di $v_1,\dots,v_k$ è l’insieme di tutte le loro combinazioni lineari:
$$ \operatorname{Span}(v_1,\dots,v_k) = \{ \alpha_1v_1+\dots+\alpha_kv_k: \alpha_i\in\mathbb{R} \} $$

[TEOREMA] **Lo span è un sottospazio**  
$\operatorname{Span}(v_1,\dots,v_k)$ è un sottospazio vettoriale di $V$.

[TEOREMA] **Compatibilità e colonne di $A$**  
Il sistema $Ax=b$ è compatibile se e solo se $b$ appartiene allo span delle colonne di $A$.

[DEFINIZIONE] **Dipendenza lineare**  
I vettori $v_1,\dots,v_k$ sono linearmente dipendenti se esistono coefficienti $\alpha_1,\dots,\alpha_k$, **non tutti nulli**, tali che:
$$ \alpha_1v_1+\dots+\alpha_kv_k=0 $$
* **OSS 4.6**: se $v_{1},\dots,v_{k}$ linearmente dipendenti $\exists a_{j}\neq 0$. dunque $v_{j} = \text{combinazione lineare degli altri vettori}$
* **conseguenza di OSS 4.6**: $\operatorname{Span}(v_{1},\dots,v_{n}) = \operatorname{Span}(v_{1},\dots,v_{j-1},v_{j+1},\dots, v_{n})$
[DEFINIZIONE] **Indipendenza lineare**  
I vettori sono linearmente indipendenti se l’unica combinazione lineare che dà il vettore nullo è quella **con tutti i coefficienti nulli**.
* **Prop 4.4**: $A\cdot x =0$ ha soluzione unica, $x=0$ se e solo se $A^1, \dots, A^n$ sono linearmente indipendenti.

[DEFINIZIONE] **Base**  
Un insieme $\{v_1,\dots,v_k\}\subseteq V$ è una base di $V$ se:
1. genera $V$:
$$ V=\operatorname{Span}(v_1,\dots,v_k) $$
2. è linearmente indipendente.

**esempio 4.14**: Quindi se $\{ v_{1},..,v_{k} \} \subseteq V$ sono lineramente indipendenti, allora $\text{Span}(v_{1},..,v_{k})$ e' sottospazio di $V$.

[TEOREMA] **Rappresentazione unica rispetto a una base**  
Se $\{v_1,\dots,v_k\}$ è una base di $V$, ogni vettore $v\in V$ si scrive in modo unico come:

$$ v=\alpha_1v_1+\dots+\alpha_kv_k $$
dunque: $av =bv \iff a= b$.

[DEFINIZIONE] **Coordinate rispetto a una base**  
Se $\mathcal{B}=\{v_1,\dots,v_k\}$ è una base di $V$, i coefficienti $\alpha_1,\dots,\alpha_k$ tali che:

$$ v=\alpha_1v_1+\dots+\alpha_kv_k $$

**allora $a_{1},\dots,a_{k}$ sono le coordinate di $v$ rispetto alla base $\mathcal{B}$.**

[DEFINIZIONE] **Sottoinsieme massimale linearmente indipendente**  
Dato $A\subseteq V$, un insieme $B\subseteq A$ è massimale linearmente indipendente se:
1. $B$ è linearmente indipendente;
2. aggiungendo a $B$ un altro elemento di $A$, l’insieme diventa linearmente dipendente.

[TEOREMA] **Base come insieme massimale indipendente**  
Un insieme è una base se e solo se è massimale linearmente indipendente.

## 3. Teoremi / risultati importanti

[TEOREMA] **Equivalenza tramite combinazioni lineari di equazioni**  
Idea: posso sostituire un’equazione con una combinazione lineare opportuna senza cambiare le soluzioni del sistema.  
Ipotesi: sostituzione fatta con coefficiente adatto, in particolare con $k\neq 0$ nella forma indicata negli appunti.  
Tesi: il sistema ottenuto è equivalente al precedente.  
A cosa serve: giustifica il metodo di Gauss.  
Dimostrazione: presente; da sapere almeno l’idea.

[TEOREMA] **Sistema quadrato con soluzione unica**  
Idea: durante Gauss, se tutti i pivot sono non nulli, si arriva a un sistema triangolare risolvibile univocamente.  
Ipotesi: sistema lineare quadrato.  
Tesi: soluzione unica se e solo se ogni pivot è non nullo.  
A cosa serve: riconoscere quando una matrice è non singolare e quando il sistema ha unica soluzione.  
Dimostrazione: non completamente sviluppata nel PDF; da sapere il risultato e il collegamento con Gauss.

[TEOREMA] **Soluzioni di un sistema omogeneo come sottospazio**  
Idea: se $v$ e $w$ sono soluzioni di $Ax=0$, allora anche $v+w$ e $\lambda v$ sono soluzioni.  
Ipotesi: sistema lineare con termini noti nulli.  
Tesi: l’insieme delle soluzioni è un sottospazio di $\mathbb{R}^n$.  
A cosa serve: collega sistemi lineari e spazi vettoriali.  
Dimostrazione: presente; da sapere.

[TEOREMA] **Lo span è un sottospazio**  
Idea: le combinazioni lineari sono chiuse rispetto a somma e prodotto per scalare.  
Ipotesi: $v_1,\dots,v_k\in V$.  
Tesi: $\operatorname{Span}(v_1,\dots,v_k)$ è sottospazio di $V$.  
A cosa serve: costruire sottospazi generati da vettori.  
Dimostrazione: presente; da sapere.

[TEOREMA] **Compatibilità di $Ax=b$ e span delle colonne**  
Idea: $Ax$ è una combinazione lineare delle colonne di $A$.  
Ipotesi: sistema lineare $Ax=b$.  
Tesi:
$$ Ax=b \text{ compatibile} \iff b\in\operatorname{Span}(A^1,\dots,A^n) $$
dove $A^1,\dots,A^n$ sono le colonne di $A$.  
A cosa serve: interpretare geometricamente un sistema lineare.  
Dimostrazione: presente in forma compatta; da sapere.

[TEOREMA] **Indipendenza delle colonne e sistema omogeneo**  
Idea: le colonne di $A$ sono linearmente indipendenti se l’unica soluzione di $Ax=0$ è $x=0$.  
Ipotesi: matrice $A$ con colonne $A^1,\dots,A^n$.  
Tesi:
$$ Ax=0 \text{ ha solo soluzione } x=0 \iff A^1,\dots,A^n \text{ sono linearmente indipendenti} $$
A cosa serve: testare indipendenza lineare con un sistema omogeneo.  
Dimostrazione: presente; da sapere.

[TEOREMA] **Rappresentazione unica in una base**  
Idea: una base genera tutto lo spazio senza ridondanze.  
Ipotesi: $\{v_1,\dots,v_k\}$ linearmente indipendente.  
Tesi: se due combinazioni lineari degli stessi vettori danno lo stesso vettore, allora i coefficienti coincidono.  
A cosa serve: definire bene le coordinate rispetto a una base.  
Dimostrazione: presente; da sapere.

[TEOREMA] **Base e massimalità**  
Idea: una base è un insieme indipendente che non può essere ampliato senza perdere l’indipendenza.  
Ipotesi: $B\subseteq V$.  
Tesi: $B$ è base se e solo se è massimale linearmente indipendente.  
A cosa serve: criterio teorico per riconoscere basi.  
Dimostrazione: iniziata/parziale nel PDF; [DUBBIO] se da sapere completa.

## 4. Metodi operativi per esercizi

### Applicare l’eliminazione di Gauss
1. Scrivi il sistema come matrice aumentata $[A|b]$.
2. Cerca un pivot non nullo nella prima colonna.
3. Se serve, scambia due righe.
4. Usa il pivot per annullare gli elementi sotto di lui.
5. Passa alla colonna successiva.
6. Ripeti fino a ottenere una matrice triangolare superiore.
7. Risolvi il sistema dal basso verso l’alto.

---

### Capire se un sistema quadrato ha soluzione unica
1. Applica Gauss.
2. Controlla i pivot.
3. Se tutti i pivot sono non nulli, il sistema ha soluzione unica.
4. Se almeno un pivot è nullo, non puoi concludere l’unicità: il sistema può avere zero o infinite soluzioni.

---

### Verificare se un insieme è sottospazio
Per controllare $W\subseteq V$:
1. Prendi due elementi generici $w_1,w_2\in W$.
2. Controlla se $w_1+w_2\in W$.
3. Prendi $\lambda\in\mathbb{R}$.
4. Controlla se $\lambda w_1\in W$.
5. Se entrambe le proprietà valgono, $W$ è sottospazio.

---

### Trovare lo span di alcuni vettori
1. Scrivi la combinazione lineare generica:
$$ \alpha_1v_1+\dots+\alpha_kv_k $$
2. Calcola le componenti.
3. Descrivi l’insieme ottenuto al variare dei coefficienti.
4. Se possibile, riconosci se è una retta, un piano, tutto $\mathbb{R}^n$, ecc.

---

### Verificare se $b$ appartiene allo span delle colonne di $A$
1. Scrivi le colonne di $A$: $A^1,\dots,A^n$.
2. Imposta:
$$ x_1A^1+\dots+x_nA^n=b $$
3. Questo equivale a risolvere $Ax=b$.
4. Se il sistema è compatibile, allora $b\in\operatorname{Span}(A^1,\dots,A^n)$.
5. Se il sistema è incompatibile, allora $b\notin\operatorname{Span}(A^1,\dots,A^n)$.

---

### Verificare indipendenza lineare
1. Dati $v_1,\dots,v_k$, imposta:
$$ \alpha_1v_1+\dots+\alpha_kv_k=0 $$
2. Risolvi il sistema nelle incognite $\alpha_1,\dots,\alpha_k$.
3. Se l’unica soluzione è:
$$ \alpha_1=\dots=\alpha_k=0 $$
allora i vettori sono linearmente indipendenti.
4. Se esiste una soluzione non banale, sono linearmente dipendenti.

---

### Trovare coordinate rispetto a una base
1. Hai una base $\mathcal{B}=\{v_1,\dots,v_k\}$.
2. Hai un vettore $v$.
3. Imposta:
$$ v=\alpha_1v_1+\dots+\alpha_kv_k $$
4. Risolvi il sistema per $\alpha_1,\dots,\alpha_k$.
5. I coefficienti trovati sono le coordinate di $v$ rispetto a $\mathcal{B}$.

## 5. Formule da ricordare

$$ Ax=b $$
Forma matriciale di un sistema lineare.

$$ \operatorname{Span}(v_1,\dots,v_k) = \{ \alpha_1v_1+\dots+\alpha_kv_k: \alpha_i\in\mathbb{R} \} $$
Insieme di tutte le combinazioni lineari dei vettori.

$$ \alpha_1v_1+\dots+\alpha_kv_k=0 $$
Equazione da usare per verificare dipendenza o indipendenza lineare.

$$ Ax=b \text{ compatibile} \iff b\in\operatorname{Span}(A^1,\dots,A^n) $$
Criterio di compatibilità tramite le colonne della matrice.

$$ Ax=0 \text{ ha solo } x=0 \iff A^1,\dots,A^n \text{ linearmente indipendenti} $$
Criterio di indipendenza lineare delle colonne.

$$ v=\alpha_1v_1+\dots+\alpha_kv_k $$
Espressione di un vettore rispetto a una base.

## 6. Note del professore

[NOTA PROF]  
Nell’eliminazione di Gauss è lecito scambiare l’ordine delle equazioni: il sistema rimane equivalente.

[NOTA PROF]  
L’obiettivo di Gauss è trasformare il sistema in uno triangolare superiore, non “risolvere a caso” le equazioni.

[NOTA PROF]  
I pivot sono centrali: se in un sistema quadrato tutti i pivot sono non nulli, c’è soluzione unica.

[NOTA PROF]  
Lo span va visto come l’insieme di tutti i vettori ottenibili combinando quelli di partenza.

[NOTA PROF]  
Se tra i vettori c’è il vettore nullo, l’insieme è automaticamente linearmente dipendente.

[NOTA PROF]  
Se due vettori dell’insieme sono uguali, l’insieme è linearmente dipendente.

[NOTA PROF]  
Le coordinate di uno stesso vettore cambiano se cambia la base.

[NON DA FARE]  
Non risultano indicate parti esplicitamente escluse in questo PDF.

[DUBBIO]  
La dimostrazione completa della proposizione “base se e solo se massimale linearmente indipendente” sembra solo iniziata nella pagina finale. Serve verificare se nei PDF successivi viene completata.

## 7. Mini-checklist del PDF

Dopo questo PDF devo saper:
- applicare l’eliminazione di Gauss;
- riconoscere pivot e matrici non singolari;
- capire quando un sistema quadrato ha soluzione unica;
- definire spazio vettoriale e sottospazio;
- verificare se un insieme è sottospazio;
- definire combinazione lineare e span;
- usare lo span per interpretare la compatibilità di $Ax=b$;
- verificare indipendenza e dipendenza lineare;
- definire base;
- trovare coordinate rispetto a una base;
- capire che le coordinate dipendono dalla base scelta.
# PDF 3 — Basi, dimensione, sottospazi, applicazioni lineari, rango e sistemi a scala
## 2. Concetti da sapere

[TEOREMA] **Da generatori a base**  
Se $B=\{v_1,\dots,v_r\}\subseteq V$ e $\operatorname{Span}(B)$ contiene un sistema di generatori di $V$, allora:

$$ V=\operatorname{Span}(B) $$

[TEOREMA] **Base da insieme massimale indipendente**  
Se $A=\{v_1,\dots,v_k\}$ è un sistema di generatori di $V$ e $B\subseteq A$ è massimale tra i sottoinsiemi linearmente indipendenti, allora $B$ è una base di $V$.

[METHOD] **Trovare una base da un insieme di generatori**  
Dato $V=\operatorname{Span}(v_1,\dots,v_k)$:

1. verifica quali vettori sono linearmente indipendenti;
2. elimina i vettori dipendenti;
3. conserva un sottoinsieme massimale indipendente;
4. quel sottoinsieme è una base di $V$.

[TEOREMA] **Teorema del completamento**  
Se $B=\{v_1,\dots,v_n\}$ è una base di $V$ e $w_1,\dots,w_p$ sono linearmente indipendenti, con $p\le n$, allora si possono aggiungere $n-p$ vettori della base $B$ a $w_1,\dots,w_p$ per ottenere una base di $V$.

[DEFINIZIONE] **Dimensione**  
Se $V$ ha una base con $n$ vettori, allora $n$ si chiama dimensione di $V$:

$$ \dim V=n $$

[TEOREMA] **Tutte le basi hanno lo stesso numero di elementi**  
Se $B$ e $C$ sono due basi dello stesso spazio vettoriale, allora hanno la stessa cardinalità.

[TEOREMA] **In dimensione $n$, ogni $n$-upla indipendente è base**  
Se $\dim V=n$, allora ogni insieme di $n$ vettori linearmente indipendenti è una base di $V$.

[TEOREMA] **Più di $n$ vettori sono dipendenti**  
Se $\dim V=n$, allora ogni insieme con più di $n$ vettori è linearmente dipendente.

[TEOREMA] **Sottospazi e dimensione**  
Se $W\subseteq V$, allora:

$$ \dim W\le \dim V $$

e

$$ \dim W=\dim V \iff W=V $$

[DEFINIZIONE] **Somma di sottospazi**  
Se $U,W\subseteq V$ sono sottospazi:

$$ U+W=\{u+w: u\in U,\ w\in W\} $$

Anche $U+W$ è un sottospazio.

[DEFINIZIONE] **Intersezione di sottospazi**  
Se $U,W\subseteq V$, allora:

$$ U\cap W $$

è l’insieme dei vettori che appartengono sia a $U$ sia a $W$. Anche $U\cap W$ è sottospazio.

[TEOREMA] **Formula di Grassmann**

$$ \dim(U+W)=\dim U+\dim W-\dim(U\cap W) $$

Serve per collegare dimensione della somma e dimensione dell’intersezione.

[TEOREMA] **Soluzioni di un sistema non omogeneo**  
Se $y^0$ è una soluzione di $Ax=b$, allora ogni soluzione è della forma:

$$ y=y^0+w $$

dove $w$ è soluzione del sistema omogeneo associato:

$$ Ax=0 $$

Quindi:

$$ \{x:Ax=b\}=y^0+\{x:Ax=0\} $$

[DEFINIZIONE] **Applicazione lineare**  
Una funzione $T:V\to W$ è lineare se:

$$ T(x+y)=T(x)+T(y) $$

$$ T(\lambda x)=\lambda T(x) $$

per ogni $x,y\in V$, $\lambda\in\mathbb{R}$.

[FORMULA] **Applicazione lineare associata a una matrice**  
Data $A\in M_{m,n}(\mathbb{R})$, si definisce:

$$ L_A:\mathbb{R}^n\to\mathbb{R}^m $$

$$ L_A(x)=Ax $$

Questa è un’applicazione lineare.

[TEOREMA] **Una lineare è determinata dai valori su una base**  
Se $\{v_1,\dots,v_n\}$ è una base di $V$ e $w_1,\dots,w_n\in W$, allora esiste un’unica applicazione lineare $T:V\to W$ tale che:

$$ T(v_i)=w_i $$

per ogni $i$.

[DEFINIZIONE] **Nucleo**

$$ \ker T=\{v\in V:T(v)=0\} $$

[DEFINIZIONE] **Immagine**

$$ \operatorname{Im}T=\{T(v):v\in V\} $$

[TEOREMA] **Nucleo e immagine sono sottospazi**  
Se $T:V\to W$ è lineare, allora:

$$ \ker T\subseteq V $$

$$ \operatorname{Im}T\subseteq W $$

sono sottospazi.

[TEOREMA] **Criterio di iniettività**

$$ T \text{ iniettiva} \iff \ker T=\{0\} $$

[DEFINIZIONE] **Rango di un’applicazione lineare**

$$ \operatorname{rg}T=\dim(\operatorname{Im}T) $$

[TEOREMA] **Teorema rango-nullità**

$$ \dim V=\dim(\ker T)+\operatorname{rg}T $$

[TEOREMA] **Rouché-Capelli**

Per un sistema $Ax=b$, indicando con $A'$ la matrice completa $(A|b)$:

$$ Ax=b \text{ ammette soluzioni} \iff \operatorname{rg}A=\operatorname{rg}A' $$

Inoltre, se il sistema ha $n$ incognite, la soluzione è unica quando:

$$ \operatorname{rg}A=n $$

[DEFINIZIONE] **Matrice a scala**  
Una matrice è a scala se i pivot si spostano progressivamente verso destra scendendo di riga, e sotto ogni pivot gli elementi sono nulli.

[TEOREMA] **Rango di una matrice a scala**  
Se una matrice a scala $S$ ha $r$ pivot, allora:

$$ \operatorname{rg}S=r $$

## 3. Teoremi / risultati importanti

[TEOREMA] **Teorema del completamento**  
Idea: un insieme indipendente può essere completato a una base aggiungendo vettori da una base già nota.  
Ipotesi: $B$ base di $V$, $w_1,\dots,w_p$ linearmente indipendenti.  
Tesi: esistono $n-p$ vettori di $B$ che, aggiunti ai $w_i$, formano una base.  
A cosa serve: costruire basi partendo da insiemi indipendenti.  
Dimostrazione: presente; da sapere almeno l’idea.

[TEOREMA] **Formula di Grassmann**  
Idea: quando sommo due sottospazi, la parte comune viene contata due volte, quindi va sottratta.  
Ipotesi: $U,W$ sottospazi di $V$, $V$ di dimensione finita.  
Tesi:

$$ \dim(U+W)=\dim U+\dim W-\dim(U\cap W) $$

A cosa serve: calcolare dimensioni di somme e intersezioni.  
Dimostrazione: presente; importante.

[TEOREMA] **Applicazione lineare determinata dalla base**  
Idea: per conoscere una funzione lineare basta sapere dove manda i vettori di una base.  
Ipotesi: $\{v_1,\dots,v_n\}$ base di $V$, vettori $w_1,\dots,w_n\in W$.  
Tesi: esiste un’unica lineare $T$ con $T(v_i)=w_i$.  
A cosa serve: costruire applicazioni lineari e dimostrare unicità.  
Dimostrazione: presente; da sapere.

[TEOREMA] **Nucleo, immagine e iniettività**  
Idea: il nucleo misura quali vettori vengono mandati a zero.  
Ipotesi: $T:V\to W$ lineare.  
Tesi:

$$ T \text{ iniettiva}\iff \ker T=\{0\} $$

A cosa serve: verificare iniettività risolvendo un sistema omogeneo.  
Dimostrazione: presente; da sapere.

[TEOREMA] **Teorema rango-nullità**  
Idea: la dimensione del dominio si divide tra parte che va a zero e parte effettivamente “visibile” nell’immagine.  
Ipotesi: $T:V\to W$ lineare, $V$ di dimensione finita.  
Tesi:

$$ \dim V=\dim\ker T+\operatorname{rg}T $$

A cosa serve: calcolare rango, dimensione del nucleo o dimensione dell’immagine.  
Dimostrazione: presente; importante.

[TEOREMA] **Rouché-Capelli**  
Idea: un sistema è compatibile quando aggiungere la colonna dei termini noti non aumenta il rango.  
Ipotesi: sistema $Ax=b$, matrice completa $A'=(A|b)$.  
Tesi:

$$ Ax=b \text{ compatibile}\iff \operatorname{rg}A=\operatorname{rg}A' $$

A cosa serve: stabilire se un sistema ha soluzioni e se sono uniche.  
Dimostrazione: presente in forma collegata a span/rango; da sapere.

## 4. Metodi operativi per esercizi

### Trovare una base di uno span

1. Metti i vettori come colonne di una matrice.
2. Riduci la matrice a scala.
3. Individua le colonne pivot.
4. I vettori originali corrispondenti alle colonne pivot formano una base dello span.
5. Il numero di pivot è la dimensione dello span.

---

### Verificare se un insieme è base

1. Conta quanti vettori hai.
2. Conosci o calcola $\dim V$.
3. Se hai esattamente $\dim V$ vettori, basta verificare l’indipendenza lineare.
4. Se sono indipendenti, sono una base.
5. Se sono dipendenti, non sono una base.

---

### Calcolare $\dim(U\cap W)$ con Grassmann

1. Trova $\dim U$.
2. Trova $\dim W$.
3. Trova $\dim(U+W)$, spesso mettendo insieme le basi di $U$ e $W$ e calcolando il rango.
4. Usa:

$$ \dim(U\cap W)=\dim U+\dim W-\dim(U+W) $$

---

### Verificare se una funzione è lineare

1. Controlla la somma:

$$ T(x+y)=T(x)+T(y) $$

2. Controlla il prodotto per scalare:

$$ T(\lambda x)=\lambda T(x) $$

3. Se entrambe valgono, $T$ è lineare.
4. Se anche una sola fallisce, $T$ non è lineare.

---

### Trovare nucleo di una matrice/applicazione

1. Scrivi $T(x)=0$.
2. Se $T=L_A$, risolvi:

$$ Ax=0 $$

3. Lo spazio delle soluzioni è $\ker T$.
4. Una base del nucleo si ottiene parametrizzando le soluzioni.

---

### Trovare immagine di una matrice/applicazione

1. Se $T=L_A$, considera le colonne di $A$.
2. L’immagine è lo span delle colonne:

$$ \operatorname{Im}A=\operatorname{Span}(A^1,\dots,A^n) $$

3. Riduci a scala per trovare le colonne pivot.
4. Le colonne pivot originali formano una base dell’immagine.
5. Il numero di pivot è il rango.

---

### Usare rango-nullità

Per $T:V\to W$:

1. Calcola $\dim V$.
2. Calcola $\dim\ker T$ oppure $\operatorname{rg}T$.
3. Usa:

$$ \dim V=\dim\ker T+\operatorname{rg}T $$

4. Ricava il valore mancante.

---

### Studiare un sistema con Rouché-Capelli

1. Scrivi la matrice dei coefficienti $A$.
2. Scrivi la matrice completa $A'=(A|b)$.
3. Calcola $\operatorname{rg}A$.
4. Calcola $\operatorname{rg}A'$.
5. Se i ranghi sono diversi, il sistema è incompatibile.
6. Se i ranghi sono uguali, il sistema è compatibile.
7. Se inoltre $\operatorname{rg}A=n$, con $n$ numero di incognite, la soluzione è unica.
8. Se $\operatorname{rg}A<n$, ci sono infinite soluzioni con parametri liberi.

## 5. Formule da ricordare

$$ \dim V=n $$
Numero di vettori di una base di $V$.

$$ \dim(U+W)=\dim U+\dim W-\dim(U\cap W) $$
Formula di Grassmann.

$$ \{x:Ax=b\}=y^0+\ker A $$
Soluzioni di un sistema non omogeneo.

$$ L_A(x)=Ax $$
Applicazione lineare associata a una matrice.

$$ \ker T=\{v\in V:T(v)=0\} $$
Nucleo.

$$ \operatorname{Im}T=\{T(v):v\in V\} $$
Immagine.

$$ \operatorname{rg}T=\dim(\operatorname{Im}T) $$
Rango.

$$ \dim V=\dim\ker T+\operatorname{rg}T $$
Teorema rango-nullità.

$$ Ax=b \text{ compatibile} \iff \operatorname{rg}A=\operatorname{rg}(A|b) $$
Rouché-Capelli.

$$ \operatorname{rg}S=\text{numero di pivot di }S $$
Rango di una matrice a scala.

## 6. Note del professore

[NOTA PROF]  
Per trovare una base di uno spazio generato da vettori, non bisogna tenere tutti i generatori: bisogna eliminare quelli dipendenti e conservare un insieme massimale indipendente.

[NOTA PROF]  
Le coordinate di un vettore dipendono dalla base scelta; lo stesso vettore può avere coordinate diverse in basi diverse.

[NOTA PROF]  
Per calcolare basi e dimensioni, il metodo pratico centrale è la riduzione a scala.

[NOTA PROF]  
Il nucleo di $L_A$ coincide con le soluzioni di $Ax=0$.

[NOTA PROF]  
L’immagine di $L_A$ è lo spazio generato dalle colonne di $A$.

[NOTA PROF]  
Il rango si può vedere come dimensione dell’immagine.

[NOTA PROF]  
Un sistema compatibile non ha per forza soluzione unica: serve anche controllare se il rango è uguale al numero di incognite.

[NON DA FARE]  
Non risultano indicate parti esplicitamente escluse in questo PDF.

## 7. Mini-checklist del PDF

Dopo questo PDF devo saper:

- estrarre una base da un insieme di generatori;
- usare il teorema del completamento;
- definire dimensione;
- usare i criteri su basi, indipendenza e dimensione;
- calcolare somma e intersezione di sottospazi;
- applicare la formula di Grassmann;
- riconoscere e costruire applicazioni lineari;
- trovare nucleo e immagine;
- calcolare il rango;
- usare il teorema rango-nullità;
- applicare Rouché-Capelli;
- risolvere sistemi tramite riduzione a scala.
# PDF 4 — Rango, prodotto di matrici, invertibilità e determinanti

## 1. Cosa tratta

Questo PDF chiude la parte su rango e sistemi lineari, poi introduce il prodotto di matrici e il legame tra composizione di applicazioni lineari e prodotto matriciale. La parte centrale riguarda le matrici invertibili e le condizioni equivalenti all’invertibilità. Infine introduce i determinanti: definizione tramite proprietà, calcolo con triangolari e sviluppi di Laplace, teorema di Binet e regola di Cramer.

## 2. Concetti da sapere

[TEOREMA] **Riduzione a scala e rango**  
Se $S$ è una riduzione a scala di $A$, allora:

$$ \operatorname{rg}A=\operatorname{rg}S $$

Inoltre, le colonne pivot corrispondenti danno una base dell’immagine di $A$.

[METODO] **Tecniche di calcolo per basi e dimensioni**  
Per trovare base e dimensione di:

$$ \operatorname{Span}(v_1,\dots,v_k) $$

si mettono i vettori in matrice e si riduce a scala.

Per trovare base e dimensione di $U+W$, si mettono insieme generatori di $U$ e $W$ e si calcola il rango.

Per trovare $\dim(U\cap W)$, si può usare Grassmann:

$$ \dim(U\cap W)=\dim U+\dim W-\dim(U+W) $$

[DEFINIZIONE] **Prodotto di matrici**  
Se:

$$ A\in M_{m,n}(\mathbb{R}), \qquad B\in M_{n,p}(\mathbb{R}) $$

allora:

$$ AB\in M_{m,p}(\mathbb{R}) $$

e l’elemento $(i,j)$ di $AB$ è:

$$ (AB)_{ij}=A_i\cdot B^j $$

cioè prodotto tra la riga $i$-esima di $A$ e la colonna $j$-esima di $B$.

[TEOREMA] **Composizione e prodotto matriciale**

$$ L_A\circ L_B=L_{AB} $$

Il prodotto di matrici rappresenta la composizione di applicazioni lineari.

[FORMULA] **Proprietà del prodotto di matrici**

$$ A(B+C)=AB+AC $$

$$ (A+B)C=AC+BC $$

$$ (\lambda A)B=\lambda(AB) $$

$$ (AB)C=A(BC) $$

$$ AI=IA=A $$

$$ A0=0A=0 $$

$$ (AB)^T=B^TA^T $$

[DEFINIZIONE] **Matrice invertibile**  
Una matrice quadrata $A\in M_{n,n}(\mathbb{R})$ è invertibile se esiste $B\in M_{n,n}(\mathbb{R})$ tale che:

$$ AB=BA=I_n $$

La matrice $B$ è unica e si indica con:

$$ A^{-1} $$

[FORMULA] **Inverse notevoli**

$$ (A^{-1})^{-1}=A $$

$$ (A^T)^{-1}=(A^{-1})^T $$

$$ (AB)^{-1}=B^{-1}A^{-1} $$

[TEOREMA] **Condizioni equivalenti all’invertibilità**  
Per $A\in M_{n,n}(\mathbb{R})$, sono equivalenti:

1. $A$ è invertibile;
2. $L_A$ è invertibile;
3. $L_A$ è iniettiva;
4. $L_A$ è suriettiva;
5. $\operatorname{rg}A=n$;
6. le colonne di $A$ sono linearmente indipendenti;
7. le righe di $A$ sono linearmente indipendenti;
8. $Ax=0$ ha unica soluzione $x=0$;
9. per ogni $b\in\mathbb{R}^n$, $Ax=b$ ha unica soluzione;
10. tutti i pivot di $A$ sono non nulli.

[METODO] **Calcolare l’inversa con Gauss**  
Per trovare $A^{-1}$:

1. costruisci la matrice aumentata:

$$ (A\mid I_n) $$

2. applica Gauss fino a trasformare $A$ in $I_n$;
3. ottieni:

$$ (I_n\mid B) $$

4. allora:

$$ B=A^{-1} $$

[DEFINIZIONE] **Determinante ($2\times 2$)**  
Per:

$$ A= \begin{pmatrix} x & y\\ z & w \end{pmatrix} $$

$$ \det A=xw-yz $$

[TEOREMA] **Invertibilità ($2\times 2$)**  
Una matrice $2\times 2$ è invertibile se e solo se:

$$ \det A\neq 0 $$

[PROPRIETÀ] **Proprietà caratterizzanti del determinante**  
Il determinante è una funzione che soddisfa:

1. se una riga è nulla, allora $\det A=0$;
2. moltiplicare una riga per $\lambda$ moltiplica il determinante per $\lambda$;
3. aggiungere a una riga un multiplo di un’altra riga non cambia il determinante;
4. $\det I_n=1$.

[TEOREMA] **Determinante di una matrice triangolare superiore**  
Se $A$ è triangolare superiore, allora:

$$ \det A=a_{11}a_{22}\cdots a_{nn} $$

[DEFINIZIONE] **Minore ($A_{ij}$)**  
Il minore $A_{ij}$ è la matrice ottenuta cancellando la riga $i$ e la colonna $j$ da $A$.

[TEOREMA] **Sviluppo di Laplace**

$$ \det A a_{i1}\det(A_{i1}) a_{i2}\det(A_{i2}) +\dots+ (-1)^{i+n}a_{in}\det(A_{in}) $$

Lo sviluppo si può fare lungo qualunque riga o colonna.

[TEOREMA] **Trasposta e determinante**

$$ \det(A^T)=\det(A) $$

[TEOREMA] **Binet**

$$ \det(AB)=\det(A)\det(B) $$

[TEOREMA] **Cramer**  
Per un sistema quadrato $Ax=b$ con $\det A\neq 0$, l’unica soluzione è:

$$ x_i=\frac{\det B_i}{\det A} $$

dove $B_i$ è la matrice ottenuta sostituendo alla colonna $i$-esima di $A$ la colonna $b$.

## 3. Teoremi / risultati importanti

[TEOREMA] **Composizione di applicazioni lineari e prodotto matriciale**  
Idea: moltiplicare matrici equivale a comporre le applicazioni lineari associate.  
Ipotesi: $A\in M_{m,n}$, $B\in M_{n,p}$.  
Tesi:

$$ L_A\circ L_B=L_{AB} $$

A cosa serve: capire perché il prodotto di matrici è definito riga per colonna.  
Dimostrazione: presente con esempio; da sapere.

[TEOREMA] **Equivalenze dell’invertibilità**  
Idea: per matrici quadrate, invertibilità, rango massimo, pivot non nulli, indipendenza delle colonne e unicità delle soluzioni sono lo stesso fenomeno.  
Ipotesi: $A\in M_{n,n}(\mathbb{R})$.  
Tesi: equivalenza delle condizioni elencate sopra.  
A cosa serve: riconoscere invertibilità in molti modi diversi.  
Dimostrazione: presente in parte; da sapere almeno le equivalenze e i collegamenti principali.

[TEOREMA] **Determinante di triangolare superiore**  
Idea: con Gauss posso ridurre a triangolare e il determinante diventa il prodotto degli elementi diagonali.  
Ipotesi: $A$ triangolare superiore.  
Tesi:

$$ \det A=\prod_i a_{ii} $$

A cosa serve: calcolo rapido del determinante.  
Dimostrazione: presente; utile.

[TEOREMA] **Sviluppo di Laplace**  
Idea: il determinante di ordine $n$ si riduce a determinanti di ordine $n-1$.  
Ipotesi: matrice quadrata.  
Tesi: si può sviluppare lungo qualunque riga o colonna con i segni alternati.  
A cosa serve: calcolare determinanti, soprattutto se ci sono molti zeri.  
Dimostrazione: indicata tramite induzione; da sapere il metodo.

[TEOREMA] **Binet**  
Idea: il determinante del prodotto è il prodotto dei determinanti.  
Ipotesi: $A,B\in M_{n,n}(\mathbb{R})$.  
Tesi:

$$ \det(AB)=\det(A)\det(B) $$

A cosa serve: capire invertibilità del prodotto e semplificare calcoli.  
Dimostrazione: presente in forma schematica; [DUBBIO] se richiesta completa.

[TEOREMA] **Cramer**  
Idea: in un sistema quadrato invertibile, ogni incognita si ottiene come rapporto tra due determinanti.  
Ipotesi: $Ax=b$, $A$ quadrata, $\det A\neq 0$.  
Tesi:

$$ x_i=\frac{\det B_i}{\det A} $$

A cosa serve: risolvere sistemi quadrati piccoli o dimostrare risultati teorici.  
Dimostrazione: presente; da sapere almeno formula e ipotesi.

## 4. Metodi operativi per esercizi

### Calcolare il prodotto di due matrici

1. Controlla le dimensioni:

$$ A\in M_{m,n},\quad B\in M_{n,p} $$

2. Il prodotto $AB$ esiste solo se il numero di colonne di $A$ coincide con il numero di righe di $B$.
3. Il risultato è in $M_{m,p}$.
4. Calcola ogni elemento con:

$$ (AB)_{ij}=A_i\cdot B^j $$

---

### Verificare se una matrice quadrata è invertibile

Puoi usare uno di questi criteri:

1. riduci a scala e controlla i pivot;
2. calcola il rango e verifica se $\operatorname{rg}A=n$;
3. verifica se $Ax=0$ ha solo soluzione nulla;
4. controlla se le colonne sono linearmente indipendenti;
5. calcola il determinante e verifica se $\det A\neq 0$.

---

### Calcolare l’inversa con Gauss

1. Scrivi:

$$ (A\mid I_n) $$

2. Applica operazioni elementari di riga.
3. Cerca di ottenere:

$$ (I_n\mid B) $$

4. Se ci riesci, $B=A^{-1}$.
5. Se non riesci a trasformare $A$ in $I_n$, allora $A$ non è invertibile.

---

### Calcolare un determinante con Gauss

1. Usa operazioni di riga per arrivare a una matrice triangolare superiore.
2. Ricorda gli effetti sul determinante:
    - scambiare due righe cambia segno;
    - moltiplicare una riga per $\lambda$ moltiplica il determinante per $\lambda$;
    - sommare a una riga un multiplo di un’altra non cambia il determinante.
3. Alla fine moltiplica gli elementi diagonali.
4. Correggi il risultato in base alle operazioni fatte.

---

### Calcolare un determinante con Laplace

1. Scegli una riga o colonna con molti zeri.
2. Per ogni elemento non nullo $a_{ij}$, cancella riga $i$ e colonna $j$.
3. Calcola il minore $A_{ij}$.
4. Usa il segno:

$$ (-1)^{i+j} $$

5. Somma i contributi:

$$ a_{ij}(-1)^{i+j}\det(A_{ij}) $$

---

### Usare Cramer

1. Verifica che $A$ sia quadrata.
2. Calcola $\det A$.
3. Se $\det A=0$, Cramer non si applica.
4. Per ogni incognita $x_i$, costruisci $B_i$ sostituendo la colonna $i$-esima di $A$ con $b$.
5. Calcola:

$$ x_i=\frac{\det B_i}{\det A} $$

## 5. Formule da ricordare

$$ (AB)_{ij}=A_i\cdot B^j $$

Prodotto riga per colonna.

$$ L_A\circ L_B=L_{AB} $$

Prodotto matriciale come composizione.

$$ (AB)^T=B^TA^T $$

Trasposta del prodotto.

$$ AB=BA=I_n $$

Definizione di inversa.

$$ (A^{-1})^{-1}=A $$

$$ (A^T)^{-1}=(A^{-1})^T $$

$$ (AB)^{-1}=B^{-1}A^{-1} $$

Formule sulle inverse.

$$ \det \begin{pmatrix} x & y\\ z & w \end{pmatrix} xw-yz $$

Determinante $2\times2$.

$$ A \text{ invertibile} \iff \det A\neq 0 $$

Criterio tramite determinante.

$$ \det A=a_{11}a_{22}\cdots a_{nn} $$

Per matrici triangolari superiori.

$$ \det(A^T)=\det(A) $$

Determinante della trasposta.

$$ \det(AB)=\det(A)\det(B) $$

Teorema di Binet.

$$ x_i=\frac{\det B_i}{\det A} $$

Regola di Cramer.

## 6. Note del professore

[NOTA PROF]  
Nel prodotto $AB$, l’ordine conta: in generale $AB\neq BA$, e a volte uno dei due prodotti può non essere nemmeno definito.

[NOTA PROF]  
L’inversa, se esiste, è unica.

[NOTA PROF]  
Per calcolare l’inversa si usa Gauss sulla matrice aumentata $(A\mid I_n)$.

[NOTA PROF]  
Per l’invertibilità di una matrice quadrata, puoi scegliere il criterio più comodo: pivot, rango, determinante, colonne indipendenti, sistema omogeneo.

[NOTA PROF]  
Nel calcolo del determinante con Laplace conviene scegliere righe o colonne con molti zeri.

[NOTA PROF]  
Cramer si applica solo se $\det A\neq 0$.

[NON DA FARE]  
Non risultano indicate parti esplicitamente escluse in questo PDF.

[DUBBIO]  
La dimostrazione completa del teorema di Binet è molto schematica negli appunti: non è chiaro se il professore richieda la dimostrazione completa o solo enunciato e uso.

## 7. Mini-checklist del PDF

Dopo questo PDF devo saper:

- calcolare rango e basi tramite riduzione a scala;
- calcolare il prodotto di matrici;
- collegare prodotto matriciale e composizione di applicazioni lineari;
- definire matrice invertibile;
- conoscere le equivalenze dell’invertibilità;
- calcolare un’inversa con Gauss;
- calcolare determinanti $2\times2$ e $3\times3$;
- usare le proprietà del determinante nelle operazioni di riga;
- calcolare determinanti con Laplace;
- usare $\det(A^T)=\det(A)$;
- usare Binet;
- applicare Cramer quando $\det A\neq 0$.
# PDF 5 — Teorema degli orlati, autovalori, autovettori, diagonalizzabilità

## 1. Cosa tratta

Questo PDF chiude la parte sul rango con il **teorema degli orlati**, utile per calcolare il rango tramite sottomatrici quadrate non singolari. Poi introduce la parte sugli **autovalori e autovettori** di un’applicazione lineare $T:V\to V$. Vengono definiti spettro, autospazi, diagonalizzabilità e triangolabilità, con esempi pratici sul calcolo degli autovalori tramite determinante.

## 2. Concetti da sapere

[DEFINIZIONE] **Sottomatrice quadrata di ordine $p$**  
Data una matrice $A\in M_{m,n}(\mathbb{R})$, una sottomatrice quadrata di ordine $p$ si ottiene scegliendo solo $p$ righe e $p$ colonne di $A$.
Esempio: da una matrice più grande posso estrarre una matrice $2\times 2$, $3\times 3$, ecc.

[DEFINIZIONE] **Orlare una sottomatrice**  
Orlare una sottomatrice $A'$ significa aggiungere una riga e una colonna della matrice di partenza, ottenendo una sottomatrice quadrata di ordine superiore.

[TEOREMA] **Teorema degli orlati**  
Se $A\in M_{m,n}(\mathbb{R})$ e $\operatorname{rg}(A)\ge r$, allora:
$$ \operatorname{rg}(A)=r $$
se e solo se esiste una sottomatrice $A'$ di ordine $r$ non singolare e tutte le sottomatrici di ordine $r+1$ ottenute orlando $A'$ sono singolari.

[DEFINIZIONE] **Autovettore**  
Sia $T:V\to V$ un’applicazione lineare. Un vettore $x\neq 0$ è autovettore di $T$ se esiste $\lambda\in\mathbb{R}$ tale che:
$$ T(x)=\lambda x $$

[DEFINIZIONE] **Autovalore**  
Il numero $\lambda$ è un autovalore di $T$ se esiste almeno un vettore $x\neq 0$ tale che:
$$ T(x)=\lambda x $$

[DEFINIZIONE] **Spettro**
$$ \operatorname{sp}(T) $$
è l’insieme degli autovalori di $T$.

[DEFINIZIONE] **Autospazio associato a $\lambda$**
$$ V_\lambda=\{v\in V:T(v)=\lambda v\} $$
Equivalentemente:
$$ V_\lambda=\ker(T-\lambda \operatorname{id}) $$

[NOTA]  
$\lambda$ è autovalore se e solo se:
$$ V_\lambda\neq \{0\} $$
cioè se il nucleo di $T-\lambda \operatorname{id}$ contiene vettori non nulli.

[FORMULA] **Criterio matriciale per autovalori**  
Se $T=L_A$, allora $\lambda$ è autovalore se e solo se:
$$ \ker(A-\lambda I)\neq \{0\} $$
cioè se:
$$ A-\lambda I $$
è singolare.
In termini di determinante:
$$ \det(A-\lambda I)=0 $$

[DEFINIZIONE] **Diagonalizzabilità**  
Un’applicazione lineare $T:V\to V$ è diagonalizzabile se esiste una base di $V$ composta da autovettori di $T$.

[DEFINIZIONE] **Triangolabilità**  
Un’applicazione lineare $T:V\to V$ è triangolabile se esiste una base di $V$ rispetto alla quale la matrice di $T$ è triangolare superiore.

## 3. Teoremi / risultati importanti

[TEOREMA] **Teorema degli orlati**  
Idea: per calcolare il rango non serve controllare tutte le sottomatrici possibili; basta trovare una sottomatrice non singolare di ordine $r$ e controllare gli orlati di ordine $r+1$.  
Ipotesi: $A\in M_{m,n}(\mathbb{R})$, $\operatorname{rg}(A)\ge r$, $A'$ sottomatrice di ordine $r$ non singolare.  
Tesi: $\operatorname{rg}(A)=r$ se e solo se tutti gli orlati di $A'$ di ordine $r+1$ sono singolari.  
A cosa serve: metodo pratico per calcolare il rango tramite determinanti.  
Dimostrazione: non sviluppata nel PDF; da sapere soprattutto enunciato e uso.

[TEOREMA] **Autovalore tramite nucleo**  
Idea: $T(v)=\lambda v$ equivale a $(T-\lambda\operatorname{id})(v)=0$.  
Ipotesi: $T:V\to V$ lineare.  
Tesi:
$$ \lambda \text{ autovalore} \iff \ker(T-\lambda\operatorname{id})\neq\{0\} $$
A cosa serve: trasforma la ricerca degli autovalori in un problema di sistemi lineari.  
Dimostrazione: immediata; da sapere.

[TEOREMA] **Autovalore tramite determinante**  
Idea: per avere autovettori non nulli, il sistema omogeneo $(A-\lambda I)x=0$ deve avere soluzioni non banali.  
Ipotesi: $A$ matrice quadrata associata a $T$.  
Tesi:
$$ \lambda \text{ autovalore} \iff \det(A-\lambda I)=0 $$
A cosa serve: calcolare gli autovalori.  
Dimostrazione: collegata al criterio di invertibilità/singolarità; da sapere.

[TEOREMA] **Diagonalizzabilità**  
Idea: $T$ è diagonalizzabile quando posso scegliere una base fatta interamente di autovettori.  
Ipotesi: $T:V\to V$ lineare.  
Tesi: esiste una base di autovettori; in quella base la matrice di $T$ è diagonale.  
A cosa serve: semplifica la matrice dell’applicazione lineare.  
Dimostrazione: non sviluppata qui; da sapere la definizione e il significato operativo.

## 4. Metodi operativi per esercizi

### Calcolare il rango con il teorema degli orlati
1. Cerca una sottomatrice quadrata $A'$ di ordine $r$ con determinante non nullo.
2. Questo garantisce:
$$ \operatorname{rg}(A)\ge r $$
3. Orla $A'$, cioè aggiungi una riga e una colonna per ottenere sottomatrici di ordine $r+1$.
4. Calcola i determinanti degli orlati.
5. Se tutti gli orlati sono singolari, cioè hanno determinante zero, allora:
$$ \operatorname{rg}(A)=r $$
6. Se almeno un orlato ha determinante non nullo, allora il rango è almeno $r+1$.

---

### Trovare gli autovalori di una matrice
1. Parti da una matrice quadrata $A$.
2. Costruisci:
$$ A-\lambda I $$
3. Calcola:
$$ \det(A-\lambda I) $$
4. Risolvi:
$$ \det(A-\lambda I)=0 $$
5. Le soluzioni $\lambda$ sono gli autovalori.

---

### Trovare l’autospazio associato a un autovalore
1. Prendi un autovalore $\lambda$.
2. Risolvi il sistema omogeneo:
$$ (A-\lambda I)x=0 $$
3. Lo spazio delle soluzioni è:
$$ V_\lambda=\ker(A-\lambda I) $$
4. Una base delle soluzioni è una base dell’autospazio.
5. I vettori non nulli di $V_\lambda$ sono autovettori associati a $\lambda$.

---

### Verificare se una matrice/applicazione è diagonalizzabile
1. Trova tutti gli autovalori.
2. Per ogni autovalore $\lambda$, calcola l’autospazio:
$$ V_\lambda=\ker(A-\lambda I) $$
3. Trova basi degli autospazi.
4. Metti insieme gli autovettori trovati.
5. Se riesci a ottenere una base di tutto $V$, allora $T$ è diagonalizzabile.
6. Se non riesci a ottenere abbastanza autovettori indipendenti, $T$ non è diagonalizzabile.

---

### Costruire la matrice di $T$ rispetto a una base di autovettori
1. Scegli una base:
$$ \mathcal{B}=\{v_1,\dots,v_n\} $$
composta da autovettori.
2. Per ogni $v_i$, calcola:
$$ T(v_i)=\lambda_i v_i $$
3. La matrice di $T$ rispetto a $\mathcal{B}$ è diagonale:
$$ \begin{pmatrix} \lambda_1 & 0 & \cdots & 0\\ 0 & \lambda_2 & \cdots & 0\\ \vdots & \vdots & \ddots & \vdots\\ 0 & 0 & \cdots & \lambda_n \end{pmatrix} $$

---

### Verificare se $T$ è triangolabile
1. Cerca una base di $V$ rispetto alla quale la matrice di $T$ sia triangolare superiore.
2. Se esiste, $T$ è triangolabile.
3. In questo PDF è data la definizione, ma non un criterio completo di calcolo.  
[DUBBIO] Il metodo operativo completo potrebbe comparire nei PDF successivi.

## 5. Formule da ricordare

$$ T(x)=\lambda x $$
Definizione di autovettore e autovalore.

$$ V_\lambda=\{v\in V:T(v)=\lambda v\} $$
Autospazio associato a $\lambda$.

$$ V_\lambda=\ker(T-\lambda\operatorname{id}) $$
Autospazio come nucleo.

$$ \lambda\in\operatorname{sp}(T) \iff V_\lambda\neq\{0\} $$
Criterio per essere autovalore.

$$ \lambda\in\operatorname{sp}(A) \iff \ker(A-\lambda I)\neq\{0\} $$
Criterio matriciale tramite nucleo.

$$ \det(A-\lambda I)=0 $$
Equazione caratteristica per trovare gli autovalori.

$$ T \text{ diagonalizzabile} \iff \exists \text{ base di } V \text{ composta da autovettori di }T $$
Definizione operativa di diagonalizzabilità.

## 6. Note del professore

[NOTA PROF]  
Nel teorema degli orlati, una sottomatrice non singolare di ordine $r$ mostra che il rango è almeno $r$; per concludere che il rango è esattamente $r$, bisogna controllare gli orlati di ordine $r+1$.

[NOTA PROF]  
Un autovettore non può essere il vettore nullo. L’autospazio invece contiene sempre anche il vettore nullo, perché è un nucleo.

[NOTA PROF]  
L’autovalore $\lambda$ si cerca imponendo che $T-\lambda\operatorname{id}$ non sia iniettiva, cioè abbia nucleo non banale.

[NOTA PROF]  
Nel caso matriciale, questo diventa il controllo di singolarità di $A-\lambda I$, quindi:
$$ \det(A-\lambda I)=0 $$

[NOTA PROF]  
La diagonalizzabilità dipende dall’esistenza di una base di autovettori, non solo dall’esistenza di qualche autovettore.

[NON DA FARE]  
Non risultano indicate parti esplicitamente escluse in questo PDF.

[DUBBIO]  
La triangolabilità viene solo definita alla fine del PDF; non è ancora chiaro dai materiali se sarà sviluppata con criteri e teoremi nei PDF successivi.

## 7. Mini-checklist del PDF

Dopo questo PDF devo saper:
- definire sottomatrice quadrata e orlato;
- usare il teorema degli orlati per calcolare il rango;
- definire autovalore e autovettore;
- ricordare che un autovettore deve essere non nullo;
- definire spettro e autospazio;
- usare $V_\lambda=\ker(T-\lambda\operatorname{id})$;
- calcolare gli autovalori tramite $\det(A-\lambda I)=0$;
- calcolare gli autospazi risolvendo $(A-\lambda I)x=0$;
- capire cosa significa diagonalizzabile;
- capire cosa significa triangolabile.
