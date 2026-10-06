
lista di comandi per comando:
* `file exefile`: elenca proprieta di un file, e potenziali vulnerabilita
	* `dynamically linked`: il sistema operativo deve cercare la lib c per eseguire le chiamata di sistema e altre funzioni. 
	* `not stripped`: posso vedere i nomi delle funzioni originali

* `gets`: non limita il numero di byte letti e da scrivere nel buffer. e' super vulnerabile.
* `checksec --file vuln`: notifica quali meccanismi di difesa non attua un eseguible. 
	* **RELRO:** Rende la tabella dei puntatori alle funzioni (GOT) a sola lettura per impedire che venga sovrascritta.
	- **STACK CANARY:** Pone un valore sentinella sullo stack per rilevare e bloccare la corruzione del return address prima dell'uscita dalla funzione.
	- **NX:** Disabilita l'esecuzione di codice nelle aree dati (stack/heap), impedendo l'avvio diretto di shellcode iniettato.
	- **PIE:** Carica il codice a un indirizzo casuale in memoria a ogni esecuzione, rendendo imprevedibili le posizioni di funzioni e gadget.
	- **RPATH / RUNPATH:** Definisce percorsi hardcoded per le librerie dinamiche, esponendo al rischio di librerie malevole se configurato su cartelle insicure.
	- **Symbols:** Mantiene o rimuove i nomi di variabili e funzioni, influenzando la facilità di reverse engineering del binario.
	- **FORTIFY:** Sostituisce funzioni C insicure con controparti che verificano automaticamente i limiti dei buffer a compilazione o runtime.
**static/dynamic** analysis:
- `gdbpwndbg`
	- `file vuln`: carica il file
	- `info functions`: lista tutte le funzioni usate nel file caricato
	- `disassemble main`
	- `break main`: metti un break point 
	- `delete breakpoints`
	- `x $eax` hex
	- `p $eax` decimal
	- `n`: next instruction
	- `c`: continue
- `ghidra auto vuln`: carica il file vuln velocemente
- `ltrace`:  intercepts and records dynamib library calls.
	- `-c`: count time and calls for each lib call
	- `-S`: display system calls as well as library calls
	- there are filters too...
- `ropper --file vuln`
- `ropper --file vuln --search nop`
- `a=asci(97)`, might be useful to know if you spot `97` in program output after inputing `a` 

# overwriting stack
https://www.youtube.com/watch?v=jrG1Gqatj7U

```bash
gcc login.c -o login -fno-stack-protector -z execstack -no-pie -m32
```

* using `ltrace login` shows clearly `strcmp(input_string, "pass")`


# extra things

```bash
gcc vuln.c -o vuln -fstack-protector-all
```

> *Emit extra code to check for buffer overflows, such as stack smashing*
 *attacks.  This is done by adding a guard variable to functions with*
 *vulnerable objects.  This includes functions that call "alloca", and*
 *functions with buffers larger than or equal to 8 bytes.  The guards are*
 *initialized when a function is entered and then checked when the func‐*
 *tion exits.  If a guard check fails, an error message is printed and*
 *the program exits.  Only variables that are actually allocated on the*
 *stack are considered, optimized away variables or variables allocated*
 *in registers don't count.*

```bash
gcc vuln.c -o vuln -fno-stackprotector -z execstacl -no-pie -m32
```

> Disabilita le protezioni di gcc all'interno dell'eseguibile compilato. niente stack canary, stack con permessi di esecuzione, niente pie.

