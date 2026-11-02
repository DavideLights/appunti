
**fiber**: 
* laser: it's the transimetter for fiber. transmits light.
* **wavelength**: is also color.
	* **monocolor**: only one color
	* **muticolory**: higher bitrate
* each light impulse is a bit. light impulse is spread over the band width, so we send multiple bits at one time
* bits cannot be too near, otherwise, after transmission there is too much noise. so band width cannot be used all.

*10:00* we can put somewhere optical devices: **amplifiers**.
* an amplifiers recovers the original impulse.
* fiber is used underwater because there is low attenutation on long distances.
* non ho capito che c'entrano gli amplifiers col discorso

**tre configurazioni** (guarda immagine):
* una fibra per ogni casa. 
* una fibra verso uno switch. più fibre dallo switch alle case
	* **switch**: e' un membro attivo elettricamente della rete
* uno splitter: semplicemente e' un punto in cui si attaccano fisicamente piu fibre. non richiede elettricita. every time we split the signal, power is reduced by $10 \log 0.5 = 3\text{dB}$
	* c'e' lo splitter 1x2 e lo splitter 1xN.



**21:00 fttc** e **ftth**: bo

**daisy chain architecture**: 
* there is one passive fiber
* multiple switch, each other with a fiber connecting multiple houses.
* used in metropolitan areas

**fiber distribution point**: can be put on street lamps, or in the building. its were fiber splitting is done

## 25:30 basic pon operations
* guarda la slide
* one fiber for downstream
* one fiber for upstream
* using WDD: multiplexing of 
* **OLT**: optical line terminator, network element locating the lasers putting data in transimssion. contains photodiodes receiving signal.
* **ONT**: optical netowrk termintor
* **distance order**: kilometers. passive 
* **seminar**: passive optical line terminal with passive splitting at home!
* **router**: optical terminator unit

**EPON**: extends ethernet on passive optical fiber. fully compatible

**48:00**

**57:00**: security issues, you can analyze the pattern of the communication. which kind of apps you can use, and other things.

EPON: domanda aperta importante!!!!