# How to Master Graph Engineering — Study Notes

## Context: Why Graphs Are the Current Trend

Boris Cherny, the engineer who built Claude Code, described no longer prompting his AI directly — instead he "writes loops that prompt it for him" and steps away, running hundreds of agents overnight while he sleeps. Shortly after this idea spread, the same online circles moved on to a new buzzword: graphs. Senior engineers pushed back immediately, calling graphs "a decades-old idea wearing a new hoodie." That objection is actually correct — but it is good news, not a criticism. Graphs are a pattern that has run banks, airlines, and power grids for roughly 30 years without breaking down. What's new in this moment isn't the concept, it's that the tooling has finally become easy enough for anyone to use: modern graph tools let you drag boxes and arrows onto a canvas and the tool wires up the underlying code, so you design the plan rather than write it.

The course structure: four short lessons (what a graph is, the one pattern worth mastering, the stop rule, the human gate), followed by three complete graph builds — a deep research desk, an SEO content machine, and a go-to-market kit.

## Lesson 1: What a Graph Actually Is

A graph is simply a plan for your AI work, drawn out so you can see it — not code, not math. It's a picture of who does what and in what order, and drawing that picture honestly is described as 90% of the actual skill involved. The picture answers exactly two questions:

1. Which jobs need to happen at all?
2. Which job has to wait for which other job before it's allowed to start?

### The Three Core Vocabulary Words

**Job** — one discrete task you'd hand to a single assistant and walk away from (e.g., "research one competitor," "write one section of an article," "check one claim against one source"). The test: if it fits on one sticky note, it's a job; if it needs three sticky notes, it's actually three separate jobs.

**Arrow** — connects two jobs when one needs the result of the other before it can begin. An arrow carries exactly one meaning: *wait*. "This job cannot start until that job hands over its answer." Because arrows are where all the waiting in a system lives, the number of arrows you draw directly determines how much delay your system has — fewer arrows, less waiting.

**State** — a small set of running notes that travels along with the work: what's been found, what's been decided, what's still left to do. Picture a clipboard passed from worker to worker. Every job can read it and add to it, and this is how many workers stay coordinated without ever talking to each other directly. This is what elevates a graph above a simple checklist: a checklist just lists steps, but state means the work carries memory, so a job halfway through can use something discovered at the very top.

Jobs, arrows, state — that's the entire vocabulary of the trend. A box per job, an arrow per wait, a clipboard riding along collecting notes.

### The Homework: Hunting Fake Arrows

A practical 10-minute exercise: look at whatever AI system you already run and find every hidden "and then." For each one, ask honestly: does the next job actually need the previous job's result to do its work? An arrow is only real if something actually flows through it — otherwise it's a "lie you drew out of habit," and that lie costs real time on every run.

**Worked example:** "Summarize this file *and then* check my calendar." This looks like a natural sequence, but the calendar step doesn't need a single word of the summary. The two jobs never needed to wait for each other — the arrow between them is fake. Once you start looking, most real systems have two or three of these fake edges sitting in plain sight, adding pure delay for no benefit.

Most systems today are drawn as one straight line: job → arrow → job → arrow, each step politely waiting for the one before it. This works, but it's the slowest possible design, because one stuck job freezes everything downstream of it — like one stalled car creating a mile of brake lights. The entire point of building a graph is to cut the fake arrows so independent jobs can run at the same time. That single move — cutting fake arrows — accounts for most of the speed gain graphs offer.

## Lesson 2: The Diamond — The One Pattern That Pays for Itself

Across serious agent systems, one shape recurs constantly: work splits into pieces, several workers dig in parallel, something checks their output, and it all merges into one answer. Summarized as four moves: **split, work, check, merge**. Drawn out, this forms a diamond — narrow at the top (single starting point), wide in the middle (parallel work), narrow again at the bottom (merged single output). This one shape is claimed to cover roughly 90% of what people charge money to build.

### Minimal Example
Ask three workers to research the same company, each looking in a different place — one reads the website, one reads customer reviews, one reads recent news — then a fourth worker reads all three and writes an honest summary. That's a complete diamond you could sketch on a napkin.

### Real-World Case: Claude's Research Feature
This diamond runs in production inside Claude's research feature. A lead agent reads the user's question and plans the angles of attack; then a handful of worker agents (Anthropic spawns three to five at once) gather evidence in parallel, each in its own separate context window, deliberately blind to what the others are doing — they don't chat or compare notes, which avoids slowing each other down.

**Anthropic's published results** for this multi-agent diamond design, compared to a single hardworking agent on research tasks:
- **90% improvement** in research task performance — attributed to the shape of the work, not a smarter or bigger model.
- **Up to 90% reduction in time-to-answer**, since five workers digging simultaneously naturally finish in a fraction of the time one worker grinding through the same list alone would take.
- A secondary, quieter benefit: five workers approaching a question from five different angles give a range of views to weigh, instead of one agent confidently talking itself into a single answer.

### The Check Step Is Non-Negotiable

The check node — sitting in the bottom half of the diamond just before the merge — is the part beginners most often skip, and skipping it is described as "the exact part that decides whether your graph is any good at all."

**Supporting research:** A Google DeepMind paper titled *"Large Language Models Cannot Self-Correct Their Reasoning Yet"* tested strong models asked to grade and fix their own answers with no outside input. Scores did not improve — in several cases they got worse. The explanation given: the model evaluating the answer is the same "brain" that produced the mistake, so it waves its own error through with confidence.

**The rule:** Never let the same agent grade its own homework — it's "the single most confident wrong judge you will ever hire," and because it's free, it's especially tempting to trust anyway. Instead, hand the checking job to a separate worker whose sole purpose is to attack the answer, find its weakest claim, and try to break it privately before a reader can break it publicly. This mirrors how newsrooms have used a second set of eyes/editors for a century — the diamond simply bakes that editor into the machine.

**Caveat from Anthropic's own guidance:** Don't reach for a diamond when a single call would suffice. Start with the simplest approach that works, and only add parallel workers and checking steps once the task is genuinely big enough to justify them.

## Lesson 3: The Stop Rule — Protecting Your Budget

A loop is a job that keeps running until something tells it to stop — repetition is its whole nature. The trap that catches nearly every builder once: if you forget to specify when to stop, the loop simply doesn't stop. It keeps calling the model, spending money, and circling the same problem — often getting slightly worse with each pointless additional pass. People have woken up to very large bills from a single loop left running overnight with no defined exit — it felt clever at midnight and expensive at breakfast, even though the agent behaved exactly as instructed (to keep going indefinitely).

**Rule:** every loop gets a stop rule defined *before* you press run, not after something goes wrong.

### Three Kinds of Stop Rules (can be combined)

1. **A cap** — e.g., "try at most five times, then hand me whatever you have." Simple and a bit blunt, but guarantees the loop can never run forever even on a hard problem.
2. **A budget** — e.g., "spend at most this many dollars, or make at most this many calls, then stop and report." This converts an open-ended agent into a controlled, bounded line item.
3. **A bar** — a clear, predefined quality test; the moment the answer meets it, stop early rather than continuing to pay for marginal improvement past "good enough."

**Practical advice:** start small and cheap, watch one real run, then loosen the constraints. A suggested starting point: three tries and a $2 cap — described as teaching more in one evening than a week of reading. Pick at least one of the three rule types before running anything, ideally two. A loop with no stop rule at all is characterized as "a slow leak with your credit card taped to the bottom of it."

## Lesson 4: The Human Gate

A human gate is a deliberate pause point in the graph where the whole process stops and waits for the human's approval before proceeding — it effectively asks, "Do I have your yes before this goes into the real world?" and does nothing further until answered. Good graph tools support this natively: the run pauses, you review the output, you either approve it or send it back with a short correction note (e.g., "too aggressive, soften it"), and it resumes from that exact point. The rhythm is: **pause, review, resume** — costing roughly 30 seconds of attention.

**Don't over-gate.** Gating every single step just turns the automated system back into fully manual work, one nervous click at a time, defeating the purpose of building the graph at all. The rule given: gate only the steps that are irreversible — an email that actually sends, a post that actually publishes, a payment that actually clears. Everything reversible should run freely and fast. A cited failure mode: a fully automated system once sent a broken draft to a real client list because no gate existed before the send step — a single human gate would have caught it in seconds. The guiding principle: put the gate where the regret would live.

## Build 1: The Deep Research Desk

This diamond targets time-consuming deep research work. Example input: a single high-stakes, fuzzy question — *"Should we launch our product in Germany next quarter?"*

**Structure:**
- **Lead job (top of diamond):** breaks the one fuzzy question into five sharp sub-questions, the way a good analyst would before touching any source. In the example: market size, local competitors already established, applicable rules/taxes, what price the market will bear, and what could go wrong after committing.
- **Five parallel research workers (wide middle):** each owns exactly one sub-question and pulls real, cited sources for that slice only — no single worker tries to cover everything. This is where a two-day analyst task compresses into roughly four minutes of wall-clock time (framed as: what might take a junior analyst two full days here takes about the time to refill a coffee).
- **Skeptic worker (check step):** the node that separates a genuinely trustworthy tool from a toy — described as something you should never skip to save cost. Its sole job is to try to kill the findings: hunting for weak sources, stale numbers (e.g., three years old), and confident claims resting on nothing solid. Anything that survives this adversarial pass is something defensible in a real meeting; anything that dies there saves you from being confidently wrong in public.
- **Merge:** surviving findings are compiled into one clean brief, with every source placed directly next to the specific claim it supports — no unsupported assertions, and every line is quickly verifiable.
- **Human gate (bottom):** the finished brief waits for the human to read and approve it before anything is considered final.

**Example prompts used at each stage:**
- To the lead: "Split my question into five distinct research angles and nothing more."
- To the workers: "Answer only your assigned angle, cite every source you use, and do not guess. If you cannot find something solid, say clearly that you could not find it" — an honest gap is preferred over a smooth invented answer.
- To the skeptic: "Attack every claim in this brief, flag anything thin or outdated, and keep only what genuinely holds up under pressure."
- Final step: stop and wait for human approval before considering the work finished.

Net effect: a two-day research task becomes roughly a 20-minute review, at comparable depth but with more consistent thoroughness than a tired human under deadline pressure.

## Build 2: The SEO Content Machine

Same diamond shape, applied to turning one target keyword into a finished, publish-ready article.

**Input:** one keyword plus the search intent behind it. Example: someone typing "best CRM for small teams" isn't looking for a dictionary definition — they want a short, honest comparison ending in a clear recommendation. That underlying intent, not the literal keyword, is the real brief driving the work.

**Structure:**
- **Lead job:** builds the article outline and assigns each section to its own dedicated writer (introduction, each main point, conclusion), cleanly dividing the piece along its natural seams.
- **Parallel writers (wide middle):** each drafts one section simultaneously, so a task that would normally eat a full afternoon drafts in a single pass.
- **Editor (check step):** critically, this must be a *separate* agent from the writers — letting a writer approve its own work is exactly the mistake the self-correction research warns against. The editor checks facts, cuts filler, removes repetition, and unifies the voice so that sections written by multiple different workers read as one consistent human voice rather than an obvious committee effort.
- **Merge:** produces one formatted, ready article.
- **Human gate:** the human reviews the piece before it goes live, since it will carry their name, not the machine's.

**Prompt used:** "Outline the keyword, assign the sections to separate writers, then have a separate editor fact-check and unify the entire draft into one voice."

## Build 3: The Go-to-Market Kit

Described as feeling "like cheating" the first time you watch it run.

**Input:** a single short paragraph describing the product — what it is, who it's for, what it does.

**Structure:**
- **Parallel workers (wide middle), all running simultaneously rather than sequentially:** one drafts positioning (the core promise everything else must hang from), one writes launch emails, one writes the landing page, one writes ad angles, one writes social posts — five lanes on one clock, each producing a finished deliverable rather than a rough sketch.
- **Reviewer (check step):** unlike the other two builds, this check isn't primarily about grammar — it's about cross-piece *consistency*. It verifies all the pieces tell the same story rather than five workers each inventing a slightly different version of the product, and fixes any piece that has drifted off message (e.g., ensuring emails and landing page promise the exact same thing in the exact same voice).
- **Merge:** one folder of finished copy, all pointed at a single clear promise.
- **Human gate:** the human reviews and approves before anything ships, keeping the final voice authentically theirs rather than a robotic impression of them.

**Prompt used:** "From this product, write positioning, emails, a page, and ads — all in one unified voice."

Net effect: roughly a week of dreaded launch-writing work collapses into a single relaxed afternoon of editing.

## Three Common Beginner Mistakes

1. **Letting the writer check its own work to save a node.** As established by the DeepMind research, self-grading doesn't improve scores — it lets the model wave its own errors through with confidence.
2. **Building a well-designed graph with no stop rule and running it overnight.** The graph may work "perfectly" — it just works perfectly thousands of times in a row, and the bill the next morning reflects that.
3. **Gating every single step out of fear**, which just recreates doing the whole job manually one click at a time and erases the speed benefit of building the graph in the first place. The advice: gate only the send/publish/irreversible actions, and let everything reversible run freely.

## Closing Method Recap

- A graph consists of jobs, arrows, and state. A job is one task for one assistant; an arrow means "wait for this first"; state is the clipboard that travels with the work.
- Cutting fake arrows lets independent jobs run in parallel — this is the primary source of speed gained from switching to a graph.
- The diamond (split → work → check → merge) is the default shape for most tasks: split work into lanes, run lanes in parallel, check the result with a separate judge who did not produce the original answer, then merge into one output.
- Every loop needs an explicit stop rule — a cap, a budget, or a bar — so it can never run unchecked overnight.
- The human remains the final "yes" before anything reaches the real world.

**Suggested homework:** draw your current AI system as a straight line of jobs on paper, identify the two or three arrows where nothing actually flows between steps, cut them, and let those now-independent jobs run side by side — which constitutes designing and building a first real graph.

---

Source: [How to Master Graph Engineering (Full Course 25 minutes )](https://youtu.be/-90E2Pke9BQ?si=mta-DPqL5bQbZfgn) — Cloud AI
