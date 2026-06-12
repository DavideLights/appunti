**retta ortogonale** alle rette $r_{1},r_{2}$ che passa per un punto **P**: *e' la retta che ha come vettore direttore i coefficienti di $ax+by+cz+\dots$ equazione del piano parallelo ad $r_{1},r_{2}$.* il punto di riferimento rispetto all'origine sara $P$, dunque $\overrightarrow{OP}$

**Scrivere la retta passante per un punto e parallela a un vettore**: 
* $P_{0} = (x_{0},y_{0})$
* $\vec{q} = (l,m)$
$$ \begin{pmatrix}x\\ y\end{pmatrix} =  \begin{pmatrix}x_0\\y_0\end{pmatrix} + t \begin{pmatrix}\ell \\ m\end{pmatrix} $$

**Retta passante per due punti**:
$$
\begin{pmatrix}x\\y\end{pmatrix} =\begin{pmatrix}x_1\\y_1\end{pmatrix} + t \begin{pmatrix} x_2-x_1\\ y_2-y_1 \end{pmatrix}
$$
**Piano passante per un punto e parallelo a due vettori**:
$$ \overrightarrow{OP}= \overrightarrow{OP_0} + t_1\vec i + t_2\vec j $$

**determinare piano passante per** $A,B,C$: $\pi: \overrightarrow{OA} + t\overrightarrow{AB} + s\overrightarrow{AC}$
# da applicazioni a vettori

### Come si passa da Applicazione a Matrice?
Per "catturare" completamente il comportamento di questa funzione e racchiuderlo in una matrice, si usa un trucco: **si guarda cosa fa la funzione ai vettori della base canonica** dello spazio di partenza.

I passaggi sono tre:
1. **Prendi i vettori della base canonica** dello spazio di partenza (chiamiamoli e1​,e2​,…).
2. Nutri la funzione f con questi vettori e calcola i risultati: $f(e_1​),f(e_2​), \dots$
3. Prendi questi vettori risultanti e **mettili in colonna**, uno di fianco all'altro. La tabella che ottieni è la matrice associata all'applicazione.

### Un esempio pratico
Prendiamo una funzione $f:R^2→R^2$ definita così:
$f(x,y​)= \begin{vmatrix}2x + 3y \\ x-y\end{vmatrix}$

Ora affianchiamo i risultati per creare le colonne della matrice $A$:
![[Pasted image 20260611015130.png]]
Ossia:
$$
A = \begin{vmatrix}
2 \ 3 \\ 1 \ -1
\end{vmatrix}
$$

Moltiplicare questa matrice per un qualsiasi vettore (xy​) farà esattamente lo stesso identico lavoro della funzione originale.

## 2. Cosa simboleggiano le Colonne?

> **Significato geometrico:** Le colonne descrivono come la trasformazione deforma lo spazio di partenza. Se le colonne sono linearmente indipendenti, lo spazio mantiene le sue dimensioni; se sono dipendenti (matrice singolare), lo spazio si schiaccia.
## 3. Cosa simboleggiano le Righe?

Le **righe** di una matrice rappresentano **le singole equazioni o componenti della trasformazione**.

Riprendendo la matrice di prima:
- La **prima riga** $(2​ \\\ 3​)$ si occupa esclusivamente della **prima coordinata del risultato** (2x+3y). Ti dice che la prima componente dell'output è fortemente influenzata da y (peso 3) e un po' meno da x (peso 2).
- La **seconda riga** $(1​ \ −1​)$si occupa della **seconda coordinata del risultato** $(1x−1y)$.

# sistemi, matrici e vettori (4 carrara)
**sistema omogeneo**: $Ax=b$ con $b=(0 ,\dots, 0)$
* **spazio vettoriale**: se $Ax = b$ e' omogeneo, *allora le soluzioni formano uno spazio vettoriale*.

**sistema compatibile**: $Ax=b$ e' compatibile se esistono una o piu soluzioni per $x$.

**un sistema quadrato ha soluzione unica**: se e solo se, dopo aver  applicato Gauss, i pivot sono tutti non nulli.

**verificare indipendenza lineare**: i vettori sono linearmente indipendenti, se e solo se l'unica soluzione per il sistema $a_{1} v_{1}+ \dots + a_{k}v_{k} = 0$ e' $(a_{1},\dots,a_{k}) = (0,\dots,0)$

**sostituire un vettore in $\mathcal B$ con** $v \notin \mathcal B$ : posso farlo se $v$ posso esprimerlo come combinazione lineare di  $\mathcal D \subseteq \mathcal B$. Se si posso 

**rango**: numero di pivot identificati in $A$ **ridotta a scala**.
* $\text{rg }A$
* $\text{rg } A = \dim \text{Im } A$, *ossia il rango mi dice quanto e' grande la base per l'immagine di $A$.*

**dimensione**:
* $\dim V$ e' il numero di vettori di una base di $V$
* $\dim V = \dim \ker V + \dim \text{ Im } = \textcolor{red}{ \dim \ker V + \text{rg } A}$
* $\dim V = n$

**Iniettivita** e **suriettivita**:
* $T \text{ iniettiva} \iff \ker T=\{0\}$
* Sia $T: R^n \to R^m$, $T \text{ suriettiva }\iff \dim \mathrm{Im}T = m$   

**grassman**:
$$
\dim V + U = \dim V + \dim U - \dim U 
\cap W
$$

**METODO: trovare base del kernel**.
* prendi $Ax=0$, riduci a scala,  risolvi
* **colonne con un pivot**: indicano che la variabile corrispondente e' fissata
* **colonne senza un pivot**: indicano che la variabile corrispondente e' legata al variare di $t,s, \dots \in R$ 
* i coefficienti per $t,s, \dots$ sono le basi del kernel.
* **ATTENZIONE**: se l'unica soluzione del sistema e' $x=(0, \dots, 0)$ allora $\mathcal B = \{  \}=\emptyset$

**METODO**: **trovare base dell'immagine**
* prendi $Ax$, riduci a scala, ottenendo $B$
* Per ogni colonna $j$, se $B^j$ contiene un pivot, allora $A^j$ e' un vettore della base dell'immagine

**METODO: capire se un sistema $Ax = b$ e' compatibile**
* prendi $A|b$ e riducilo a scala
* se $rg(A)=rg(A|b)$ allora il sistema e' compatibile
	* se $rg(A)=n$ allora la soluzione e' unica
	* se $rg(A) < n$ allora ci sono infinite soluzioni

> [!error] Differenza tra Ker e Immagine
>⚠️ Un errore da NON fare (Differenza tra Ker e Immagine)
Mentre riduci con Gauss, le relazioni tra le colonne cambiano. Questo significa che:
> - **Per il $\ker$:** Puoi usare direttamente la matrice ridotta $U$ per fare i calcoli. Le soluzioni di $U\mathbf{x} = \mathbf{0}$ sono _identiche_ a quelle di $A\mathbf{x} = \mathbf{0}$. 
 > - **Per l'Immagine ($\text{Im}(T)$):** Se devi estrarre una base dell'immagine, i pivot ti dicono _quali_ colonne prendere, ma devi andare a recuperare le colonne **della matrice originaria $A$**, non quelle di $U$!
 > \

## determinante
**Determinante**: 
$$
A = \begin{vmatrix}
x \ y \\ z \ w
\end{vmatrix} \to \det A=xw-yz $$
1. se una riga è nulla, allora $\det A=0$
2. moltiplicare una riga per $\lambda$ moltiplica il determinante per $\lambda$
3. aggiungere a una riga un multiplo di un’altra riga non cambia il determinante

**Binet**:
$$ \det(AB)=\det(A)\det(B) $$
**Cramer**:
Per un sistema quadrato $Ax=b$ con $\det A\neq 0$, l’unica soluzione è:

$$ x_i=\frac{\det B_i}{\det A} $$
dove $B_i$ è la matrice ottenuta sostituendo alla colonna $i$-esima di $A$ la colonna $b$.

**determinante e rango massimo**: 
$$\text{rg }A = n = \text{ numero colonne} \iff \det A \neq 0$$
**matrice singolare**: vuol dire $\det A \neq 0$

**METODO: calcolare rango con determinante**.
* sia $A$ matrice $n \times n$ con determinante $\det(A) = 0$
* allora se esiste una sottomatrice $m\times m$ con $m=n-1$ con $\det = 0$, allora $A$ ha rango $n-1$
* e cosi via...
**METODO**: **calcolare determinante con laplace**:
$$\det (A) = \sum_{j=1}^n(-1)^{i+j} a_{ij} \det(M_{ij})$$
$$
\det(A) = (-1)^{i+j} a_{i 1} \det(M_{i {1}}) + (-1)^{i+j} a_{i 2} \det(M_{i {2}}) + \dots 
$$
* **a priori**: scelgo una riga/colonna che contenga il maggior numero di 0 possibili
* **a posteriori**: applico la formula, ossia la somma per ogni $a_{i,j}$ sulla riga/colonna scelta, moltiplicata per il determinante della matrice ottenuta eliminando da $A$ la riga $i$ ed la colonna $j$

**METODO**: **trovare inversa di $A$.**
* **inversa esiste se e solo se: ** $\det(A) \neq 0$
* sia $I$ la base canonica della stessa grandezza di $A$
* trasforma $A|I$ in $I|B$ attraverso **gauss**
* $B$ e' l'inversa di $A$
## autovalori e autovettori
**autovettore**: e' $x$ tale che, $\exists \lambda$
$$
T(x) = \lambda x
$$
**autovalore**:  e' $\lambda$ tale che $\exists x \neq 0$ per cui
$$
T(x) = \lambda x
$$**Autospazio associato a $\lambda$**
$$ V_\lambda=\{v\in V:T(v)=\lambda v\} $$

**METODO: trovare gli autovalori**
* **Teoria**:  $\lambda$ e' autovalore se e esolo se $\ker(A-\lambda I)\neq \{0\}$
* **Conseguenza**: vogliamo vedere se $A-\lambda I$ e' singolare, ossia $\det(A - \lambda I) = 0$

1. Costruisci il sistema $A-\lambda I = 0$ e mettilo a matrice
2. I valori di $\lambda \text{ t.c.} \det(A - \lambda I) = 0$ sono gli autovalori

**METODO: trovare gli autovettori a partire** da $\lambda$
* Costruisci matrice $A - \lambda I=0$
* Il vettore delle soluzioni genera gli autovalori per $\lambda$

**METODO: diagonalizzare matrice
1. Trova tutti gli autovalori.
2. Per ogni autovalore $\lambda$, calcola l’autospazio:
$$ V_\lambda=\ker(A-\lambda I) $$
3. Trova basi degli autospazi.
4. Metti insieme gli autovettori trovati.
5. Se riesci a ottenere una base di tutto $V$, allora $T$ è diagonalizzabile.
6. Se non riesci a ottenere abbastanza autovettori indipendenti, $T$ non è diagonalizzabile.

**METODO: costruire la matrice $T$ rispetto ad una base di autovettori**:
1. Scegli una base:
$$ \mathcal{B}=\{v_1,\dots,v_n\} $$
composta da autovettori.
2. Per ogni $v_i$, calcola:
$$ T(v_i)=\lambda_i v_i $$
3. La matrice di $T$ rispetto a $\mathcal{B}$ è diagonale:
$$ \begin{pmatrix} \lambda_1 & 0 & \cdots & 0\\ 0 & \lambda_2 & \cdots & 0\\ \vdots & \vdots & \ddots & \vdots\\ 0 & 0 & \cdots & \lambda_n \end{pmatrix} $$

**METODO: Verificare se $T$ e' triangolabile**
7. Cerca una base di $V$ rispetto alla quale la matrice di $T$ sia triangolare superiore.
8. Se esiste, $T$ è triangolabile.
9. In questo PDF è data la definizione, ma non un criterio completo di calcolo.  