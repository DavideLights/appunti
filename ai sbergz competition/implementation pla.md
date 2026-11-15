# 1. ricerca

## VanLehn
Uso di un ITS con feedback granulare per singolo passaggio, che agisce come tutor che verifica i passaggi intermedi
## Sweller 
* i principianti apprendono meglio da esempi guidati
* gli esperti da problemi aperti

**Intuizione**: ridurre gradualmente i suggerimenti man mano che l'IA valuta l'utente piu o meno esperto.

## 1. methods
Bilanciare:
* carico intrinseco: complessita dell'argomento rispetto all'esperienza dell'utente
* carico estraneo: rumore informativo, spiegazioni dispersive
* massimizzare carico germano: guided reason and interaction with what you already learnt

Come?
* **mastery learning**: we should not unlock next module until the user does not a master of the module.
	* **Bloom, B. S. (1984).** _The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring._ **Educational Researcher**, 13(6), 4–16. (`DOI: 10.3102/0013189X013006004`)
	* chi usa mastery learning di **due deviazioni standard** (98° percentile) quelli che seguono lezioni tradizionali.
* **step based learning**: use a tutor system (ITS) based on intermediate steps
	* **practically**: decompose exercises and theory in verifiable steps 
	* Gli ITS _step-based_ ottengono un effect size di **d = 0.76**, virtualmente indistinguibile dai tutor umani (**d = 0.79**), mentre i sistemi _answer-based_ si fermano a **d = 0.31**.
	* **VanLehn, K. (2011).** _The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems._ **Educational Psychologist**, 46(4), 197–221. (`DOI: 10.1080/00461520.2011.611369`) 
* Worked EXample and Expertise Reversal Effect:
	* Worked Example: step by step is reduces external load
	* Expertise Reversal Effect: if you mastered a topic, then step by step examples are countereffective.
	* **pratically**: understand if user mastered a topic so to understand how should be detailed and "step-by-step" an explanation/review.
* Retrieval Practice:
	* Rievocare attivamente ricostruisce e rafforza la traccia mnestica contro l'illusione di familiarità. _High Utility_ (_Dunlosky, 2013_
	* **goal**: open questions, generanted via RAG, immediate correction.
	* **Dunlosky et al. (2013)**; **Adesope et al. (2017, _Rev. Educ. Res._)**; **Rowland (2014, _Psychol. Bull._)**
* Pretesting / Prequestioning:
	* Tentare risposte _prima_ della lettura attiva il fallimento produttivo (_errorful generation_) e orienta l'attenzione sui concetti chiave. Guadagno
	* **St. Hilaire et al. (2023, meta-analisi)**; **Pan & Sana (2021)**
* Interleaved Practice:
	* Alternare problemi e concetti affini di capitoli diversi allena a discriminare _quale_ principio applicare, simulando l'esame reale.
	* **Brunmair & Richter (2019, _Psychol. Bull._)**; **Dunlosky et al. (2013)**
* Self-Explanation
	* Esplicitare _perché_ un passaggio è valido integra le nuove idee negli schemi pregressi e svela misconcezioni.
	* Self-Explanation e Tutor Socratico AI
* Learning-
## 2. organization
how to study over the time?
1. Distributed Practice + FSRS algorithm: Distribuire i ripassi nel tempo contrasta la curva dell'oblio e rafforza il consolidamento nella memoria a lungo termine (High Utility su 254 studi, oltre 14.000 partecipanti in Dunlosky et al., 2013). Nei benchmark retrospettivi su 9.999 collezioni Anki (~350 milioni di ripassi), l'algoritmo open-source FSRS (basato su Difficulty, Stability, Retrievability) supera il vecchio SM-2 nel 99,4% dei mazzi (log loss 0,346–0,356 contro 0,62–0,72), tagliando del 20–30% il numero di ripassi a parità di ritenzione target (es. 90%) ed evitando il blocco su intervalli brevissimi (ease hell).
2. Semantic segmentation and pre-training
	1. semantic segmentation to reduce overload
	2. **Rey et al. (2019, 56 studi, 88 confronti)** dimostrano che la segmentazione migliora sia ritenzione sia trasferimento riducendo la difficoltà percepita (es. **d = 0,43**).
## 3. attention span
how to reduce attention span?
1. introduce small tests 
	1. **goal**: interpolated questions every $t$ minutes to reduce distractions due to *mind wandering* in digital study
	2. **Szpunar, K. K., Khan, N. Y., & Schacter, D. L. (2013).** _Interpolated memory tests reduce mind wandering and improve learning of online lectures._ **Proceedings of the National Academy of Sciences (PNAS)**, 110(16), 6313–6317. (`DOI: 10.1073/pnas.1221764110`)
2. less is more (??)
	1. **goal**:  tre principi empirici per prevenire il sovraccarico dei canali visivo-verbali su schermo: **Segmenting Principle** (l'apprendimento migliora nettamente quando un contenuto complesso è diviso in segmenti brevi avanzati manualmente dall'utente), **Coherence Principle** (rimuovere testi/immagini decorativi aumenta la comprensione) e **Signaling Principle** (evidenziare visivamente i nessi logici guida l'attenzione selettiva).
	2. **concrectly**: mporre vincoli di formattazione sull'output dell'LLM: risposte spezzate in **micro-unità atomiche da massimo 120–150 parole**, avanzamento a step controllato dall'utente (_progressive disclosure_), grassetti strutturali sulle parole chiave e assenza totale di testo introduttivo ridondante.
	3. **Mayer, R. E., & Moreno, R. (2003).** _Nine Ways to Reduce Cognitive Load in Multimedia Learning._ **Educational Psychologist**, 38(1), 43–52. (`DOI: 10.1207/S15326985EP3801_6`)
3. **timers**:
	1. **goal**: user can choose between micro-sprint or standard-sprint schedule. study $x$ minuts, then $y$ of pause
		1. at the end of the pause the AI shows you a resume to regain the context.
		2. maybe the AI can find the optimal schedule while studying?
	2. **Biwer, F., Wiradhany, W., Oude Egbrink, M. G. A., & de Bruin, A. B. H. (2023).** _Understanding effort regulation: Comparing ‘Pomodoro’ breaks and self-regulated breaks._ **British Journal of Educational Psychology**, 93(S2), 353–367. (`DOI: 10.1111/bjep.12593`)
4. **anti-switching**: less tabs $\equiv$ more concentration
		1. **Gloria Mark (UC Irvine, studi sul _context switching_)**; **Mayer** (_principio di contiguità spaziale_).
		2. **goal**: ai should produce an organized workspace, with few tabs


# how ai should be used?

AI should not be permissive: **Bastani et al. (2025, _PNAS_)** hanno dimostrato che un chatbot GPT privo di vincoli migliora la resa durante gli esercizi (+0,137), ma provoca un **crollo del 17%** (-0,054 su scala 0–1) all'esame finale svolto senza.


# what to do that other tools don't do?
