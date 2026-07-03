## `array-test.c`
**Obiettivo**: capire come funzionano gli indici e a cosa servono i tipi negli array.

`int a[10] = {1,2,3,4,5,6,7,8,9,10}` e' un array dove ogni dato occupa 4 byte:
* dunque `sizeof(a)=40`
* e' definita fuori dal `main`, dunque si trova nella sezione data del compilato.

`p = (char *)a + sizeof(a)` e' un passaggio fondamentale per capire l'aritmetica dei puntatori
* Quando sommo un puntatore $\text{ptr}$ che manipola dati di un certo $\text{tipo}$  ad un certo $\text{valore}$ , allora C in automatico trasforma l'espressione nella seguente
$$
\text{ptr} = \text{indirizzo\_di\_a} + \text{sizeof}(\text{tipo}) \cdot \text{valore}
$$
* ossia: 
$$p = \text{a} + 1 \cdot 40$$

`p = a + sizeof(a)` non e' corretto!
* secondo quanto detto prima, se intendiamo $p$ come puntatore ad `int`
$$p = a + 4 \cdot 40$$

> "Se `p` è un puntatore a un qualche tipo di dato, allora `p + n` è un puntatore al `n`-esimo elemento successivo rispetto a quello a cui punta `p`. [...] Il compilatore moltiplica `n` per la dimensione dell'oggetto a cui `p` punta."

`printf("%d ",((int*)p)[-i])` e' necessario il casting poiche' devo dire al compilatore che i dati che sto manipolando sono degli interi.
* `((int*)p)[-i]` equivale ad ottenere l'intero che si trova in $p-4*i$.
* ricordiamo che $p$ punta all'ultimo elemento e che ogni intero e' formato da $4$ byte.

![[Pasted image 20260629121018.png]]
* si puo' notare che effettivamente `a+sizeof(a)` ed $p$ sono due indirizzi completamente differenti
* se accedo all'area di memoria di `a` estraendo un char per volta, leggo 1 byte per volte, ricordando che un intero e' formato da 4 byte.

## `basic-buffer-overflow.c`
Con il ciclo `while` sono in grado di accedere alla memoria e di scrivere dove voglio, **applicando uno spiazzamento rispetto** a `v` che e' un puntatore ad interi. Dunque, se conosco l'indirizzo di `control_variable`, posso scriverci dentro ed uscire dal `while`.

**senza `#define IN_STACK`**, le variabili a cui mi riferisco in `main` sono quelle globali.
![[Pasted image 20260629121940.png]]
* con il comando vado a guardare che cosa contiene la sezione `.bss`
* tra `v` e `control_variable` c'e' una differenza di 32 posizioni (ossia 32 byte tra l'inizio di `v` e di `control_variable`)
* 32 posizioni equivale ad 8 interi (un intero sono 4 byte)
* Dunque se riesco ad eseguire l'istruzione `v[-8]=0;` posso interrompere il ciclo while, vedi l'immagine sotto!

![[Pasted image 20260629122548.png]]

**con `#define IN_STACK`**, dobbiamo vedere come sono disposte le variabili nello stack.
![[Pasted image 20260629130421.png]]
* compilando con `-g`, effettuo il debug con gdb 
* con il comando `x` esamino gli indirizzi di memoria forniti 
* tra `control_variable` ed `v` ci sono 4 byte di differenza, dunque...

![[Pasted image 20260629130537.png]]

## `busy-loop.c`
> [!note] `-nostartfiles`
> Con questa opzione  evito di linkare in fase di compilazioni le istruzioni per il setup dell'eseguibile, ossia `_start`.

## `dynamic-printf.c`
**OSS**: posso passare a printf una stringa fornita dall'utente, che puo decidere come formattare i valori passati come argomento a printf.

## `environment.c`
`environ`:
* `extern`: deve essere risolto dal compilatore
* `char **`: e' una lista di stringhe

>The variable _environ_ points to an array of pointers to strings
   called the "environment".  The last pointer in this array has the
   value NULL.  This array of strings is made available to the
   process by the [execve(2)](https://www.man7.org/linux/man-pages/man2/execve.2.html) call when a new program is started.  When
   a child process is created via [fork(2)](https://www.man7.org/linux/man-pages/man2/fork.2.html), it inherits a _copy_ of its
   parent's environment.
