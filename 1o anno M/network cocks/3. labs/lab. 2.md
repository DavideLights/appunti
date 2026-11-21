**focus**: on Network layer and data link, so MAC, IP subnetting and IP routing.
* **1. Physical Layer**: physical transmission.
* **2. Data Layer**:
	* **goal**: manages addressing between adjacent nodes in the network.
	* **MAC**: network layer L2 unique identifier for devices.
* **3. Network Layer**: manages addressing between distant nodes.
	* **IP**: each node has a unique identifier.
* **4. Transport Layer**: end-to-end transport via **ports** and multiplexing.
	* `netcat` operates at transport level, it incapsulates user's data here.
* 5. **Application layers**: session, presentation and application
	* between transport and application may be applied TLS for example.

**addresses**: each node in a network has at least one IP address and one MAC address.
* **MAC address**: identify a network interface, and gets assigned from the manufacter's pool of addresses.
* **IP address**: assigned logicaly to create different subnetworks. May change over the time.

**ARP**: address resolution protocol
* **goal**: discover MAC address associated to an IP address
* **scenario**: we know ip address, we want to deliver the packet the device, but we do not know the MAC address.
* **ARP request**: what's the MAC address of 10.10.10.3?
* **ARP reply**: i'm 10.10.10.3 and my MAC address is ...

> [!note] extra: why do we need MAC and IP together?
> 1. **hierachical structure**:
> 	1. **MAC addressing involves a flat structure**, because a MAC address does not reveal anything about the topology of the network, it's not a logical address.
> 	2. **IP addressing is hierarchical**, an ip address has a network prefix and a suffix identifyng the end host. IP allow routers to aggregate destinations to make routing easier.
> 2. **hop-by-hop** vs end-to-end:
> 	1. hop-by-hop: a MAC address is valid only in the local subnetwork when routing a packet from an end point to another.  Each hop for a packet involves discarding and creating a new frame with new values for the destination MAC address.
> 	2. end-to-end: ip source and destination are fixed when the packet travels the network.
> 3. **IP is independent from the link layer**, while MAC depends on what protocol we are using
> 4. **assignment**:
> 	1. **IP**: may be static, choosen by the user, or assigned dynamically by the DHCP server.
> 	2. **MAC**: its static and assigned by the **manufacter**.

**cache**: MAC address collected by ARP are stored in a cache.
* `ip neigh` shows that cache
* **states**: an entry in the ARP table might be in one of the following states 
	* INCOMPLETE
	* REACHABLE
	* STALE
	* DELAY
	* PROBE
	* FAILED
* **timers**: regulate state changes. The new states depends on the current state and elapsed time and other things that you can see in the kernel code.

**main ARP rule**:
1. first check if we have an entry for an IP address
2. if not present, then make an  ARP request.

**ARP example**:
* **scenario**:  `pc1 <-> r1 <-> s1`
* **goal**: `pc1` wants to ping `s1`
![[Pasted image 20261121000156.png]]

* **note**: two ARP requests are needed
* **broadcast**: an ARP requests has `Dst: ff:ff:...:ff:ff`
	* it specifies the **sender MAC** address and the **sender IP** address
* **ARP reply**: an ARP reply has the answer in the **sender MAC** and **sender IP** fields
* other ARP packets:
	* **ARP Probe**: check if an IP address is used, expect so a reply from the owner
	* **ARP Announcement**:![[Pasted image 20261121001207.png]] 
		* announce to everyone my IP address

**(extra) why ARP probe and ARP announcement?**
* **scenario**: `A` to avoid IP conflicts, needs to know if in the subnetwork there are other hosts using the same IP
* **solution**: 
	* send a few ARP probes specifing an IP address
	* if no one responds i can claim that IP address
	* issue an ARP Announcement
* **broadcast**: ARP probe and ARP announcement are sent in broadcast.

**(extra) ARP probe**: has **src IP field** and the target MAC address **empty**

![[Pasted image 20261121002159.png]]

**(extra) ARP announcement**:
![[Pasted image 20261121002208.png]]

**the lie behind MAC**:
* **theory**: MAC addresses assigned by manufacter
* **practice**: `ip link set eth0 address 00:11:22:33:44:55`

**security**: 
* **exploiting MAC**: do not use MAC to identify users and give grants to them! An attacker can pretend to be someone else thrusted.
* **ARP spoofing**: an attackers pretends to be someone else by exploiting ARP to associate its MAC to someone else's IP address.
	* after ARP spoofing what?
		* inspect
		* and then redirect to the original receiver.
		* or do not redirect causing DoS
* **tracking**: Wi-Fi based localization
	* devices sends to a remote server mac addresses of near Wi-Fi access points
	* server updates a database, some have milions of record 
	* some of the MAC have a known position, so you can estimate someone's position just by their MAC.

**How many IP addresses belong to a subnet**? $2^n-2$
* one is the subnet itself
* the other one is the broadcast address
* **howerver**: by convention, **they are valid** ip addresses to assign.

## commands
> [!note] tcp dump trick
> `tcpdump -i any -w file.pcap` to dump all interfaces.

**exercise**:
1. From pc1 try to ping an unreachable local destination, e.g. 192.168.1.7, in the same subnet of pc1.
	1. `pc1` tries to send ARP request for `192.168.1.7` but it does not get any response
2. From pc1 try to ping an unreachable remote destination, e.g. 10.8.0.20, in the same subnet of s1
	1. `pc1`