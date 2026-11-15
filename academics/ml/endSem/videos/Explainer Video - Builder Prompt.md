# Explainer Video: Builder Prompt

Copy everything inside the box below into a new AI session. Replace the three `<...>` paths first.

````text
You are building a narrated, 3Blue1Brown-style explainer video (Manim Community Edition + MiKTeX + Sarvam AI voice + ffmpeg) from ONE source document. Accuracy and complete coverage of the source matter more than fancy animation.

INPUT FILES
- Style guide (look, colours, motion, voice, Topic Sheet template): <PATH>\Explainer Video - Theme and Style.md
- Setup guide (tools, folder layout, voice script, render and join commands): <PATH>\Explainer Video - Setup Guide.md
- SOURCE document (the only content of the video): <PATH TO SOURCE .md>

HARD RULES
1. Read all three files completely before doing anything else, every line. Don't skim, don't stop at a length limit; read in parts if a file is long. Also open every image, figure or file the source links to.
2. The source is the single source of truth. Teach everything in it and nothing that contradicts it. Don't invent facts, numbers, examples or claims. Short bridging sentences are allowed, but anything not in the source (an extra example, an analogy, a correction) must be marked "[added]" in the script and listed for my approval.
3. Nothing from the source may be lost. Every heading, definition, formula, rule, step, list item, table row, worked example, figure, caveat and note becomes a numbered coverage item, and each one must appear in the video. Exclude something only if I say so.
4. Follow the style guide exactly: role colours, fonts, motion vocabulary, pacing, accuracy rules, don'ts. No π creatures, presenter, mascot, character, logo, or 3Blue1Brown intro or music.
5. Every number, plot and result on screen is computed in code and checked with an assert. Never type results by hand.
6. If the source looks wrong, unclear or contradicts itself, don't silently fix or guess. Ask me, then show the agreed correction visibly as the style guide says.
7. Ask before anything costly or hard to undo: installing software, sending text to Sarvam (it costs money), deleting files, committing to git.
8. Keep the API key secret. Read it from the .env file named in the setup guide. Never print it, write it into files, or ask me to paste it into chat.
9. Work so another session can continue at any time: keep <video folder>/PROGRESS.md up to date (see Phase 7).

PHASE 1: READ AND INVENTORY (no questions yet)
- Read the two guides and the whole source.
- Create the video folder as in the setup guide §4: pick a short lowercase slug from the topic and copy the source document into <slug>/source/.
- Write <slug>/COVERAGE.md: a numbered table of every coverage item in source order.
  Columns: ID | source location (heading / line) | type (definition, formula, example, figure, list, caveat, …) | exact content or a faithful summary | scene (fill in later) | status.
  Formulas are copied exactly, in LaTeX. Worked examples keep all their numbers. Lists keep every item.
- Write a short summary for me: what the source covers, how many coverage items, which parts are image-only or unclear, any errors you suspect, and a rough length estimate.

PHASE 2: ASK ME QUESTIONS (then stop and wait)
Ask one numbered list of questions, grouped by topic, each with your recommended default so I can reply "default" or just a number. Ask only what the files don't already answer. Cover at least:
  a. Audience and level (e.g. first-time students, exam revision, general public) and what they already know.
  b. Language: English, Hindi or both; and tone (calm teacher, friendly, energetic).
  c. Target length and whether to split into parts.
  d. Depth: teach everything in equal depth, or which parts get more time / exam focus.
  e. Anything to skip, merge or reorder; anything to emphasise.
  f. Examples: only the source's own, or may you add [added] examples where the source has none?
  g. Each suspected source error or unclear part, listed with its location: how should it be handled?
  h. Real images: does the topic need photos/figures, and do I have files I own or should you use public-domain ones?
  i. Sarvam speaker name (the exact name from my dashboard) and language code.
  j. Video folder slug and title; whether to include a title card, a recap screen, a short quiz at the end.
  k. Is the machine already set up (MiKTeX, uv project, theme.py, make_voice.py, voiced.py), or should you check and set it up?
  l. Anything else specific to this source that would change the video.
Then STOP. Don't continue until I answer. If my answers raise new doubts, ask a second short round. Record all my answers in <slug>/DECISIONS.md.

PHASE 3: ENVIRONMENT CHECK
- Follow the setup guide §0–§3 and §6. Run the check commands (`uv run manim checkhealth`, `latex --version`, `dvisvgm --version`, `ffmpeg -version`).
- If something is missing, tell me exactly what and the commands to install it, and wait for my OK before installing.
- Make sure theme.py, voiced.py and make_voice.py exist at the projects root exactly as in the guides.

PHASE 4: TOPIC SHEET AND SCENE PLAN (stop for approval)
- Fill <slug>/TOPIC_SHEET.md from the style guide §11 template: role colours (max 5), symbol colours, scene plan, numbers to verify, source mistakes.
- Map every coverage ID to a scene in COVERAGE.md. No ID may be left without a scene.
- Each scene plan row says: the main visual, which coverage IDs it teaches, its length, and the order of the video shape (hook → intuition → mechanism → formula → worked example → why it matters → recap).
- Show me the Topic Sheet and the coverage-to-scene map. STOP and wait for approval.

PHASE 5: SCRIPT (stop for approval)
- Write <slug>/script.json in the setup guide §4 format: scenes in order, short lines (one idea each), simple spoken language as the style guide §9 describes.
- Every coverage item is spoken or clearly shown. Formulas are read aloud in words the first time. Mark [added] lines.
- Also write <slug>/SCRIPT_REVIEW.md: the script as plain readable text per scene, with the coverage IDs each scene covers and the planned visual beside each line, plus the total character count and the Sarvam cost estimate from the setup guide.
- STOP and wait for my approval or edits.

PHASE 6: VOICE AND BUILD
- After approval, ask once more before sending text to Sarvam, giving the character count. Then run make_voice.py as the setup guide §5 shows, starting with one scene to check the voice before doing the rest.
- Build scenes one at a time, in order, as the setup guide §5 and §7 show (VoicedScene, say(...), shared theme.py, asserts).
- After each scene: render with -ql, make a contact sheet of frames (setup guide §7) and LOOK at it. Check for overlapping or cut-off text, objects outside the safe margin, wrong colours, numbers that don't match the asserts, and visuals out of sync with the voice. Fix before moving on.
- Update COVERAGE.md status to "done" for each item a finished scene teaches.
- Show me each finished scene's contact sheet and a one-line summary; continue unless I say stop.

PHASE 7: FINISH
- Final render with -qh, join and normalise loudness as the setup guide §8 shows.
- Go through the setup guide §9 "Done means" checklist item by item and report each one honestly (passed, failed, or not checked and why).
- Final report to me: where the video is, its length, the coverage table (every ID "done", or the reason it isn't), [added] content, source corrections, and anything left unverified.

PROGRESS.md (keep it current from Phase 1 onward)
- Current phase and the next step.
- Decisions made (or link to DECISIONS.md).
- Scenes: planned / scripted / voiced / built / checked.
- Open questions and known problems.
A new session must be able to read the guides, PROGRESS.md, DECISIONS.md, COVERAGE.md and TOPIC_SHEET.md and carry on without asking me what happened before.

START NOW with Phase 1. Your first message to me is the Phase 1 summary followed by the Phase 2 questions.
````

## Notes for you

- To pick up an unfinished video in a new session, use the same prompt and add one line at the end: `RESUME: read <slug>/PROGRESS.md and continue from the step it names.`
- The AI stops for your input four times: questions (Phase 2), Topic Sheet (Phase 4), script (Phase 5), and before spending Sarvam credit (Phase 6).
