#!/usr/bin/env python3
"""Flag "AI style" patterns in a text deliverable and report its length.

Usage:
    python text_check.py FILE [--lang es|en|ca] [--target-words N] [--wpp 375]

FILE: .docx, .md, .txt, .tex, .html, or a source-code file (only its comments
are checked). --lang defaults to automatic detection (es/en/ca); other languages
get only the language-independent checks.

The checks come from research on how expert readers spot LLM text (Russell et al.
ACL 2025; Wikipedia "Signs of AI writing"; excess-vocabulary studies). A hit is a
prompt to reread and rewrite, not proof of anything; clusters matter more than
single hits. Run it, fix, re-run, then do the manual checklist in
references/writing-rules.md (structure, voice and specificity can't be checked
automatically).

Standard library only.
"""
import argparse
import os
import re
import statistics
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

VOCAB = {
    "en": [
        r"delv\w*", r"dive into", r"intricac\w*", r"intricate", r"tapestry", r"testament", r"underscor\w*",
        r"showcas\w*", r"pivotal", r"crucial", r"vital", r"paramount", r"vibrant", r"enduring", r"profound",
        r"multifaceted", r"nuanced", r"comprehensive", r"robust", r"seamless\w*", r"meticulous\w*",
        r"landscape", r"realm", r"journey", r"navigat\w*", r"foster\w*", r"enhanc\w*", r"leverag\w*",
        r"harness\w*", r"garner\w*", r"bolster\w*", r"embark\w*", r"unlock\w*", r"unleash\w*", r"elevat\w*",
        r"resonat\w*", r"align\w* with", r"interplay", r"a myriad of", r"plethora", r"notably",
        r"it is (important|worth|crucial) to note", r"it'?s (important|worth) noting",
        r"in today'?s (fast-paced |digital |modern )?world", r"plays? an? (crucial|vital|pivotal|key|significant) role",
        r"rich (history|heritage|tradition)", r"nestled", r"ever-evolving", r"game-changer", r"key takeaways?",
    ],
    "es": [
        r"adentr\w+", r"profundiz\w+ en", r"sumerg\w+ en", r"entramado", r"tapiz", r"crisol", r"testimonio d(e|el)",
        r"subray\w+", r"resalt\w+", r"pone(n)? de manifiesto", r"fundamental(es)?", r"crucial(es)?",
        r"vital(es)?", r"primordial(es)?", r"vibrantes?", r"intrincad\w+", r"multifac[eé]tic\w+",
        r"exhaustiv\w+", r"robust\w+", r"panorama", r"naveg\w+", r"foment\w+", r"potenci\w+", r"impuls\w+",
        r"abord\w+", r"desempeñ\w+ un papel", r"jug\w+ un papel", r"se erige(n)? como",
        r"se posiciona(n)? como", r"constituye(n)? un hito", r"marca(n|r)? un antes y un despu[eé]s",
        r"es (importante|fundamental|crucial) (destacar|señalar|mencionar|resaltar)", r"cabe (destacar|señalar|mencionar)",
        r"vale la pena (mencionar|destacar)", r"en el mundo (actual|de hoy)", r"hoy en d[ií]a m[aá]s que nunca",
        r"en un mundo cada vez m[aá]s", r"sin lugar a dudas?", r"un sinf[ií]n de", r"una amplia gama de",
        r"a lo largo de la historia",
    ],
    "ca": [
        r"endins\w+", r"aprofund\w+ en", r"teixit", r"testimoni d(e|el)", r"subratll\w+", r"ressalt\w+",
        r"fonamentals?", r"crucials?", r"vitals?", r"vibrants?", r"intricat\w*", r"polifac[eè]tic\w*",
        r"exhaustiu\w*", r"robust\w*", r"panorama", r"naveg\w+", r"foment\w+", r"potenci\w+", r"impuls\w+",
        r"abord\w+", r"jug\w+ un paper", r"s'erigeix(en)? com", r"constitueix(en)? una fita",
        r"marca(r|n)? un abans i un despr[eé]s", r"[eé]s (important|fonamental|crucial) (destacar|assenyalar|esmentar)",
        r"cal (destacar|assenyalar|esmentar)", r"val la pena (esmentar|destacar)", r"en el m[oó]n actual",
        r"avui dia m[eé]s que mai", r"sens dubte", r"una [aà]mplia gamma de", r"al llarg de la hist[oò]ria",
    ],
}

PATTERNS = {
    "en": {
        "negative parallelism": [r"\bnot only\b[^.]{0,80}\bbut( also)?\b", r"\b(it'?s|this is|is) not (just|only|merely)\b",
                                 r"\bisn'?t (just|only|merely)\b", r"\bit'?s not [^.,]{1,40}, it'?s\b"],
        "copula avoidance": [r"\b(serves?|stands?|acts?) as\b", r"\bboasts?\b", r"\bholds the distinction\b"],
        "significance tail": [r",\s+(highlighting|underscoring|showcasing|reflecting|emphasi[sz]ing|ensuring|"
                              r"contributing to|fostering|solidifying|cementing|marking|paving|setting the stage|"
                              r"symboli[sz]ing|demonstrating)\b"],
        "false range": [r"\bfrom [^,.]{2,30} to [^,.]{2,30}(, and| and everything)\b"],
        "generic opener": [r"^(in today'?s|throughout history|since the dawn|in an (ever|increasingly)|in the (modern|digital) (age|era|world))"],
        "summary closer": [r"^(in conclusion|in summary|to sum up|overall|ultimately|all in all)\b"],
        "rhetorical setup": [r"\bhere'?s the thing\b", r"\bbut what does this (really )?mean\?", r"\blet'?s (dive|delve|take a closer look)\b"],
    },
    "es": {
        "negative parallelism": [r"\bno solo\b[^.]{0,80}\bsino( tambi[eé]n| que)?\b", r"\bno solamente\b[^.]{0,80}\bsino\b",
                                 r"\bno es (solo|solamente|simplemente|únicamente)\b", r"\bno se trata (solo|solamente|únicamente) de\b"],
        "copula avoidance": [r"\bse erige(n)? como\b", r"\bse posiciona(n)? como\b", r"\bsirve(n)? como\b", r"\bse presenta(n)? como\b"],
        "significance tail": [r",\s+(destacando|subrayando|resaltando|reflejando|evidenciando|consolidando|marcando|"
                              r"sentando|contribuyendo|fomentando|demostrando|poniendo de manifiesto|simbolizando)\b"],
        "false range": [r"\bdesde [^,.]{2,30} hasta [^,.]{2,30}"],
        "generic opener": [r"^(en la actualidad|en el mundo actual|hoy en d[ií]a|desde tiempos inmemoriales|"
                           r"a lo largo de la historia|en un mundo cada vez|vivimos en)"],
        "summary closer": [r"^(en conclusi[oó]n|en resumen|en definitiva|para concluir|para finalizar|en s[ií]ntesis|a modo de conclusi[oó]n)\b"],
        "rhetorical setup": [r"¿(pero )?qu[eé] significa (esto|realmente)", r"\bveamos\b"],
    },
    "ca": {
        "negative parallelism": [r"\bno nom[eé]s\b[^.]{0,80}\bsin[oó]( tamb[eé]| que)?\b", r"\bno [eé]s (nom[eé]s|simplement|únicament)\b",
                                 r"\bno es tracta (nom[eé]s|únicament) de\b"],
        "copula avoidance": [r"\bs'erigeix(en)? com\b", r"\bserveix(en)? com\b", r"\bes presenta(n)? com\b"],
        "significance tail": [r",\s+(destacant|subratllant|ressaltant|reflectint|evidenciant|consolidant|marcant|"
                              r"contribuint|fomentant|demostrant|simbolitzant)\b"],
        "false range": [r"\bdes de [^,.]{2,30} fins a [^,.]{2,30}"],
        "generic opener": [r"^(en l'actualitat|en el m[oó]n actual|avui dia|des de temps immemorials|al llarg de la hist[oò]ria|vivim en)"],
        "summary closer": [r"^(en conclusi[oó]|en resum|en definitiva|per concloure|per acabar|en s[ií]ntesi)\b"],
        "rhetorical setup": [r"¿?per[oò] qu[eè] significa (aix[oò]|realment)"],
    },
}

MARKERS = {
    "en": [r"\bi think\b", r"\bi believe\b", r"\bprobably\b", r"\bmaybe\b", r"\bseems?\b", r"\bso\b", r"\bactually\b",
           r"\bin my (opinion|view)\b", r"\bbasically\b", r"\bkind of\b"],
    "es": [r"\bcreo\b", r"\bpienso\b", r"\bparece\b", r"\bquiz[aá]s?\b", r"\bprobablemente\b", r"\ben mi opini[oó]n\b",
           r"\bpor eso\b", r"\bo sea\b", r"\bla verdad\b", r"\bes decir\b", r"\bme parece\b", r"\bsupongo\b"],
    "ca": [r"\bcrec\b", r"\bpenso\b", r"\bsembla\b", r"\bpotser\b", r"\bprobablement\b", r"\bper aix[oò]\b",
           r"\bo sigui\b", r"\b[eé]s a dir\b", r"\bem sembla\b", r"\bla veritat\b"],
}

AI_MENTION = r"\b(chat ?gpt|claude|gemini|copilot|llm|openai|anthropic|inteligencia artificial|intel·lig[eè]ncia artificial|" \
             r"artificial intelligence|generated (by|with)|generado (por|con)|generat (per|amb)|as an ai|como (ia|modelo de lenguaje))\b"

STOP = {
    "es": {"el", "la", "los", "las", "que", "de", "y", "en", "es", "por", "con", "una", "para", "del", "se", "como", "pero", "más"},
    "en": {"the", "and", "of", "to", "is", "in", "that", "it", "for", "with", "as", "was", "on", "are", "this", "be"},
    "ca": {"el", "la", "els", "les", "que", "de", "i", "en", "és", "per", "amb", "una", "del", "es", "com", "però", "més", "dels"},
}

CODE_EXT = {".py", ".c", ".h", ".cpp", ".hpp", ".cc", ".java", ".js", ".ts", ".jsx", ".tsx", ".cs", ".go", ".rs",
            ".kt", ".swift", ".php", ".rb", ".r", ".m", ".sql", ".sh", ".scala", ".dart", ".lua", ".hs", ".vhd", ".vhdl", ".asm", ".s"}

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")


# ------------------------------------------------------------------ reading
def read_docx(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    paras, headings, bold_runs, list_paras = [], 0, 0, 0
    for p in root.iter(W + "p"):
        style = ""
        ppr = p.find(W + "pPr")
        if ppr is not None:
            ps = ppr.find(W + "pStyle")
            if ps is not None:
                style = ps.get(W + "val", "").lower()
            if ppr.find(W + "numPr") is not None:
                list_paras += 1
        text = "".join(t.text or "" for t in p.iter(W + "t"))
        is_heading = style.startswith(("heading", "ttulo", "titulo", "título", "title")) or re.match(r"(t[ií]tulo|heading)\s*\d", style)
        if is_heading and text.strip():
            headings += 1
            paras.append(("H", text))
            continue
        for r in p.iter(W + "r"):
            rpr = r.find(W + "rPr")
            t = "".join(x.text or "" for x in r.iter(W + "t"))
            if rpr is not None and rpr.find(W + "b") is not None and t.strip():
                b = rpr.find(W + "b")
                if b.get(W + "val", "true") not in ("0", "false"):
                    bold_runs += 1
        if text.strip():
            paras.append(("P", text))
    return paras, {"headings": headings, "bold": bold_runs, "lists": list_paras}


def read_markup(text, ext):
    if ext in (".html", ".htm"):
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>", "\n\n", text)
        text = re.sub(r"<[^>]+>", " ", text)
    stats = {"headings": 0, "bold": 0, "lists": 0}
    paras = []
    if ext == ".tex":
        text = re.sub(r"(?m)%.*$", "", text)
        stats["bold"] = len(re.findall(r"\\textbf\{", text))
        stats["lists"] = len(re.findall(r"\\item\b", text))
        for m in re.finditer(r"\\(sub)*section\*?\{([^}]*)\}", text):
            paras.append(("H", m.group(2)))
            stats["headings"] += 1
        text = re.sub(r"\\(sub)*section\*?\{[^}]*\}", "\n\n", text)
        text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{([^}]*)\})?", r" \3 ", text)
    stats["bold"] += len(re.findall(r"\*\*[^*\n]+\*\*|__[^_\n]+__", text))
    for block in re.split(r"\n\s*\n", text):
        lines = [l for l in block.strip().split("\n") if l.strip()]
        if not lines:
            continue
        for l in lines:
            if re.match(r"\s*([-*+•]|\d+[.)])\s+", l):
                stats["lists"] += 1
        if len(lines) == 1 and re.match(r"#{1,6}\s", lines[0]):
            stats["headings"] += 1
            paras.append(("H", lines[0].lstrip("# ").strip()))
            continue
        body = " ".join(re.sub(r"^\s*([-*+•]|\d+[.)]|#{1,6})\s+", "", l) for l in lines)
        body = re.sub(r"\*\*|__|`", "", body)
        paras.append(("P", body))
    return paras, stats


def read_code_comments(text, ext):
    comments = []
    if ext in (".py", ".sh", ".rb", ".r"):
        comments += re.findall(r"(?m)#(?!!)\s?(.*)$", text)
        comments += re.findall(r'(?s)"""(.*?)"""|\'\'\'(.*?)\'\'\'', text)
    elif ext in (".sql", ".lua", ".hs", ".vhd", ".vhdl"):
        comments += re.findall(r"(?m)--\s?(.*)$", text)
    elif ext == ".m":
        comments += re.findall(r"(?m)%\s?(.*)$", text)
    elif ext in (".asm", ".s"):
        comments += re.findall(r"(?m);\s?(.*)$", text)
    else:
        comments += re.findall(r"(?m)//\s?(.*)$", text)
        comments += re.findall(r"(?s)/\*(.*?)\*/", text)
    flat = []
    for c in comments:
        if isinstance(c, tuple):
            c = " ".join(x for x in c if x)
        c = re.sub(r"(?m)^\s*\*\s?", "", c).strip()
        if c:
            flat.append(("P", c))
    return flat, {"headings": 0, "bold": 0, "lists": 0}


# ------------------------------------------------------------------ analysis
def norm(s):
    return unicodedata.normalize("NFC", s)


def detect_lang(text):
    words = re.findall(r"[a-zà-ÿ·']+", text.lower())
    scores = {k: sum(1 for w in words if w in v) for k, v in STOP.items()}
    if re.search(r"\b(però|amb|dels|perquè|també|és)\b", text.lower()):
        scores["ca"] += 5
    return max(scores, key=scores.get) if any(scores.values()) else None


def sentences(text):
    parts = re.split(r"(?<=[.!?¿¡…])\s+(?=[A-ZÁÉÍÓÚÑÇÀÈÒ¿¡\"«(])", text)
    return [s for s in parts if len(s.split()) >= 3]


def cv(values):
    if len(values) < 3:
        return None
    m = statistics.mean(values)
    return statistics.pstdev(values) / m if m else None


def title_case(h):
    words = [w for w in re.findall(r"[A-Za-zÀ-ÿ]+", h) if len(w) > 3]
    return len(words) >= 3 and sum(w[0].isupper() for w in words[1:]) >= max(2, len(words[1:]) * 0.6)


def main():
    # Windows consoles default to cp1252; don't crash on accents or symbols.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--target-words", type=int, default=None)
    ap.add_argument("--wpp", type=int, default=375, help="words per page for the page estimate (A4, 12pt, 1.5 spacing ≈ 375)")
    ap.add_argument("--allow-ai-mentions", action="store_true", help="use only for AI_USAGE.md")
    a = ap.parse_args()

    ext = os.path.splitext(a.file)[1].lower()
    is_code = ext in CODE_EXT
    if ext in (".docx", ".docm", ".dotx"):
        paras, st = read_docx(a.file)
    else:
        with open(a.file, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        paras, st = read_code_comments(raw, ext) if is_code else read_markup(raw, ext)

    body = [norm(t) for k, t in paras if k == "P"]
    heads = [norm(t) for k, t in paras if k == "H"]
    text = "\n\n".join(body)
    words = len(re.findall(r"\w+(?:[-'’·]\w+)*", text))
    lang = a.lang or detect_lang(text)
    issues, notes = [], []

    def hit(sev, msg):
        (issues if sev == "!" else notes).append(msg)

    low = text.lower()
    # 1. vocabulary
    if lang in VOCAB:
        found = {}
        for pat in VOCAB[lang]:
            for m in re.finditer(r"(?<![\w])(?:" + pat + r")(?![\w])", low):
                found[m.group(0)] = found.get(m.group(0), 0) + 1
        total = sum(found.values())
        density = 1000 * total / max(words, 1)
        if found:
            listing = ", ".join(f"{k}×{v}" for k, v in sorted(found.items(), key=lambda x: -x[1]))
            sev = "!" if density > 6 or total >= 5 or any(v >= 3 for v in found.values()) else "i"
            hit(sev, f"AI-typical vocabulary: {total} hit(s), {density:.1f}/1000 words → {listing}")
    # 2. constructions
    if lang in PATTERNS:
        sent_list = sentences(text)
        for name, pats in PATTERNS[lang].items():
            if name in ("generic opener", "summary closer"):
                continue
            n = sum(len(re.findall(p, low, flags=re.M)) for p in pats)
            if n:
                hit("!" if n >= 2 or name in ("negative parallelism", "copula avoidance") else "i",
                    f"{name}: {n} occurrence(s)")
        if body:
            first = body[0].lower().strip()
            if any(re.search(p, first) for p in PATTERNS[lang]["generic opener"]):
                hit("!", f"generic opening: {body[0][:70]!r}")
            last = body[-1].lower().strip()
            if not is_code and any(re.search(p, last) for p in PATTERNS[lang]["summary closer"]):
                hit("!", f"formulaic closing paragraph: {body[-1][:70]!r}")
        # rule of three (X, Y and Z)
        conj = {"en": "and", "es": "y|e", "ca": "i"}[lang]
        triads = len(re.findall(r"\b[\wÀ-ÿ]+(?: [\wÀ-ÿ]+)?, [\wÀ-ÿ]+(?: [\wÀ-ÿ]+)?,? (?:" + conj + r") [\wÀ-ÿ]+", low))
        if triads and words:
            rate = 1000 * triads / words
            if rate > 4 and triads >= 3:
                hit("!", f"many three-item lists ('X, Y and Z'): {triads} ({rate:.1f}/1000 words) — use the real number of items")
        # markers
        if not is_code and words > 250:
            m = sum(len(re.findall(p, low)) for p in MARKERS[lang])
            if m == 0:
                hit("i", "no discourse/epistemic markers (e.g. 'creo que', 'parece', 'por eso'); student prose usually has a few")
        _ = sent_list
    # 3. AI mentions
    if not a.allow_ai_mentions and os.path.basename(a.file).upper() != "AI_USAGE.MD":
        m = re.findall(AI_MENTION, low)
        if m:
            hit("!", f"mentions of AI in the deliverable ({len(m)}): declare AI use only in AI_USAGE.md")
    # 3b. leftover generator metadata in Office files
    if ext in (".docx", ".docm", ".dotx", ".xlsx", ".pptx"):
        try:
            core = zipfile.ZipFile(a.file).read("docProps/core.xml").decode("utf-8", "replace").lower()
            if re.search(r"python-docx|python-pptx|openpyxl|steve canny|generated (by|using)|claude|chatgpt", core):
                hit("!", "document properties contain generator/library metadata — run scripts/clean_metadata.py "
                         "(only on files you created; keep a template's own properties)")
        except KeyError:
            pass
    # 4. formatting
    em = len(re.findall(r"(?<!^)(?<!\n)\s?—\s?", text))
    if em:
        hit("!" if em >= 3 else "i", f"em dashes used for asides: {em} — prefer commas or parentheses")
    if EMOJI.search(text + " ".join(heads)):
        hit("!", "emoji found")
    if not is_code:
        if st["bold"]:
            hit("!" if st["bold"] >= 3 else "i", f"bold in running text: {st['bold']} run(s)")
        if st["lists"] and words:
            hit("!" if st["lists"] > max(6, len(body) * 0.5) else "i", f"list items: {st['lists']} — arguments and explanations belong in prose")
        if st["headings"]:
            per_page = st["headings"] / max(words / a.wpp, 1)
            if per_page > 2:
                hit("!", f"{st['headings']} headings for ~{words / a.wpp:.1f} pages — too many for a student text of this size")
            if lang in ("es", "ca"):
                tc = [h for h in heads if title_case(h)]
                if tc:
                    hit("!", f"Title Case headings in {lang} (use sentence case): {tc[:3]}")
        # 5. rhythm
        sl = [len(s.split()) for s in sentences(text)]
        c = cv(sl)
        if c is not None and len(sl) >= 8:
            msg = f"sentence length: mean {statistics.mean(sl):.0f} words, variation {c:.2f}"
            hit("!" if c < 0.35 else "i", msg + (" — too uniform; mix short and long sentences" if c < 0.35 else ""))
        pl = [len(p.split()) for p in body if len(p.split()) > 15]
        c2 = cv(pl)
        if c2 is not None and len(pl) >= 4 and c2 < 0.25:
            hit("!", f"paragraph lengths very uniform (variation {c2:.2f}) — let length follow content")
        # 5b. density of specifics (names, figures, quotes): above the class when packed
        if words >= 80:
            names = set()
            for s in sentences(text):
                for w in re.findall(r"[\wÀ-ÿ’']+", s)[1:]:
                    if w[0].isupper() and len(w) > 2 and not w.isupper():
                        names.add(w.rstrip("’'s").rstrip("’'"))
            per100 = 100 * len(names) / words
            figures = len(re.findall(r"(?<![\w.,])\d[\d.,]*%?", text))
            # quoted titles of works ("Death of a Loyalist Soldier") are not quotes
            quotes = sum(1 for q in re.findall(r"[\"“«]([^\"”»]{12,}?)[\"”»]", text) if not title_case(q))
            hit("i", f"density: {len(names)} distinct names ({per100:.1f}/100 words), {figures} figure(s), {quotes} quote(s)")
            # thresholds ≈ 90th percentile of real pre-AI intro-course posts (history, art history, teacher education)
            if per100 > 7:
                hit("!", f"{per100:.1f} distinct names per 100 words — denser than a typical student; keep the reading's main "
                         "points and cut minor names (student-level.md §4)")
            if figures > max(3, words / 100):
                hit("!", f"{figures} figures/dates — more than a typical student uses; keep the ones the point needs")
            if quotes > max(2, words / 200):
                hit("!", f"{quotes} direct quotes — a typical student quotes once or twice in a short answer")
        # 6. length
        pages = words / a.wpp
        hit("i", f"length: {words} words ≈ {pages:.1f} pages at {a.wpp} words/page")
        if a.target_words:
            diff = (words - a.target_words) / a.target_words
            if abs(diff) > 0.10:
                hit("!", f"length is {diff:+.0%} off the target of {a.target_words} words")
    else:
        hit("i", f"checked {len(body)} comment(s), {words} words")

    print(f"TEXT CHECK  {a.file}  (lang: {lang or 'unknown'})")
    print("\nFIX (likely AI-style or out of budget):" if issues else "\nNo strong signals found.")
    for i in issues:
        print("  !", i)
    if notes:
        print("\nINFO (review, may be fine):")
        for n in notes:
            print("  ·", n)
    print("\nNext: the manual checklist in references/writing-rules.md (specificity, voice, structure).")


if __name__ == "__main__":
    main()
