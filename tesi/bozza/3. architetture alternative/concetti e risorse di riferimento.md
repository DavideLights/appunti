# Sezione 3 — Architetture Alternative: Concetti Fondamentali e Risorse Bibliografiche

Questo documento sintetizza le nozioni teoriche, le primitive del kernel Linux e la bibliografia essenziale per comprendere, argomentare e difendere i pregi e i difetti di ciascuna architettura alternativa analizzata nel **Capitolo 3**.

---

## Mappa delle Architetture Alternative

| Sottosezione | Architettura Alternativa                 | Pregio Principale                           | Difetto Fatale (*Fatal Flaw*)                                                                  |
| :----------- | :--------------------------------------- | :------------------------------------------ | :--------------------------------------------------------------------------------------------- |
| **3.1**      | **Shadow Bridge L2 (senza GW)**          | Zero complessità SDN, primitive kernel pure | **No WAN**: container isolati da Internet (niente `apt`, DNS o chiamate esterne).              |
| **3.2**      | **Dual NIC (`eth0` + `wlan1`/`eth1`)**   | Ripristina connettività Internet            | **Rottura fedeltà topologica**: routing asimmetrico, drop pacchetti per `rp_filter`.           |
| **3.3**      | **PID Namespace Separato**               | Zero overhead di clonazione storage/RAM     | **Leaky**: payload visibile su filesystem (`/tmp`, log), loopback `tcpdump`, crash live.       |
| **3.4**      | **Network Namespace Host Separato**      | Isolamento IP nativo senza demoni SDN       | **Bypass API orchestratore**: route drift, gestione manuale veth, no supporto cluster.         |
| **3.5**      | **Esecuzione In-Memory + Mascheramento** | Fileless execution senza clonazione         | **Security through Obscurity**: bypassabile con binari statici (Go/Rust), eBPF kernel tracing. |

---

## 1. Analisi Dettagliata per Sottosezione

### 3.1 Shadow Bridge (Bridge L2 senza Gateway Host)
*File di riferimento: [3.1 bridge L2 senza gateway.md](file:///home/davidel/appunti/tesi/3.%20architetture%20alternative/3.1%20bridge%20L2%20senza%20gateway.md)*

#### Concetti Fondamentali da Conoscere
1. **L2 Switching vs L3 Routing nel Kernel Linux**:
   - Un Linux Bridge (`struct net_bridge`) opera come uno switch Ethernet a livello datalink (L2): gestisce una Forwarding Database (FDB) con apprendimento degli indirizzi MAC e inoltra frame tra porte senza bisogno di un indirizzo IP assegnato all'interfaccia bridge dell'host.
   - All'interno del bridge L2, due container possono comunicare direttamente usando ARP e frame Ethernet se appartengono alla stessa subnet.
2. **Risoluzione Next-Hop e Protocollo ARP**:
   - Quando un container vuole comunicare con un IP esterno alla propria subnet (es. DNS `1.1.1.1` o repository di pacchetti), la Forwarding Information Base (FIB) del container seleziona il default gateway (`10.k.1.1`) e invia una richiesta ARP broadcast (`who-has 10.k.1.1`).
   - Nel caso dello Shadow Bridge, l'interfaccia host non ha IP configurato per non creare conflitti con `br-team-k`. Di conseguenza, nessuno risponde alla richiesta ARP: il pacchetto scade con `Destination Host Unreachable` o `Network is unreachable`.
3. **Collisione delle Tabelle di Routing sull'Host (FIB Collision)**:
   - Se si tentasse di assegnare `10.k.1.1` al bridge di verifica nello stesso network namespace dell'host, il kernel si troverebbe con due interfacce distinte (`br-team-k` e `br-verify-k`) che dichiarano la stessa subnet `10.k.1.0/24`. L'algoritmo `fib_lookup` non potrebbe distinguere a quale interfaccia inviare il traffico di risposta, generando indeterminismo e perdita di pacchetti.

---

### 3.2 Dual NIC (`eth0` verso Shadow Bridge + interfaccia secondaria verso `incusbr0`)
*File di riferimento: [3.2 interfaccia wlan1 verso incusbr0.md](file:///home/davidel/appunti/tesi/3.%20architetture%20alternative/3.2%20interfaccia%20wlan1%20verso%20incusbr0.md)*

#### Concetti Fondamentali da Conoscere
1. **Routing Asimmetrico e Multi-Homing**:
   - Avere due schede di rete collegate a due gateway distinti introduce il problema del percorso asimmetrico: il pacchetto entra da un'interfaccia (`eth0`) ma la risposta viene instradata verso l'altra interfaccia (`eth1`/`wlan1`) perché lì risiede la default route.
2. **Linux Reverse Path Filtering (`rp_filter`)**:
   - Meccanismo di sicurezza del kernel (`sysctl net.ipv4.conf.*.rp_filter`).
   - In modalità Strict (`rp_filter=1`), se un pacchetto arriva su `eth0` ma la tabella di routing dell'host o del container utilizzerebbe un'altra interfaccia (`eth1`) per raggiungere l'IP sorgente, il kernel considera il pacchetto come "spoofato" e lo scarta silenziosamente (*silent drop*).
3. **Policy Routing & Source-Based Routing (`ip rule`)**:
   - Per far funzionare due interfacce con due default route, bisognerebbe iniettare regole di routing avanzato nel container basate sull'IP sorgente (`ip rule add from ... table ...`). Questo viola la semplicità di configurazione e sporca l'ambiente del concorrente.
4. **Fedeltà Topologica (Topological Fidelity)**:
   - Principio cardine dei cyber range: l'ambiente di test deve essere identico all'ambiente reale. Aggiungere una seconda interfaccia modifica il comportamento di bind dei demoni (`0.0.0.0`), l'output di comandi come `ip a` o `ss`, e le regole di firewall locali (`iptables`/`nftables`) scritte dal concorrente.
5. **Overhead di Allocazione Kernel**:
   - Raddoppia il numero di coppie `veth` create nel kernel dell'host (da $N$ a $2N$), aumentando l'impronta di memoria di rete e il carico per il processing degli interrupt software (ksoftirqd).

---

### 3.3 PID Namespace Separato per la Verifica (In-Place Execution)
*File di riferimento: [3.3 pid namespace separato.md](file:///home/davidel/appunti/tesi/3.%20architetture%20alternative/3.3%20pid%20namespace%20separato.md)*

#### Concetti Fondamentali da Conoscere
1. **Linux Namespaces: PID vs Mount Namespace**:
   - `CLONE_NEWPID` virtualizza l'albero dei processi: il processo figlio riceve PID 1 nel proprio namespace, ma mantiene un PID corrispondente nel parent namespace.
   - Isolare solo il PID namespace non isola il filesystem virtuale `/proc`: se non si crea contestualmente un Mount namespace (`CLONE_NEWNS`) e non si rimonta `/proc` (`mount -t proc proc /proc`), il processo vede comunque i PID dell'intero container.
2. **Side-Channel di Monitoraggio Processi (`pspy`, Inotify su `/proc`)**:
   - Tool di spionaggio come `pspy` non eseguono solo un polling continuo (`sys_getdents64`), ma sfruttano le API `inotify` del kernel su directory di sistema e `/proc`. La creazione di qualsiasi directory numerica in `/proc` genera un evento che rivela comando, argomenti e timestamp dell'exploit di test al partecipante.
3. **Isolamento del Filesystem e File/Log Leaks**:
   - Poiché il filesystem del container rimane unico e condiviso, qualsiasi interazione del verificatore con i servizi (Apache, Nginx, PostgreSQL) scrive record nei file di log (`/var/log/...`) o file temporanei in `/tmp`. Il partecipante può estrarre il payload dell'exploit semplicemente ispezionando i log.
4. **Network Sniffing su Loopback (`AF_PACKET`)**:
   - Un PID namespace condivide lo stesso network namespace. Se lo script di verifica colpisce il servizio tramite `localhost` o l'IP di `eth0`, un semplice comando `tcpdump -i lo` o `tcpdump -i eth0` lanciato dal partecipante cattura il payload completo in chiaro prima che raggiunga l'applicazione.
5. **Blast Radius e Degradazione SLA**:
   - Nei contest Attack-Defense o Blue Team, gli exploit di verifica possono essere di tipo distruttivo (es. *denial-of-service*, corruzione di memoria, deadlock di tabelle SQL). Eseguirli in produzione fa crashare il servizio reale, causando penalità sull'SLA e interrompendo il lavoro del team.

---

### 3.4 Network Namespace Separato sull'Host (senza OVN/SDN)
*File di riferimento: [3.4 network namespace separato.md](file:///home/davidel/appunti/tesi/3.%20architetture%20alternative/3.4%20network%20namespace%20separato.md)*

#### Concetti Fondamentali da Conoscere
1. **Network Namespaces (`CLONE_NEWNET`, `ip netns`)**:
   - Crea un'istanza completamente isolata dello stack di rete: proprie interfacce, tabelle di routing, ARP cache, regole di Netfilter/iptables.
   - Permette a due bridge distinti di avere lo stesso indirizzo IP (`10.k.1.1`) perché risiedono in namespace diversi del kernel.
2. **Interconnessione via `veth` e Masquerading**:
   - Per dare connettività WAN al nuovo namespace, serve una coppia di interfacce virtuali `veth`: un'estremità nel namespace `verify-k` e l'altra nell'host root, con regole di IP Forwarding e SNAT/MASQUERADE tramite Netfilter.
3. **Bypass e Disallineamento dell'API dell'Orchestratore (Incus)**:
   - Incus non espone primitive di alto livello per collegare un container a un bridge gestito dentro un `ip netns` arbitrario dell'host.
   - L'agente dovrebbe spostare le interfacce con comandi shell a basso livello (`ip link set dev ... netns ...`), creando uno stato fantasma non tracciato dal database interno di Incus.
4. **Lifecycle delle Risorse Kernel, Dangling Devices e `rtnl_lock`**:
   - Creare e distruggere decine di namespace e coppie veth ad ogni ciclo di verifica (turnover elevato) provoca contese sul lock globale di routing (`rtnl_lock`).
   - Se un processo o socket mantiene aperto un riferimento all'interfaccia (`dev_hold`), il namespace rimane in stato dangling (`unregister_netdevice: waiting for dev to become free`), con rischio di esaurimento delle risorse kernel.
5. **Mancanza di Astrazione Multi-Nodo (Cluster Support)**:
   - I network namespace del kernel sono rigorosamente locali alla singola macchina fisica. OVN, invece, astrae switch e router logici incapsulando il traffico L2 in tunnel Geneve/UDP su rete fisica underlay, permettendo al sistema di scalare su cluster multi-nodo.

---

### 3.5 Esecuzione In-Memory con Mascheramento di `/proc`
*File di riferimento: [3.5 esecuzione in-memory con mascheramento.md](file:///home/davidel/appunti/tesi/3.%20architetture%20alternative/3.5%20esecuzione%20in-memory%20con%20mascheramento.md)*

#### Concetti Fondamentali da Conoscere
1. **Dynamic Linker Hooking (`ld.so`, `LD_PRELOAD`, `/etc/ld.so.preload`)**:
   - Funzionamento: sovrascrive le funzioni della libreria C dinamica (es. `readdir`, `opendir` in `libprocesshider`) per filtrare e nascondere cartelle numeriche associate al PID in `/proc`.
   - **Perché fallisce**:
     * Funziona solo con binari linkati dinamicamente. Binari statici (compilati con `-static`) o linguaggi moderni come **Go** e **Rust** non passano da `glibc`: effettuano syscall dirette (`SYS_getdents64`) in assembly, rendendo l'hook `LD_PRELOAD` completamente inefficace.
     * Lo sfidante con accesso root al container può modificare o cancellare `/etc/ld.so.preload` in qualsiasi momento.
2. **Fileless Execution (`memfd_create` e `fexecve`)**:
   - `memfd_create(2)` crea un descrittore di file anonimo residente unicamente in RAM (memoria volatile protetta).
   - `fexecve(3)` esegue il file binario referenziato dal descrittore senza che vi sia una dentry su disco.
   - Nonostante non vi siano file sul disco fisico, `/proc/[pid]/exe` punta comunque alla stringa `/memfd:... (deleted)`, denunciando in modo evidente l'attività furtiva.
3. **Osservabilità Kernel-Level (eBPF, Tracepoints, Auditd)**:
   - L'occultamento in user-space non ha alcun effetto sul kernel: hook eBPF su `tracepoint:syscalls:sys_enter_execve` o `kprobe:do_execve` intercettano la creazione del task in ring 0 con parametri, variabili d'ambiente e PID originali.
4. **Principio di Saltzer e Schroeder (Sicurezza Formale vs Obscurity)**:
   - *"Open Design"* e *"Complete Mediation"*: l'isolamento deve basarsi su barriere architetturali matematicamente verificate (hypervisor, namespaces, CoW snapshots), non su trucchi di evasione ("security through obscurity").
   - L'occultamento non previene il salvataggio dei log applicativi, non isola il traffico di rete e non evita il crash distruttivo del servizio.

---

## 2. Bibliografia e Risorse Consigliate per lo Studio

### A. Sistemi Operativi, Programmazione di Sistema e Namespaces
1. **Michael Kerrisk — *The Linux Programming Interface (TLPI)*** (No Starch Press, 2010)
   - *Capitoli chiave*:
     - **Cap. 6 (Processes)**: anatomia di un processo, layout di memoria, PID.
     - **Cap. 19 (Monitoring File Events with inotify)**: meccanica usata da `pspy` per rilevare processi tramite `/proc`.
     - **Cap. 24–28 (Process Creation, Execution, Termination)**: `fork`, `execve`, gestione dell'albero dei processi.
     - **Cap. 41–42 (Shared Libraries & Dynamic Linking)**: funzionamento del loader dinamico `ld.so`, caricamento simboli e uso di `LD_PRELOAD`.

### B. Networking del Kernel Linux, Bridge e Routing
1. **Christian Benvenuti — *Understanding Linux Network Internals*** (O'Reilly, 2005)
   - Testo di riferimento per:
     - Architettura del Linux Bridge e Forwarding Database (FDB).
     - Gestione ARP e neighbor table nel kernel.
     - Routing table lookup (FIB) e instradamento L3.
2. **Rami Rosen — *Linux Kernel Networking: Implementation and Theory*** (Apress, 2014)
   - *Capitoli chiave*:
     - **Cap. 11 (Network Namespaces)**: implementazione di `struct net`, isolamento delle tabelle di routing e coppie `veth`.
     - **Cap. 5–6 (Netfilter and Routing)**: architettura di hook packet filtering, connection tracking e NAT.
3. **Vincent Bernat — Articoli Tecnici di Architettura di Rete**:
   - *"Dangers of some Linux sysctl: rp_filter"* (analisi indispensabile per comprendere il fallimento del multi-homing in 3.2).
   - *"Introduction to Linux network namespaces"* e *"Bridge vs Open vSwitch"*.

### C. Software Defined Networking (SDN), Open vSwitch e OVN
1. **Ben Pfaff et al. — *The Design and Implementation of Open vSwitch*** (USENIX NSDI, 2015)
   - Il paper accademico fondamentale che spiega i limiti di scalabilità e flessibilità del bridge Linux classico e i vantaggi del datapath OpenFlow separato tra kernel fast-path e control-plane in user-space.
2. **Open Virtual Network (OVN) Documentation**:
   - `ovn-architecture(7)`: architettura dei Logical Switches, Logical Routers, Northbound DB, Southbound DB, `ovn-northd` e `ovn-controller`.
   - RFC 8926: *Geneve: Generic Network Virtualization Encapsulation* (protocollo di overlay su porta UDP 6081 usato da OVN).
3. **Siddhartha D., Goransson P., Black C. — *Software Defined Networks: A Comprehensive Approach*** (Morgan Kaufmann, 2016)
   - Concetti formali di separazione tra Data Plane e Control Plane, centralizzazione logica e astrazione di topologie di rete.

### D. Sicurezza dei Container, eBPF e Principi di Isolamento
1. **Liz Rice — *Container Security: Fundamental Technology Concepts that Protect Containerized Applications*** (O'Reilly, 2020)
   - Spiega nel dettaglio perché i container Linux condividono il kernel host, come i namespace e i cgroups creano confini e quali sono le vie di fuga (filesystem leaks, network visibility).
2. **Brendan Gregg — *BPF Performance Tools*** (Addison-Wesley, 2019)
   - Dimostra l'uso di eBPF per il tracciamento di sistema (`execsnoop`), dimostrando come qualsiasi mascheramento tentato in user-space (3.5) sia visibile dal kernel.
3. **Jerome H. Saltzer & Michael D. Schroeder — *The Protection of Information in Computer Systems*** (Proceedings of the IEEE, 1975)
   - Il pilastro della teoria della sicurezza informatica: i principi di "Complete Mediation", "Economy of Mechanism" e il rifiuto formale della "Security through Obscurity".
