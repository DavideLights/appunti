**access network**: e'divisa dalla backbone/core network/transport network
* access network: tecnologie eterogenee
* core network: tecnologie omogenee

> **FTTC**: curb/cabinet. e' la piu usata, grazie al cazzo. avviene lo switching da fibra ad un'altro medium, es: copper.


# wireless

fixed network element: one closed to the core, another one close to the user.

fixed network access: when core and sbors are fixed (???)

wireless is cheaper than fiber/copper.

**cellular wireless access**: has two main components
* first is wireless
* second gives the **mobility**
* mobility it is not available in the other case

> **D**: what the name in case you don't have cellulare wireless

**2g and 3g**: 
* standardize a mobile network $\equiv$ a new generation $G$.
* **name for 2g and 3g**: GSM
* wireless part is only from antenna to the node, everything else is wired.
* network element/entity, **RNC** (Radio Network Conotroller???)
	* each generation the name changes, but function is the same
	* manages connectio 
	* **cell**: hexagon, represents and area covered by an antenna. multiple users connected to the antenna.
	* **role for RNC**: manages access for the users.
	* **node B**: base station is the name for the antenna in the standard.
* network elemen **BSC**: base station controller
	* **example**: if thousand of people are connected to the nearest base station it might be overloaded. can we balance the load to another near station?
* mobile switching center **MSC**: manages mobility.
	* what happens if we move from a station to another?
		* and if you have an open session?
	* it traces your position, and id in the network.
	* guarantees continuity for the service.

**hand over**: switching name for continuity, it's the mechanism allowing continuity.


what happenend between 3g and 4g/5g:
* 3g is design for voice calls
* 4g/5g: paradigm shift, from voice calls to the data.

5g network: in the access part the paradigm switch
* Packed Switch Network: packet based switching is design inside 5g
* architecture:
	* **AMF**: Access and mobility management function. Same role as RNC.
	* **SMF**: Session Management Function. High level details, how to manage authentication, cyphering, ecc...
	* **UPF**: User Plane Function. data management, where packets are?

**AMF and SMF are inside the control plane**: intelligence of the network

**UPF**: is in the planning plane, 

**SMF interacts with UPF**: SMF decids priority for packets, there are 3 category of services with it's own charateristics.


**AMF interacts with antenna**: trivial.

**gNB**: node base station.

**UE**: user equipment

**wireless**: it's only between UE and gNB.


**wireless spectrum**:
* 3 questions:
	* where the communication has to go?
	* cost of the access to the spectrum: about 7 billions in italy.
* band
	* **speed**: depends on band length
	* **distance**: lower is the frequency, the larger is the distance.
		* television is lower frequency than sbergs.

5g operates on high frequency: because there is large bandwidth available
* increase density of antennas

**edge**: when there is no coverage for 4g, there is back compatibility with edge at bad speed.

**gsm**: forza europa!!! e' nato in eu, grazie alla standardizzazione. in america c'e' standardizzazione differente. now we are collapsing to one standard.

**3gpp**: original standardization body. it allows every country to adopt the same standard nowdays.

**WiFi standard**: IEEE 802.11. supports wireless access in local area network, quite short.
* in the original standard, mobility is not included
* adding it is hard

**RAN, MAN, LAN, PAN**: personal, local metropolitan, regional.

**bluetooth**.

**WiFi6**: integrates wifi with mobile network. appendix for mobile so you can do calls on top of it.
* WiFi6 does not connect you to a fixed infrastructure, it connects you to the 5g network

why????