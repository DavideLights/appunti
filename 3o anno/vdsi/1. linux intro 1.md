### 1. Fondamenti e Filosofia Unix
- **Tutto è un file**: I*n Linux, ogni cosa (documenti, tastiera, hard drive) viene trattata dal sistema operativo come un file*. 
- **Il Kernel**
- **GNU/Linux**: *Il sistema che usiamo è l'unione del kernel creato da Linus Torvalds (1991) e degli strumenti (shell, compilatori, editor) del progetto GNU di Richard Stallman*. È tutto rilasciato sotto licenza **GPL** (Free Software).

### 2. Esplorazione del File System e Terminale
- **Struttura a albero**:
    - `/dev/`: Contiene i file relativi ai dispositivi hardware.
    - `/etc/`: File di configurazione del sistema.
    - `/proc/` e `/sys/`: Interfaccia astratta per interagire direttamente con il kernel.
    - `/usr/`: Risorse di sistema e programmi installati dall'utente.
- **tty (Virtual Terminal)**: *È l'interfaccia testuale principale fornita dal kernel*. In una macchina senza interfaccia grafica (GUI), verresti accolto da una tty. 
	- **Virtuale**: nel senso che il kernel emula diverse console fisiche su un unico monitor e posso saltare da una all'altra con `Ctrl+Alt+F1,F2,...`
	- **Esiste sempre**: indipendentemente se sto usando o no un server grafico.
- **pseudo-tty**: l'emulatore di terminale (Gnome Term, kitty, xterm, ...) richiede una pseudo-tty per comunicare con bash, zsh, ssh, ecc...
	- Lato **Master**: *l'emulatore scrive qua*
	- Lato **Slave**: *bash legge quello che l'emulatore di terminale fornisce*
- **pwd** (_Print Working Directory_): *Mostra il percorso della cartella corrente.* 
- **which -a**: Utilissimo per trovare il percorso esatto di un eseguibile nel sistema. `-a` mostra tutti i match in `PATH`.
### 3. Variabili d'Ambiente e Shell
- **Shell**: Un interprete di riga di comando (es. `bash`, `zsh`) che accetta input e restituisce output.
- **Variabili d'ambiente**: Variabili globali che configurano l'ambiente di sistema (es. `$USER`, `$HOME`, `$TERM`).
    - `printenv` o `env`: Mostrano **tutte** le variabili d'ambiente correnti.
    - `export`: Permette di rendere una variabile disponibile anche ai programmi figli (come uno script Python).
    - `unset`: Rimuove una variabile.
- **Esportazione ai processi figli**: *In Linux, quando crei una variabile semplicemente assegnandole un valore (es. `MIA_VAR="ciao"`), questa esiste solo all'interno dell'istanza corrente della shell*. Se da quella shell lanci un programma (come uno script Python o un altro comando), quel programma **non vedrà** la variabile.
- **$PATH**: Una lista di cartelle in cui la shell cerca i programmi quando digiti un comando, evitando di scansionare l'intero disco ogni volta.
- **echo**: Stampa i suoi argomenti. Se usato con `$`, stampa il valore delle variabili (es. `echo $PATH`).

### 4. Gestione dei File Descriptor (FD) e Redirezioni
Ogni programma lavora di default con tre file:
1. **fd 0 (stdin)**: Standard Input (di solito la tastiera).
2. **fd 1 (stdout)**: Standard Output (di solito lo schermo).
3. **fd 2 (stderr)**: Standard Error (canale separato per i messaggi d'errore).

**Sintassi delle Redirezioni:**
- `>`: Redireziona lo stdout *verso un file* (es. `cat file.txt > output.txt`).
- `<`: Redireziona lo stdin (es. `programma < input.txt`).
- **Unire gli stream**: `2>&1` indirizza lo stderr nello stesso posto dello stdout.    
    - _Esempio:_ `cat file.txt > out.txt 2>&1` mette sia errori che output nel file.
- **Scartare output**: `2>/dev/null` è il "buco nero".

### 5. Pipe e Manipolazione Testo con comandi
- **Anonymous Pipes (`|`)**: Collegano lo stdout di un programma direttamente allo stdin di un altro. (es. `prog1 | prog2`).
- **Named Pipes (FIFO)**: Create con `mkfifo`. Esistono nel file system e bloccano il processo finché non c'è sia un "**produttore**" che scrive che un "**consumatore**" che legge.
* `cat /tmp/myfifo`, legge dalla fifo aspettando **EOF**.
- **Programmi di filtraggio**:
    - `grep`: Filtra l'input in base a regole o stringhe.
    - `awk`: Estrae "**token**" (colonne) da una riga. _Esempio:_ `ls -l | awk '{print $9}'` stampa solo i nomi dei file (nona colonna).
    - `sed`: Sostituisce stringhe; `cut`: Taglia parti di stringhe.
### . Comandi
* `id`: stampa le informazioni dell'utente (privilegi, ecc...)
* `cat`: concatena file e stampa su standard output
	* `cat -`: usa come parametro lo standard input
	* `CTRL-D`: `EOF`
* `cat << VSDI` (???)
* * `/dev/null` dispositivo che mangia i byte.
* `2>/dev/null` e' utile per scartare gli errori.
* `ls -l | awk '{print $8}'` con `awk` seleziono l'ottavo token.
* `ls -lah`: mostra tutto e human readable.

```bash
echo "cane" > ciao.txt
echo "gatto" > ciao.txt
cat ciao.txt
gatto
```
**Nota**: La ridirezione verso file sovrascrive tutto!
 

