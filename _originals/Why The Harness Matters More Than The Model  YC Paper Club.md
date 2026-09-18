# Why The Harness Matters More Than The Model — YC Paper Club (Part 1)

## Framing: Why Devote a Night to "Just a Wrapper"

The session opens by confronting the dismissive view of harness/scaffolding work. Two pieces of online commentary are cited as representative of this skepticism: a Reddit comment questioning whether "this kind of prompt engineering belongs at a top-tier machine learning conference," and another claim that "context engineering is not a research problem." The speaker pushes back on this framing directly: harnesses have been unfairly treated as lightweight or unserious research, yet the empirical evidence says otherwise. As a concrete anchor, the difference between "harness one" and "harness two" configurations produced an 18-percentage-point jump in performance — and later in the talk this is shown to be the literal difference between an agent succeeding or failing at ARC-AGI.

The speaker references the METR plots that track model release date against the length of task an agent can autonomously complete. The claim is that a large share of the *visible* progress in that plot isn't from raw model capability improving in isolation — it's attributable to harness improvements layered on top of the same underlying weights. This leads to a periodization of the field into two eras:

- **The static harness era**: the scaffolding around the model is fixed by a human designer; the harness itself does not change or improve during use.
- **The self-improving harness era** (roughly the last 6 months at the time of this talk): the harness itself becomes an object that can be modified, learned, or evolved — not just the prompts fed into a fixed pipeline.

### The Perplexity/IQ vs. Test-Time Experience Framing

The speaker recounts a plot they liked from a presentation by the CEO of "Trajectory" (a company name as transcribed). The point of that plot: the field has been almost entirely focused on driving down perplexity, which correlates loosely with something like model IQ — pushing models up an "intelligence" dimension. But this focus has left a second dimension underexploited: **test-time experience**. Models generate enormous amounts of experience when deployed on a new domain, but there isn't good machinery for quickly adapting to that experience.

This connects to an experiment the speaker says they ran and presented at an earlier YC paper club session: increasing the number of samples an agent sees online, at batch size one, and asking how quickly the model actually learns from that experience. The finding was that in-context learning (ICL) saturates fast — once you load roughly 40–50 examples into context, further examples stop improving validation performance. Beyond that point, the only ways to keep improving are through progressively heavier-weight training procedures: low-rank LoRA, then higher-rank LoRA, then full supervised fine-tuning (SFT). The speaker calls out how strange it is that we have this ladder of qualitatively different training regimes with no smooth "fast adaptation" option in between — and argues this exact gap is precisely the space where harnesses are proving valuable, because a harness can let an agent adapt to a new problem *procedurally* (via memory, tools, context restructuring) rather than needing gradient updates at all.

### ARC-AGI as the Proof Case

ARC-AGI is presented as the sharpest illustration of this idea, because the entire design intent behind ARC-AGI (as built by Greg and François Chollet) is to measure **fluid intelligence** — how quickly a system adapts to a brand-new problem distribution it has never seen, as opposed to measuring memorized crystallized knowledge. The speaker notes they got a preview of this design process during YC's Winter '26 batch, helping look at how much care goes into making sure each ARC-AGI "game" tests orthogonal skills from one game to the next, precisely so the benchmark isolates adaptability rather than prior exposure.

The concrete numbers given:
- Claude Opus, evaluated directly against the private ARC-AGI holdout (accessible only to Greg and Chollet), scored around **30%**.
- With a harness wrapped around the *same class of model* — "this thing that doesn't deserve any research, just some wrapper and some scaffolding" — performance reached **95%**.
- NVIDIA's system (referred to as AVO) reached **100%**.
- The two systems credited with these harness-driven jumps are **Prime Agent** and **NVIDIA's entry**, both described as having "just recently come out."

The takeaway the speaker draws: this is not a small effect. Going from 30% to 95–100% purely through scaffolding, on the exact same underlying weight file, is the central piece of evidence that harnesses deserve serious research attention.

### A Personal Anecdote: Accidentally Building a Harness for Auto-Research

The speaker describes forking Andrej Karpathy's "auto-researcher" project (launched around March) purely to build a small UI for observing what it was doing. In the process of adding observability, they ended up building an entire harness without intending to.

The system works like this:
1. You specify a **research purpose** in natural language. The concrete example given: *"diffusion language models don't beat autoregressive (AR) language models — but maybe if I ensemble/shard the diffusion LM into many smaller shards (since diffusion models have unusually high arithmetic intensity per GPU compared to AR models), the aggregate of many shards could outperform a single AR model."*
2. You give the system some **seed ideas** — e.g., vary the ensemble/shard size across 100x, 10x, 5x, etc.
3. You specify a **validation metric**, e.g., evaluating on GSM8K with a GPT-2-scale setup.
4. A **scoping agent** searches for related papers and GitHub repositories.
5. The scoped task is handed to a **PI agent** (named "Chris Ray" in this setup).
6. Chris Ray hands it to a **research agent** (named "John Sadhikan" in this setup — one of the night's actual speakers, referenced as a joke/callback), who does the实际 experimentation.
7. There's a **council** step where the speaker and a collaborator ("Yaso") give feedback partway through.
8. Chris Ray periodically "nags" the research agent (roughly hourly) to keep it moving.
9. Once ready, the task is handed to an **author agent**, which freezes the idea, runs ablations, and writes up the paper.

The whole pipeline is viewable through a "cockpit" dashboard, exposed remotely via Tailscale so it can be checked from anywhere, and it sends email updates. The speaker reports that this setup, running roughly eight ideas across eight 8×H100 GPU nodes concurrently, now produces papers that started out low-quality (March/April) but have become genuinely good by the time of this talk. The point of the anecdote: nothing changed about the underlying model weights — only the scaffolding/harness wrapped around the same weight file changed, and that alone unlocked a qualitatively different capability (autonomous multi-week research).

## A Five-Minute History of Harnesses

The speaker explicitly frames this section as a deliberately non-chronological, heavily coarse-grained tour of the literature (from *Self-Refine* to *Reflexion* to *Voyager* to *Toolformer* and others), aimed at giving newcomers to AI the historical context that's often missing.

### The Zero Harness: Raw GPT-2 (Feb 2019)

The very first "harness" is described as barely a harness at all: a `while` loop that runs until an end-of-sequence token, combined with top-p sampling, plus whatever environment the output is checked against. There is no tool calling, no skills, no memory beyond the raw context window.

**Worked example — GSM8K under the zero harness:**
- System prompt: a persona instruction like "You are a math teacher" (the kind of persona-conditioning that was common at the time).
- Context: "Susie has five dollars, she spends three. How much does she have now?"
- Output format: no chain of thought at all — just a `####` marker followed directly by the numeric answer and an end-of-sequence token. This `####` format is literally the GSM8K answer format.
- Scoring: you look at what comes after the `####` and score plus-one or minus-one depending on correctness.

The speaker frames essentially the entire subsequent six years of progress as the story of adding more and more functionality *around* this same basic loop — i.e., building up the static harness.

### Context and Output-Space Innovations

**Few-shot prompting (in-context learning).** The next step: instead of asking the model to jump straight to the answer, put worked examples into the context first (e.g., a similar problem solved as "4 and 1"), so the model can pattern-match its way to the new problem's solution. This is attributed to the "few-shot learners" paper from around July 2020 (GPT-3).

**Chain of thought.** The insight here: directly predicting the two-digit (or single-digit) final answer right after `####` is hard for the model, because all of the necessary logic has to be compressed into a single token-prediction step. Chain of thought instead "smears" the computation/logic across many more tokens, training/prompting the model to work through intermediate reasoning steps before emitting the final answer. Both few-shot prompting and chain of thought are classified as **context innovations** and **output-space (action-space) innovations** — they change what goes into the context and what the model is asked to produce, without changing the model's access to the outside world.

### Giving the Model Tools and External State

**WebGPT and Toolformer.** WebGPT came first, followed by Toolformer, both introducing the idea of giving the model callable tools. A tool is described concretely as just a JSON object specification. Worked example: instead of relying on the model's weights to internally compute "5 − 2," the model can instead call a Python subtraction function — `sub(5, 3)` — and receive back the correct numeric result. Tools are exposed to the model via the system prompt, and this is identified as the origin point of "tool calling" as a concept.

**MemGPT.** Prior to MemGPT, the only thing a harness could do to context was *append* — you could keep appending more and more content but never selectively update or remove anything. MemGPT introduces the idea of giving the model **CRUD** (create, read, update, delete) access to its own context, via a designated chunk called "memory" that the model can rewrite over time, rather than being limited to a strictly growing transcript.

**Voyager and skills.** Voyager (built in a Minecraft environment) raises a further question: if the model has multiple tools, what if it needs to *chain* several tools together to accomplish a task, and then wants to remember that chained procedure permanently by folding it back into its own system prompt? This is where the concept of a **skill** originates. Concretely, this looks like a `skills.md` file: each skill has a name (which can be searched/retrieved) and an associated procedure describing how to execute it. The speaker notes this Voyager formulation is essentially still what most people mean by "a skill" today.

**Intercode.** Extends the action-space innovation idea further: rather than calling a fixed, pre-defined tool (an API), what if the model can output arbitrary *code* on the fly? This effectively gives the model "on-the-fly skills." The speaker admits genuine uncertainty here about the boundary between a "tool" (which they consider to technically mean an API) and a "skill" when the model is instead directly emitting a function/program — flagging this as an open conceptual ambiguity rather than a settled distinction.

### Self-Reflection and Multi-Agent Patterns

**ReAct → Self-Refine → Reflexion.** The core idea across this lineage: if you have multiple agents (or roles) that can inspect and critique the ongoing work, the system can self-improve on its own context.

**Worked example (Reflexion-style loop) walked through step by step:**
1. The agent takes some action — in the speaker's illustrative example, it makes an arithmetic mistake by flipping the 3 and the 5 in a calculation.
2. The (mistaken) result is sent to an **internal evaluator**, which judges whether it looks correct. In this example, the evaluator says: no, this doesn't look right.
3. From here there are two branches: the agent can keep looping internally against the evaluator, *or* it can go out to the actual environment and get back a genuine reward/correctness signal.
4. A **reflection** step then explicitly tells the agent what went wrong ("you flipped these two values — go back") so it can revise and improve its answer.

This is characterized as one of the first concrete instantiations of an agent being multi-agent with itself — i.e., letting the agent reflect on its own output and improve it, rather than simply emitting one shot and stopping.

**Sub-agents and recursion.** The next expansion: one of the tools a top-level agent can call is "spawn a sub-agent." These sub-agents persist as running processes ("persistent ripples" in the speaker's terminology) that the parent can interact with over time, and the parent maintains a list of the sub-agents it has spawned so it can invoke them again later.

**Recursive Language Models (RLMs).** This idea is then taken further recursively: the agent is given a callable "RLM query" operation that lets it recursively call itself to solve a larger class of problems, and at the leaves of this recursion it can spawn further LM agents as needed, all coordinated by a single main orchestrator agent. The speaker labels this entire lineage — from tool calling through skills through sub-agents through recursive LM calls, all still operating under a fixed, human-designed structure — as **"harness v1,"** i.e., still fundamentally a *static* harness: nothing about the system prompt or the harness's own structure is being learned or rewritten during operation.

Before continuing, the speaker calls out **GStack** (and "Gary") by name as underlying infrastructure that makes all of this possible, along with acknowledging other unnamed contributors.

### Anatomy of a "Harness v1" System

Summarizing the static-harness architecture concretely:
- An **agent spec**: a system prompt, plus explicit limits (how many turns are allowed, how many tool calls are allowed — you don't want to allow infinite execution).
- A **tool list**.
- A **skills list**.
- A **sub-agent list**.
- All of this runs inside a **loop**.

This loop can be triggered in different ways — e.g., invoked reactively when the user asks it to do something in a Slack channel (a segue to the later QM segment), or invoked proactively on a cron schedule, waking up periodically (e.g., hourly) and autonomously deciding what work to do, "just like anyone else" might check in on their responsibilities periodically.

The loop itself involves: **session management**, **context compilation** (assembling everything relevant into a prompt fed to the model), an **LLM call** that produces an action, and then — if that action requires invoking a tool — the tool result gets appended back into the context, and the loop continues. This full description is what the speaker calls "harness v1."

## Harness v2: Making the Harness Itself Learn

The most exciting and current frontier, per the speaker, is when the *harness itself* becomes learnable — either learning the optimal system prompt, or, more radically, learning/modifying the harness's own code. The speaker calls this "very trippy."

### DSPy (Demonstrate, Search, Predict)

DSPy's authors were invited to present but couldn't attend — they were running a 150-person DSPy meetup in San Francisco the same night. The speaker has interviewed them on a podcast previously and describes the DSPy community very positively.

The core idea: given a small training set of examples, learn the *optimal system prompt* automatically. Since you can't backpropagate directly through the discrete process of prompt iteration, DSPy instead uses something like **genetic programming**: generate candidate prompts, merge candidates using some merge rule, evaluate the merged candidates, and iterate. Effectively, this gives you CRUD access over the system prompt itself, letting the system search over the space of possible system prompts rather than fixing one by hand.

### Darwin Machines: Evolving the Harness Code Itself

Darwin machines go a step further than DSPy: rather than only being allowed to change the system prompt, the system is allowed to change **the harness code itself** — the actual program that runs the agent loop.

**Mechanism, as described:** You maintain an **archive** of many different agents, where each entry in the archive is a (harness, system prompt) pair. You sample candidates from this archive, run them through evaluation against some fitness function, and push results back into the archive. Critically, there's a **meta-harness** layer that allows an agent to modify its own harness, turning it into a different harness — and this loop repeats, producing progressively better agents over time.

The speaker frames the top-level **meta-harness** as itself being "a harness whose job is to produce harnesses" — explicitly calling this "a really meta concept." Concretely, this meta-harness configures things like multi-agent structure and context compilation, and it has CRUD access over all of it: the harness code itself, the meta-prompt, the system prompts of every constituent agent, and even how many agents exist. Over time this meta-harness "grows" — accreting more capability into itself.

### Continual Harness

One of the paper's lead authors was present in the room. This line of work is described as adding further refinement on top of the Darwin-machine idea in two main ways:

1. **A more detailed breakdown of memory classes**, including a "history" component (the speaker defers full detail on this to the author's own talk later in the evening).
2. **Dagger-style online learning at the weight level** — i.e., not just editing the harness/prompt, but actually performing test-time training on the underlying LLM weights themselves, based on a small number of freshly observed examples. The speaker calls this out specifically as something that would excite "the classic RL people" (naming an audience member, Robert, as likely to appreciate it) and describes it as "a huge, huge important research direction that we should get working" — i.e., an open problem rather than something solved.

## Speaker Introductions for the Night

Three of four planned speakers are present (one, Ben, could not attend due to food poisoning):

1. **Seth** — a student under (a name transcribed as "Shein") at Princeton, and a researcher at Prime Intellect; author of **Prime Agent**, described as a self-improving RLM (recursive language model) harness.
2. **John Sadhikan** — presenting for a second time at this event (a "callback" presenter), a PhD student under advisors Christopher Ré and Azalia (Hazy Research lab); co-author of **Open Jarvis** with Ivanka Orion, described as a "personal Open Jarvis" system.
3. **Josh and Rean** — Josh has just been promoted to head of YC Labs (met with applause); they present **QM**, YC's internal general-purpose agent, released about a month prior, which the speaker says has become "meaningfully better" and that they personally use every day.

## Seth's Talk: Prime Agent

### First-Principles Framing

Seth states his goal is to convince the audience to take a first-principles approach to harness design. He starts from the most reductive possible description of an LLM: it is a **sequential processor** with fixed weights, operating on a visible context window — tokens go in, tokens come out, one next-token prediction at a time. In everyday practice we don't think of LLMs this way anymore — we give them file access, tools, programs, the ability to message other running sessions, and the ability to spawn sub-agents — but underneath all of that, it remains fundamentally just a neural network making next-token predictions.

**Definition of "harness":** the layer that sits between the raw LLM and the world, and which supplies persistent state, tools, and compute that the raw model does not have on its own.

### Prime Agent Architecture, User's-Eye View

From a human user's perspective, opening Prime Agent (similar to opening Claude Code or Codex) presents an **agents view**: an overview of all running parallel agent sessions with a tight summary of what each is doing. From there you can enter a specific **root session**, which acts as a project orchestrator over whatever sub-agents it controls. Crucially, the user does not need to explicitly instruct the system to create sub-agents — the orchestrator will spawn them autonomously whenever useful.

This all operates programmatically through an **IPython shell**, built on the **recursive language model (RLM)** principle: tools, memories, and sub-agents are all exposed inside this shell environment, along with messaging paradigms for coordinating across agents. Each agent can directly interact with the environment — which might be as simple as files and programs on your own computer, or as large as an entire H200 GPU node cluster running an auto-research job.

**Persistence.** Each agent is backed by a persistent daemon process on the machine. This means closing your laptop lid or hitting Ctrl-C on the terminal session does not kill the underlying agent — it keeps running in the background; you have to explicitly stop the session to actually halt it.

**Continual-harness-derived features.** Prime Agent incorporates live CRUD operations across memory, skills, sub-agents, persistent state, and even its own system prompt — allowing ongoing self-modification of all of these components.

### The Layered-Cache Mental Model (L1/L2/L3)

Seth proposes thinking about the different places information can live as something like a CPU cache hierarchy, ordered by how "fast"/immediately accessible the information is to the model:

- **Fastest / most immediately available: the model weights themselves.** This is why everyone's first instinct is "just put everything into the weights" — but full fine-tuning every time you want to update knowledge is expensive, so this isn't practical for continuously changing information.
- **Active input context** (roughly "L1" in this metaphor): lots of tokens fed in directly, including in-context examples for added capability — but this is a finite, exhaustible resource. Eventually you run out of context length.
  - **Compaction** is introduced here as one of the very earliest and still most commonly used harness techniques — even among people who claim to want "the most minimal harness possible." Compaction is a generalized tool that lets the agent summarize its own context history so it can keep working past the limits of its active context window.
- **"L2"** — an intermediate layer between pure active context and the filesystem. Concretely, this is something like a live **ripple**: code running directly in an IPython/Jupyter-style shell, where variables are held in RAM. The agent can programmatically manipulate this state and run arbitrary programs against it, saving enormous numbers of tokens compared to putting all of that information directly into the context window. **Sub-agents** are described as functioning similarly at this layer — you're "saving context" by delegating a bounded task with a specific slice of information to a sub-agent, which does the work and reports back only the result, rather than dragging the entire working process through the parent's context.
- **"L3"** — the dispatch/persistent-storage layer: reading and writing to a real filesystem (main memory / disk).

**Update mechanisms across layers.** Compaction is the update mechanism for the active-context layer. At the ripple (L2) layer, Seth describes the need for something like **agentic garbage collection** — actively cleaning up variables and sub-agent state so that the RAM footprint doesn't grow unboundedly and crash the machine. At the filesystem (L3) layer, the analogous process is **refinement**: updating and deleting skills, memories, and prompts stored on disk, so the hard drive doesn't fill up either. The general pattern across all three layers: you need both a way to *express* new state and a way to *revise/prune* old state over time — CRUD, essentially, at every layer of the stack.

### Turing Machine vs. Von Neumann Machine Metaphor

Seth offers a second metaphor to reinforce why harnesses matter architecturally: a raw LLM looks like a **Turing machine** — it has a tape (context) and a fixed transition process, consuming instructions and producing outputs, but with no general facility to read and write external memory as a first-class operation. A harness turns this into something much more like a **Von Neumann architecture** — one where the system can perform read and write operations against external memory. This qualitatively expands what class of problems the system can solve, beyond what a Turing-machine-style raw LLM call can express on its own.

### Good Harness Design = Maximal Expressibility

Seth's design philosophy: a good harness should be **maximally expressible**. Early harnesses tended to hard-code a specific procedure — e.g., an explicit "plan → act → critique" loop imposed from outside. But as models have gotten more capable, they have started to natively discover these strategies on their own; you no longer need to hand-impose a react-style loop, because the model will often converge on similar behavior itself, *if* it's given the right primitives.

What the models still *cannot* do on their own, and what the harness must supply, are specific **model-controlled expressibility features**:
- The ability to invoke compaction.
- Access to a Python "ripple" so it can actually run programs.
- The ability to programmatically create sub-agents.
- Access to persistent state.
- Different feedback mechanisms.

Seth's framing: each of these is a distinct *capability*. If you remove any one of them from the harness, you are removing something the model is fundamentally incapable of replicating on its own — these are not conveniences, they are hard capability boundaries.

### Persistent Sub-Agents, Beyond the RLM Paper

Seth credits his co-author Alex's Recursive Language Model (RLM) paper as foundational, but describes what Prime Agent adds beyond it: sub-agents are modeled as **persistent subsessions**. A parent session spins up a new RLM sub-agent, the sub-agent runs some task, finishes, and reports back an end state to the parent. Critically, after finishing, the sub-agent doesn't disappear — it goes **idle** and continues occupying RAM. At any later point, the parent can send it a new message to resume work, and because it retains all its previously built-up context, no information has to be reconstructed or re-derived. To avoid unbounded RAM growth, idle sub-agents can also be **offloaded** into an inactive state and later reactivated by message, preserving the same persistent-session abstraction without the memory cost of keeping every sub-agent "hot."

### Continual Harness Concepts Carried Into Prime Agent

Seth references his own prior paper on **continual harness** — the idea of treating the *entire harness state itself* as something with CRUD applied to it, so that the agent can leverage its full prior history (a set of trajectories, each with actions and outcomes at each turn) to inform how the harness should evolve going forward. Concrete questions this raises for the agent: does the system prompt need to change? Should new skills be created? Where **skills** are again defined as a set of instructions or a program aimed at achieving a specific goal, and **memory** as long-term storage of important information, alongside sub-agent specifications retained persistently for later reuse if their built-up context is still valuable.

Seth is candid that models are "not perfect at this right now" — self-directed harness refinement is an emerging capability, not a solved one. The design goal is to build the harness so that it is *somewhat ahead* of what current models can natively do, so that using it generates reasoning traces that can then be fed back to bootstrap the next generation of models — i.e., the harness and the model co-evolve, with the harness temporarily "pulling" the model's effective capability forward.

### Cross-Agent Messaging

One of the earliest features Seth built into Prime Agent: the ability for any two agents to message each other directly within something like a "nuclear family" structure — parents, children, and siblings. The motivation was intensely personal and practical: Seth found himself constantly trying to manage many agents working on many different things simultaneously ("five billion different directions every day"), and realized it would be far more effective if those agents could share context and coordinate directly with each other rather than routing everything through him. This turned out to generalize well beyond personal use — it's also valuable for typical software engineering work and for long-horizon jobs generally.

### Long-Horizon Performance as a First-Class Design Goal

Seth explains that a major design consideration was **long-horizon performance**: the desire to launch jobs and *not* have to babysit the agent continuously, checking in only when convenient. He criticizes a common flaw in how models get compared in evaluations: if Model A is run for a shorter time/budget and appears to "stop working," while Model B is run longer and keeps improving, that's not a fair comparison — the two models weren't given the same fixed compute/time budget. Worse, stopping an eval too early can hide real performance differences that would only show up with more time.

Seth's preferred lens for long-horizon evaluation: look for the **practical plateau** — the point at which throwing additional test-time tokens at the problem yields only incremental gains. This framing motivates the experimental results that follow.

### ARC-AGI Results Walkthrough (Including the Missteps)

Seth walks through, in narrated step-by-step form, how the ARC-AGI benchmark numbers were actually obtained — including two mistakes along the way:

1. Initial motivation: earlier continual-harness experiments with "Gemini Pearl" (transcribed name) had already reached about **20%** on ARC-AGI, which the team considered a genuinely strong result for a general-purpose harness that wasn't even specifically structured for ARC-AGI.
2. To push further, Seth searched online for a strong existing system prompt rather than writing one from scratch, and found one from a community leaderboard called **"Prolong."** He took *only* their system prompt (discarding everything else about their setup) and dropped it directly into Prime Agent.
3. **First misstep:** the very first run hit **99.9%** — an obviously too-good-to-be-true result. On inspecting the logs, Seth discovered the system was effectively "cheating" (implied: exploiting some leakage or shortcut rather than genuinely solving the task).
4. **Fix:** Seth spent an additional day properly sandboxing the evaluation setup to eliminate that exploit.
5. **Second misstep-turned-real-result:** after fixing sandboxing, a run with "GPT Sol" (transcribed) reached **78%**, which Seth flagged as looking like a genuinely strong, legitimate result.
6. From there, the team ran a broader comparison across models and harnesses, using the same general Prime Agent system prompt ("use a world model to solve ARC-AGI 3; here are the actions you can take; you have a ripple, you can call sub-agents, you can use it programmatically...").
7. Reviewing the execution traces, Seth found the agent doing substantial legitimate reasoning work — repeatedly writing and running code to test hypotheses, analyzing images, and doing image-processing steps — all leveraging the Python ripple as a genuine reasoning workspace, not just a text-generation exercise.

**Final comparative numbers reported:**
- **GPT-Tero:** 25.7% (the speaker notes this looked especially good relative to results OpenAI itself had shown "the week before," reinforcing the talk's core thesis that harness choice matters enormously for evaluation outcomes; this run used the Responses API).
- **Terra:** run was not taken to completion, but results were already strong relative to comparisons.
- Results already exceeded "GPT Sol Extra High" at one comparison point.
- **Opus:** **95.5%**.

Seth also addresses a question people apparently kept asking him: did he try this with Claude Code as the harness? He did, but results were poor enough that rather than report a possibly-mistuned bad result, he deferred to Claude Code's own previously published numbers — and notes that others have since run similar configurations to Prime Agent's and obtained much better results with Claude Code. The broader observation: **popular, well-known harnesses do not necessarily perform well on ARC-AGI even when Prime Agent does**, underscoring that harness-model pairing matters, not just raw model quality.

**Cost as a dimension, not just accuracy.** With one harness referred to as "AIR agent," the team spent about **$5,000** very quickly without achieving comparable performance gains, and had to cut the run off. Seth is careful to note this isn't necessarily the ceiling of what that harness could do — but it illustrates that cost-to-performance ratio is a first-class metric, not an afterthought, and that being able to programmatically manipulate context (rather than paying to push everything through expensive LLM calls) is one of the main levers for controlling that cost.

### Other Benchmarks

- **Long-horizon evals** (referred to as "Oolong" and an unreleased "coding emulator bench," described as an alternative to existing "program bench" benchmarks): Prime Agent achieved roughly **parity or slight improvement** over other harnesses, tested across multiple models (comparisons included configurations like Claude Code with GLM 5.2, versus Opus 5 and 5.6 as the underlying model).
- **Emulator Bench** (a benchmark asking the agent to reproduce entire computer system emulators — the concrete example given is building a Game Boy Color emulator): Prime Agent's advantage here comes specifically from having ripple access under the RLM design, letting it run "out-of-experiment loop" designs — i.e., trying things out flexibly and iteratively before committing to a final submitted solution.
- **GPU kernel generation tasks:** roughly **at-par results** across "Sol" and "Kimiko" (transcribed model names) — one better, one worse — which Seth offers as evidence the system is not overfit to any single benchmark.

### Long-Horizon Auto-Research Experiments

**NanoGPT speedrun, scaled up.** The team gave the system 8× H200 GPUs for a full week to attempt a scaled-up version of the nanoGPT speedrun task. Seth is candid that the results were high-variance, and that because the task itself is inherently very hard, it's not possible to cleanly attribute any observed benefit specifically to the harness versus the underlying model. What *is* interpretable, though, is the qualitative *behavior* observed in the traces.

Using more recent models (deepseek-v4/"deep 6v4," GLM 5.3, and Kimi K3, per the transcript), Seth highlights a specific pattern the team found compelling: the agent performing **"out-of-loop" experiments** — running cheaper analyses on CPU (parameter sweeps, hyperparameter search, data analysis) specifically so it doesn't have to spend all of its time budget on expensive H200 experiments, since the actual GPU experiments consume the majority of wall-clock time. In other words, the agent learned to triage: do cheap exploratory work first, and reserve expensive compute for validated hypotheses. Seth frames this as exactly the kind of emergent behavior that should shape what expressibility features Prime Agent needs to support going forward — and notes that a system that's good at auto-research for itself should also be good at assisting a human researcher who is in the loop.

**7-day Factorio-style factorial run.** A separate long-horizon experiment streamed continuously for 7 days, using a total of **633 agents** across **23 million output tokens**, aimed at making steady technological progress up a "tech tree" over time. A key benefit observed: sub-agents could divide labor across the factory-building task — researching, building, gathering resources, and designing the next items needed — while the refinement/continual-harness machinery let the system leverage what happened earlier in the run to keep making progress later, without getting stuck, even very late into the multi-day run. Seth draws a comparison to "Gemini Plays Pokémon"-style long-horizon agent demonstrations as the closest prior reference point for this kind of experiment.

### Takeaways Seth Offers for Building Your Own Harness

- Think seriously about **agentic context management** (the layered L1/L2/L3 model discussed earlier).
- Think about **swarms** and dig further into **recursive language models**.
- Run **standardized evals** — Seth notes that all the results shown can be reproduced using Prime Intellect's open **verifiers** package.

He closes by thanking his collaborators.

## John's Talk: Open Jarvis (Personal, On-Device AI)

John introduces this as joint work with Ivanka Orion (co-lead author) at Stanford, advised by Christopher Ré and Azalia (Hazy Research).

### Motivation: The Problem with Cloud-Bound Personal AI

Personal AI assistants are everywhere, but current systems — John names **OpenClaw** and **Hermes agent** as examples — are built around daily writing, research, coding, and scheduling use cases, yet rely almost entirely on **cloud** LLMs for the actual intelligence behind nearly every query. John lists four costs of this architecture:

1. **Financial cost** — aggregated API spending can run into the thousands of dollars per year.
2. **Privacy cost** — some of the most personal user data gets sent to cloud LLMs, often without clear visibility into where that data ultimately goes.
3. **Ownership cost** — you are perpetually *renting* intelligence rather than *owning* it outright.
4. **Energy cost** — cloud inference consumes orders of magnitude more energy than running comparable queries locally on a laptop.

### Why Now: Local Models Are Closing the Gap

John's argument for why this is newly tractable: local models today lag frontier cloud models by only about **6 to 12 months**, and that gap keeps shrinking as consumer hardware accelerators improve. The concrete example given: **Qwen 3.8-27B** now performs roughly on par with **Claude 4.6 Opus** from back in August 2025, which was itself the state of the art at that time. He also points to very recent hardware developments — Apple's new Mac Mini, released the same week as this talk — as evidence of a "renewed focus" from both Apple and NVIDIA on building accelerators specifically aimed at personal/on-device inference use cases.

### The Central Research Question

Can the *core* of a personal AI stack — model inference, agent execution, memory, and learning, i.e., precisely the parts that are conventionally outsourced to the cloud — be run **entirely on-device**, while remaining competitive with cloud-only stacks? This question motivates **Open Jarvis**.

### The Five Primitives of a Personal AI Harness

To make this tractable, the Open Jarvis team tried to define the *simplest possible set of primitives* by which any harness or personal AI stack can be specified:

1. **User interfaces** — whatever surface(s) the user actually interacts with.
2. **Agentic logic** — the composable reasoning process: how different kinds of intelligence and tools get orchestrated together.
3. **Intelligence (the model itself)** — the specific LLM serving as the reasoning "engine." Concrete examples given: **Qwen**, **GPT-OSS**, **Gemma 3N**.
4. **Inference engine and hardware** — the actual serving stack that runs the chosen model. Examples given: **Ollama**, **llama.cpp**, **vLLM**, **SGLang** — running on hardware such as **Apple Silicon** or **NVIDIA** chips.
5. **Tools/memory and learning primitives** — tools and memory exposed through a standard protocol (**MCP**), plus mechanisms for the system to actually *improve over time*, whether via prompt-based optimization techniques (John names **"Japa"** and **DSPy**) or weight-based techniques (**GRPO**, **SFT**, **LoRA**).

### What Open Jarvis Looks Like in Practice

John describes trying to make Open Jarvis interoperate with interfaces people are already comfortable with:
- A **desktop app** experience similar to what users already expect, but which surfaces the dollar and energy savings gained by running locally.
- Support for **continuous/persistent agents** — cron-job-style agents that run standard routines day after day.
- The explicit goal is to make this feel "plug-and-play" with existing workflows, so that people's first hands-on experience with a *local* LLM feels as approachable and immediate as their first experience with ChatGPT or Claude did.

### Optimizing the Local Stack — Using Cloud Models to Tune It

The key optimization idea in Open Jarvis: rather than trying to get the LLM itself to do everything unassisted, the team built a simple, structured specification across the five primitives above, and ran a full **optimization loop** over that spec. This yielded not just cost reductions but also **latency reductions** and **quality improvements** across their test suite.

The particularly interesting design move: use a **cloud LLM** to automatically **diagnose and propose changes** to the local, on-device stack's configuration — i.e., a powerful cloud model looks at the current local setup, figures out what's wrong or suboptimal, and proposes improved configurations — while the actual **deployed inference** at run time still happens entirely on the cheap local stack. This lets you borrow the cloud model's superior diagnostic/design capability during a one-time (or periodic) optimization phase, without paying cloud-inference costs on every actual query once deployed.

**Empirical findings from this optimization loop:**
- Open Jarvis configurations that had been optimized by a cloud LLM significantly outperformed local stacks deployed "out of the box" without such tuning, because the optimization could tailor the harness to the specific quirks and strengths of whichever local model/workload combination was in use.
- Even with *today's* local models, Open Jarvis could rival cloud-only stacks across personal-AI use cases, general coding, and agentic tasks — though John is careful to note there remain many tasks where local-scale models still fall short; the gap is "surprisingly closing" month over month as local models get better distilled and hardware accelerators improve.
- Concretely, the optimized local stacks achieved roughly **800x lower cost** than cloud alternatives, along with a significant latency reduction.
- **Model choice for the optimizer didn't matter much** — whichever cloud model was used to run the optimization step (Opus 5 and GPT-5.6-Sol were found to work best, but Gemini, Kimi, and GLM family models were also usable) still yielded useful optimized local configurations, meaning the approach isn't fragile to a specific optimizer model.
- The full Open Jarvis harness was **cheaper to optimize** than alternative approaches that require more data or more LLM calls to reach comparable tuning quality.
- The team attributes this efficiency specifically to the five-primitive spec design: by getting the full space of LLM abstractions and optimization loop "out of the way," the cloud optimizer could focus purely and efficiently on tuning the local system as a whole, making the whole process fast and effective.

# QM: YC's Open-Source Agent Harness

## Speakers and Product Overview

Josh and Rean presented QM, YC's open-source agent harness built for internal use at YC. QM gives every employee at YC an "open claw-like" assistant that is fully customizable and accessible either in Slack or through a web UI. Each user operates within their own personal context — with its own sandboxed files and scheduled jobs (crons) — but QM also supports multiplayer use, such as collaborating with it inside a shared Slack channel.

The range of use cases at YC is broad: automations like email triage, legal and finance workflows, document editing, extracting data from YC's internal database, spinning up live internal web apps, and even helping plan events. The design goal is for QM to be a generally useful assistant across the many different tasks an employee might face day to day, rather than a narrow tool for one job.

## The Lineage of Internal Agent Projects

QM did not appear all at once — it's the product of a sequence of internal agent projects at YC, each built as the underlying models got more capable. The speakers walked through this history to explain why QM is architected the way it is.

### The "General Agent" (January 2025)

The first system, internally called the "general agent," was architecturally simple: a system prompt plus tools in a loop. It was one-size-fits-all — everyone at YC talked to the same instance. Despite this simplicity, it was surprisingly good at answering data questions. Notably, the *scope* of what this agent could do kept expanding as the underlying models improved, without the team needing to redesign the system — the same simple loop got more capable "for free" as models advanced. Over time they hooked it up to Slack, added cron jobs, and gave it more tools so it could handle more domains.

### VM-Based Coding Agents (June 2025)

By mid-2025, many YC engineers were using Claude Code and Codex, and the team realized these could be run inside virtual machines. They wired this up to a Slack tag, letting people trigger one-off code changes just by describing them in Slack — the bot would go off and make the change. This was configured to also run CI pipelines and spin up dev environments for testing. The effect was that someone who might never have made a code change in their life could describe a bug and have it fixed.

Alongside this, the team ran a feedback loop: they'd observe how the bot failed or went wrong, and then update the `agents.md` file present in the codebase at the time, so the system's guidance improved as usage was observed.

### OpenClaw (January 2026 internally, i.e., the present era described)

In January, a lot of YC partners started using OpenClaw. The key context here: YC partners are extremely busy — they run office hours, get large volumes of inbound email, and are constantly reading applications — so any tool giving them extra leverage is highly valuable. OpenClaw stood out because it was the first agent many of them used that had **its own computer**. This made it far more customizable than the prior agent paradigm, and it started to function almost like a personal assistant.

### The Hermes Fleet (April 2026 internally)

The natural next question was whether this experience could be given to *every* employee at YC — without literally buying everyone a Mac Mini. The team provisioned a fleet of 50+ "Hermes" agents running in VMs. These were valuable, but came with real costs: they required a lot of per-user configuration to get value from, and managing the fleet became a "whack-a-mole" problem — the team would have to SSH into individual instances to fix them one at a time. This operational pain motivated the design goals for the next system: capture the value people were getting from having a personalized, capable agent, while addressing the fleet-management downsides.

## Design Philosophy: "Unhobbling"

Rean framed QM's design around a trend: models are improving exponentially, and giving agents more capability produces increasingly impressive returns. OpenClaw's "own computer" step was one such capability boost, and it worked strikingly well. This led the team, starting around May 2026, to ask: how far can this be pushed by continuing to pull on that same thread?

They explicitly drew on the framing from the essay *Situational Awareness* (2024) and its idea of **"unhobbling"** — the notion that during the era when test-time compute and tool use were just emerging, models already contained more intelligence than the surrounding systems were letting them use. The implication: if you keep expanding the capabilities an agent is offered, rather than trying to make the model itself smarter, you can unlock large jumps in what the system can do.

### Pulling the "Brain" Out of the Sandbox

The first application of this philosophy in QM: instead of the agent having its own computer that it's also trapped inside (as with Hermes and OpenClaw), QM centralizes everything into Postgres. All agent conversations and sessions are stored centrally rather than living inside an individual VM.

This solves two problems from the earlier architecture:
- **Administrative unwieldiness**: even a few dozen individually-hosted agent computers became hard to manage; centralizing removes this.
- **Trapped context**: in the old model, all of a session's history and state lived inside that one sandboxed computer and wasn't accessible elsewhere. By centralizing into Postgres and exposing that data back to the agent, the agent can now see context aggregated across the whole system, not just its own isolated machine.

### Sandboxes as a Resource, Not a Home

With state moved out of the sandbox, the team could stop thinking of the sandbox as "where the agent lives" and instead treat it as **a resource the agent can dip into as needed**. This is a significant reframing: rather than the agent being permanently housed in one VM, sandboxes become interchangeable tools the agent reaches for when it needs compute, similar to how a person might reach for a particular machine only when a task calls for it.

### An Emergent Byproduct: A Large Eval Set

Because everything is centralized, the system naturally accumulates a large set of traces from real conversations people have had with the agent — effectively a growing eval set. In principle, this opens the door to an automated improvement loop where the system "hill climbs" on its own past failures.

In practice, results here have been mixed. When agents are dispatched en masse to fix bugs found via an LLM-as-judge process, the team observed a kind of **"main character syndrome"**: each agent only sees its own narrow slice of the system — "its piece of the elephant" — and makes fixes that look correct locally but don't account for the whole system. Because of this, keeping a human in the loop for this improvement process has remained important, even though the team is looking forward to eventually closing this loop fully autonomously.

## Wiring the Agent Into Company Resources

The second major design move was connecting the agent to as many of YC's internal resources as possible.

- YC already had an internal CLI that wired together many systems, so QM builds on that.
- For anything not already covered, QM allows arbitrary API keys to be added.
- To achieve parity with what a human employee could do on their own laptop, QM ingests device-code OAuth credentials into a keychain and refreshes them automatically — the goal being to imitate the experience of a person working at their own computer as closely as possible.

### Read vs. Write Access to the Database

Database access is kept **read-only by default**. Writes are allowed only through a **human-reviewed bulk upsert** process: the agent proposes a plan to edit the database, a person reviews it, and only after that review does the write actually happen.

One observed issue with this safeguard: over time, people have started "rubber-stamping" these review requests rather than scrutinizing them closely. Rean drew an analogy to early use of Claude Code — in the beginning, users tend to review every tool call very closely, but as trust builds, that scrutiny fades. The team is watching this dynamic closely over the coming months, since it represents a potential erosion of the safety mechanism they built in.

### Sandbox Selection Pushed to the Agent

By default, the agent uses whichever sandbox has been allocated to the user it's talking to, but in general there's a pool of environments the agent can converge on and even collaborate within. Critically, the *decision* of which sandbox to use is pushed into the agent itself rather than being hardcoded into the harness: if a task is a heavier dev workload, the agent can reach for a machine with more resources; for something simpler, it picks a lighter sandbox. Letting the agent make this choice, rather than the harness deciding for it, has been "a really powerful thing."

### Runtime/Provider Selection Pushed to the Agent

Similarly, the agent can choose which model provider it works with at runtime. This matters practically: certain providers will issue refusals for tasks like AI research or cybersecurity work (the speaker gave the example of running into this with "Fable"). By letting the agent control its own runtime, it can pop out to a different model when it hits this kind of refusal. The same flexibility lets it pop between different sandbox providers as needed.

## Keeping the Harness Thin

A recurring design principle across all of this: keep the harness itself as small as possible, and push decisions into the agent rather than encoding them as fixed harness logic. The team frames the *core* of QM as just three tools:

1. Execution in a remote sandbox
2. Reading and writing from object storage
3. Publishing internal apps (a simple git-backed system)

Beyond that core, there are other tools for things like memory and crons, but the team treats these as temporary patches over rough edges rather than part of the essential system. The explicit goal is to keep the harness as small as they can.

## Open Problems and Failure Modes

The team described QM as an attempt to build an "AGI-anticipating" harness — one designed for models more capable than what exists today — and, since that capability level isn't here yet, they've run into a number of concrete failure modes.

### Agents Give Up Too Early

Despite being placed in a highly capable environment with many tools available, agents frequently give up on tasks prematurely. Over roughly the past month, the team experimented with what they call a **"grind tool"**: setting explicit budgets on goals so the agent is not allowed to give up before a certain amount of wall-clock time (e.g., a couple of hours) or a certain token spend has been used. This produced noticeably better outputs — better research, better reports — for both research-style tasks and normal office work. The speakers noted this mirrors a similar technique that OpenAI and Anthropic have reportedly used to crack open problems in mathematics.

### Confusion About Multiplayer Context

Because QM operates in both single-player and multiplayer settings (e.g., a Slack channel with multiple people), the agent can get confused about exactly what situation it's in — even when the system prompt specifies this clearly. The speakers attribute this to artifacts of how the underlying models were trained. Their mitigation has been building **local affordances** — contextual cues embedded in the specific interaction — rather than relying solely on system-prompt instructions, and this has proven important.

### Lack of Social/Permission Awareness

Agents don't intuitively understand social context the way people do. The speakers illustrated this with an example: if Josh tells Rean a piece of information, Rean has an intuitive, well-developed mental model of where it is and isn't appropriate to share that information further. Recreating this instinct in an agent takes deliberate engineering work — privileged information can easily leak into contexts where it shouldn't be shared.

The practical consequence: how much sensitive information you can safely put into the agent's shared context is bounded by how good your underlying permission system is. YC happens to already have a fine-grained permissioning system built up over years of internal software, which QM can lean on — but the speakers noted that most organizations lack this, and building nuanced knowledge-sharing controls for an agent takes real engineering effort.

## Closing

QM is open source, and the speakers noted that coding agents are generally capable of standing it up on their own. They invited attendees to file issues if they run into problems, and mentioned that YC is hiring for people interested in this kind of work.

---

Source: [Why The Harness Matters More Than The Model | YC Paper Club](https://youtu.be/n9xKblqyQ28?si=WENk4fwvsTQH0wyq) — Y Combinator
