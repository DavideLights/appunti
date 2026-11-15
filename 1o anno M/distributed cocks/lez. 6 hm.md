**ex**: you are on asyncrhonus system, and you have a fair-lossy channel with the property
* if $p$ sends $m$ to $q$ at time $t$, and $m$ not lost, its received at most at $t+1$, or more generally in $t+\Delta$

does this channel give a stronger version of p2p that is bounded on delivery time? 

answer: **no**, because its lossy.
* we send a message, and its lost
* we send another and its lost
* and so on
* we send a message and its **delivered**, but maybe at time after $t+\Delta$.
	* **property**: eventually the message is delivered in fair lossy.
* so even if its bounded, but lossy, i cannot bound.

**ex**: wich pattern (a) or (b) is bad for christian algorithm?
* in chirstian algorithm the bad patter is the one were idk and i dont remember.

**ex**: you have to peer review a synchronisation algorithm for arbitrary graphs.
* you take teh clocks of all the neighbours
* you compute the average and set your clock to its value

what's wrong with this strategy? we could go back in time!


**ex**: execut Lamport Mutual Exclusion in a system not FIFO. Discuss if every property can be violated.

