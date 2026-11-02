# satelites 0:00-12:00

**LEO**: 500-2000 km of altitude
* **example**: spacex.
* satelites are not in a fixed point.
* after 90 minutes the position changes completly respect a fidex point on earth.

**GEO**: 35.000km of altitude
* the satelites run at the same speed of the earth, is always on the same point.

**5:30**: graphical example. In LEO you need a cosetllation
* a single LEO satelite has a little coverage.
	* **challenge**: how do you manage low orbit and interconnection? you switch often the LEO satelite you are connected to.
	* **switching**: we switch from a satelite to another and we have to mantain connection stable.
* a single GEO satelite has a wider coverage.
	* with 3 GEO satelits you can cover the whole earth.

**advantage**: low latency, and a large amount of satelites.
* spaces x uses 5.000 satelites.

**research**: lot of research in improving LEO technology.

**routing**: since the coveradge is short, to cover connection in a wide area we need to do multi hop between satelites.
* since LEO changes positions, ther's a different approach to routing. the neighbour LEO is not always know. (???)

# DSL 13:30-
**DSL**: in a subscriber line (also in phone terminology), a subscriber is someone who as a contract to get a digital interconnection. the contract name is subscriber line.

**xDSL**: DSL has a long story, represented by the xDSL family.
* **IDSL**: design to provide a digital interconnection on top of the telephone lines. 
* **HDSL**
* **SDSL**: symmetric
* **ADSL**: asymmetric, the winner in the story. there are some evolutions.
	* ADSL lite
	* Rate Adaptive ADSL
	* VDSL: very high speed DSL
	* **VDSL2**: is the winner, very high speed SDL version 2.

why DSL?
* lots of copper wires, hundered of millions of kilomters of copper. we'd like to use this network to transmit data
* **foundamental data for the discussion**:
	* from hour house to the Central Office there is a wire of copper
	* transmission is in analog form, while the core was entirely digital.
	* the distance from CO to house in in average **1.5km**, quite short.

**22:46: pre-DSL architecture**:
* red wires: copper. 
* copper is a twisted pair: we have two copper wires twisted together.
* users have an individual connection to the CO
* between COP and users we have cabinets

**important to notice**: analyze cooper in the frequency domain.
* **for the telephone**, the signal was transmitted in the **0 to 4kHz $=B_{1}$** bandwidth
* **shannon capacity**: how fast (bitrate) i can trasmit data in a bandit $B$? gives and **upperbound**
	* $C = B_{1} \cdot \log_{2}(1+\text{SNR})$ with $\text{SNR}=\frac{P_{S}}{P_{N}}$
		* $\text{SNR}=\text{signal noise rapport}$
	* **28:31**: mesures how noise affects transmission.
	* if power of the signal is high respect to the power to the noise then the value is high, otherwise low.

**note**: $\text{speed} \equiv \text{bandwidth}$, given a fixed SNR, bitrate is proprtional to bandwidth.

**nominal speed for copper**: 56kbps. it was not pheasible. (fattibile)

## ADSL 32:30
is it possible to use larger bandwidth in the same copper wire? yes

we can use higher frequency bandwidth, larger than $B_{1}$
* **tradeoff**: using higher frequency implies higher noise.

**ADSL**: this configuration is asymmetric. while telephone was symmetric.
* **contemporary**: in telephone you send your voice while hearing the other end voice.
* **asymmetric**: stream is divided and achieved using two streams, on two different bands,  **upstream and downstream**
	* when ADSL was developed, common interest was to download data and not to upload, so ADSL reflects that interest.
	* **downstream**: has lower frequency and shorter bandwidth than upstream
	* **upstream**: has higher frequency and large bandwidth with bad SNR.

**future**: quantum based communication where channon theory is not applied. a single qbit can represents a lot of states.

> da adesso in poi i timestamp sono relativi a *network lez 3 p2*

**0:00 frequency has impact on the noise**: copper wire is a guided medium. if there are two different copper wires running close there is interference.
* initial configuration of past network used to have a **big pipes**, and inside this there were lots of different copper wires.
* increasing the frequency, increases probaiblity that signal in a wire crosses to another wire.

**note**: red, green, and blue bandwidths (look at the slides) do not interfere.
* to avoid interference between down stream and up stream there is a gap in frequencies (look at the slide)

**cross talk**: there are multiple types of cross talk interference.
* **FEXT cross talk**: we have a 2 transimtters and 2 receiers, two cables are near, and part of the signal from the transimtter interferes with an unrelated receiver
* **NEXT cross talk**: we have a trasmitter and a recived. the trasmitter interferes with the other transimtter.

note that FEXT and NEXT does not affect transmitter data going to the planned receiver.



* FEXT is not a problem, non ho capito perche
* if RX is hon the houses and TX on the CO, then there is no interference because TX are never near on the CO, so no interference
* if RX and TX on the same house and RX and TX on the CO
	* if there is a gap between upstream and down stream frequencies then there is no interference

**note**: if we want to have a larger downstream, we make it contemporary to the upstream in the bandwidth and frequencies.
* larger downstream <-> faster bit rate
* **problem**: near RX and TX cables may interfere because.

**binder group**: if two cables are in the same binder group, then they can interfere. it's like a cable that connects user to the CO.

**echo cancellation**: allows CO to cancel from the received signal, the noise observed. 
* if i trasmit signal to a user and i'm contemporary receiving from another user
	* and TX and RX are in the same CO, in the same entity
* then i know what it takes to cancel the interference, it's like muting a channel if it makes noise.
* a machine can cancel from the signal its own echo.
* **note**: echo cancellation is required to use large bandwidth for downstream shared with upstream.

# ADSL frequency bands 4:00

**attenuation**: at different frequencies i have different levels of attenuation.
* **best channel possible**: has large bandwidth, and a **uniform attenuation on all frequencies**.
* in copper, **attenuation is not flat/uniform**, if we didn't had this problem, to receive a strong signal we could simply increase the volume.
* sono stanco e non ci sto capendo un cazzo

**solution to non uniform attenuation**: Discrete MultiTone (DMT) Modulation
* divide bandwidth in sub bands.
* split the main transmission in parallel transimssions: $T_{1},\dots,T_{n}$
* each transmission goes in a single tone
* **advantage**: if the tones are enough short, inside a tone the attenuation would look uniform and error due to attenuation is smaller.
* every band is 4KHz, and
* **some bands are not used (why????)**

**note**: the bands do not all have the same bitrate since they have different SNR.water filling 

**water filling**: algorithm that allows automatically to configure the parallel ransmissions
* **not al copper is the same**: old cables, interference in the house, ecc...
* works like a water bucket filling different buckets
* the floor of the pool is SNR inverted
	* if the floor is lower we have lot of water
	* if the floor is higher we have little water.
* this algorithm puts more water were the NSR (SRN inverted): were the noise is lower, or the signal strong enough. (check this)
* NSR is $\frac{N}{S}$ so for $S \to \infty$ then $\frac{N}{S} \to 0$, so lower floor and more water inside that bucket.


