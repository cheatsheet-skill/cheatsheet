# Writing rules: sound like a real student, not a chatbot

Apply these to **every** piece of text you produce for the deliverable: essays, reports, lab write-ups (memorias), short answers, slide text, captions, spreadsheet notes and code comments.

## Contents
1. Where these rules come from
2. The goal (and what it is not)
3. Vocabulary
4. Sentence-level constructions
5. Paragraph and document structure
6. Formatting
7. Voice, stance and content
8. Natural variation instead of fake mistakes
9. Code comments and short answers
10. Final checklist

---

## 1. Where these rules come from

- **Russell, Karpinska & Iyyer (ACL 2025)**, *People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text*. Five readers who use LLMs heavily misclassified 1 of 300 articles by majority vote, even after paraphrasing and "humanising". Their explanations rely mostly on vocabulary (≈53%), sentence structure (≈36%), grammar/punctuation, originality, quotes, clarity, formatting, conclusions, formality, names and tone. Two findings matter a lot here: humans write more run-on and slightly ungrammatical sentences than AI does, and humans happily repeat plain words ("says") where AI cycles synonyms ("notes", "explains", "highlights").
- **Wikipedia: Signs of AI writing** (WikiProject AI Cleanup). A field guide built from thousands of cases: puffed-up significance, "serves as / stands as" instead of "is", superficial "-ing" analyses, negative parallelisms, rule of three, synonym cycling, "Challenges / Future prospects" sections, bold-label bullet lists, title case headings, emojis. It stresses that surface signs point to a deeper problem: generic content that could fit any topic.
- **Kobak et al. (2024/2025)** and **Juzek & Ward (COLING 2025)**: excess-vocabulary studies on millions of abstracts ("delve", "intricate", "underscore", "showcase", "pivotal"…), with evidence that preference tuning (RLHF) contributes.
- **Herbold et al. (2023)**, large comparison of student vs ChatGPT argumentative essays: ChatGPT uses fewer discourse and epistemic markers, more nominalisations and higher lexical diversity than students.
- **Format and length bias in reward models** (e.g. *From Lists to Emojis*, 2024; length-bias literature): preference models reward bold text, lists and length, which is why chat models over-format and pad.

## 2. The goal (and what it is not)

The goal is writing that reads like a capable student on this course wrote it: specific, grounded in the course material, with a voice, an appropriate level of polish and nothing generic. That is simply better writing, and the student must be able to stand behind every sentence.

It is **not** evasion. AI use is declared in `AI_USAGE.md`. Don't add deliberate spelling mistakes or fake errors (section 8 explains what to do instead), and don't pad with invented personal anecdotes.

## 3. Vocabulary

Avoid these unless the course material itself uses the word in its technical sense (e.g. "key" in databases, "landscape" in ecology). One occurrence in a long text is fine; clusters are the problem. Prefer the plain word a student would use.

**English** — delve, dive into, intricate, intricacies, tapestry, testament, underscore, highlight (as "shows"), showcase, pivotal, crucial, vital, paramount, vibrant, enduring, profound, multifaceted, nuanced, comprehensive, robust, seamless, meticulous, landscape (figurative), realm, journey, navigate (figurative), foster, enhance, leverage, harness, garner, bolster, embark, unlock, unleash, elevate, resonate, align with, interplay, a myriad of, plethora, notably, moreover, furthermore, additionally (as sentence openers, repeatedly), it is important/worth noting that, in today's (fast-paced/digital) world, plays a crucial/vital/pivotal role, serves as a testament, stands as, marks a turning point, rich (history/heritage), nestled, ever-evolving, game-changer, in conclusion / in summary / overall (as the start of the final paragraph).

**Español** — adentrarse, profundizar en (como muletilla), sumergirse en, entramado, tapiz, crisol, testimonio de, subrayar, resaltar, destacar (repetido), poner de manifiesto, fundamental, crucial, clave (como adjetivo comodín), vital, primordial, vibrante, intrincado, multifacético, exhaustivo, robusto, panorama, ámbito (repetido), navegar (figurado), fomentar, potenciar, impulsar, abordar (repetido), aprovechar, desempeña un papel crucial/fundamental, juega un papel clave, se erige como, se posiciona como, constituye un hito, marca un antes y un después, es importante destacar/señalar que, cabe destacar que, vale la pena mencionar, en el mundo actual, en la actualidad (como arranque), hoy en día más que nunca, en un mundo cada vez más…, sin lugar a dudas, en definitiva, en conclusión, en resumen (como arranque del último párrafo), no solo… sino también (repetido), un sinfín de, una amplia gama de, a lo largo de la historia (como arranque).

**Català** — endinsar-se, aprofundir en (com a crossa), teixit, testimoni de, subratllar, ressaltar, destacar (repetit), fonamental, crucial, clau (adjectiu comodí), vital, vibrant, intricat, polifacètic, exhaustiu, robust, panorama, àmbit (repetit), navegar (figurat), fomentar, potenciar, impulsar, abordar (repetit), juga un paper fonamental/clau, s'erigeix com, constitueix una fita, marca un abans i un després, és important destacar que, cal destacar que, val la pena esmentar, en el món actual, avui dia més que mai, sens dubte, en definitiva, en conclusió, en resum (com a inici del darrer paràgraf), no només… sinó també (repetit), una àmplia gamma de.

For other languages, apply the same idea: find the local equivalents of "crucial", "it is important to note", "plays a key role", "in conclusion", "not only… but also", and the inflated verbs (foster, enhance, underscore).

**Plain verbs win.** Use "is", "has", "shows", "uses", "says", "causes", "changed" rather than "serves as", "boasts", "underscores", "leverages", "marks a shift". Repeat a plain word rather than cycling synonyms: if the source "says", it can say three times.

## 4. Sentence-level constructions

| Pattern | AI version | Student version |
|---|---|---|
| Copula avoidance | "La Revolución Francesa **se erige como** un punto de inflexión…" | "La Revolución Francesa **fue** un cambio enorme para…" |
| Significance puffing | "…, **lo que subraya su importancia** en la historia europea." | Delete, or say concretely what changed. |
| "-ing"/gerund tail | "Napoleón reformó el código civil, **consolidando** así su poder **y sentando** las bases de…" | Split it: "Napoleón reformó el código civil. Con eso consiguió…" |
| Negative parallelism | "**No es solo** una reforma, **es** una revolución." / "It's not X, it's Y." | Say the claim directly. |
| Rule of three | "rápido, eficiente y escalable"; three examples every time | Use the number of items that actually exist: one, two, four. |
| False range | "**desde** la economía **hasta** la cultura" (unrelated items) | List what you mean, or pick the one that matters. |
| Synonym cycling | dice / señala / explica / destaca / subraya | dice / dice / comenta |
| Nominalisation | "**la realización de la implementación** del algoritmo" | "**implementar** el algoritmo" |
| Vague attribution | "Los expertos coinciden en que…" | Name the source from the course material, or drop the claim. |
| Rhetorical setup | "Pero, ¿qué significa esto realmente?" / "Here's the thing:" | Just state it. |

Also:
- **Vary sentence length on purpose.** Mix a short sentence with a long one that runs on a bit with a couple of commas. AI text tends to have uniformly medium sentences.
- **Punctuation.** Don't use em dashes (—) for asides in expository text; use commas or parentheses. (Spanish/Catalan dialogue rayas are fine when writing dialogue.) Use straight quotes or the language's normal quotes («» or "") consistently with the template.
- **Discourse and epistemic markers.** Students write "creo que", "parece que", "en mi opinión", "por eso", "o sea", "es decir", "la verdad es que" (register permitting); "I think", "probably", "so", "basically". Use a few. AI under-uses them.

## 5. Paragraph and document structure

- **Introduction.** Don't restate the prompt or open with a sweeping statement ("Desde tiempos inmemoriales…", "In today's world…"). Start with the specific topic, a concrete fact, a question from the statement, or what the work is going to do, in one or two sentences.
- **Conclusion.** Don't summarise every section, and don't end on an upbeat moral ("…demuestra que todo es posible", "a beacon of hope"). End with the actual answer to the question, a personal assessment, or a limitation. It's fine for a student conclusion to be short and a bit abrupt.
- **No template sections.** Don't add "Desafíos y perspectivas futuras", "Challenges", "Impacto en la sociedad", "Reflexión final" unless the statement or rubric asks for them.
- **Uneven on purpose.** Sections and paragraphs shouldn't all be the same length. Spend more words where the content is, fewer where it isn't.
- **Not every paragraph needs a topic sentence + mini-summary.** Let some paragraphs continue the previous one ("Esto se ve también en…").
- **Follow the requested structure**, not a generic report skeleton. If the statement lists questions, answer them in that order with their numbering.

## 6. Formatting

- **Headings** only if the document type uses them (reports, memorias, long works) or the template has them. A 2-page essay usually has a title and no section headings. In Spanish and Catalan, headings use sentence case ("Causas de la revolución", not "Causas De La Revolución").
- **Bold**: essentially never in running text. Never bold-label bullet lists ("**Ventaja 1:** …").
- **Bullet lists** only for genuinely list-like content (materials, steps of a procedure) or where the template/statement uses them. Arguments, explanations and analyses go in prose.
- No emojis, no horizontal rules between sections, no decorative quotes boxes.
- Match the template or the teacher's examples for fonts, spacing, numbering and citation style.

## 7. Voice, stance and content

This is the deepest layer, and the one that "humanising" tricks don't fix.

- **Be specific.** Use the concrete facts, dates, names, figures, terms and examples from the course material and sources the student gave you. Generic statements that would fit any topic are the strongest AI signal and the weakest writing.
- **Take a position** where the task asks for analysis or opinion. Don't automatically balance "on one hand… on the other" when the question has a reasonable answer.
- **Tone isn't uniformly positive.** Name problems, failures, uncertainty, the dark side of a historical event. AI text softens and drifts toward optimism.
- **First person** if the course genre allows it (many essays and reflective tasks do; formal lab reports often use impersonal forms — follow the teacher's examples).
- **Register of the level.** A first-year student doesn't write like a journal article. Prefer common vocabulary, technical terms only where the course uses them, and explanations that show understanding rather than polish.
- **Names.** Don't invent people, quotes or studies. If an example needs a name and none exists in the material, avoid the name. (Invented "Dr. Sarah Thompson / Emily Carter"-style names were one of the most reliable tells in the Russell study.)
- **Citations.** Only cite sources you actually have or can verify. Use the citation style the teacher uses.

## 8. Natural variation instead of fake mistakes

Real student text isn't perfect, but planted typos look planted and cost marks. Instead, allow the variation real writers have:

- occasional long sentence with several clauses; occasional very short one;
- starting a sentence with "Y", "Pero", "Así que" / "And", "But", "So" when it flows;
- parenthetical asides (like this one);
- a little repetition of key words;
- one idea per paragraph not being strictly enforced;
- slightly informal connectors, if the register and the teacher's examples allow it;
- contractions in English when the genre allows them.

Never introduce spelling errors, wrong facts or broken grammar on purpose.

## 9. Code comments and short answers

**Code comments** (see also `student-level.md`):
- Match the starter code: same language (often the student's language, not English), same comment symbol style, same density. If the starter has few comments, add few.
- Short and literal: `# creamos los hilos`, `// suma parcial de cada hilo`. Not `# Step 1: Initialize the thread pool for optimal concurrency`.
- No docstrings, headers or banners unless the teacher's code has them.
- Don't comment code you didn't write or change.
- Never comment about the AI, about "improvements", or about what you removed.

**Short answers / exercises:**
- Answer directly in the first sentence. Don't restate the question.
- Show the reasoning the teacher expects at this level (steps for maths, justification for theory), no more.
- No closing summary line.

## 10. Final checklist

Run `scripts/text_check.py` first, then go through this by reading the text yourself. Fix, then re-run.

- [ ] Length within budget (count it, don't estimate).
- [ ] No cluster of words from section 3; plain verbs used; no synonym cycling.
- [ ] No "serves as/se erige como", no significance tails, no "not only… but also / no es solo… es", no automatic triplets.
- [ ] Intro doesn't restate the prompt; conclusion doesn't summarise everything or end on a moral.
- [ ] No template sections the statement didn't ask for; structure follows the statement.
- [ ] No bold in running text, no bold-label bullets, no unnecessary headings, sentence-case headings in ES/CA, no emojis, no em-dash asides.
- [ ] Paragraph and sentence lengths vary; some discourse/epistemic markers present.
- [ ] Every paragraph contains something specific from the material (a fact, term, name, figure, example). Delete paragraphs that could fit any topic.
- [ ] Position taken where the task asks for one; tone not uniformly positive.
- [ ] Register matches the course year; technical terms are ones the course uses.
- [ ] No invented names, quotes, data, sources or experiences.
- [ ] Code comments match the starter's language, style and density.
- [ ] No mention of AI anywhere in the deliverable.
