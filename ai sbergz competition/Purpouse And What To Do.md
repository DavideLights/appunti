# AI Learning Harness — Authoritative Product, Pedagogical & Functional Context (for Step 4 Implementation Planning)

> **Purpose of This Document:** This file is the single source of truth defining *what* to build, *why* every pedagogical constraint exists, and *how* the system behaves functionally.
> **Target Consumer:** An AI software architect using this context to produce the **Step 4 Technical Implementation Plan** (tech stack, database schema, API contracts, RAG pipeline, LLM orchestration & prompts, state machine, UI architecture, and phased build roadmap).
> **Initial Target Domain:** University **STEM** students (must natively support LaTeX formulas, mathematical proofs, code/algorithms, and diagrams/SVGs).

---

## 1. Core Vision & Product Principle

### 1.1 What We Are Building
An **AI Learning Harness** — a structured cognitive study environment where AI and student collaborate through an evidence-based learning loop, rather than a generic chatbot next to a blank text editor or a one-click summary generator.

The harness organizes course materials, delivers source-grounded adaptive explanations, enforces active student elaboration, diagnoses misconceptions via Socratic feedback, consolidates student notes via diff/merge, and schedules long-term spaced retrieval.

### 1.2 North-Star Principle
> **Do not optimize the amount of information the AI transfers to the student. Optimize how much the student understands, retains, and can apply independently without AI assistance.**

### 1.3 Core Learning Loop
Every study unit follows one continuous cycle:

$$\text{Understand} \rightarrow \text{Re-elaborate} \rightarrow \text{Reason} \rightarrow \text{Correct} \rightarrow \text{Consolidate} \rightarrow \text{Retrieve}$$

### 1.4 The Three Coordinated Responsibilities
These operate as a single unified system, never as disconnected features:
1. **Organizer:** Ingests and indexes sources, maps concept dependencies (DAG), detects prerequisites, sets priorities, and dynamically schedules study and spaced reviews.
2. **Cognitive Tutor:** Produces expertise-calibrated explanations, supports reasoning with Socratic hints, identifies misconceptions, and guides error correction.
3. **Formative Evaluator:** Tracks demonstrated competence separately from note quality, logs recurring errors, distinguishes mere familiarity from independent application, and schedules unassisted verification.

### 1.5 Core Workspace: Single-Screen Dual-Pane UI
- **Left Pane — AI Explanation:** Interactive, source-grounded, progressively disclosed explanation blocks with inline contextual Q&A and source citations.
- **Right Pane — Student Notes:** Mandatory active workspace where the student independently organizes and writes what they understood, later refined through AI-proposed diff/merge revisions.
- **Unified Anti-Switching Layout:** Source citations/previews, explanation, notes editor, and inline micro-checks coexist in one screen with minimal tabs to eliminate context switching.

---

## 2. Non-Negotiable Pedagogical Rules & AI Guardrails

These rules are empirically grounded constraints that **must** be enforced in system prompts, state transitions, and UI design.

### 2.1 Cognitive Load Balancing
Balance the three types of cognitive load across every interaction:
- **Intrinsic Load (Calibrate):** Match topic complexity to prior mastery; check prerequisites first and segment content into **5–10 minute** semantic blocks (*d = 0.43*; Rey et al., 2019).
- **Extraneous Load (Minimize):** Eliminate visual clutter, conversational fluff, dispersive prose, and tab/window switching.
- **Germane Load (Maximize):** Force active elaboration, causal reasoning, self-explanation, and connections to prior knowledge.

### 2.2 Cognitive Offloading Boundary & Non-Permissive AI
- **Automate Logistical Load Only:** AI may automate chunking, scheduling, RAG citation lookup, and note diff/merge formatting — **never** offload *germane/generative* cognitive effort (Risko & Gilbert, 2016). Uncritical AI reliance strongly degrades critical thinking (*r = -0.68*; Gerlich, 2025).
- **Non-Permissive Tutoring:** System prompts **must forbid** giving direct answers or complete solutions on the first attempt; provide Socratic hints and reasoning prompts first.
  - *Evidence:* Unconstrained chatbots boost practice scores (+0.137) but cause a **17% drop** on unassisted final exams (-0.054), whereas hint-constrained GPT tutors prevent this drop (-0.004; Bastani et al., 2025, *PNAS*).
- **Anti-Summary Rule:** Ban one-click AI summaries or pre-built concept maps as primary study modes; students must construct explanations/schemas themselves (*g = 0.72* for self-constructed maps vs. *g = 0.37* for pre-made maps; Schroeder et al., 2018).

### 2.3 Mastery Gating, Step-Based ITS & Expertise Reversal
- **Mastery Gating:** Do not unlock dependent/next modules until the student demonstrates mastery of the current module (*2σ* advantage; Bloom, 1984). (Provide a controlled override/autonomy escape hatch only if needed, without falsely marking the concept as mastered.)
- **Step-Based Tutoring (ITS):** Decompose theory and exercises into verifiable intermediate steps with granular step-level feedback (*d = 0.76* vs. *d = 0.31* for answer-only systems; VanLehn, 2011).
- **Expertise-Adaptive Scaffolding (Worked Example vs. Expertise Reversal Effect):**
  - *Novices / Unfamiliar concepts:* Provide detailed step-by-step worked examples and structured scaffolding to reduce extraneous load.
  - *Mastered / Advanced concepts:* Fade hints and switch to open-ended problems, concise summaries, and edge-case probing (detailed step-by-step examples become counterproductive once mastery is achieved; Sweller).
- **Self-Explanation:** Prompt the student to articulate *why* a step is valid to expose hidden misconceptions (*g = 0.55* overall, *g = 0.35* vs. provided explanations; Bisra et al., 2018; Socratic AI RCT *0.73–1.3 SD* in less time, Kestin et al., 2025).

### 2.4 Grounding, Provenance & Evaluation Safeguards
- **Strict Source Grounding:** Base explanations primarily on uploaded course materials with verifiable document/page citations.
- **Provenance Labeling:** Any external AI supplementation must be clearly marked as external; discrepancies between sources must be surfaced, never hidden.
- **Exercise Hierarchy:** Official professor exercises/past exams always take top priority. AI-generated exercises must be explicitly labeled as AI-generated.
- **Notes ≠ Mastery:** Clean, merged notes in the Right Pane are a study artifact, **not** evidence of learning. Mastery can only be recorded from independent recall, problem-solving, or explanation without AI hints.

### 2.5 LLM Output & Attention Constraints
Digital study suffers from ~40% mind wandering and a **47-second** median on-screen focus before tab-switching (incurring a **23m 15s** refocus cost; Gloria Mark, UC Irvine). Apply Mayer's *Segmenting, Coherence, Signaling,* and *Spatial Contiguity* principles (Mayer & Moreno, 2003):
- **Atomic Micro-Units:** Hard-cap each explanation step/card at **120–150 words**.
- **Progressive Disclosure:** User-controlled step advancement (never dump long multi-section lectures at once).
- **Structural Formatting:** Bold key terms, highlight logical transitions, and eliminate all redundant intro/outro filler.
- **Interpolated Micro-Checks:** Insert 1–2 brief recall questions at natural semantic boundaries to cut mind wandering in half (*39–41% -> 19%*; Szpunar et al., 2013).
- **STEM Visuals:** Reuse figures/formulas from slides and generate clean diagrams (e.g., SVG/Mermaid) when conceptually helpful.

### 2.6 Scheduling, Retention & Flowtime Continuity
- **Spaced Active Recall:** Track *when* a concept was verified, *what errors occurred*, and *hint-free performance*. Retention activities must vary across: definition/concept recall, explanation reconstruction, targeted re-testing of past errors, applied exercises, cross-topic connections, and mixed/interleaved problems (*g = 0.42–0.46*; Brunmair & Richter, 2019).
- **Scheduling Algorithm:** Use **FSRS** (*Difficulty, Stability, Retrievability*) as the primary spaced-repetition engine behind a clean scheduler interface/abstraction (Dunlosky et al., 2013; FSRS outperforms SM-2 in 99.4% of decks with 20–30% fewer reviews).
- **Dynamic Syllabus Planning:** Decompose workload up to the exam date and dynamically redistribute missed sessions across remaining days without punitive "review debt" spikes (Steel, 2007; Theobald, 2021; Aeon et al., 2021).
- **Flexible Task-Aware Breaks (No Rigid Pomodoro):** Do not interrupt mid-thought with rigid timers (Smits, 2025; Göksu, 2026). Offer optional sprints/Flowtime and suggest flexible off-screen breaks **only at natural block boundaries** (suggesting >10 min off-screen after high-load cycles; Albulescu et al., 2022).
- **Post-Break Context Recap:** On return from any pause/session resume, immediately display a concise recap: *what was understood*, *what remains unclear*, and *next step*.
- **Zero Dead Time:** Prefetch/stream upcoming blocks and run heavy indexing asynchronously so the student is never stuck waiting idly.

---

## 3. End-to-End Functional Workflows

The system supports two entry/study paths sharing the same core dual-pane learning engine.

### 3.1 Workflow A — Lecture by Lecture (First-Time / Progressive Mastery)
*Target user: Student learning a subject from scratch or following lectures week by week.*

1. **A1 — Source Acquisition:** Upload slides, textbooks, lecture transcripts, or notes; parse and index with page/section provenance.
2. **A2 — Prerequisite Diagnostics:** Short, targeted diagnostic check on relevant prerequisite concepts (plus optional 3–5 pretesting questions per chapter to prime attention; St. Hilaire et al., 2023).
3. **A3 — Course Organization & Planning:** Build concept map (DAG), segment lectures into 5–10 min learning units, and generate a schedule matching student availability.
4. **A4 — Guided Explanation (Left Pane, Block $i$):** Deliver expertise-calibrated, 120–150 word progressive micro-units with worked examples, prerequisite links, and source citations.
5. **A5 — Mandatory Self-Notes & Contextual Inquiry (Right Pane):** Student writes their own synthesis/explanation in the Right Pane. They may highlight Left Pane text to ask contextual clarification questions without leaving the workspace.
6. **A6 — Targeted Socratic Feedback:** Once the initial draft is submitted, AI detects omissions and misconceptions and initiates a short, targeted Q&A:
   - *Novice / Struggle:* Step-by-step Socratic hints and worked scaffolding.
   - *Demonstrated Mastery:* Deeper open-ended reasoning / edge-case questions.
   - *Rule:* Never reveal the direct answer on the first attempt.
7. **A7 — Notes Revision & Merge:** AI proposes targeted additions/corrections as a structured diff; the student reviews and applies the merge to produce clean, source-linked consolidated notes in the Right Pane.
8. **A8 — Progress & Retention Update:** Record learning evidence, errors, hint usage, and updated FSRS/mastery state (keeping note quality separate from mastery).
9. **A9 — Next Block & Spaced Review:** Proceed to block $i+1$ (pre-fetched) or trigger scheduled interleaved reviews.

### 3.2 Workflow B — Exam Preparation (Diagnostic & Gap-Driven)
*Target user: Student preparing for an upcoming exam with partial/fragmented knowledge.*

1. **B1 — Exam Scope & Material Acquisition:** Collect syllabus, slides, notes, professor's official exercises, and past exams; capture exam date and format (**written, oral, practical, or mixed**).
2. **B2 — Knowledge Diagnosis:** Administer a compact, representative diagnostic (open questions, problems, explanation prompts; self-assessment may supplement but never replace observed performance). Classify every syllabus topic into:
   - *Already Known* | *Incompletely Remembered* | *Recurring Errors* | *Never Studied* | *Unproven Exam Skills*.
3. **B3 — Priority-Based Planning:** Order modules by exam weight, diagnosed gaps, concept DAG prerequisites, and days remaining. Configure each module mode:
   - *Question/Drill-heavy* (for known/rusty topics), or
   - *Theory-first* (where B2 revealed foundational gaps), with calibration ranging from concise recap to full guided explanation.
4. **B4 — Targeted Dual-Pane Study:** Same Dual-Pane workspace (`Left`: calibrated explanation; `Right`: mandatory active reconstruction/elaboration).
5. **B5 — Feedback & Merge:** Same Socratic feedback and diff/merge cycle as Workflow A.
6. **B6 — Active Practice & Retrieval:** Triggered after completing scheduled module clusters (heavier weight than Workflow A). Includes open questions, **professor-style exercises (highest priority)**, multi-step problems, cross-topic connections, formula/proof reconstructions, reasoning questions, and oral exam drills. *(AI-generated exercises must be labeled.)*
7. **B7 — Interleaved Distributed Review:** FSRS-scheduled reviews mixing concepts from different modules, specifically targeting confusable procedures or principles.
8. **B8 — Unassisted Exam Simulation:** Format-matched mock exam **with AI explanatory scaffolding disabled**. Afterward, analyze errors and feed gaps back into FSRS/study priorities.

---

## 4. Conceptual System Architecture & Functional Nodes

### 4.1 Four ITS Macro-Layers
1. **Domain Model:** Course structure, RAG-indexed sources with citations, concept DAG, prerequisites, definitions, examples, exercises, and exam mappings.
2. **Student Model:** Observable learning state (initial diagnosis, mastery states, FSRS parameters, drafts, answers, recurring error log, schedule/availability, explicit preferences). *Must remain inspectable and evidence-based — no opaque psychological profiling.*
3. **Pedagogical Engine:** Policy & orchestration layer deciding *what* topic to present, *what* scaffolding level to apply (Worked Example vs. Open Problem), *when* to quiz, *how* to give Socratic feedback, *when* to fade hints, and *how* to reschedule. (This policy engine — not just a prompt — differentiates the harness from a generic chatbot.)
4. **Interaction Layer:** Context-aware Dual-Pane UI exposing only the controls needed for the current step.

### 4.2 Functional Nodes (`N1`–`N12`)
*Note: Nodes define logical responsibilities; Step 4 may consolidate multiple nodes into shared services/modules where appropriate.*

| Node | ITS Layer | Responsibility | Primary Output |
| :--- | :--- | :--- | :--- |
| **N1 — Course Setup** | Interaction / Student | Captures goal (Path A/B), exam format/date, and time availability | Course & Path Profile |
| **N2 — Source Manager** | Domain | Ingests, chunks, and indexes materials while preserving page/source provenance | Indexed Source Library |
| **N3 — Knowledge Mapper** | Domain | Extracts concepts, prerequisites (DAG), lectures, and 5–10 min learning units | Subject Concept Map & Units |
| **N4 — Diagnostic Engine** | Pedagogical / Student | Runs A2/B2 diagnostics and classifies initial topic mastery & gaps | Diagnostic Profile |
| **N5 — Study Planner** | Pedagogical | Orders modules by DAG/gaps/deadline and builds/adapts the study calendar | Dynamic Study Plan |
| **N6 — Explanation Engine** | Pedagogical / Domain | Generates source-grounded, 120–150w progressive blocks adapted to mastery | Pedagogical Blocks |
| **N7 — Student Workspace** | Interaction | Manages Right-Pane note editing, drafts, and Left-Pane contextual Q&A | Student Drafts & Queries |
| **N8 — Feedback Engine** | Pedagogical | Evaluates drafts against unit objectives & sources; runs Socratic Q&A | Misconceptions, Q&A & Errors |
| **N9 — Notes Consolidator** | Pedagogical / Interaction | Generates structured correction/merge diffs applied by the student | Consolidated Notes |
| **N10 — Assessment Engine** | Pedagogical / Domain | Runs exercises, interleaved drills, and unassisted exam simulations | Learning Evidence |
| **N11 — Progress & Retention** | Student / Pedagogical | Updates mastery states, error logs, and FSRS review scheduling | Learning State & Review Queue |
| **N12 — Session Coordinator** | Pedagogical / Interaction | Manages unit state machine, prefetching, Flowtime breaks, and context recaps | Session State & Transitions |

### 4.3 Node Orchestration Pipelines
- **Setup Pipeline:** `N1 -> N2 -> N3 -> N4 -> N5`
- **Core Unit Learning Loop:** `N6 <-> N7 -> N8 -> N9 -> N11` *(orchestrated by `N12`)*
- **Practice & Retention Loop:** `N10 -> N11 -> N5` *(orchestrated by `N12`)*

---

## 5. Minimum Information Model & Memory Architecture

### 5.1 Core Domain Entities (Database Schema Inputs)
Step 4 must formalize schemas and foreign-key/graph links across these 13 entities:
1. `Course` (subject, syllabus, path A/B, exam format & date)
2. `Source` (file metadata, type [slides/book/transcript/exam], provenance anchors)
3. `Concept` (topic, definitions, DAG prerequisite edges)
4. `LearningUnit` (5–10 min block, learning objectives, linked `Concept`s and `Source` chunks)
5. `StudyPlan` (prioritized units, deadlines, availability constraints)
6. `StudySession` (active state, current unit, step phase, break/recap state)
7. `Explanation` (generated micro-units, scaffolding level, source citations)
8. `StudentDraft` (versioned Right-Pane student notes before merge)
9. `FeedbackSession` (Socratic prompts, student answers, detected errors, hint count)
10. `ConsolidatedNotes` (post-merge versioned notes linked to sources)
11. `LearningEvidence` (quiz/exercise/sim outcomes linked to `Concept`, `Source`, and triggering error)
12. `StudentProgress` (per-concept mastery state, FSRS `D/S/R` parameters, recurring misconception log)
13. `ReviewTask` (scheduled spaced/interleaved recall task and priority)

### 5.2 Three-Tier Selective Memory & Hierarchical Context
Never stuff full session history into every LLM call. Retrieve selectively across three tiers:
1. **Course Memory:** Syllabus, concept DAG, unit summaries, indexed source chunks.
2. **Student Memory:** Concept mastery states, recurring error log, FSRS queue, explicit preferences.
3. **Session Memory:** Current `LearningUnit`, active `StudentDraft`, recent feedback turns, break-recap state.

Use a **3-Level Retrieval Hierarchy** for token efficiency and low latency:
- *Level 1 (Always in Prompt):* Path goal, pedagogical guardrails, current unit objective, student mastery/error summary for this concept.
- *Level 2 (Module Context):* Structured unit/lecture summary, immediate prerequisite concepts.
- *Level 3 (On-Demand RAG):* Exact source chunks, slide figures, and page references fetched when generating explanations or verifying claims.

---

## 6. Prototype (MVP) Scope vs. Post-MVP & Configurable Hypotheses

### 6.1 Phase 1 MVP (Validate the Core Hypothesis First)
The MVP must test whether the structured *Explain -> Self-Elaborate -> Socratic Feedback -> Merge -> Unassisted Check* loop outperforms passive chatbot use. Build these **10 core capabilities** first:
1. Course creation (Path A or B basics) and multi-file upload/ingestion.
2. Semantic segmentation into lessons and 5–10 min conceptual units.
3. Single-screen Dual-Pane Study Workspace.
4. Source-grounded, progressive 120–150w explanations (with citations & STEM LaTeX support).
5. Mandatory independent note-writing in the Right Pane before unlocking feedback.
6. Inline contextual Q&A on selected Left-Pane passages.
7. Targeted Socratic feedback phase (no direct first-attempt answers).
8. AI-assisted diff/merge into consolidated notes.
9. Versioned note persistence and basic per-concept progress/error tracking.
10. At least one unassisted verification / recall check (no AI hints).

### 6.2 Post-MVP / Progressive Extensions
Defer until the core loop is working cleanly (or design clean extension points for):
- Full FSRS parameter optimization & dynamic missed-session rebalancing.
- Interactive oral exam simulation mode.
- Behavioral inference of optimal Flowtime break intervals.
- Automated SVG/diagram synthesis beyond source figure extraction.
- External calendar integrations.

### 6.3 Tunable Experimental Parameters (Do NOT Hardcode)
Expose these as configurable policy parameters so they can be A/B tested and tuned per STEM discipline:
- Target learning unit length (word count / estimated minutes).
- Micro-unit chunk size (default: 120–150 words).
- Number of Socratic feedback questions per block.
- Mastery unlock threshold and hint-fading decay curve.
- Break suggestion cadence and high-load threshold (>10 min off-screen trigger).

---

## 7. Step 4 Directives: What the Implementation Plan Must Decide

Using this specification as ground truth, produce a concrete, actionable **Technical Implementation Plan** covering:
1. **Tech Stack & Deployment Architecture:** Frontend, backend, database(s), vector/hybrid search store, auth/storage, and local vs. cloud deployment model.
2. **Database & Graph/Vector Schema:** Concrete tables/collections for the 13 entities, `Concept` DAG storage, FSRS state fields, and source-provenance chunk metadata.
3. **Ingestion & RAG Pipeline:** Parsing STEM PDFs/slides/transcripts (preserving math/LaTeX, tables, figures, page numbers), semantic segmentation into 5–10 min units, DAG extraction, and 3-level retrieval.
4. **Pedagogical State Machine & LLM Orchestration:** Concrete state transitions for Workflows A & B, agent/node consolidation (`N1`–`N12`), model routing (fast vs. reasoning models), streaming/prefetching for zero dead time, and strict system prompts enforcing Socratic non-permissiveness + 120–150w progressive disclosure.
5. **Scheduler & Student Model Mechanics:** FSRS integration, mastery gating logic, Expertise Reversal scaffolding policy, and dynamic workload redistribution.
6. **Frontend Dual-Pane Workspace & UX Spec:** Editor choice (Markdown + LaTeX + diff/merge UI), Left-Pane progressive cards + inline contextual inquiry, Source provenance viewer, and unassisted exam/quiz mode.
7. **API Contracts & Phased Build Roadmap:** Endpoint/WebSocket specs and step-by-step engineering milestones separating **MVP** from **Post-MVP**.
