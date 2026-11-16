# Problem that we want to solve

1. **"I use AI to study, feel productive, and still bomb the exam"** _(Illusion of competence & cognitive offloading)_
    
    - **Non-permissive / Socratic AI** (Sec 2.7, 5): Refuse direct answers on first attempt; give step-by-step hints instead.
    - **Anti-summary rule** (Sec 2.9): Replace one-click summaries with closed-book concept mapping, self-explanation, or _Teach the AI_ (_Protégé_ mode, Sec 2.8).
    - **Expertise-adaptive scaffolding** (Sec 1.1, 2.3): Worked examples for novices, fading into open-ended problems as mastery grows.
2. **"I have 800 pages, an exam in 3 weeks, and I freeze or fall behind"** _(Planning paralysis & review burnout)_
    
    - **Syllabus-to-schedule chunking** (Sec 3.2, 3.3): Break uploaded files into 5–10 min units mapped to an exam date, auto-redistributing missed days without punitive "review debt."
    - **If-Then initiation cues** (Sec 3.4): Concrete environmental triggers to overcome starting friction.
3. **"I get distracted every minute hopping between PDF, notes, flashcards, and ChatGPT"** _(Fragmentation & focus decay)_
    
    - **Single-pane anti-switching workspace** (Sec 4.5): Source, notes, quiz, and AI side-by-side.
    - **Micro-units + interpolated checkpoints** (Sec 4.2, 4.3): 120–150 word progressive disclosure with 1–2 quick questions at section boundaries.
    - **Task-Aware Flowtime + return recap** (Sec 4.4): Breaks suggested only at natural module boundaries, with a brief AI context recap afterward.
4. **"I study chapter-by-chapter, forget it in two weeks, or mix up similar concepts"** _(Weak retention & transfer)_
    
    - **Pre-training + pretesting** (Sec 2.5, 3.2): Key glossary + 3–5 diagnostic questions _before_ reading a chapter.
    - **Cross-chapter interleaved FSRS** (Sec 2.6, 3.1): Adaptive spaced repetition that mixes confusable concepts across chapters rather than isolating per PDF.
    - **Mastery gating** (Sec 2.1): Locking the next module until the current one is demonstrated.

# Proposed Direction

The software so should do all the following
* **[skip for now]Planning**: The software should focus on use raw course material and exam dates to get a realistic daily plan. Lightweight checkpoints, and use of FSRS. Low friction.
* **No AI slop study**: banning passive summaries (Sec 2.9), enforcing Socratic/step-based tutoring (Sec 2.2, 2.7), pretesting (Sec 2.5), and _Protégé_ mode (Sec 2.8). _Higher friction, solves "ChatGPT is making me lazy/unprepared."_
* **Information Load**:  Focus on the unified workspace (Sec 4.5), progressive 120–150 word pacing (Sec 4.3), boundary micro-tests (Sec 4.2), and Flowtime breaks with context 