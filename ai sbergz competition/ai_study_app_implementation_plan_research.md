# 1. Core Pedagogical Principles & Cognitive Load

## 1.1 Foundational Frameworks

* **Granular Step-by-Step Tutoring (VanLehn):** Use an Intelligent Tutoring System (ITS) that provides granular feedback on individual steps, acting as a tutor that verifies intermediate reasoning rather than just final answers.

* **Expertise-Adaptive Scaffolding (Sweller):**

  * Novices learn better from worked (guided) examples.

  * Experts learn better from open-ended problems.

  * **Core Design Intuition:** Gradually fade (reduce) hints and scaffolding as the AI assesses the user's increasing mastery of a topic.

## 1.2 Cognitive Load Management

Balance the three types of cognitive load across all AI interactions:

* **Intrinsic Load (Calibrate):** The inherent complexity of the topic relative to the user's prior experience.

* **Extraneous Load (Minimize):** Information noise, visual clutter, and unfocused or dispersive explanations.

* **Germane Load (Maximize):** Guided reasoning and active interaction connecting new concepts with what the user has already learned.

# 2. Study Methodologies

## 2.1 Mastery Learning

* **Rule:** Do not unlock the next module until the user demonstrates mastery of the current module.

* **Evidence:** Students learning under mastery conditions outperform those in traditional lectures by two standard deviations ($2\sigma$, $98\text{th}$ percentile).

* **Reference:** Bloom, B. S. (1984). *The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring.* Educational Researcher, 13(6), 4–16. (`DOI: 10.3102/0013189X013006004`)

## 2.2 Step-Based Learning

* **Rule:** Use an Intelligent Tutoring System (ITS) structured around intermediate steps.

* **Implementation:** Decompose both theoretical concepts and exercises into verifiable intermediate steps.

* **Evidence:** Step-based ITS achieve an effect size of $d = 0.76$, virtually indistinguishable from human tutors ($d = 0.79$), whereas answer-based systems reach only $d = 0.31$.

* **Reference:** VanLehn, K. (2011). *The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems.* Educational Psychologist, 46(4), 197–221. (`DOI: 10.1080/00461520.2011.611369`)

## 2.3 Worked Examples & Expertise Reversal Effect

* **Worked Example Effect:** Step-by-step demonstrations reduce extraneous cognitive load for learners acquiring new schemas.

* **Expertise Reversal Effect:** Once a user has mastered a topic, detailed step-by-step examples become counterproductive.

* **Implementation:** Track per-topic mastery to dynamically adjust how detailed and step-by-step explanations or reviews should be.

## 2.4 Retrieval Practice

* **Mechanism:** Actively recalling information reconstructs and strengthens memory traces, countering the illusion of familiarity (*High Utility*; Dunlosky et al., 2013).

* **Evidence:** Outperforms passive restudy with $g = 0.50$ ($61$ studies; Rowland, 2014) and $g = 0.60$ ($188$ experiments; Adesope et al., 2017), maximized when paired with immediate corrective feedback.

* **Implementation:** Generate open-ended questions grounded in uploaded files via RAG and provide immediate corrective feedback.

* **References:** Dunlosky et al. (2013); Adesope et al. (2017, *Rev. Educ. Res.*); Rowland (2014, *Psychol. Bull.*).

## 2.5 Pretesting / Prequestioning

* **Mechanism:** Attempting to answer questions *before* reading triggers productive failure (*errorful generation*) and directs attention toward key concepts.

* **Evidence:** Yields $g = 0.66$ on pre-questioned concepts (St. Hilaire et al., 2023) and $g = 0.43$ over post-testing (Pan & Sana, 2021), but has zero effect on non-pretested details ($g = 0.01$).

* **Implementation:** Administer $3\text{--}5$ diagnostic pre-questions per chapter immediately after file upload, linked to source pages.

* **References:** St. Hilaire et al. (2023, meta-analysis); Pan & Sana (2021).

## 2.6 Interleaved Practice

* **Mechanism:** Alternating related problems and concepts from different chapters trains the student to discriminate *which* principle to apply, simulating real exam conditions.

* **Evidence:** Achieves $g = 0.42$ across $59$ studies ($g = 0.46$ across $3$ combined meta-analyses; Brunmair & Richter, 2019), peaking on easily confusable concepts.

* **Implementation:** Mix cross-chapter concepts during review sessions rather than isolating quizzes by single PDF.

* **References:** Brunmair & Richter (2019, *Psychol. Bull.*); Dunlosky et al. (2013).

## 2.7 Self-Explanation & Socratic AI Tutoring

* **Mechanism:** Articulating *why* a step is valid integrates new ideas into existing mental schemas and exposes misconceptions.

* **Evidence:** Self-explanation achieves $g = 0.55$ overall and $g = 0.35$ even compared to provided explanations ($64$ reports; Bisra et al., 2018). In a Harvard RCT ($N = 194$), a Socratic AI tutor more than doubled median learning gains vs. active classroom instruction ($4.5$ vs. $3.5$ post-test on a $2.75$ baseline; $0.73\text{--}1.3$ SD) in less time ($49\text{ min}$ vs. $60\text{ min}$; Kestin et al., 2025).

* **Implementation:** Enforce system prompts that forbid giving direct solutions on the first attempt, providing only Socratic hints.

* **References:** Bisra et al. (2018, *Educ. Psychol. Rev.*); Kestin et al. (2025, *Sci. Rep.*).

## 2.8 Learning-by-Teaching (*Protégé Effect*)

* **Mechanism:** Preparing to explain and answering clarification questions forces logical selection and reorganization of knowledge.

* **Evidence:** Achieves $g = 0.35$ for preparation alone and $g = 0.56$ during interactive teaching ($28$ studies; Kobayashi, 2019; confirmed at $g = 0.27$ across $39$ studies in Kobayashi, 2024).

* **Implementation:** Include an inverse *"Teach the AI"* mode where the model acts as a curious peer probing the user's knowledge gaps.

* **References:** Kobayashi (2019, *J. Educ. Psychol.*); Kobayashi (2024).

## 2.9 Active Concept Mapping vs. Passive Habits (Anti-Summary Rule)

* **Mechanism:** Building node-link schemas from memory exposes causal relationships, whereas passive rereading, highlighting, and reading pre-made summaries induce an illusion of competence (*Low Utility*; Dunlosky et al., 2013).

* **Evidence:** Constructing concept maps yields $g = 0.72$ (stable at $g = 0.72$ beyond $4$ weeks) vs. $g = 0.37$ for studying pre-made maps ($142$ effects, $N = 11,814$; Schroeder et al., 2018).

* **Implementation:** Ban one-click AI summaries or pre-built maps as primary study modes; require closed-book schema construction verified by the AI.

* **References:** Schroeder et al. (2018, *Educ. Psychol. Rev.*); Dunlosky et al. (2013).

# 3. Study Organization Over Time

## 3.1 Distributed Practice + FSRS Algorithm

* **Mechanism:** Distributing reviews over time counters the forgetting curve and strengthens long-term memory consolidation (*High Utility* across $254$ studies, $>14,000$ participants; Dunlosky et al., 2013).

* **Evidence & Algorithm:** In retrospective benchmarks across $9,999$ Anki collections ($\approx 350\text{M}$ reviews), the open-source **FSRS** algorithm (modeled on *Difficulty*, *Stability*, and *Retrievability*) outperforms legacy SM-2 in $99.4\%$ of decks (log loss $0.346\text{--}0.356$ vs. $0.62\text{--}0.72$), cutting review volume by $20\text{--}30\%$ for the same target retention (e.g., $90\%$) and preventing short-interval lock-in (*ease hell*).

## 3.2 Semantic Segmentation & Pre-Training

* **Mechanism:** Apply semantic segmentation to break files into $5\text{--}10\text{ min}$ logical units (*event boundaries*) to reduce overload, and deliver a key-term glossary upfront (*pre-training*) to build baseline schemas prior to reading.

* **Evidence:** Segmentation improves both retention and transfer while reducing perceived difficulty (e.g., $d = 0.43$; Rey et al., 2019).

* **References:** Rey et al. (2019, $56$ studies, $88$ comparisons); Mayer (*Cognitive Theory of Multimedia Learning*).

## 3.3 Self-Regulated Learning (SRL) & Dynamic Scheduling

* **Mechanism:** Decomposing syllabus workload up to the exam date, tracking progress, and dynamically recalculating schedules prevents procrastination (negatively correlated with grades at $r = -0.19$, $N = 7,447$; Steel, 2007).

* **Evidence:** Time management reduces psychological distress ($r = -0.358$) and boosts performance ($r \approx 0.25$; Aeon et al., 2021). SRL interventions with structured feedback improve achievement ($g = 0.37$), metacognition ($g = 0.40$), and concentration ($g = 0.61$) across $49$ studies ($N = 5,786$; Theobald, 2021).

* **Implementation:** Automatically redistribute missed sessions across remaining days without punitive "review debt" spikes.

* **References:** Theobald (2021); Aeon, Faber & Panaccio (2021, *PLOS ONE*); Steel (2007).

## 3.4 Implementation Intentions (*If-Then Planning*)

* **Mechanism:** Linking a concrete environmental cue to an immediate micro-action ("If 

  $$
  time/location X
  $$

  , then within seconds \[start first quiz Y\]") automates study initiation without depleting willpower, bridging the intention-behavior gap (where a median $47\%$ of intentions fail; Sheeran, 2002).

* **Evidence:** Achieves a medium-to-large effect size of $d = 0.65$ across $94$ independent tests (Gollwitzer & Sheeran, 2006).

* **References:** Gollwitzer & Sheeran (2006, *Adv. Exp. Soc. Psychol.*); Sheeran (2002).

# 4. Attention Span & Focus Management

## 4.1 Baseline Behavioral Reality (Debunking Myths)

* **Empirical Findings:** Popular claims of an "8-second goldfish attention span" or a fixed $10\text{--}15\text{ min}$ lecture drop-off lack primary scientific evidence (Wilson & Korn, 2007; Bradbury, 2016; Bunce et al., 2010 instead observe recurring $\sim 1\text{ min}$ micro-lapses).

* **Core Digital Bottlenecks:** Average on-screen attention span has fallen to $47\text{ seconds}$ due to tab/window switching, requiring $23\text{ minutes } 15\text{ seconds}$ to regain deep focus after an interruption (Gloria Mark, UC Irvine), compounded by $\sim 40\%$ *mind wandering* during passive digital reading.

## 4.2 Interpolated Micro-Tests

* **Implementation:** Insert $1\text{--}2$ retrieval questions at semantic section boundaries (every $t$ minutes) to curb *mind wandering* without interrupting open reasoning threads (Jing et al., 2016).

* **Evidence:** Halves *mind wandering* from $39\text{--}41\%$ down to $19\%$ ($d = 1.01\text{--}1.05$) and lowers perceived mental effort (median $2$ vs. $3.5\text{--}4$; Szpunar et al., 2013).

* **References:** Szpunar, K. K., Khan, N. Y., & Schacter, D. L. (2013). *PNAS*, 110(16), 6313–6317 (`DOI: 10.1073/pnas.1221764110`); Jing, Szpunar & Schacter (2016).

## 4.3 Multimedia Cognitive Load Principles ("Less is More")

* **Core Principles:** Apply three empirical principles to prevent visual-verbal channel overload on screen:

  1. **Segmenting Principle:** Learning improves significantly when complex content is divided into short, user-paced segments.

  2. **Coherence Principle:** Removing decorative text and images increases comprehension.

  3. **Signaling Principle:** Visually highlighting logical connections guides selective attention.

* **LLM Output Constraints:**

  * Split responses into **atomic micro-units of max** $120\text{--}150$ **words**.

  * Enforce user-controlled step progression (*progressive disclosure*).

  * Use structural bolding on key terms.

  * Eliminate redundant introductory text.

* **Reference:** Mayer, R. E., & Moreno, R. (2003). *Nine Ways to Reduce Cognitive Load in Multimedia Learning.* Educational Psychologist, 38(1), 43–52. (`DOI: 10.1207/S15326985EP3801_6`)

## 4.4 Adaptive Study Timers (Task-Aware Flowtime & Off-Screen Breaks)

* **Evidence:** While structured intervals reduce initiation inertia (Biwer et al., 2023, $N = 87$), recent controlled trials show rigid timers (e.g., $25/5$ or $12/3$ Pomodoro) do **not** improve exam grades and can break cognitive *flow* (Smits, 2025, $N = 94$; Göksu, 2026, $N = 176$). Off-screen micro-breaks $\le 10\text{ min}$ boost vigor ($d = 0.36$) and reduce fatigue ($d = 0.35$), but do not restore performance after high-load cognitive tasks ($d = -0.09$), where breaks $>10\text{ min}$ are required (Albulescu et al., 2022, $22$ samples, $N = 2,335$).

* **Implementation:**

  * Allow users to choose between a **micro-sprint**, **standard-sprint**, or **Task-Aware Flowtime** schedule that proposes breaks only at natural micro-module boundaries (suggesting $>10\text{ min}$ off-screen after heavy cycles).

  * At the end of each break, display a brief AI context recap to restore working memory.

  * *Exploratory Feature:* Dynamically infer and recommend the user's optimal study/break schedule based on study behavior.

* **References:** Biwer et al. (2023, *Br. J. Educ. Psychol.*, `DOI: 10.1111/bjep.12593`); Smits (2025); Göksu (2026); Albulescu et al. (2022, *PLOS ONE*).

## 4.5 Anti-Switching Workspace

* **Core Principle:** Fewer tabs $\equiv$ higher concentration.

* **Implementation:** Generate a unified, single-screen workspace (source document, notes, quiz, and AI tutor side-by-side) with minimal tabs to eliminate the $47\text{ s}$ switching loop and $23\text{ min}$ refocus penalty.

* **References:** Gloria Mark (UC Irvine, context-switching research); Richard E. Mayer (*Spatial Contiguity Principle*).

# 5. AI Guardrails & Cognitive Offloading Boundary

* **Cognitive Offloading Rule:** AI must automate *extraneous/logistical* load (chunking, scheduling, RAG verification) and **never** offload *germane/generative* effort (Risko & Gilbert, 2016). Uncritical AI reliance correlates strongly with reduced critical thinking ($r = -0.68$; Gerlich, 2025).

* **Non-Permissive AI Rule:** The AI tutor must **not** be permissive or provide direct answers on demand.

* **Evidence:** An unconstrained GPT chatbot improves performance during practice exercises ($+0.137$), but causes a $17\%$ **drop** ($-0.054$ on a $0\text{--}1$ scale) on the final exam taken without AI assistance—whereas a hint-constrained *GPT Tutor* prevented this drop ($-0.004$; Bastani et al., 2025).

* **References:** Bastani et al. (2025, *PNAS*); Risko & Gilbert (2016, *Trends Cogn. Sci.*); Gerlich (2025).

# 6. Reference End-to-End Study Workflow (6 Sequential Phases)

1. **Phase 1 — Ingestion & Study Contract:** Semantic parsing of uploaded files into $5\text{--}10\text{ min}$ chunks (Rey et al., 2019), dynamic calendar distribution up to the exam date (Theobald, 2021), and creation of an *If-Then* trigger rule (Gollwitzer & Sheeran, 2006).

2. **Phase 2 — Pre-Training & Pretesting:** Display a concise key-term glossary (Mayer) followed by $3\text{--}5$ diagnostic pre-questions per chapter with source citations (St. Hilaire et al., 2023).

3. **Phase 3 — Guided Interpolated Study:** Active reading in the single-pane anti-switching workspace (Mark) with boundary micro-checkpoints (Szpunar et al., 2013) and step-by-step Socratic scaffolding adapted to user mastery (VanLehn, 2011; Sweller; Kestin et al., 2025).

4. **Phase 4 — Task-Aware Flowtime Break:** Off-screen pause triggered at module completion (Smits, 2025; $>10\text{ min}$ after high-load cycles; Albulescu et al., 2022), followed by a 3-bullet AI context recap upon return.

5. **Phase 5 — Generative Consolidation:** Closed-book concept mapping verified by AI (Schroeder et al., 2018) or active explanation in *Teach the AI* (*Protégé*) mode (Kobayashi, 2019).

6. **Phase 6 — Interleaved FSRS Review Queue:** Long-term spaced repetition scheduled via FSRS (Ye) mixing confusable concepts across chapters (Brunmair & Richter, 2019) until mastery thresholds are met (Bloom, 1984).

# 7. Dual Modular Abstraction Architecture

## 7.1 Cognitive Abstraction: ICAP Framework + SRL Loop

Every app feature is classified along the **ICAP** cognitive engagement hierarchy (Chi & Wylie, 2014, *Educ. Psychol.*) inside a continuous Self-Regulated Learning cycle ($\text{Plan} \rightarrow \text{Execute/Monitor} \rightarrow \text{Adapt}$):

* **Passive:** Targeted micro-reading of $120\text{--}150$ word atomic segments.

* **Active:** Pretesting, interpolated micro-checkpoints, and FSRS recall prompts.

* **Constructive:** Step-by-step self-explanation and closed-book concept mapping.

* **Interactive:** Socratic AI dialogue and *Teach the AI* (*Protégé*) questioning.

## 7.2 Engineering Abstraction: 4-Module ITS Architecture

Decouple the application backend into four domain-agnostic modules:

1. **Domain Model:** Extracts the concept dependency graph (DAG), key-term glossary, and RAG-indexed source chunks from uploaded files.

2. **Student Model:** Tracks per-concept FSRS memory parameters (*Difficulty* $D$, *Stability* $S$, *Retrievability* $R$), mastery unlock states, and recurring misconception logs.

3. **Pedagogical Module:** Policy engine that selects the optimal intervention (Worked Example vs. Open Problem via Expertise Reversal, Pretesting, Cross-Chapter Interleaving, Socratic Hinting, or *Protégé* Mode) and enforces non-permissive LLM guardrails.

4. **Communication / UI Module:** Single-pane workspace enforcing low extraneous load (Coherence, Signaling, Spatial Contiguity), $120\text{--}150$ word progressive disclosure, and Task-Aware Flowtime pacing.