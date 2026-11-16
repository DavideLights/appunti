
1. **Pre: Mini Brain Storming**: what we want to do that is innovative and effective? Max: 20 minutes.
2. **Source finding**: each team member finds sources online and should produce `memberName-ideas.md`
	1. Step 1: **takes a lot of time**. Deep Search or similar tools, give an effective structure for the output.
	2. Step 2: **concurrent to Step 1**, since it takes a lot of time. Ask to AI, witouth doing a Deep Search on the internet, for papers, resources and ask to resume them briefly.
		1. Why Step2? So each team member has a view of the problem.
		2. **IMPORTANT**: Ask ai to match what he found with real documents on internet.
		3. **NOTE**: Do Not Read entire documents, let the AI resume them for you, its a waste of time.
	3. Step 3: use Step 2 as Input to produce `memberName-rawideas.md`, it should contain
		1. research papers
		2. product ideas
		3. design ideas
		4. nothing practical.
	4. Step 4: use AI to merge the most important topics `memberName-rawideas.md` and the most important ones returned by the Deep Search to produce `memberName-ideas.md`

> [!note] how to ask AI for innovative ideas?
> It should select ideas that maximize: innovation but also effectiveness.

2. **Brainstorming**:
	1. Step1: each member reads the most important topics of its `memberName-ideas.md` and discuss them.
	2. Step2: collect for each `memberName-ideas.md` files the most important topics
		1. Max 2/3 topics for member
	3. Step3: ask ai to produce `ideas.md` using the most important ideas 
	4. Step4: manual review, even parallelized.

3. **Implementation Plan**:
	1. Step1: `preImpl.md` should contain a guide line. Maybe AI guided, or write 
		1. what the software will do?
		2. what are the main ideas behind the software?
		3. use cases to solve
		4. use examples
		5. workflow example
		6. what software to rely on
		7. **NOT**: how to implement in detail/low level.
		8. **NOT**: too deep architectural details.
	2. Step2: use `preImpl.md` and give UI guidelines to produce `UIMockUpImplementationPlan.md`
		1. Tell the AI to ASK you questions
		2. Here you'll define how user interacts with the software and identify
	3. Step 2.1: optional, ask AI to produce the UIMockup.
	4. Step3: if you have time do the same to produce `ExtendedImplementationPlan.md`
		1. Here you'll define how the ENTIRE software works
		2. If you have enough time, pass the UIMockImplementationPlan produced in Step2 for better context.
	5. Step4: ask AI to produce the first milestone. Eventually use UIMockup as input.