# Report di Analisi e Revisione: CyTrONE vs BlueAgent
**Documento analizzato:** `1.3.3_CR_Alternativi_CyTrONE.md`  
**Data:** 09/10/2026  

---

## 1. Come "blastare" CyTrONE in ottica BlueAgent (Dominio A/D e Patch Management)

Il framework **BlueAgent** è progettato specificamente per competizioni **Attack-Defense (A/D)** e scenari complessi di **Patch Management**, contesti caratterizzati da vincoli operativi e architetturali stringenti che CyTrONE non è strutturalmente in grado di soddisfare.

### Punti critici da evidenziare contro CyTrONE:
1. **Side-Channel Leakage sistematico nei controlli:**
   - In una competizione A/D, la verifica periodica tramite checker automatizzati richiede l'invio di exploit/payload per testare lo stato di vulnerabilità del servizio.
   - CyTrONE adotta un *cyberattack controller* remoto che scaglia attacchi (es. via Metasploit) direttamente attraverso la rete del partecipante.
   - **Conseguenza critica:** Un concorrente può eseguire `tcpdump` o Wireshark sulla propria interfaccia di rete, intercettare il payload malevolo inviato dal checker e **replicarlo immediatamente contro gli altri team**, distruggendo l'integrità e l'equità della competizione.
   - **Soluzione BlueAgent:** Separazione netta tra ambiente Live e Sandbox. Le verifiche avvengono su cloni Copy-on-Write (CoW) isolati tramite OVN/Linux network namespaces, impedendo qualunque sniffing o fuga di payload.

2. **Rischio di Denial of Service / Crash del sistema Live:**
   - L'esecuzione di payload aggressivi o malformati contro l'istanza live di training può provocare kernel panic, corruzione di database o blocco dei servizi.
   - In CyTrONE ciò compromette l'intero ambiente del partecipante, richiedendo interventi manuali o lunghi reset.
   - In BlueAgent, il test viene eseguito esclusivamente su un'istanza clonata effimera: anche in caso di crash totale del clone, l'ambiente di produzione del team rimane intatto e operativo.

3. **Latenza di Provisioning e Ripristino (Rollback Inaccettabile):**
   - Durante una CTF è frequente che un concorrente renda instabile il proprio sistema e necessiti di un ripristino.
   - CyTrONE impiega minuti (fino a 8+ minuti per scenari base con sole 2 VM) e degrada esponenzialmente con l'aumentare dei nodi.
   - BlueAgent garantisce provisioning e rollback in **~100–500 ms** grazie all'uso di container di sistema Incus/LXC e snapshot a livello di blocco (ZFS/Btrfs).

4. **Inadeguatezza dell'Isolamento Topologico:**
   - Una CTF A/D moderna richiede topologie di rete complesse e omogenee (es. subnet identiche `10.k.1.0/24` per ogni team $k$) per non dover riscrivere script o regole di routing.
   - CyTrONE si affida a clonazione tradizionale (`parallel-scp`) su hypervisor KVM, risultando rigido e non scalabile nella gestione di reti virtualizzate multi-tenant isolate.

---

## 2. Punti da Approfondire nel Testo

- **Quantificazione dell'overhead delle Macchine Virtuali (VM):**
  - Esplicitare i costi reali: 1–4 GB di RAM pre-allocata per VM guest, overhead di virtualizzazione CPU (VT-x/AMD-V) e boot time completo del kernel OS.
  - Confrontarlo con i container di sistema (LXC/Incus): overhead di memoria ridotto a ~100–300 MB e condivisione sicura del kernel host.
- **Dicotomia "Training Guidato" vs "Competizione Dinamica":**
  - CyTrONE assume verifiche elementari basate sul confronto di stringhe/flag note (*Assunzioni 1 e 2*).
  - Nel Patch Management contemporaneo la validazione è **stateful e bivalente**: deve attestare sia la neutralizzazione della falla, sia la conservazione dell'integrità funzionale (SLA del servizio per utenti legittimi).

---

## 3. Elementi Mancanti di Rilievo Architetturale

- **Mancanza del concetto di Sandbox / Dual-Environment:**
  - CyTrONE opera su una singola istanza per utente. Manca completamente il paradigma fondamentale di BlueAgent: **biforcazione tra Live Environment e Sandbox effimera**.
- **Modernità dello Storage (CoW vs Immagini monolitiche):**
  - La clonazione di intere immagini disco via rete con `parallel-scp` è un collo di bottiglia non accettabile; mancano riferimenti alla gestione moderna tramite filesystem Copy-on-Write (ZFS/Btrfs).
- **Sicurezza di Connessione e Anti-Spoofing:**
  - Assenza di meccanismi di VPN crittograficamente confinata (come il Cryptokey Routing di WireGuard in BlueAgent) per prevenire intercettazioni e spoofing tra team differenti.

---

## 4. Revisione Qualitativa del Documento e Correzioni Formali

### Punti di Forza:
- Ottima linearità nell'esposizione dei macro-componenti (CyLMS, CyRIS, CyPROM).
- Sezione benchmark quantitativi (1.3.3.1) chiara, efficace e ben argomentata tramite dati sperimentali (StarBED).
- Perfetta impostazione per introdurre il contrasto prestazionale cercato dalla tesi.

### Correzioni Formali da apportare (Typo e Sintassi):
1. **Riga 7:** `si occupa d icaricare` $\rightarrow$ `si occupa di caricare`
2. **Riga 14:** `si conentra` $\rightarrow$ `si concentra`
3. **Riga 16:** `Quindi l'esperienza utente si concentra sul fatto che...` $\rightarrow$ Stile informale. Riformulare in:  
   *«L'esperienza utente è incentrata sulla fruizione del percorso didattico tramite piattaforma LMS e sul contestuale accesso al Cyber Range dedicato.»*
4. **Riga 23:** `Training Coordinator".Le` $\rightarrow$ Spaziatura errata dopo le virgolette e il punto (`Training Coordinator". Le`).
5. **Riga 31:** `vulnearbilita` $\rightarrow$ `vulnerabilità`
6. **Riga 33 e 35:** `Tutta via` $\rightarrow$ `Tuttavia`
7. **Riga 59:** `Nella figura sborgz viene analizzato...` $\rightarrow$ **Placeholder rimasto nel testo (`sborgz`)**. Sostituire con il corretto riferimento (`Nella Figura X` o `Nella figura sottostante`).
8. **Riga 66:** `Con il nostro lavoro di tesi, si vuole cercare di abbattere...` $\rightarrow$ Preferibile formula accademica attiva:  
   *«L'obiettivo del presente lavoro di tesi è abbattere il tempo complessivo di approvvigionamento $T$, riducendolo dall'ordine dei minuti a quello dei secondi su hardware non dedicato.»*
