**(approfondimento) QAM**: low snr implies a lower number of bit encoded to lower **BER** (bit error rate)
* **good SNR**: then i can use an high bit rate, because errors are rare.
* **bad SNR**: then i have to use a lower bit rate, because errors are frequent
* **goal**: is to have a god BER.
* **curves**: describe the bit rate.

## ADSL Modulation
In DMT modulation the signal is splitted in different signals:
* **TODO**: approx how the scheme works

**UTP**: unshielded twisted pair. is the copper
* it's recycled from the telephone infrastructure

**ATU** (ADSL Termination Unit): ADSL termination unit, implements modulation and demodulation (based on waterfall). are presents at bot side of the copper, recever and transimtter
* **ATU-R**: remote
* **ATU-C**: central office
* **modulation**: applied on transimssion
* **demodulation**: applied when we receive.

**splitter**: divides/splits in frequencies, part of the frequencies dedicated to the telephone from the rest. 
* POTS-R: gets lower part of the frequencies
* ATU-R: get higher part with data of the frequencie

the architecture shown is **specular**, in both sides is the same.

**modem**: **ATU-R + splitter** implements the modem.
* modem: modulation/demodulation


### more detail on end-to-end design 23:12
we have **modems (ATU-R + splitter**) on the remote sides and on the central office sides.
modems are interconnected using **DSLAM (DSL Access Mulitplexer)**

**DSLAM**: does mutliplexing for the data towards the internet.

**CO**: contains as much modems as the number of users are served.
* a modem in the CO is a network interface, phisically inserted inside a rack of modems.

**detailed example** (look at the slides):
* **ATU-R modem at home towards CO**: has to be interconnected with the copper.
	* it implements a physical protocol for modulation/demodulation.
	* **ATM/AAL**: 2 protocols for transmission on copper, on Layer 1
	* **37:00 PPP**: protocol for Layer 2 
	* Then, on Layer 3 we have IP, and so on...
	* **modem** does not implement over IP layerer
* At home, there is a private network (cable based, wireless based).
	* it runs at Layer 2 and 1 protocols to run wifi and ethernet.
* in the DSLAM side:
	* Layer 3 is IP
	* In the lower layers you might have ethernet 

**why service degrades with larger distance**?
* large distance $\equiv$ weak signal
* weak signal $\equiv$ higher BER $\equiv$ less bit rate

**how to short the distance**?
* put **UC close to the end user**, in a **cabinet**
	* so cabinet might contain all the router
	* **space problem**: for this, you need space in the street cabinet.
	* in the cabinets resides the termination unit
* **47:00**: so the internet provider might put DSLAM inside the cabinet

**VDSL**: from home to cabinet we have ADSL. from ADSL to CU we have fiber, or a more efficient medium.
* **VTU-O**: is **VDSL Termination Unit** at the Optical termination unit. (???)

**how to get higher speed**? use higher frequencies. it's feasible if communciation is on short cables.

**FDD solution**: upstream and downstream are splitted in frequencies. (frequency division duplexing)

**TDD solution**: upstream and downstream are in the same frequencies, but splitted in time (time division duplexing)

**VDSL2** uses a larger frequency spectrum on short cables: wins
**ADSL** uses lower freq spectrum on larger cables: loses

**FTTB**: cabinet is close to the building, and then VDSL/ADSL

**1:06:00 FTTH**: there is an Opitcal Terminator in my hose. There is no need for VDSL/ADSL


**crosstalk**: depends on distance between cables, shielding, and the use of high frequencies.
* so the use of high frequencies in VDSL might generate cross talk
* but we can use echo cancellation

**vectoring**: is a smarter noise cancellation protocol. garantuees a better bit rate. consider:
* before transmitting data, i transmit a **flat** test signal that i know.
* this signal goes to receiver. he receives an alterated signal, not anymore **flat**
* tx and rx must agree on what the test signal looks like
* rx transmits back the difference of the signal
* tx transmits data using a **shape augmented/decresed with the diffrence sent my the receiver**.

**1:12:00**: rx and tx must **agree** on the **test signal**!!!!

**1:14:00**: non ho capito
* se uso il vectoring, abbasso il BER, allora posso alzare il bit rate della trasmissione
* **tradeoff**: fare il vectoring costa, deve essere processato.

## PPP 12:22:30
allows to transmit packets on IP.
* it has an upper interface to IP/IPX and other L3 protocols
* it has an lower interface for the link layer.

The structure for the frame is similar to an ethernet frame:
* it has two flag, to indicate start and end of the frame for interfaces listening on the medium.
* the flag is weel known, and is 1 byte long
* ip packet goes into **additional info**

the PPP frame then goes inside ethernet, or AALS/ATM stack protocol.


**no need for addressing information**: the link is P2P, so the address is redoundant.
* address is set by default to `1111...111`: broadcast address

PPP is made of:
* network control layer
* link control layer

**network control layer**: manages connection in the PPP protocol.
* does authentication in the network from the router to te CU
* states transition in the network layer for the PP protocol: $\text{dead} \to \text{estabilishment} \to \text{authentication} \to \text{network}$
* this protocol is right under IP protocol.
* **negotiation parameters**: unit size, kind of auth protocol, data compression, link quality monitoring.

**authentication**: 
* **PAP**: password authentication protocol, from the modem toward s the network. so i send an $\text{(username, password)}$ pair. this is very awful and risky.
* **1:33:00** **CHAP**: challenge based auth protocol. CU provides a challenge sent to the end user
	* the user has a password know on the other side, we don't transmit the password
	* we solve the challenge using the password
	* **hash function**: produces a string of bit,  a combination of the password known between user and CU.
	* the hash result of the function is sent on CHAP.
	* it is not possible to reconstruct a stream from the hash.






