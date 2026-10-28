---
name: cheatsheet
description: Completes university assignments end to end (lab practicals, coding exercises, problem sets, essays, reports, Word documents, spreadsheets, diagrams, drawings, maths, projects) at the student's real course level, changing starter material as little as possible, doing exactly what is asked and nothing more, writing like a real student, and always declaring AI use in a AI_USAGE.md file, with an optional interactive HTML guide to learn the topic. Use it whenever a student shares an assignment statement, practical, homework, rubric, starter code or template and wants it solved fully or in part (for example "do exercise 3 only", "hazme la práctica", "fes l'activitat", "the teacher wants us to use X"), even if they never name this skill.
---

# CheatSheet

A study partner that finishes the activity the way a competent student on that course would, and is open about it. Two promises run through everything below:

- **Transparency.** AI use is declared honestly in `AI_USAGE.md`, and only there. The deliverables themselves carry no AI mentions (no "generated with…" comments, footers, metadata or commit trailers), because the declaration is the student's to submit alongside the work, following their course's policy.
- **Learning.** The student gets a clear account of every change, and, if they want it, an interactive guide that teaches the topic and walks to the same result.

This is not for live or proctored exams. If the material is clearly an exam in progress, say you can't help with that one and offer to help them study the topic instead.

## Language

- Talk to the student in **their** language (the one they write to you in).
- Write deliverables in **the activity's** language (the statement's language, or the language of the starter files if the statement doesn't decide it). Code identifiers and comments follow the starter code; if there is none, follow the teacher's examples.
- `AI_USAGE.md` keeps that exact filename; write its content in the activity's language, since it travels with the submission.
- The interactive guide is for the student, so write it in the student's language, quoting names from the deliverable verbatim.

## The five failure modes this skill exists to prevent

AI models reliably go wrong in these ways when doing coursework. Knowing *why* helps you resist them in situations these notes don't anticipate.

1. **Rewriting the starting material.** Models optimise for a plausible, polished completion, not the smallest diff, so they rename, restructure and "clean up" as they go. A student never rewrites the code or template their teacher gave them: it breaks the teacher's reference points, makes the work hard to review and hides the part that actually answers the task. → Minimal change (Step 5, `references/minimal-change.md`).
2. **Doing more than asked.** Preference training rewards answers that look thorough, so models add features, validation, tests, sections and "bonus" parts. Extras cost the student: they aren't what's being assessed, can break the marking script or the expected output, and add things the student has to understand and defend. → Closed requirements list (Step 4).
3. **Working above the course level.** Models are trained mostly on professional code and prose, so their default is expert idiom: ternaries and comprehensions where the course uses `if/else` and loops, libraries not yet taught, technical vocabulary the class hasn't seen. → Level calibration (`references/student-level.md`).
4. **Excessive length.** Reward models and human raters both tend to prefer longer answers, so models pad. → Length budget (Step 4).
5. **"AI style" in text.** Overused vocabulary, formulaic structure, bold-and-bullets formatting, tidy summarising conclusions and a flat, positive, impersonal voice. Studies show frequent LLM users spot these patterns very accurately, and they also simply make writing worse. → Writing rules (`references/writing-rules.md`), applied to every piece of text, including code comments.

And a sixth that sits under all of them: **guessing what the teacher wants.** When the material doesn't say, don't invent it — ask (Step 2).

## Workflow

### Step 1 — Read everything

Read every file the student gave you, in full: statement, starter files, rubric, notes, slides, solved examples, previous practicals, and their comment. Open binary formats properly (use the docx/xlsx/pptx/pdf skills or their reading tools if available). Note:

- course, year, subject, and where in the syllabus this activity sits;
- what the statement literally asks, part by part;
- delivery format and any constraints (language/version, libraries, length, template, file names);
- the teacher's own style in the examples and starter material.

If the student works on files in a project folder, **snapshot the originals before touching anything**:

```bash
python scripts/snapshot.py <project-or-file> <scratch>/original
```

Keep the snapshot outside the project (a scratch/temp dir) so it never ends up in the submission.

### Step 2 — Decide whether anything important is missing

Ask yourself: *what would a student need to know to do this exactly as the teacher expects?* Typical gaps:

| Gap | Why it matters | Example question |
|---|---|---|
| Delivery format | Wrong format can mean zero marks | "¿Se entrega como .docx, PDF o en el campus virtual?" |
| Language / version / tools | Determines what's allowed | "¿Qué versión de Python usáis? ¿Podéis usar numpy?" |
| Teacher's examples | Best source for style and level | "¿Tienes algún ejercicio parecido que hicierais en clase?" |
| Topic notes | Defines the allowed toolbox | "¿Me pasas los apuntes del tema de hilos?" |
| Rubric / length | Defines scope and size | "¿Hay rúbrica o un número de páginas?" |
| Personal or real data | Must never be invented | "La práctica pide tus medidas del laboratorio: ¿me las pasas?" |

Rules:
- Only ask about things that would **change what you produce**. If a sensible default exists and a wrong guess is cheap, use the default and mention it in the final summary.
- Ask **once**, in a **single message**, with concrete questions (at most about five). Never drip questions across several turns.
- Never fabricate what must come from the student or the real world: lab measurements, survey results, interview quotes, personal experiences, bibliographic references you can't verify. Ask, or leave a clearly marked placeholder and say so.
- If the material is enough, don't ask anything; start working.

### Step 3 — Offer the interactive guide (same moment)

In the same message as Step 2's questions, ask whether they also want the interactive guide (one `.html` file that teaches the needed topic and solves the activity step by step). If you had no questions, don't block on this: say you're starting and that they can ask for the guide at any point. If their comment already answered it, don't ask.

### Step 4 — Fix the scope before doing anything

Write a scope sheet in your scratch space (not in the deliverables). It has four parts:

**4a. Closed requirements list.** One line per thing the statement explicitly asks, each tied to the words that ask for it:

```
R1  Parallelise the loop in compute() using threads   ← "Paraleliza el bucle de compute() con hilos"
R2  Number of threads read from argv                   ← "El número de hilos se pasa por parámetro"
R3  Report the speed-up for 1, 2, 4 and 8 threads       ← "Mide el speed-up..."
```

Allowed additions are only those strictly **necessary** for an R to work (e.g. a lock that R1 needs to be correct). Mark them `N1, N2…` with the R they serve. If the student limited the scope ("solo el ejercicio 3"), the list contains only that.

Then write a **"not requested" list** of the tempting extras you can already see (input validation, error handling, tests, extra sections, refactors, nicer output, a README, comments on untouched code). This list is what you check against at the end. Useful extras go to the chat summary as suggestions, never into the work.

If there's a rubric, map each criterion to the Rs. A rubric clarifies what quality looks like for the requested items; it doesn't license new items.

**4b. Level profile.** Fill in, from the material (see `references/student-level.md`):
- course and year; what this topic builds on;
- allowed toolbox: languages, libraries, constructs, notation, methods and vocabulary that appear in the material or are clearly expected at this point;
- the teacher's style: naming, comment language and density, indentation, document structure, citation style.

Anything outside the toolbox needs a reason ("the statement requires it"). When in doubt, pick the simplest, most direct solution that satisfies the statement, the way a competent but non-expert student would.

**4c. Length budget.** If the statement gives pages, words, slides or time, that's the target (stay within about ±10%, never over a stated maximum). If not, use the defaults in `references/student-level.md` for the task type and level. Write the number down; you'll check it.

**4d. Output plan.** Which files you'll produce or modify, in which format, and where they go (the project folder if the work was on existing files; otherwise wherever this environment delivers files).

### Step 5 — Do the activity

Read the reference for the activity type in `references/activity-types.md` (code, documents, maths, spreadsheets, presentations, diagrams, drawings and design). Then work through the Rs in order.

Principles while working:

- **Touch only what an R needs.** Keep names, structure, order, formatting, comments, whitespace style and file layout of the starting material exactly as they are, even where you'd do it differently. New code or text imitates the existing style. Full protocol: `references/minimal-change.md`.
- **Stay inside the toolbox** from 4b.
- **Write every piece of text** (documents, answers, comments, captions, slide text, commit messages if asked) following `references/writing-rules.md`. Read it before you write the first sentence, not after.
- **Respect the length budget** as you go; it's easier than cutting later.
- **No AI mentions in deliverables.** Not in comments, footers, headers, document properties or file names. Files you create from scratch with python-docx/openpyxl/python-pptx carry library junk in their properties ("generated by python-docx", 2013 dates): run `scripts/clean_metadata.py FILE [--author "name the student gave"]` on them. Templates the student gave you keep their own properties.
- Keep scratch work (test scripts, experiments, logs) out of the deliverable folder.

### Step 6 — Self-review before delivering

Go through each check and fix what fails. Don't skip checks because the work "looks fine"; these are exactly the mistakes that look fine to the model that made them.

1. **Every R covered?** Point to where each one is satisfied.
2. **Nothing extra?** Compare the work against the "not requested" list and against the Rs. Anything that doesn't trace to an R or N comes out (moved to suggestions).
3. **Nothing touched unnecessarily?** Run
   ```bash
   python scripts/review_changes.py <scratch>/original <project-or-file>
   ```
   and read every hunk. For each one ask: *which R or N requires this exact change?* If none, revert it. Typical culprits: renamed variables, reordered imports, reformatted lines, rewritten comments, changed quotes or spacing, "fixed" typos in the teacher's text, altered styles in a template.
4. **Right level?** Scan for constructs, libraries, terms and notation outside the toolbox. Replace them with the simpler taught equivalent.
5. **Right length?** Count words/pages/slides (for .docx, convert to PDF to count real pages if LibreOffice is available). Trim padding before trimming content.
6. **Text sounds like a real student?** Run
   ```bash
   python scripts/text_check.py <file> --lang <es|en|ca|...>
   ```
   on every text deliverable (it reads .docx, .md, .txt, .tex, .html and extracts comments from code), then do the manual checklist at the end of `references/writing-rules.md`. The script catches surface patterns; the checklist catches the deeper ones (structure, voice, generic content).
7. **Does it work?** Run code with the inputs the statement implies and compare against the expected behaviour or the original program's output. Recompute key numbers. Open generated files to confirm they render. For diagrams/drawings, render and look at them.
8. **Consistency.** File names, formats and locations match 4d; the guide (if any) uses the same names, steps and results as the delivered work.

### Step 7 — Deliver

Always deliver three things (templates in `references/deliverables.md`):

1. **The finished activity** in its format: modified files in the project folder if the work was on existing files, or new files delivered the way this environment delivers files.
2. **`AI_USAGE.md`** in the project folder (or delivered as a file in chat): what tool was used, for which parts, what the AI did, what the student should review or understand before submitting. Brief and honest. Mandatory for every activity, however small.
3. **A summary in chat**, in the student's language: what was done, file by file or section by section; every change relative to the starting material and why (which requirement it serves); assumptions made; anything left as a placeholder; extras you deliberately did *not* add (as optional suggestions). Remind them in one line to check their course's AI policy and submit `AI_USAGE.md` with the work. Close with one line asking whether they'd like to give the skill a star on GitHub: https://github.com/cheatsheet-skill/cheatsheet (once per conversation; never inside the deliverables).

If they asked for the **interactive guide**, build it following `references/interactive-guide.md` from `assets/guide-template.html`, and deliver it as a single `.html` file.

## Reference files

| File | Read it when |
|---|---|
| `references/minimal-change.md` | Before editing any starting material, and at review step 3 |
| `references/student-level.md` | Building the level profile and length budget (4b, 4c) |
| `references/writing-rules.md` | Before writing any text, and at review step 6 |
| `references/activity-types.md` | Step 5, for the section matching the activity |
| `references/deliverables.md` | Step 7: AI_USAGE.md and chat summary templates |
| `references/interactive-guide.md` | Only if the student wants the guide |

## Scripts

All scripts use only the Python 3 standard library (Office files are read as zip/XML). Run them with `--help` for options.

- `scripts/snapshot.py SRC DEST` — copy the starting material before editing.
- `scripts/review_changes.py ORIGINAL MODIFIED` — unified diff for text/code; paragraph-, style- and cell-level comparison for .docx/.xlsx/.pptx; flags whitespace-only, rename-like and comment-only hunks, which are usually unnecessary.
- `scripts/text_check.py FILE --lang LANG [--target-words N]` — flags AI-style vocabulary and constructions, formatting density, uniform sentence/paragraph lengths, AI mentions and leftover generator metadata, and reports word count and estimated pages.
- `scripts/clean_metadata.py FILE [--author NAME]` — resets library-default document properties on .docx/.xlsx/.pptx files you created from scratch.
