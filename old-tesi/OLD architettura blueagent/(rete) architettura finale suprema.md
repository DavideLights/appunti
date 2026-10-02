Ecco la scomposizione dettagliata delle due architetture, le alternative industriali e l'analisi critica supportata dalla letteratura scientifica recente per la tua seduta di laurea.


### 1. Architettura di Produzione (Ambiente Live del Team $k$)

L'architettura di produzione è progettata per fornire un accesso segmentato e sicuro ai container vulnerabili. Si basa sull'instradamento nativo del kernel Linux, delegando l'isolamento di livello 2 (L2) a switch virtuali (bridge) e l'accesso remoto di livello 3 (L3) a tunnel crittografici.

**Dettaglio Interfacce e Ruoli**
- **L'Interfaccia VPN (`wg-k`)**
    - **Ruolo:** Terminatore crittografico L3 (WireGuard).
    - **Cosa fa:** Accetta le connessioni in ingresso dai partecipanti autenticati. Le viene assegnata una subnet punto-punto ristretta (es. `10.k.0.0/30`).
    - **Utilità:** Delega l'autenticazione e la crittografia a un modulo kernel-space. Separa logicamente gli indirizzi IP sorgente dei giocatori, permettendo al firewall dell'host di applicare regole rigorose basate sull'interfaccia in ingresso.  
        
- **L'Interfaccia Bridge (`br-team-k`)**
    - **Ruolo:** Switch virtuale L2 e Gateway predefinito.
    - **Cosa fa:** Collega i container di un team allo stesso dominio di broadcast. L'host assegna a questa interfaccia l'indirizzo IP `10.k.1.1`, che funge da _default gateway_ per i container.
    - **Utilità:** Isola il traffico ARP e broadcast tra team diversi. Permette al kernel dell'host di instradare i pacchetti dalla `wg-k` verso i container e fornisce loro un punto di uscita verso Internet (tramite NAT host).
- **L'Interfaccia dei Container (`eth0`)**
    - **Ruolo:** Endpoint di erogazione del servizio vulnerabile.
    - **Cosa fa:** Riceve l'indirizzo IP statico `10.k.1.x`.
    - **Utilità:** Espone i demoni e i servizi della challenge. Mantiene una topologia standardizzata (es. il database è sempre su `.3`, il web server su `.2`).

**Pregi, Difetti e Prestazioni**
- **Pregi:** Estrema trasparenza. Non utilizza incapsulamento SDN (Software Defined Network), semplificando la diagnostica con strumenti standard come `tcpdump`.
- **Difetti:** L'aumento lineare del numero di team richiede la creazione dinamica di coppie bridge/VPN e l'aggiornamento massivo delle tabelle di routing/NAT dell'host, rischiando di saturare la tabella `conntrack` sotto stress elevato.
- **Performance:** Eccellenti. La velocità di comunicazione intra-container sul bridge opera a velocità di bus RAM (near bare-metal), mentre WireGuard introduce latenze crittografiche marginali rispetto ad alternative come OpenVPN.
    
      
    

### 2. Architettura di Verifica (Ambiente Effimero)

Per valutare il _patch management_ senza interferire con i giocatori, l'architettura sfrutta il Copy-on-Write (CoW) del filesystem per generare sandbox usa-e-getta disconnesse dal routing principale.

  

**Dettaglio Interfacce e Ruoli**
- **Il Bridge Effimero (`br-verify-l`)**
    - **Ruolo:** Switch L2 puro (Dark Bridge).
    - **Cosa fa:** Interconnette i cloni e il container checker. A differenza della produzione, **non ha alcun IP assegnato sull'host**.
    - **Utilità:** Permette ai cloni di comunicare tra loro mantenendo i medesimi IP (`10.k.1.x`) della produzione senza generare collisioni di routing (IP Overlap) sulla tabella principale dell'host.
- **L'Interfaccia Locale dei Cloni (`eth0`)**
    - **Ruolo:** Replica dello stato originario.
    - **Cosa fa:** Viene agganciata a `br-verify-l` con gli indirizzi IP `10.k.1.x` ereditati dallo snapshot.
    - **Utilità:** Permette allo script di exploit del checker di colpire bersagli identici a quelli esposti in produzione.

- **L'Interfaccia Uplink dei Cloni (`eth1`)**
    - **Ruolo:** Via di fuga verso Internet.
    - **Cosa fa:** Viene agganciata a un bridge pubblico orchestrato (es. `incusbr0`), assumendo la _default route_ (il gateway predefinito).
    - **Utilità:** Aggira l'assenza del gateway sul bridge isolato, consentendo ai cloni di scaricare dipendenze o risolvere query DNS esterne durante la fase di valutazione.
- **L'Interfaccia del Checker (`eth0`)**
    - **Ruolo:** Punto di lancio dell'attacco.
    - **Cosa fa:** Si connette a `br-verify-l` ricevendo un IP compatibile. Esegue lo script di verifica distruggendosi al termine.
    - **Utilità:** Garantisce che l'exploit parta esattamente dalla stessa sottorete L2 dei bersagli, testando in modo veritiero le patch applicate al traffico locale.        

**Pregi, Difetti e Prestazioni*
- **Pregi:** Annulla la necessità di gestire complessi router virtuali SDN (come OVN). Il ciclo di vita della verifica (snapshot, avvio, test, cancellazione) è totalmente incapsulato e sicuro.
- **Difetti:** L'introduzione di una `eth1` altera il numero di interfacce rispetto alla produzione e sposta il _default gateway_. Patch strettamente legate all'interfaccia originale (`eth0`) per il traffico in uscita genereranno falsi negativi.
- **Performance:** Dominanti in I/O. Grazie a file system ZFS/Btrfs, i cloni a freddo nascono in millisecondi. Il traffico di exploit non impatta le CPU dedicate all'host routing, restando confinato nello switch virtuale.

### Alternative Industriali (Ricerca e Mercato)

**Alternative per la Produzione (Isolamento Team):**

L'alternativa standard del settore cloud-native è l'utilizzo di orchestratori come **Kubernetes (K8s) o Docker Swarm con reti Overlay**. Anziché usare Bridge e WireGuard per team, ogni team corrisponde a un _Namespace_ K8s isolato tramite _Network Policies_ (es. Calico CNI).
- _Perché è scartabile:_ L'astrazione K8s è eccellente per erogare microservizi web stateless, ma aggiunge un enorme overhead cognitivo e computazionale per CTF di _patch management_ puro, dove i partecipanti devono avere accesso shell o SSH root-like persistente ai container.
    
      
    

**Alternative per la Verifica (Clonazione e IP Overlap):**

L'approccio accademico per risolvere il problema dei cloni con IP identici si basa spesso su **Cyber Ranges pesanti basati su OpenStack (es. Kypo)**. OpenStack Magnum e il modulo Neutron creano router SDN (Software Defined Network) completamente isolati per ogni scenario di test.
- _Perché è scartabile:_ Richiede datacenter dedicati. Alzare un'istanza Neutron per valutare uno script Python di 10 secondi introduce latenze di provisioning intollerabili in una competizione in tempo reale.
### Validazione Accademica per la Seduta di Laurea

In sede di discussione, ti verrà chiesto perché non hai semplicemente adottato Kubernetes o una piattaforma Cyber Range pre-esistente per orchestrare l'infrastruttura.

  

La letteratura recente individua un vuoto netto tra i frontend di semplice gestione (come l'installazione standalone di CTFd) e le pesanti piattaforme Cyber Range (come KYPO). I recenti paper accademici che affrontano l'erogazione di "CTF as a Service" (CaaS) o infrastrutture basate su container, evidenziano che l'isolamento dinamico degli ambienti (soprattutto in competizioni Attack-Defense o Patch Management) rappresenta ancora un collo di bottiglia operativo. Spesso gli istituti si affidano a complesse configurazioni Docker Swarm con overlay network o pesanti istanze OpenStack.

  

**La tua difesa dell'architettura si basa sul concetto di "Efficienza Orizzontale per Ambienti Stateful":**

1. **L'argomentazione sulla Semplicità (Rasoio di Occam):** Il tuo sistema è più semplice perché rifiuta le astrazioni SDN pesanti. Progettare un backend FastAPI che dialoga nativamente con l'API di Incus per configurare namespace e bridge L2 garantisce un controllo deterministico dell'infrastruttura di patching. Rispetto all'utilizzo di orchestratori generici (come Kubernetes, studiato per microservizi stateless e _fault tolerance_), il tuo modello a "container pesanti" supportati dalle funzionalità native del kernel Linux rappresenta la forma più pulita per garantire accessi shell pseudo-bare-metal richiesti dal patch management.
    
2. **L'argomentazione sull'Efficienza (Storage e CoW):** L'infrastruttura basata su clonazione effimera a freddo batte in prestazioni i Cyber Range accademici classici. Ottenere un clone per la verifica tramite gli snapshot differenziali (Copy-on-Write) di Incus abbatte i tempi di provisioning a frazioni di secondo, operazione che in sistemi basati su macchine virtuali o pipeline Terraform/Ansible richiederebbe dai decine di secondi ai minuti per ogni sottomissione.

**L'Autocritica (Se l'infrastruttura non fosse la più efficiente in assoluto):**

Devi essere intellettualmente onesto con la commissione: il tuo sistema **non è il più scalabile orizzontalmente**. Se il backend FastAPI dovesse gestire migliaia di team distribuiti su decine di datacenter, il modello a singoli bridge L2 e routing iptables per team sull'host saturerebbe. In scenari cloud multi-nodo massivi, l'approccio _GitOps_ basato su Kubernetes o reti OVN distribuite diventa obbligatorio. Tuttavia, per il _domain bound_ di competizioni universitarie (fino a qualche centinaio di container), delegare la separazione del traffico a primitive native del kernel garantisce il massimo grado di affidabilità e la minima latenza possibile, centrando perfettamente i requisiti del progetto.