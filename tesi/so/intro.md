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
1. ad ogni funzione C compilata e linkate staticamente 
