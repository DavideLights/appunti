#### Introduzione Data Stream
Prima di introdurre Count-Min Sketch, parto dal modello dei data stream. In questo modello i dati arrivano come una sequenza di elementi $x_1,\dots,x_m$​, spesso molto lunga, e non posso assumere di memorizzarla interamente. 

L’algoritmo deve quindi processare ogni elemento man mano che arriva, usando poca memoria.

Per questo spesso si accetta una risposta approssimata, controllata da parametri di errore e probabilità di fallimento.

Nel nostro caso il problema è stimare la frequenza di un elemento $y$. cioè quante volte compare nella stream, senza mantenere un contatore esatto per ogni possibile elemento dell’universo $[n]$.

###### PROBLEMA
Data una stream $x_1,...,x_m$ di interi con $x_i \in [n]$ per ogni elemento $y \in [n]$ 
si definisce la frequenza di $y$ come il numero di volte in cui appare nella Stream
$$f_y=|\{i:x_i=y\}|$$
###### Parametri in gioco e struttura dati
il Count min sketch usa:
- matrice $M \in \mathbb{N}^{t \times s}$ 
	- dove t sono le righe, numero di funzioni hash indipendenti
	- s sono le colonne è la dimensione dei bucket utilizzati per inserire gli elementi dopo hashing
	- $s \times t$ determina proprio il fattore di errore e la probabilità di successo
- funzioni hash universali indipendenti per ogni riga $j=1, ..., t$ 
	- $h_j: [n] \rightarrow [s]$ 
rapida spiegazione di funzione hash e di significato di indipendenza e universalità

Una funzione hash ci permette di mappare un elemento in un insieme più piccolo come un insieme di bucket
$$h_j(x) = \text{colonna in cui aggiornare x nella riga j }$$
Una famiglia di funzioni hash è **universale** se, presi due elementi diversi $x \neq y$, la probabilità che collidano è bassa:
$$Pr[h(x)=h(y)] \le \frac{1}{s}$$
dove $s$ è il numero di bucket.
###### Idea algoritmo e pseudocodice
ogni volta che arriva un elemento $x$ lo inserisco nello sketch eseguendo per ogni $j=1, ..., t$ 
$$M(j,h_j(x))=M(j,h_j(x))+1$$
uso gli elementi della matrice come contatore delle occorrenze di un certo elemento $x$ 
quando si deve restituire una certa query $y \in [n]$ in quel caso basta restituire
$$F(y)=min\{M(j,h_j(y)):j=1,...,t\}$$
prendo il min perché potrei avere una sovrastima
```python
CountMin sketch for frequencies
M[t][s] matrice inizializzata a 0
scelgo t funzioni hash indipendenti
	h_j: [n] -> [s]
Update(x):
	for j=1 to t:
		M[j][h_j(x)]=M[j][h_j(x)]+1
Query(y):
	return min_{j=1,...,t}M[j][h_j(y)]
```

###### Proprietà fondamentali del Count-Min
- $M(j,h_j(y)) \geq f(y)$ non sottostima mai $f(y)$
	- ogni occorrenza reale di $y$ incrementa sicuramente quel contatore
	- il problema avviene quando si hanno delle collisioni
- per ogni $z \in [n]$ con $z \neq y$ tale che $h_j(z)=h_j(y)$ ho una collisione
	- con probabilità molto bassa perché comunque ho hashing universali ma ho comunque una collisione
il nostro stimatore prende il minimo dalla matrice M per tutte le funzioni hash $j=1, ...,t$ per cui sbaglia solo se avviene una collisione su ognuna di queste righe senza definire ancora un fattore di tolleranza di fallimento

###### Stimiamo la probabilità di sovrastima per una singola riga j
Fissiamo un elemento $y$ e una riga $j$.
Si vuole definire $Pr[M(j,h_j(y)) \ge f(y) +\epsilon \ m]$ per $\epsilon >0$
sia $1(j,x,y)$ una variabile aleatoria definita come
$$\mathbf{1}(j,x,y)= \begin{cases} 1 & \text{se } h_j(x)=h_j(y) \\ 0 & \text{altrimenti} \end{cases}$$
e sia $S=\{x \in [n]: f(x)>0\}$ un insieme di elementi distinti della Stream

il contatore 
$$M(j,h_j(y))=f(y)+\sum_{x \in S, x \neq y} f(x) 1(j,x,y)$$
poiché è composto sicuramente dalle occorrenze reali di $y$ più le occorrenze che collidono in quella riga $j$
- il secondo termine è il rumore dovuto dalle collisioni
L'obiettivo è mostrare che questo rumore non è troppo grande con buona probabilità
quindi
$$\mathbb{E}[M(j,h_j(y))]=f(y)+\mathbb{E}[\sum_{x \in S, x \neq y}f(x)\ 1(j,x,y)]=f(y)+\sum_{x \in S, x \neq y} f(x) \mathbb{E}[1(j,x,y)]$$
- al secondo passaggio si applica linearità del valore atteso dove la somma di una expectation è la sommatoria delle expectation
$h_j$ è una funzione hash universale su una tabella di $s$ slot e $1(j,x,y)$ è una variabile indicatrice

$$\mathbb{E}[1(j,x,y)]=Pr[h_j(x)=h_j(y)] \le \frac{1}{s}$$
poiché si usano funzioni hash universali
$$  
\mathbb{E}[M(j,h_j(y))]  
\le  
f(y)+\sum_{x \in S, x \neq y} f(x)\ \frac{1}{s}  
$$
sappiamo inoltre che 
$\sum_{x \in S } f(x) =m$ 
quindi $\sum_{x \in S, x \neq y} f(x)\ \frac{1}{s} \leq \frac{m}{s}$

per cui 
$$\mathbb{E}[M(j,h_j(y))] \leq f(y)+\frac{m}{s}$$
essendo $f(y)$ una costante posso sottrarla da una parte e dall'altra della disuguaglianza per ottenere
l'errore atteso della riga $j$ è:
$$\mathbb{E}[M(j,h_j(y))-f(y)] \le \frac{m}{s}$$
applichiamo la Markov inequality per avere un bound sulla probabilità
$$Pr[M(j,h_j(y)) \ge f(y) +\epsilon \ m]$$
possiamo definire quindi una variabile aleatoria che indica l'errore totale 
$$X=\sum_{x\in S, \ x\neq y}f(x)1(j,x,y)$$
definita come $M-f(y)$
ma sappiamo già che 
$$\mathbb{E}[X] \leq \frac{m}{s}$$

$$Pr[M(j,h_j(y))- f(y) \ge \frac{2m}{s}]$$
ovvero per Markov
Qual è la probabilità che l’errore sia almeno il doppio di questo valore atteso massimo?
- Sia $X \ge 0$ una variabile aleatoria.
- Fornisce un **upper bound** sulla probabilità che $X$ sia grande
	- $\Pr[X \ge a] \le \frac{\mathbb{E}[X]}{a}$ per $a > 0$.

$$Pr[X \ge \frac{2m}{s}] \leq \frac{\mathbb{E}[X]}{\frac{2m}{s}} \leq \frac{m/s}{2m/s}= \frac{1}{2}$$

per definire meglio l'errore che siamo disposti ad avere usiamo però
$\epsilon m$ quindi $\frac{2m}{s}=\epsilon m$ poniamo $s=\frac{2}{\epsilon}$
e abbiamo che
per ogni $\epsilon >0$ $Pr[M(j,h_j(y)) \ge f(y) +\epsilon \ m] \leq \frac{1}{2}$ 

rapportandolo per ogni riga abbiamo

$$Pr[F(y)\ge f(y)+\varepsilon m]\le \left(\frac{1}{2}\right)^t$$
perché $F(y)$ è il minimo e quindi supera la soglia solo se tutte le righe la superano
e oltretutto le funzioni hash delle righe sono indipendenti, gli eventi “la riga $j$ è cattiva” sono indipendenti, quindi le probabilità si moltiplicano
###### Costi computazionali
definendo una probabilità di errore che possiamo sopportare come $\delta$ 
la probabilità che l'algoritmo non fallisca quindi deve essere $\geq 1-\delta$
abbiamo che per soddisfare la probabilità di errore dobbiamo avere

$(\frac{1}{2})^t \leq \delta$
perciò $t \geq log_2(\frac{1}{\delta})$
$s=\frac{2}{\epsilon}$

*COSTO SPAZIALE*
la memoria occupata dalla matrice è  $O(t \cdot s)$ 
perciò $O(log(\frac{1}{\delta})\cdot \frac{2}{\epsilon})$ 

*COSTO TEMPORALE*
per aggiornare un elemento $x$ andiamo a scorrere tutte le righe t per $h_j(x)$
quindi costo lineare in $O(log(\frac{1}{\delta}))$

per una query ci andiamo a scorrere il min di tutte le righe $t$ per un certo $h_j(y)$
anche qui costo lineare in $O(log(\frac{1}{\delta}))$
