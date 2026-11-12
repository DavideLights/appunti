# eventual leader election $\Omega$
**why**? we use it when the link is not perfect.

**Events**:
* **indication**: $<\Omega, |\text{Trus}|p>$: indicates that $p$ is trusted to be a leader.
**Properties**:
* **ELD1**: Eventual accuracy: There is a time after wich every correct process trusts some correct process.
* **ELD2**: Eventual agreement: There is a time after which no two correct processes trust different correct processes.

> **note**: $\Omega$ ensures that eventually correct processes will elect the same correct process as their leader


using $\Omega$ implies that:
* **arbitrary**: leader can change in an arbitrary way
* **different leaders**: different leader may be elected without having crashed.

![[Pasted image 20261111225410.png]]

gemini: explain slide 53 here