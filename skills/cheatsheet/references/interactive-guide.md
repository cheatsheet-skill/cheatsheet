# The interactive guide (only if the student asks for it)

One self-contained `.html` file that teaches what's needed for this activity and then solves it step by step, arriving at exactly the result that was delivered.

## Who it's for

Someone who knows nothing about the subject. Assume no prior vocabulary: define each term the first time it appears, with an everyday comparison where it helps. Written in the **student's language**; every name, value, heading and output quoted from the deliverable appears verbatim (same variable names, same section titles, same numbers).

## Length

Proportional to the activity. A small exercise gets a short guide (a few concepts, a handful of steps); a full project gets more. No filler sections ("Introducción a la importancia de…", "Conclusión final"). Every block should either teach something needed or move the solution forward.

## Structure

Start from `assets/guide-template.html` (copy it, then replace the placeholder content; the uppercase text and `FILL` comments mark what to replace). It already has the styles, light/dark theme, progress tracking and the interactive components. Its interface strings are in Spanish ("Lo he entendido", "Ver la respuesta", "Correcto.", "Copiar"…, including those inside the `<script>`): translate them and the `lang` attribute if the student writes in another language. Delete components you don't use. Sections:

1. **Qué vamos a hacer** — the activity in two or three plain sentences, and what the final result looks like.
2. **Lo que necesitas saber** — only the concepts the activity uses, in the order they're needed. Each concept: a short explanation, a minimal example, and (where useful) one check question.
3. **Paso a paso** — the solution as numbered, collapsible steps that mirror the actual work: same order, same names. For work on starter material, show the original fragment and the changed fragment side by side (or as a diff) and explain *why* that change answers the statement. Each step ends with what you should see or have at that point.
4. **El resultado** — the final output/document/figure matching the delivered one, and how to check it yourself (how to run it, what to look for).
5. **Para comprobar que lo has entendido** — 3–6 questions that a teacher could ask in a review or oral defence, with feedback that explains the answer.

## Interactivity that's useful, not decorative

Use the template's components:

- `details.step` — collapsible steps; "Lo he entendido" button marks progress.
- `.quiz` — multiple-choice check question with per-option feedback (explain why each wrong option is wrong).
- `.reveal` — "predict, then reveal": ask what a piece of code prints or what happens next, then show it.
- `.diff` — before/after fragments with added/removed lines highlighted.
- `dfn` with `title` — glossary terms with a tooltip definition.
- `.try` — a tiny live playground **only** for things the browser can run (JavaScript, simple calculators, sliders that change a parameter in a formula and show the result). For Python/C/Java, use `.reveal` with the real output you obtained when you ran the code; don't fake execution.

No animations for their own sake, no external images, no tracking. Must work offline: inline everything; no CDN dependencies.

## Consistency check before delivering

- Every name, number and output in the guide matches the delivered work (grep for them).
- The steps produce the delivered result, in the same order as the chat summary's list of changes.
- Open the file (or render it headlessly) and click through: steps open, quizzes respond, progress updates, no console errors.
- The guide follows `writing-rules.md` for tone (plain, specific, no puffery), although it can use headings and short lists because it's a teaching page.
