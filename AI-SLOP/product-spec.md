# Product Specification: Non-Chat AI Study Notebook (Working Spec)

> **Core Thesis:** An all-in-one, minimal, **zero-chat** study workspace for university students. Instead of asking a chatbot for answers or reading passive summaries, students learn from adaptive micro-explanations and write their own explanations/proofs block-by-block—reviewed by AI via a **separate diagnostic question card** and **minimal inline diff suggestions**.

---

## 1. Target User & Problem Scope

### 1.1 Target User (v1)
* **Primary:** University students facing high study loads across **technical, theoretical, and formula-heavy** disciplines (STEM, CS, math, physics, formal theory).
* **Future Expansion (Post-v1):** Generalizable down to high school and middle school learners via calibrated scaffolding.

### 1.2 Problems Addressed in v1
1. **No AI-Slop Study ("Illusion of Competence"):** Passive summaries and permissive chatbots create fluency without understanding and degrade unassisted exam performance ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 2.9 & 5).
2. **Information Overload & Workspace Fragmentation:** Hopping across PDFs, note apps, and chat windows destroys focus; long unsegmented walls of text overload working memory ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 4.3 & 4.5).
3. **Deferred (Built to Integrate Later — Phase 2):** Long-term planning/exam scheduling, FSRS spaced repetition, and adaptive Flowtime pacing.

---

## 2. Product Manifesto (Non-Negotiable Constraints)

1. **Zero Chat:** No conversational chatbot sidebar, no open-ended chat loops. Studying happens through structured writing, targeted questioning, and inline review.
2. **Minimal, Single-Pane-Pair Interface:** Everything required for a study session lives in one distraction-free workspace.
3. **User Does the Germane Effort:** AI automates *extraneous/logistical* load (segmentation, source grounding, critique, formatting diffs) and never replaces *generative* reasoning ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 5).
4. **No One-Click AI Summaries:** Replace passive summaries with diagnostic pretesting, user-authored explanations, and inline critique.
5. **Soft Guardrails with Tracked Overrides:** Users are never hard-locked out of progressing or peeking, but every bypass is logged as `unverified` so future review scheduling (Phase 2) catches the gap.

---

## 3. Core UX: The Two-Pane "Code-Review Notebook"

### 3.1 Workspace Layout
* **Left Pane — Reference & Adaptive Guide:**
  * Simple top toggle: **`[Adaptive Explanation | Original Source]`**.
  * *Adaptive Explanation:* Displays one 120–150 word micro-unit at a time, calibrated to the student's current mastery of the topic.
  * *Original Source:* Shows the exact uploaded PDF/slide/note passage anchored to the current module so the student can verify claims anytime.
* **Right Pane — User Notebook (Markdown + LaTeX):**
  * Block-based editor supporting **Markdown + LaTeX math** (v1 scope).
  * **Blind-Write Toggle:** Automatically fades or hides the left pane while the user writes in the right pane (with a soft-override peek button) to enforce closed-book recall instead of transcription.
  * Committed blocks accumulate into a persistent, structured session notebook.
* **Review Question Card (Separate UI Card):**
  * Triggered on submission; surfaces targeted clarifying questions outside the prose flow before any inline edits are proposed.

### 3.2 End-to-End Study Loop (v1)

```text
[1. Ingest Sources]
        │
        ▼
[2. Once-Per-Topic Diagnostic Pretest] ──► Sets initial mastery level
        │
        ▼
┌─► [3. Left Pane: Adaptive Micro-Explanation (120–150w)] ◄──► Toggle: [Original Source]
│       └─ User Inline Feedback: [Inaccurate | Too Complex | Too Easy] (+ optional note)
│          └─ AI edits that specific block (citing source if Inaccurate) and stops.
│
│   [4. Right Pane: User Writes Explanation / Proof (Markdown + LaTeX)]
│       └─ Blind-Write Toggle fades/hides Left Pane during active writing.
│
│   [5. Submit ──► Separate Question Card]
│       └─ AI asks targeted questions on errors, missing proof steps, or ambiguities.
│       └─ User answers questions inside the card.
│
│   [6. Inline Minimal Diff Proposal]
│       └─ Using original notes + Question Card answers, AI proposes surgical inline diffs
│          on the Right Pane notes.
│       └─ User reviews, manually edits/accepts/rejects changes.
│
│   [7. Commit Block to Notebook] (or Soft Override ──► tagged `unverified`)
└───────┴──► Next micro-module
```

---

## 4. Detailed Feature Mechanics & Pedagogical Mapping

### 4.1 Ingestion & Segmentation
* **Supported Inputs (v1):** PDFs, lecture slides, Markdown (`.md`), and plain text notes (`.txt`).
* **Semantic Chunking:** Sources are segmented into logical topics and atomic micro-modules (5–10 min conceptual units, broken into 120–150 word progressive steps; [doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 3.2 & 4.3).
* **Source Grounding:** Every generated micro-unit and critique maintains page/section links back to the uploaded source.

### 4.2 Once-Per-Topic Diagnostic Pretest
* **Trigger:** Administered once when starting a new topic (3–5 diagnostic questions).
* **Purpose:**
  1. Measures baseline mastery to calibrate the Left Pane's starting scaffolding (*Expertise Reversal*: worked step-by-step examples for novices vs. concise conceptual/problem prompts for advanced users; [doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 1.1 & 2.3).
  2. Triggers productive failure / pretesting attention priming ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 2.5).

### 4.3 Bidirectional Inline Feedback on Left Pane
* **Mechanism:** The user can select/click any section of the AI-generated explanation and flag it with one of three tags (+ optional 1-line note):
  * **`Inaccurate / Wrong`** (forces source re-check and explicit page/slide citation)
  * **`Too Complex`** (increases worked-step scaffolding / lowers intrinsic load)
  * **`Too Easy`** (strips introductory fluff / increases abstraction)
* **Strict Behavior ("Edit and Stop"):** The AI regenerates/edits *only* that targeted block and stops. It does **not** start a chat thread or silently alter unrelated settings.

### 4.4 Right Pane Recall, Question Card & Minimal Diffs
1. **Blind-Write Recall:** Writing in the right pane activates *Self-Explanation* and the *Protégé Effect* ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 2.7 & 2.8) while preventing copy-paste illusions.
2. **Submit → Separate Question Card:** Upon clicking **Submit**, the AI evaluates the user's explanation/derivation step-by-step against the source ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 2.2) and presents targeted clarifying questions in a dedicated UI card (e.g., *"Why does this inequality hold when $x = 0$?"* or *"Which theorem justifies step 3?"*).
3. **Answer → Minimal Inline Diff:** Once the user answers the Question Card, the AI uses *both* the user's draft and their answers to propose **minimal, surgical inline diffs** on the right-pane block—never rewriting whole paragraphs from scratch.
4. **Human-in-the-Loop Commit:** The user reviews each proposed diff (accept, reject, or rewrite) and saves the finalized block into the session notebook.

### 4.5 Soft Overrides
* Users can reveal the dimmed Left Pane during Blind-Write, skip the Question Card, or commit a block without resolving diffs.
* Any bypassed step marks the committed block with `status: unverified` and logs `override_used: true` for future scheduling.

---

## 5. Competitive Landscape & Differentiation

| Existing Category | Examples | What They Do Well | Gap Filled by This Product |
| :--- | :--- | :--- | :--- |
| **Closed Mastery Systems** | *Math Academy*, *Brilliant.org* | Zero chat, diagnostic pretests, adaptive step scaffolding | Fixed curricula only; cannot ingest arbitrary university PDFs/slides or build personal notes |
| **Feynman / Blurt Evaluators** | *`ptah23/feynman-ai`*, *Mindko (Blurt)*, *Feynman AI* | Write-first recall before AI rubric feedback | One-off scratchpads; no adaptive left pane, no inline diffing, no persistent block-by-block notebook |
| **Inline Critique Tools** | *Inline Writing Tutor*, *Class Companion*, *Monsha AI* | Passage-level inline questions/annotations instead of chat | Built for essays/K-12 grading; lacks university STEM/LaTeX support and adaptive study loop |
| **Active-Recall Notebooks** | *RemNote*, *SmarterHumans.ai*, *Recall (recall.it)* | Persistent notes, source deep-linking, FSRS cards | Flashcard/consumption-first; does not critique user-written proofs or propose minimal diffs |
| **Socratic / Grounded Chat** | *NotebookLM*, *ChatGPT Study Mode*, *Claude Learning Mode*, *Khanmigo* | Source-grounded RAG and Socratic prompting | Chat-first UX that invites conversational dependency and passive summarizing |

---

## 6. System Architecture (Adapted 4-Module ITS)

Building on the domain-agnostic architecture in [doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md) (Sec 7.2), adapted for a **non-chat, Idea-A-ready** workspace:

1. **Domain Model (Ingestion & Grounding):**
   * Parses PDFs, slides, Markdown, and text into a topic hierarchy, concept dependency graph, key-term glossary, and RAG-indexed chunks with exact page/slide anchors.
2. **Student Model (Mastery + Idea A Hooks):**
   * Tracks per-topic diagnostic mastery, per-block interaction logs, and future-ready spaced-repetition fields even while Phase 2 scheduling is disabled:
     * `block_id`, `topic_id`, `source_refs[]`
     * `initial_mastery`, `left_feedback_flags[]`
     * `question_card_attempts`, `diffs_proposed`, `diffs_accepted_vs_edited`
     * `override_used` (`boolean`), `verification_status` (`verified | unverified`)
     * `time_spent_sec`, `fsrs_state` *(placeholder: Difficulty $D$, Stability $S$, Retrievability $R$, `next_review_at`)*
3. **Pedagogical & Critique Engine (Non-Chat Pipelines):**
   * *Pretest Generator:* Creates 3–5 topic diagnostic items.
   * *Adaptive Explainer:* Generates 120–150w explanations calibrated to mastery; enforces source citations on `Inaccurate` edit requests (edit-and-stop).
   * *Step-by-Step Reviewer:* Evaluates submitted Markdown + LaTeX blocks → outputs structured Question Card items.
   * *Minimal Diff Generator:* Combines draft + Question Card responses → emits line/span-level patch suggestions without full rewrites.
4. **Workspace UI Module:**
   * Dual-pane renderer (`[Adaptive Explanation | Original Source]` + Markdown/LaTeX block editor), Blind-Write dimmer, Left-Pane inline flag popover, Separate Question Card modal/panel, Inline Diff reviewer, and Notebook exporter.

---

## 7. Scope Boundaries: v1 vs. Deferred (Phase 2)

### In Scope (v1)
* Ingestion of PDF, lecture slides, Markdown, and text notes.
* Once-per-topic diagnostic pretest.
* Two-pane workspace with `[Adaptive Explanation | Original Source]` toggle and Blind-Write toggle.
* Left-pane inline user feedback (`Inaccurate`, `Too Complex`, `Too Easy` → edit-and-stop).
* Right-pane Markdown + LaTeX block editor → Separate Question Card → Answer → Minimal Inline Diff review → Persistent session notebook.
* Soft overrides + `unverified` telemetry logging.

### Deferred to Phase 2 (Idea A & Focus Extensions)
* **Dynamic Exam Planner & Anti-Debt Scheduling:** Distributing modules across days up to an exam date and rebalancing missed sessions ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 3.3).
* **FSRS Spaced Repetition & Cross-Chapter Interleaving:** Scheduled recall queues prioritizing `unverified` and low-stability blocks ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 2.6 & 3.1).
* **Task-Aware Flowtime & Context Recaps:** Module-boundary break timers and 3-bullet return recaps ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 4.4).
* **Implementation Intentions:** If-Then study trigger rules ([doc-raw.md](file:///home/davidel/appunti/AI-SLOP/doc-raw.md), Sec 3.4).
* **Expanded Inputs & Audience:** Handwritten proof OCR, interactive diagrams, and middle/high school profiles.
