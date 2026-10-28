# Working at the student's level

How to calibrate what you produce to the course, and how students actually do practicals, write reports and size their work.

## Contents
1. Building the level profile
2. Code: what student code looks like
3. Documents: how students write coursework
4. Maths and problem sets
5. Method and effort at student scale
6. Length defaults
7. When the material leaves the level unclear

---

## 1. Building the level profile

Sources, from most to least reliable:

1. **The teacher's own material**: starter code, solved examples, slides, notes, previous practicals, the statement's wording. What appears here is the allowed toolbox.
2. **The statement and rubric**: they often name tools ("usando pthreads", "con un bucle for"), forbid others, or imply the level ("sin usar librerías externas").
3. **Course and year** plus where the topic sits in the syllabus (a "Fundamentos de Programación" practical in week 5 vs a final-year "Sistemas Distribuidos" project).
4. Only then: general knowledge of what a typical student at that level knows.

Write the profile as a short list:

```
Course: 1º Ingeniería Informática, Programación I, tema 6 (vectores)
Language: C (gcc, C99 per Makefile). No external libraries.
Seen in material: for/while, if/else, functions, arrays, scanf/printf, #define.
Not seen: structs, pointers arithmetic, malloc, ternary operator, recursion.
Teacher style: snake_case in Spanish (num_alumnos), comments in Spanish with //,
  4-space indent, opening brace on same line, main() at the bottom.
```

**Toolbox rule.** Use only what is in the "seen" list or is unavoidably required by the statement. If you need something outside it, choose the most basic option that works and name it in the chat summary and `AI_USAGE.md` ("he usado X, que no aparece en los apuntes; compruébalo con tu profesor").

**Simplest-solution rule.** Between two correct solutions, pick the one a competent but non-expert student would write: more direct, fewer abstractions, more obvious control flow. Elegance is not a goal; clarity at the course level is.

## 2. Code: what student code looks like

Research on CS1 submissions vs ChatGPT code shows AI code is easy to tell apart mostly because it uses constructs students don't: ternary operators where students write nested `if/else` (Hoq et al., 2023, >90% classification accuracy; "write like a novice" prompts didn't remove it), helper functions and extra blank lines, longer identifiers (Idialu et al., *Whodunit*, MSR 2024). Students' own comments tend to be literal or sparse (Niazi et al., 2023).

So, unless the starter code or teacher's examples do these things, **don't**:

- use ternaries, comprehensions, lambdas, `map/filter/reduce`, streams, generators, decorators, f-strings/format tricks beyond what the course uses;
- add helper functions or classes for something used once;
- add type hints, docstrings, `if __name__ == "__main__":`, `argparse`, logging, constants modules, enums, config objects;
- add input validation, try/except, error codes, defensive checks for cases the statement doesn't mention;
- add tests, CLI flags, README files, build files;
- use advanced library calls when the course does it by hand (e.g. `sorted(..., key=...)` when the topic is writing a sort; `ThreadPoolExecutor` when the teacher uses `threading.Thread`; `std::accumulate` in a course using loops);
- use modern syntax the course's version or style doesn't (C++20 features in a C++11 course, `var` vs typed declarations, arrow functions in a course using `function`).

Do:

- mirror the teacher's naming language and convention (`contador`, `suma_total`, `numHilos`), including short names where they use them (`i`, `j`, `n`, `aux`, `tmp`);
- mirror indentation, brace style, blank-line rhythm, import order and output messages;
- use the control flow taught so far (counters, flags, nested ifs, while loops);
- print output in the format the statement shows, character by character if it gives an example;
- put new code where a student would: next to the code it changes, not in new files or modules unless asked.

**Parallelism / concurrency example (common practical).** Add the threads, the work split, the join and whatever synchronisation the shared data needs. Don't convert the program to a pool/executor framework, don't extract the work into new classes, don't add timing instrumentation unless the statement asks for speed-up measurements, and keep the original sequential structure recognisable around the change.

## 3. Documents: how students write coursework

- **Structure comes from the statement or the teacher.** If the statement lists points (1. Contexto, 2. Causas…), use those as the structure. If the teacher gave a template or a model memoria, follow its sections exactly. Otherwise, use the simplest structure that suits the genre: essays are continuous prose with a title; lab reports usually have objective, procedure/method, results, discussion/conclusions; short answers are numbered answers.
- **Depth is the course's depth.** Use the concepts, authors and data from the notes. A first-year history essay explains causes and consequences with a few concrete facts and a personal assessment; it doesn't do historiography.
- **Sources.** Students cite the course readings and a few accessible sources. Don't add a long bibliography. Never invent references; if the task needs sources you can't verify, ask for the readings or mark a placeholder.
- **Figures and tables** only where the statement or genre expects them (results tables in lab reports; a diagram if asked). Number and caption them the way the teacher does.
- **Front matter.** Use the template's cover/header if there is one. Fill student-specific fields (name, group) only with what they gave you; otherwise leave the template's placeholders and mention it.

## 4. Maths and problem sets

- Use the notation and methods from the notes (if the class does integration by parts, don't use a table method or a CAS result).
- Show the steps a student is expected to show at that level: enough to follow the reasoning, not every algebraic micro-step and not a skip straight to the answer.
- Round and present results as the examples do (decimals vs fractions, units, significant figures).
- If a computer check is useful, do it privately; don't put code in a handwritten-style answer unless the course does so.

## 5. Method and effort at student scale

The level profile says *which* tools are allowed; this section says *how much* of the work to do with them. A requirement can be met in a student way or in a researcher's way, and both look "correct" to the model. Pick the student way.

**Where the scale comes from.** In order: what the statement names (inputs, sizes, thread counts, number of runs, number of sources, "una gráfica"), then what the teacher's examples and previous practicals do, then the minimum that answers the requirement. A student does what the statement lists and stops; they don't add cases to make the conclusion stronger.

**Budget it in time.** Think of the time the teacher expects (a two-hour lab session, a week of evenings). A student runs their program by hand a handful of times, not dozens. As a rough rule, if one run or one batch of runs takes more than a couple of minutes, or the work needs a background job, you've left student scale, unless the statement's own input is that heavy.

**Experiments, measurements and benchmarks** (speed-up, performance, timing, simulations, lab-style measurements on code):

- Configurations: exactly the ones the statement lists (e.g. 1, 2, 4, 8 threads). If it lists none, 3–4 values that show the trend.
- Input: the statement's or the teacher's input/size. If none is given, one size big enough for the effect to show (a run of a few seconds), not a sweep of sizes or a collection of generated files.
- Repetitions: what the statement asks. Otherwise one run per configuration, or about 3 with a plain average if the course does that. No warm-up runs, interleaving, medians of many runs, standard deviations or confidence intervals unless asked or taught.
- Breakdown: total time only, unless the statement asks to time parts. No per-stage timings, profiling or hardware counters.
- Presentation: a small table with the numbers. A chart only if the statement asks for one or the teacher's examples have one, and then a single simple chart.
- Analysis: a few sentences that read the numbers the way the course explains them ("con 8 hilos no llega a 8 porque..."). If the results are noisy or odd, say so briefly and give the likely reason; don't rerun to make them look nicer.
- Tooling: time it the way the course does (`time` in the shell, the timer the teacher's code uses). Don't build benchmark harnesses, data generators or scripts that produce the tables, charts or report.

**Written work and research:** the readings the student gave you plus, if the statement asks for more, a few accessible sources (2–5 for a first- or second-year essay). One pass of planning and writing, then the review; not several full rewrites.

**Design, drawings, diagrams:** one proposal that meets the brief, unless the brief asks for alternatives. No mood boards, style explorations, multiple colourways or mockups in context unless asked.

**Spreadsheets and data:** the calculations and charts asked for, on the data given. No dashboards, extra pivot tables or sheets "for analysis".

**Maths and problem sets:** solve each problem once with the class method. A private cross-check is fine if it's quick; don't put alternative methods or generalisations in the answer.

**Your own checks are not part of the work.** Verifying that the code runs, recomputing a number or rendering a file is fine and should be quick. Don't let verification grow into extra experiments, and never let it leak into the deliverable as extra results.

## 6. Length defaults

Use these only when the statement and the teacher's examples give no length. They're intentionally on the short side: concise and complete beats long with filler. Adjust down for early years, up slightly for final-year work.

| Task | Typical student length |
|---|---|
| Short theory answer | 3–8 sentences (60–150 words) |
| Exercise sheet answer (theory) | one short paragraph per question |
| Reflection / opinion piece | 300–600 words |
| Essay (1st–2nd year) | 2–4 pages (≈ 800–1,600 words) |
| Essay (3rd–4th year) | 4–8 pages |
| Lab report / memoria de prácticas | 3–8 pages including figures; results and discussion are most of it |
| Code practical memoria (when asked) | 2–5 pages: what was done, design decisions, results, problems found |
| Presentation | 1 slide per minute of talk, ~8–12 slides for 10 min; few words per slide |
| Code comments | roughly matching the starter's density; otherwise a comment per non-obvious block |

**Pages ↔ words.** With no format given, assume A4, 12 pt, 1.5 line spacing (common in Spanish/Catalan universities): ~350–400 words per page of plain prose; ~500 with single spacing; ~250 double-spaced. If you produce a .docx, convert it to PDF (`soffice --headless --convert-to pdf`) and count real pages.

If a stated length seems short for the content, prioritise: answer every requirement briefly rather than some at length. If it's a maximum, stay under it.

## 7. When the material leaves the level unclear

- Ask in Step 2 if the choice would change the work substantially (e.g. "¿podéis usar la STL o lo hacéis con arrays?").
- If not worth asking, pick the more basic option and say so in the summary.
- Never "upgrade" the level, or the scale of the method, because the result would look more impressive.
