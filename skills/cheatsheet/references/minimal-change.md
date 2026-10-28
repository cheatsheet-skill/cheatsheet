# Minimal change protocol

When the student gives you starting material (code, a Word template, a spreadsheet, slides, a diagram, a design file), the delivered version must look like the teacher's material with the requested work added, and nothing else changed.

## Contents
1. Why models over-edit
2. The rule
3. Before editing
4. While editing, by material type
5. The diff review (mandatory)
6. Common unnecessary changes to revert

---

## 1. Why models over-edit

- Models optimise for a plausible, polished-looking result, not for the smallest diff; every inconsistency they notice becomes a task.
- Preference training rewards answers that look more thorough, so "improvements" feel helpful.
- Professional code in training data has a different style from course code, so the model's "natural" rewrite drifts toward it.
- Long agentic edits compound: one cosmetic change makes the next look necessary.

What works against it (and what this protocol encodes): an explicit list of what's in scope and what's out, the instruction to only make changes that are directly requested or clearly necessary, and a review gate on the actual diff before delivery. Instructions alone aren't enough; the diff check is what catches the rest.

## 2. The rule

Change only what a requirement (R) or a strictly necessary addition (N) needs. Everything else stays byte-for-byte the same where the format allows it: names, order, structure, formatting, comments, whitespace, line endings, encoding, styles, file names and folder layout. New content imitates the existing style even when you'd prefer another.

That includes the teacher's quirks and mistakes: a misspelled variable, an odd indentation, a typo in a comment. Leave them. If something in the starting material is actually a bug that blocks a requirement, fix only that and say so in the summary; if it's a bug that doesn't block anything, mention it in the summary and leave it.

## 3. Before editing

1. Snapshot: `python scripts/snapshot.py <project-or-file> <scratch>/original`.
2. Note the style you must imitate (naming, indentation, quotes, line endings, comment language, document styles).
3. Locate the exact places each R touches. Plan the edit as "insert here / change these lines", not "rewrite this function".

## 4. While editing, by material type

**Code**
- Edit in place with targeted replacements. Never regenerate a whole file from memory: it silently changes whitespace, comments and order.
- Keep line endings and encoding (check for CRLF before writing).
- Don't reformat (no auto-formatters, no import sorting, no trailing-whitespace cleanup).
- Don't move code between files or split files.
- New functions/variables use the existing naming convention and language.
- If the requirement is "add X" (parallelism, a menu option, a new query), the diff should read like a patch that adds X.

**Word documents / templates (.docx)**
- Modify the existing file; don't recreate the document from scratch. Fill placeholders and add content using the template's existing paragraph and character styles (Heading 1, Normal, the template's custom styles), not direct formatting.
- Keep page setup, headers/footers, cover page, numbering, fonts, table styles and fields unchanged.
- Don't touch the teacher's instructions text unless the template expects it to be replaced (e.g. "[Escribe aquí tu respuesta]").
- Keep document properties (author etc.) as they were.

**Spreadsheets (.xlsx/.ods)**
- Only fill or change the cells the task needs. Keep sheet names, order, formats, column widths, existing formulas, named ranges and charts.
- Use formulas the course uses (SUMA/SUM, SI/IF, BUSCARV/VLOOKUP…) in the sheet's language, not newer functions they haven't seen (XLOOKUP, LET, LAMBDA, dynamic arrays) unless taught.

**Slides (.pptx)**
- Use the existing layouts and master; add slides from the template's layouts. Don't restyle existing slides.

**Diagrams (draw.io, PlantUML, Mermaid, UML tools, SVG)**
- Keep existing elements' positions, ids, styles and naming; add the new elements in the same visual style.

**Design / drawings (SVG, images, Figma exports, CAD-like files)**
- Edit the given file; preserve layers, colours, fonts and dimensions; add only what's requested.

**Text documents (.md, .txt, .tex)**
- Same as code: targeted edits, same markup conventions, no reflowing of paragraphs you didn't change.

## 5. The diff review (mandatory)

Run:

```bash
python scripts/review_changes.py <scratch>/original <project-or-file>
```

It prints a unified diff for text/code files, and for .docx/.xlsx/.pptx a paragraph/style/cell/slide-level comparison. It flags hunks that are whitespace-only, comment-only or that look like renames.

For **every** hunk, write (mentally or in your scratch notes) which R or N it serves. If you can't name one, revert that hunk. Then re-run until every remaining hunk maps to a requirement. The chat summary should be able to list each change with its reason; if a change would be awkward to explain to the student ("I also renamed `aux` to `temporary_buffer`"), it shouldn't be there.

## 6. Common unnecessary changes to revert

- Renamed variables, functions, files, sheets, styles.
- Reordered functions, imports, includes, sections or slides.
- Reformatted code (spaces vs tabs, brace style, line wrapping, quotes).
- Rewritten or "improved" existing comments; translated comments.
- Added type hints, docstrings, `const`, `final`, access modifiers, `__main__` guards.
- Added error handling or validation around unchanged code.
- Replaced loops with library calls or vice versa in untouched code.
- "Fixed" typos or wording in the teacher's text.
- Changed fonts, sizes, spacing, colours or styles in templates.
- Updated dependencies, build files, versions, `.gitignore`.
- Deleted the teacher's commented-out code or TODO notes (unless a TODO is exactly what the task asks you to complete; then replace just that TODO).
