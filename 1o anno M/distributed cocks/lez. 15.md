# alg. uniform hierarchical consensus 



# alg. proofs

# modify the algorithm.
**beb instead of reliable**: integrity, validity, and other properties can fail?
* **does integrity fail**? if a process decides twice, it executes the lines twice and sets the value to something not null. the handler cannot be triggered twice
* **does validity fail**? no, the validity is still correct. no changes in the logic
* **does agreement fail**? (=two process decide something different). No.
* **(25:00) does termination fail?** the process that sends after consensus must fail after we sent the message (otherwise it acts like reliable).
	* if i have received a message does not imply the others to!
	* that's why termination does not work anymore.

# ex. hierarchical
**R**:
* integrity is not violated
* termination is not violated
* **validity**

