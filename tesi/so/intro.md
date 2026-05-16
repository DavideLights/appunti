**a che serve un so?** rappresentano una soluzione rispetto all'utilizzabilità di un sistema di calcolo.

**virtualizzazione risorse**: 
* **condivise**
* **piu semplice**: rispetto alle risorse fisiche
* **assegnazione**: avviene in mutua esclusione, viene limitato il parallelismo
# storia
**spooling**: introduzione di una memoria disco.
* **buffer tampone**: per IO
* **input**: anticipato sul disco
* **output**: ritardato sul disco

**sistemi batch multiprogrammati**: ci sono piu job che vengono gestiti simultaneamente
* **CPU**: esegue un job per volta
* **dispositivi diversi**: esaudiscono i le richieste dei dispositivi

## multiprogrammazione e memorizzazione
**memoria con partizioni multiple**: permette di caricare piu job in memoria di lavoro.

**partizione singola**: la memoria di lavoro dei job si trova su disco e viene caricata/scaricata all'occorrenza in memoria di lavoro.

## limiti del monitor
**monitor e' un limite**: nel sistema con monitor, questo ottiene il controllo solo quando si richiede un dispositivo, il programma termina oppure va in errore.

**programmi interattivi**: e' impossibile cosi gestire in modo efficiente applicazioni interattive  senza un monitor che gestisce le risorse.

## os time-sharing
**algoritmo di scheduling**: assegna il tempo di cpu ai job
**preemption**: interruzione di un processo, nonostante stia eseguendo o abbia fatto una richiesta ad un dispositivo.

**dal monitor al sistema operativo**: con le interruzioni il controllo dal job va al monitor. questo puo' passare il controllo ad un'altro job.

**interruzione**: trasferisce il controllo da una routing di interrupt
* **interrupt vector**: contiene gli indirizzi delle rispettive routine nel sistema operativo
* **cosa vuol dire gestire un interruzione**? salvare in memoria `PC` della prossima istruzione relativa al programma interrotto, e il valore dei registri della CPU

`IDT`: in `x86` la Interrupt Descriptor Table mantiene le associazioni indirizzo-interrupt
## sistemi real-time
**hard real-time**: le deadlines devono essere rispettate, un task deve terminare entro un limite temporale.
* **si usa in processi industriali, medici, militari**
* ROM: dati e istruzioni si trovano in componenti ad accesso veloce o in memoria in sola lettura

**soft real-time**: sarebbe meglio rispettare le deadline, ma non e' la fine del mondo se succede il contrario.
* si usa in applicazioni multimediali

## processi
**a che servono**? monitorano, e controllano l'esecuzione dei programmi.

**cosa e' un processo**? entità a cui sono associati
* **dati** su cui opera
* **contesto di esecuzione**: le informazioni necessarie allo scheduler.
* **interazione**: interagisce sia col sistema operativo che con altri processi.
* **sistema operativo**: puo' essere basato su un'insieme di processi che cooperano.

**gerarchie**: i processi possono essere organizzati in base alla parentela.
* **child**: un processo che genera un'altro ne diventa padre.

## system call
**syscall**: meccanismo per accedere al software del sistema operativo.
* **come si usano**? direttamente in `C/C++`, le librerie standard invocano per me le system call in modo corretto.

**trap**: istruzioni che permettono il supporto alle syscall.
* **conseguenza**: invocare una syscall vuol dire che nell'applicazione e' presente una istruzione trap.
* **in lingguaggio c**: invoco le `stub` offerte dalle librerie.

**anatomia di una syscall**:
* **per il codice applicativo**: e' una funzione offerta da una libreria
* **per la macchina**: l'implementazione e' `machine dependent`
* **programmazione assembly**: server per le istruzioni trap e per le istruzioni di manipolazione dei registri per applicare una system call.

```c
#include <unistd.h>

int main(...){
	syscall_name(...)
}

syscall_name(...){
	...//preambolo (parzialmente asm)
	asm( machine code block )
	...//coda (parzialmente asm)
}
```

```c
int f(int x){
	if(x==1) return 1;
	return 0;
}
```

```bash
gcc -c -fomit-frame-pointer c2asm.c
objdump -d c2asm.o
```

```objdump
0000000000000000 <f>:
   0:   89 7c 24 fc             mov    %edi,-0x4(%rsp)
   4:   83 7c 24 fc 01          cmpl   $0x1,-0x4(%rsp)
   9:   75 06                   jne    11 <f+0x11>
   b:   b8 01 00 00 00          mov    $0x1,%eax
  10:   c3                      ret
  11:   b8 00 00 00 00          mov    $0x0,%eax
  16:   c3                      ret
```

**AT&T**: e' la sintassi usata nei sistemi unix, in contrasto con la sintassi `Intel`.

| AT&T                | Intel             |
| ------------------- | ----------------- |
| `movl $5, %eax`     | `mov eax, 5`      |
| `addl $0x24, %esp`  | `addp esp, 24h`   |
| `movslq %ecx, %rax` | `movsxd rax, ecx` |

## x86
* `rsp`: stack pointer
* `edi`: registro di CPU general purpouse 
* `retq`: return to caller
* `mov`: data movement instruction

# memoria di un processo
**routine macchina**: 
1. alloca lo stack per le variabili locali
2. istruzioni macchina che implementano le istruzioni C originali
3. dealloca lo stack

![[routine macchina.excalidraw]]

**visione globale** della memoria accessibile ai programmi applicativi:

![[addressspace.excalidraw]]
**ELF**: formato che struttura le sezioni di un programma in Unix
* **PE** (Portable Executable): e' il formato di windows.

**tool compilazione**: genera `ELF/exe` a partire dal sorgente

**corrispondenze tra sorgente ed eseguibile**:
1. **funzioni**: ad ogni funzione C compilata e linkate staticamente corrisponde una routine nella sezione `testo`
2. **variabili globali**: ogni variabile globale dichiarata nel programma o nelle librerie **linkate staticamente** corrisponde una locazione nella sezione `dati`
3. **heap**: permette di allocare memoria tramite `malloc`
	1. *chi tiene traccia delle aree di memoria nell'heap*? la libreria `malloc`
	2. *quanto posso allocare*? fino a saturare la memoria del contenitore dell'applicazione


**gemini**: spiega la sezione `bss`.

| istruzione/i                          | sezione corrispondente |
| ------------------------------------- | ---------------------- |
| `int x = 10;`                         | `data`                 |
| `char v[1024]`                        | `bss`                  |
| `int x;` nel contesto di una funzione | `stack`                |
| codice della funzione                 | `text`                 |

# variabili puntatore
**cosa sono**? come le variabili normali, sono collocate nello spazio di indirizzamento.
* **cosa contengono**? un'indirizzo di memoria
* **a cosa si riferiscono**? ad uno **spiazzamento** all'interno del contenitore di memoria dell'applicazione.

**a che servono**?
* indico dove salvare o leggere in memoria le informazioni (es: `scanf`)
* scandire la memoria accedendo ai suoi valori
* accedere all'heap

**operatori per leggere un'indirizzo**:
* `*`: indirezione
* `[]`: spiazzamento ed indirezione

**conseguenza**:  array e puntatori sono la stessa cosa, nel senso sono entrambi degli indirizzi in memoria.

> [!nota] locazione array
> in base a come e' stato definito, puo' trovarsi nello stack, nell'heap o nella sezione bss.

**RVALUES**: un'array a differenza di un puntatore e' un `RVALUE`, ossia non ha una locazione di memoria associata e non e' modificabile.


```c
int *x;
int y[128]; // y e' RVALUE

y = x; // espressione illecita, poiche y e 'un RVALUE
```

> [!note] `scanf`
> Lavora usando uno schema a buffer, ossia un'area di memoria gestita dalla libreria di I/O, dal quale `scanf` recupera i dati immagazzinati.
> 
> `scanf` dunque legge i dati nel buffer che non sono stati ancora recuperati!


> [!note] `printf`
> lo standard `C` prevede l'uso di ASCII per interpretare le stringhe.

**bufferizzazione**:
![[strutture_stdio.excalidraw]]

**"svuotare" buffer input/output**:
* `fflush`: svuota il buffer di output (`stdout`), ma non e' ben definito cosa succede al buffer in input
* `#define fflush(stdin) while(getchar() != '\n')` fa al caso nostro, ad un certo punto svuota lo standard input

**strutture**: costrutto del `C` che permette di accorpare in un'area di memoria  informazioni eterogenee.

```bash
int syscall_name(int, void *, struct struct_name * ...)
```
la routine della macchine e' tale per cui:
* **preambolo**: gestisce e carica nei registri appropriati i parametri passati
* **come gestisco i puntatori?** il sistema operativo puo' leggere/scrivere nello spazio di indirizzamento dell'applicazione mentre esegue la syscall.
* **valore di ritorno**: di solito la syscall scrive il ritorno dentro ad un registro del processore.

![[cambio di stack.excalidraw]]

## librerie standard
**standard di lingauggio**: definisce servizi standard su una determinata tecnologia, es: `ANSI-C`
* **librerie standard**: offrono i servizi nel linguaggio di programmazione, si basano su una specifica interfaccia.
* **system call**: le procedure delle librerie standard chiamano le system call proprie del sistema operativo in cui esegue.
* **portabilita**: posso usare la stessa procedura su sistemi differenti

es `printf`:
* `unix`: fa una chiamata `write`
* `windows`: fa una chiamata `WriteFile`

**standard di sistema**: definiscono i servizi offerti dal sistema per la programmazione in una data tecnologia (es: linguaggio `C`)
* **Unix**: usa lo standard Posix
* **WIndows**: usa la WinAPi
* **cosa definisce**? le system call offerte ai programmatori e le funzioni di libreria specifiche al sistema

## kernel
**kernel**: moduli software di base di un sistema operativo. 
* accedo ai moduli (se progettati in tal senso) tramite syscall
* il kernel contiene moduli che gestiscono interrupt e trap

**sistema operativo**: il sistema vero e proprio aggiunge moduli software, oltre al kernel, per permettere l'interazione con gli utenti (es: interprete dei comandi). questi programmi si appoggiano ai moduli del kernel.

**microkernel**: insieme ristretto di funzionalita
* gestione interruzioni e memoria
* comuncazione processi
* scheduling
* **user land**: tutti gli altri servizi del kernel sono processi utente con cui posso interaggire
	* **pro**: flessibilita, estensione, portabilita
	* **contro**: overhead dei messaggi e frammentazione del codice

## windows NT
**windows NT Executive**: e' il kernel del sistema operativo.
* **HAL**: hardware abstraction layer, crea il layer che disaccoppia l'hardware dal sistema operativo
* **microkernel**: comunica con HAL per interagire con l'hardware. si occupa di scheduling, gestione interruzione e gestione del multiprocessamento
* **executive services**: costituito dai moduli che implementano i servizi offerti dall'Executive
* **IO Manager**: gestisce l'input output, ma non parla con l'HAL, accede direttamente all'hardware.
* **Window Manager**: gestisce le finestre
* **System Services**: interfaccia per i processi in modalita utente.

**sottoinsiemi d'ambiente**: NT e' strutturato in modo da supporta applicazioni per altri sistemi operativi:
* **Win32**: e' l'API di Windows 95 e NT
* **MTVDM**: MS-DOS NT Virtual DOS Machine, dunque offre una macchina DOS.
* OS/2
* **Win16**: WIndows a 16 bit
* **POSIX**: interfaccia alle chiamate UNIX

## Unix
**codice pubblico**: alcune versioni sono accessibili a tutti.
**platform independent**: la sua architettura e' aperta, e' possibile portarlo verso altri processori.
**linguaggio C**: nasce per creare Unix

**architettura stratificata**: il kernel e' il nocciolo del sistema operativo
* molte parti eseguono in modalita utente.
* **file subsystem**: tutte le parti del sistema operativo che devono chiamare l'hardware devono parlare inevitabilmente con il **file subsystem**

## ambiente
**compilazione**: vengono seguite regole canoniche per generare gli eseguibili, sono formati da
* **codice applicativo**: il `main`, ecc...
* **ambiente di esecuzione**: un'insieme di moduli software

**esecuzione**: all'esecuzione di un programma compilato viene eseguito `_start` e non `main`! Esegue funzioni preliminare per prepara il processo all'esecuzione.

**utilizzo dell'ambiente**:
* **punto di raccordo**: tra il sistema operativo ed il codice applicativo . 
* **portabilita**: l'ambiente permette l'esecuzione dello stesso codice su differenti sistemi operativi grazie al **linking**
* **librerie**: pilota l'esecuzione di specifiche funzioni di libreria

![[ambiente.excalidraw]]
## prescindere dall'ambiente
**si puo**: se specifico la mia `_start`, con `-nostartfiles` posso evitare l'inclusione della procedura standard `_start`.

**altrimenti**: `_start` e' la prima procedura nella sezione `.text`, dunque verra' eseguita per prima.


## passaggio parametri
![[passaggioparametri.excalidraw]]

**descrittori e handle**: e' un codice operativo, identifica nel kernel l'istanza di struttura dati coinvolta nell'esecuzione della syscall

**output**: il kernel scrive il valore di ritorno in un registro della cpu.

![[Pasted image 20260514141506.png]]
* `scanf("%ms", &p)` dove al posto di $m$ specifico i byte da allocare in $p$.


### ASLR
**ASLR**: address space layout randomization
* randomizzazione di alcuni parti dello spazio di indirizzamento, specialmente lo stack
* spiazzamento randomico su `.text` e `.data`.
* gli indirizzi noti a temp di compilazione non coincideranno con gli indirizzi relativi
* **attaccante**: e' difficile trovare la randomizzazione del'offset

![[Pasted image 20260514142850.png]]

`-pie`: **post independent executable**, genero codice indipendente dalla posizione nell'area di memoria.

