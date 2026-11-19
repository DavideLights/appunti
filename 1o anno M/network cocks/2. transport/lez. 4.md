# planes
**data plane**: function related to low-level forwarding and actual packet analysis for processing.

**control plane**: deals with network control, routing and so on. Determines an end-to-end route, applies algorithms given an input routing.
* **note**: routing is not necessarily per-packet based (e.g., in circuit-switched/optical networks it sets up an end-to-end path/circuit per connection flow rather than forwarding packet-by-packet), and depends on link states between routers. Generally it is influenced by the global/local network state. #gemini
* **how it's implemented**? software
* **two architectures**: 
	* centralized: a server that executes the algorithm and sends control messages to instruct devices about how to deal with traffic.
	* decentralized: each router executes an instance of the algorithm

**management plane**: operations that a network needs to perform to manage and monitor the network.
* **monitoring**: what is the health status of the network?
* **configuration**: procedures related to configuring specific parameters on the device. Kathara labs is just configuring the management plane.
	* **through**: CLI, and OS.
	* set up VPN
	* configure routing protocol
	* PORCODDDIO

> see the cute slide

# framework example
**Optical data plane**: where user data passes

**Element management systems (EMS)**: vendor-provided (because generally optical devices are "closed" and difficult to make cooperate)
* lack of interoperability
* a single device costs like luca's mom, a lot!

**Network Management System (NMS)**: has lots of tasks
* **tracking**: keep track in a database of a list of devices installed in the network.
	* **monitor**: we have agreements (SLAs) with the customer, so we have to monitor and check that we are respecting the contract we signed.
* exposes an interface to clients to make connections
	* they ask the optical network for the creation of a logical connection
	* so to make a logical connection: the user sends a connection request through the NMS; this req contains:
		* endpoints (router in rome and router in milan as ex.)
		* QoS parameters: the level of treatment that it should guarantee
			* BER
			* Reliability
			* Percentage of time the connection is up (Availability)
			* Max delay -> among all the paths we need the path to respect Max delay.
	* received the request, we have to solve it as a routing problem. The NMS has to optimize the routing on our constraints in the req
	* then the NMS sends the configuration to the devices involved with the user's request, he want to apply the sberz
	* we need to instruct routers how to route

# optical network layers 

Communication networks are described through layered architectures.

**encapsulation**: data is encapsulated when passing in a layer. At each layer:
* **header**: is made of fields describing how the service is provided. 

**decapsulation**: 
* basic rule for a layered architecture: decapsulation is performed at the destination.
* a switch does not decapsulate the packet if he is not the final end point
	* he just looks at the Layer 2 header, that is the most external one

**monitoring**: is done at lower layers 

# otn encapsulation
* **client layer**: an ethernet frame, IP packet, or something else; we are transparent so the client is anything.
* client PDU is encapsulated inside an **OPU (Optical Payload Unit)**:
	* OPU: we add a header to it (adapts client rate and identifies payload type) #gemini
	* this header will provide information allowing the Optical network to offer services to the client.
	* protection against binary errors, forward error corrections, and so on (handled across the digital OTN layers). #gemini
* **ODU (Optical Data Unit)**: encapsulates OPU; provides end-to-end digital path monitoring (e.g., BER via BIP-8) and tandem connection monitoring. #gemini
* **OTU (Optical Transport Unit)**: is in the electrical domain, adds a header and a **FEC (Forward Error Correction)**.
	* **electrical vs optical domain**: in the **electrical domain** (OPU, ODU, OTU), frames are digital bits processed electronically (before laser modulation or after photodiode reception). In the **optical domain** (OCh, OMS, OTS), the signal is pure light ($\lambda$) traveling through fibers, muxes, and amplifiers without O-E-O (Optical-Electrical-Optical) conversion. #gemini
	* **exposed devices at OTU**: exposes only the endpoints where O-E-O conversion occurs (i.e., **transponders** and **3R regenerators**); the entire optical path between them is seen as a single black-box link/subnetwork. #gemini
* **OCh (Optical Channel)**: is in the optical domain, optical channel dio porco
	* it exposes subnetworks and single wavelength-level devices (**transponders**, **ROADMs / optical cross-connects**) #gemini
	* **exposes**: optical subnetworks, and is processed by endpoints (transponders) and wavelength switches
	* we have the visibility of a single client signal (one wavelength $\lambda_i$) #gemini
	* in OCh we have not yet multiplexed different wavelengths together!
* **OMS (Optical Multiplex Section)**: is the optical multiplex section (between **WDM MUX** and **DEMUX**); it aggregates multiple $\lambda_i$ channels and does not expose line amplifiers. #gemini
* **OTS (Optical Transmission Section)**: exposes **amplifiers** (plus MUX/DEMUX), we see the entire physical infrastructure; here we can monitor every fiber span, but we don't have control of the single client signal because all wavelengths have been multiplexed.
	* **note**: we are in the optical signal domain, we have to understand how to process the overhead.

look at the slides!!!@#E!@#%@!#%

* what if we want to monitor the BER? we can monitor at **ODU / OTU** level (electrical domain, since bits are needed to count bit errors). #gemini
	* if BER is high, something is going wrong on some equipment in lower layers.
	* good for monitoring quality provided to the customer
	* we should monitor at lower levels to understand in which subnetwork and which device the problem is.


# performance and fault management
> **ber**: if BER is negligible then the infrastructure is working.

> **optical power**: is measured at the optical layer
> * high: good
> * low: something is sbergizing!


**optical trace (Trail Trace Identifier - TTI)**: is identified by the identity of the endpoints (**SAPI** = Source Access Point ID, **DAPI** = Destination Access Point ID). Sent in the overhead so the receiver can verify it is connected to the expected transmitter and detect misconnections/misconfigurations in optical switches (raising a *TIM - Trace Identifier Mismatch* alarm). #gemini

**alarm management**: a problem detected generates an alarm. A single fault might generate a cascade of alarms across the system (alarm storm). #gemini
* the network management system should understand what was the **root-cause**!
* **alarm suppression**: based on defect indicator messages (**FDI** and **BDI**).
	* **how it works**: when a device detects a primary fault (e.g., loss of signal), it sends an alarm to the NMS and injects a **FDI (Forward Defect Indication)** downstream (and **BDI - Backward Defect Indication** upstream). Downstream devices/layers receiving the FDI know the failure occurred upstream, so they **suppress** their own secondary alarms to the NMS. #gemini

**alarm example**:
* **FDI**: allows alarm suppression; amplifier $B$ detects the broken incoming fiber (OTS $A\text{–}B$) and is in charge of generating backward (OTS-BDI to $A$) and forward (OMS-FDI) defect indicators. #gemini
* **Amplifier $C$** does not see any OTS failure when the fiber fails before $B$ (because the fiber $B\text{–}C$ and $B$'s OSC laser are still working, so OTS $B\text{–}C$ is healthy!). #gemini
* **The (de)multiplexer** instead notices the failure: there are optical supervisory channels (OSC) sensing the liveness for each multiplexed connection (OMS)
	* so **OMS** can sense those fails (via OMS-FDI sent by $B$ over the OSC) and generates **OCh-FDI** forward. #gemini
* **transponders**: they will see a lack of optical power, because the signal is lost (and suppress their alarm thanks to OCh-FDI). #gemini
* **how alarms spread across layers (and why some devices/layers are skipped)**: #gemini
	* **upward propagation across layers**: a fault detected at a lower layer ($L$) terminates at that layer's endpoint, which injects an FDI into the **next upper layer ($L+1$)** ($\text{OTS fault at } B \to \text{OMS-FDI to Demux} \to \text{OCh-FDI to Transponder} \to \text{ODU-AIS to Client}$). #gemini
	* **why a device/layer is skipped (Example 1 — Fiber cut before $B$)**: since OTS is hop-by-hop between adjacent amplifiers, OTS $A\text{–}B$ terminates at $B$. $B$ elevates the alarm to **OMS-FDI** on the OSC; **Amplifier $C$ only terminates OTS $B\text{–}C$**, so **Amplifier $C$ is skipped** (it sees a valid OSC signal from $B$ and ignores OMS-FDI), whereas the Demux terminates OMS and catches it. #gemini
	* **skipping lower layers (Example 2 — Single $\lambda$ / laser fault)**: if a single transponder laser fails before the MUX, the fiber and OSC are intact, so **OTS and OMS are completely skipped** (amplifiers and MUX/DEMUX see no link fault); only the **OCh / OTU / ODU** layers at the receiver detect the failure. #gemini

> [!WARNING] Self-Study Check: Multi-Layer Fault Scenarios #gemini
> Check the fault-propagation diagram on the **Lecture 4 slides** and trace which layer terminates vs. forwards FDI at each node (`Amp B`, `Amp C`, `MUX/DEMUX`, `Transponder`): #gemini
> * **Why $B$ sends OMS-FDI instead of OTS-FDI to $C$**: `* [INSERT HERE]` #gemini
> * **What happens if the fiber breaks between $C$ (last amplifier) and the DEMUX**: `* [INSERT HERE]` #gemini


**overhead**: in the electrical domain, the header is just extra digital bytes; in the optical domain, it is carried in two ways: #gemini
* **OSC (Optical Supervisory Channel)**: is an out-of-band wavelength/channel dedicated to monitoring. There is a separate transponder and wavelength (e.g., $1510\text{ nm}$) dedicated to monitoring porcaccia la madonna porco deddio bastardo frocio.
	* the OSC is terminated and regenerated at every device per physical link (OTS/OMS level) #gemini
	* it is a single shared control channel not tied to a single client data signal (if a single client $\lambda_i$ degrades without breaking the fiber, the OSC wavelength itself is unaffected, though it can carry control messages about channels). #gemini
* **pilot tone**:  
	* note: between real signals (or at low frequency) there is unused space to avoid interference
	* this space (or a small amplitude modulation on $\lambda_i$) can be used to insert a small sinusoidal tone
	* each tone frequency is associated to a single client $\lambda_i$, allowing intermediate nodes to monitor individual client power/presence in the optical domain without demultiplexing or O-E-O conversion! #gemini