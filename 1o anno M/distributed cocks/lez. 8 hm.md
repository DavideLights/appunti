**lecture**: [[lez. 8]] #gemini

# Homeworks — Lecture 8 (*Time 3*, Slides 77–81) #gemini

## 1. Fault-Tolerant ME using $\mathcal{P}$ and `LE` (Slide 77) #gemini
> [!warning] Study on your own — Write pseudocode & proofs for the Leader-based Fault-Tolerant ME algorithm (Slides 72–76) #gemini
> * **Problem**: Write the complete event-driven pseudocode (handling `Request`, `Release`, `Leader`, `Crash`, plus the `new_leader` interrogation phase) and prove **Mutual Exclusion** and **Liveness** (note: discuss whether **Fairness** holds when the leader crashes and requests are retransmitted). #gemini
> * **Reference**: *Time 3* slides 72–77. #gemini

* **Pseudocode**: `[INSERT HERE]` #gemini
* **Safety (Mutual Exclusion) & Liveness proofs**: `[INSERT HERE]` #gemini

---

## 2. Adaptive Timeout Strategy for $\diamond\mathcal{P}$ in Synchronous Systems with Unknown Delay (Slide 77) #gemini
* **Problem**: Suppose you are in a synchronous system with an **unknown** maximum channel delay. Design a strategy to **increase and decrease** the internal timeout $\Delta$ to: #gemini
	1. Stabilize to $\mathcal{P}$ in the fastest way. #gemini
	2. Have minimum latency when suspecting an actual crash. #gemini
* **Answer / Strategy** *(hint: think TCP congestion control / binary search / multiplicative increase & cautious decrease)*: `[INSERT HERE]` #gemini

---

## 3. Synchronous vs Fail-Stop Solvable Problems (Slides 78–79) #gemini
* **Describe two problems solvable in `Synchronous` but NOT in `Fail-Stop`**: #gemini
	1. `[INSERT HERE]` *(Slide 79: Clock Synchronization)* #gemini
	2. `[INSERT HERE]` *(Slide 79: Timed Delivery — if $p$ sends $m$ to $q$ at $t$, $q$ delivers $m$ by $t+x$)* #gemini
* **Describe one problem solvable in `Fail-Stop` but NOT in `Synchronous`**: #gemini
	* `[INSERT HERE]` *(Slide 79: Does not exist, since $\text{Problems}(\text{Fail-Stop}) \subset \text{Problems}(\text{Sync})$)* #gemini

---

## 4. Fault-Tolerant Mutual Exclusion in `Fail-Silent` and `Fail-Noisy` (Slide 80) #gemini
* **Is it possible to solve fault-tolerant mutual exclusion in a `Fail-Silent` system?** #gemini
	* `[INSERT HERE]` *(Hint: if a process crashes inside the CS, can another process ever distinguish whether it crashed or is just slow without violating Mutual Exclusion or Liveness?)* #gemini
* **Is it possible to solve fault-tolerant mutual exclusion in a `Fail-Noisy` ($\diamond\mathcal{P}$) system?** #gemini
	* `[INSERT HERE]` *(Hint: before GST, $\diamond\mathcal{P}$ can falsely suspect a live process currently inside the CS! If you revoke its CS, what happens to Safety? If you wait for its reply, what happens to Liveness if it actually crashed?)* #gemini

---

## 5. Textbook Exercises (Main Book, pp. 67–68 — Slides 77, 81) #gemini
* **Exercise 2.8 (Slide 81)**: Suppose an algorithm $A$ implements an abstraction $M$ using a failure detector $\mathcal{D}$ assumed to be eventually perfect ($\diamond\mathcal{P}$). Can $A$ violate a **safety** property of $M$ if $\mathcal{D}$ is not eventually perfect (e.g., when $\mathcal{D}$ permanently outputs $\emptyset$)? #gemini
	* `[INSERT HERE]` #gemini
* **Exercise 2.9 (Slide 81)**: Specify an abstraction $M$ and an algorithm $A$ implementing $M$ using a failure detector $\mathcal{D}$ such that the **liveness** of $M$ is violated if $\mathcal{D}$ does not satisfy its properties. #gemini
	* `[INSERT HERE]` #gemini
* **Main Book Ex 2.4, 2.6, 2.7, 2.10 (Slide 77)**: #gemini
	* `[INSERT HERE]` #gemini
