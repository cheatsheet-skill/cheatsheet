# Activity types

Read only the section that matches the activity. If an activity mixes types (a program plus a memoria), read both sections.

## Contents
- Programming practicals
- Written work: essays, reports, memorias, short answers
- Maths, physics and other problem sets
- Spreadsheets and data analysis
- Presentations
- Diagrams (UML, ER, flowcharts, networks, circuits)
- Drawings, illustrations and design
- Projects (several deliverables)

---

## Programming practicals

1. Build and run the starter code as given, before changing anything. Record its output for the inputs the statement implies; that's your baseline.
2. Implement each R as a targeted edit (`minimal-change.md`), using only the toolbox (`student-level.md`).
3. Run again. Compare with the baseline and the expected behaviour in the statement (exact output format included). For performance tasks (parallelism, optimisation), check correctness first, then measure if the statement asks for measurements.
4. Keep any test scripts in your scratch space. Deliver only the files the statement asks for.
5. If the statement asks for a memoria/report about the code, see the written-work section and keep it consistent with the actual code (same function names, same measured numbers).
6. If the environment can't run the language, say so in the summary and in `AI_USAGE.md` ("no he podido ejecutarlo; pruébalo antes de entregar").

Don't commit to git unless the student asks. If they do, write a plain, short commit message in the course's language, with no AI attribution trailer.

## Written work: essays, reports, memorias, short answers

1. Base the content on the student's material (notes, readings, sources they gave you). If key sources are missing, ask in Step 2 or work from general knowledge **only** for well-established facts, and say so in the summary.
2. Plan in a few lines: the answer to the question, and the 3–6 concrete points/facts that support it, mapped to Rs. Allocate the length budget across them.
3. Write following `writing-rules.md` from the first sentence.
4. Format: the template if there is one (use the docx skill/tools to edit it); otherwise the format the statement asks for (.docx by default for "un Word"), with simple default styling: title, body text, page numbers if typical. Don't design a fancy layout.
5. Check length on the real output and run `text_check.py`.

**Lab reports with data.** Use only the student's data. Calculations and plots follow the course's methods. Discussion interprets *their* results, including errors and deviations; don't make the results look cleaner than they are.

## Maths, physics and other problem sets

1. Solve each problem with the methods in the notes. Check results independently (a second method, a quick computation, dimensional analysis).
2. Present the working at the level of detail the teacher's solved examples show.
3. Deliver in the format requested. If unspecified: a .docx (or PDF) with numbered problems and equations written with the editor's equation tool or LaTeX if the course uses LaTeX. Keep notation identical to the notes.
4. Short explanations in prose between steps, as a student would write them ("Como la función es continua en el intervalo, podemos aplicar…").

## Spreadsheets and data analysis

1. Work in the given workbook if there is one (`minimal-change.md`). Use the formulas the course uses, in the workbook's language.
2. Prefer formulas over pasted values where the task is about calculating, so the teacher can see the work.
3. Charts: the chart types and level of formatting from class; label axes and title in the activity's language.
4. Recalculate and open the file to confirm formulas evaluate without errors.

## Presentations

1. Use the template or the course's usual format. Few words per slide; the explanation is said, not written.
2. Speaker notes only if asked.
3. Slide count from the time given (about one per minute) or the statement.
4. Text on slides still follows `writing-rules.md` (no "Key takeaways" slides, no bold-label bullets, no emoji).

## Diagrams (UML, ER, flowcharts, networks, circuits)

1. Use the notation exactly as in the notes (UML version, Chen vs crow's foot, flowchart symbols, circuit symbols).
2. Produce it in the tool or format the course uses: a `.drawio` file (XML) if they use draw.io, PlantUML or Mermaid source if those are used, otherwise an SVG/PNG plus the editable source.
3. Include only the elements the statement requires. No extra classes, attributes, layers or annotations "for completeness".
4. Render and look at the result; check that labels are readable and nothing overlaps.

## Drawings, illustrations and design

1. Clarify the medium in Step 2 if it matters (hand drawing vs digital, tool, size, format). You can only produce digital output; if the course needs a hand drawing, say that the result is a reference the student will have to redraw, and mention it in `AI_USAGE.md`.
2. Produce vector work as SVG (or the requested format) via code, at the requested dimensions, with the colours/fonts/constraints in the brief.
3. Keep it at the level of the course: a first-year design exercise doesn't need a polished agency-style result.
4. Don't reproduce copyrighted characters, logos or artworks; if the brief asks for that, propose an original design that meets the learning goal.
5. Render and check the output visually.

## Projects (several deliverables)

1. Requirements list per deliverable; one shared level profile.
2. Build in the order the statement implies; keep names and numbers consistent across code, report and slides.
3. One `AI_USAGE.md` for the whole project, covering every deliverable.
