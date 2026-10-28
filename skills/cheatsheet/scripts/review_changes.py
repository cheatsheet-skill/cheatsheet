#!/usr/bin/env python3
"""Show every change between the original starting material and the modified version,
so each change can be justified against a requirement or reverted.

Usage:
    python review_changes.py ORIGINAL MODIFIED [--context 3] [--max-lines 400]

ORIGINAL and MODIFIED can be two files or two folders (e.g. the snapshot made with
snapshot.py and the project folder).

What it reports:
  * text/code files: every change block (added / removed / changed lines) with a
    little context, tagged with hints that usually mean "unnecessary change":
      WHITESPACE-ONLY   only spaces/tabs/blank lines changed
      COMMENT-ONLY      only comment lines changed
      rename-like edit  a line with the same shape but different identifiers
      whitespace-only edit  a changed line that differs only in spacing
      LINE-ENDINGS / ENCODING / BOM / FINAL-NEWLINE  file-level format changes
  * .docx: paragraph-level diff (style + text), style-only changes, and which other
    parts changed (styles, headers/footers, page setup, document properties)
  * .xlsx: cell-level diff (value or formula) per sheet, sheet list changes,
    formatting-only changes
  * .pptx: per-slide text diff, slide count/layout changes
  * other binaries: changed / unchanged by hash
  * added and removed files

Standard library only.
"""
import argparse
import difflib
import hashlib
import io
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
             ".mypy_cache", ".pytest_cache", ".idea", ".vscode"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}

COMMENT_PREFIXES = {
    "#": {".py", ".sh", ".rb", ".r", ".pl", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".mk", "makefile", ".jl"},
    "//": {".c", ".h", ".cpp", ".hpp", ".cc", ".cs", ".java", ".js", ".ts", ".jsx", ".tsx", ".go", ".kt",
           ".swift", ".rs", ".scala", ".dart", ".php", ".v", ".sv"},
    "--": {".sql", ".hs", ".lua", ".vhd", ".vhdl", ".ada"},
    "%": {".m", ".tex", ".pro", ".erl"},
    ";": {".asm", ".s", ".lisp", ".clj", ".scm"},
    "'": {".vb", ".bas"},
}
BLOCK_COMMENT_START = ("/*", "*", "*/", '"""', "'''", "<!--", "{-", "(*")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


# ----------------------------------------------------------------- helpers
def sha(data):
    return hashlib.sha256(data).hexdigest()[:12]


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


def decode(data):
    """Return (text, encoding) or (None, None) for binary."""
    if b"\x00" in data[:8000]:
        return None, None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return None, None


def comment_prefixes_for(path):
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1] or name
    return [p for p, exts in COMMENT_PREFIXES.items() if ext in exts or name in exts]


def is_comment_line(line, prefixes):
    s = line.strip()
    if not s:
        return True
    if any(s.startswith(p) for p in prefixes):
        return True
    return s.startswith(BLOCK_COMMENT_START)


IDENT = re.compile(r"[A-Za-z_áéíóúñçàèòïüÁÉÍÓÚÑÇÀÈÒÏÜ][\wáéíóúñçàèòïüÁÉÍÓÚÑÇÀÈÒÏÜ]*")


def shape(line):
    return IDENT.sub("ID", re.sub(r"\s+", " ", line.strip()))


def classify_block(removed, added, prefixes):
    """Tags for one change block, plus per-line notes for lines that look unnecessary."""
    tags, notes = [], []
    if "".join(removed).split() == "".join(added).split():
        return ["WHITESPACE-ONLY"], notes
    if prefixes and all(is_comment_line(l, prefixes) for l in removed + added):
        tags.append("COMMENT-ONLY")
    # pair removed lines with added lines that are the same apart from whitespace or identifiers
    used = set()
    for r in removed:
        for j, a in enumerate(added):
            if j in used:
                continue
            if r.split() == a.split() and r != a:
                notes.append(f"whitespace-only edit: {a.strip()[:70]!r}")
                used.add(j)
                break
            if r.strip() != a.strip() and shape(r) == shape(a) and r.strip():
                notes.append(f"rename-like edit: {r.strip()[:50]!r} -> {a.strip()[:50]!r}")
                used.add(j)
                break
    if removed and len(notes) == len(removed) == len(added):
        tags.append("RENAME/WHITESPACE ONLY")
    return tags, notes


# ----------------------------------------------------------------- text files
def diff_text(rel, a_bytes, b_bytes, context, max_lines, out):
    a_text, a_enc = decode(a_bytes)
    b_text, b_enc = decode(b_bytes)
    if a_text is None or b_text is None:
        out.append(f"\n=== {rel}: binary file changed (hash {sha(a_bytes)} -> {sha(b_bytes)})")
        return 1
    file_tags = []
    if (b"\r\n" in a_bytes) != (b"\r\n" in b_bytes):
        file_tags.append("LINE-ENDINGS")
    if a_enc != b_enc and not {a_enc, b_enc} <= {"utf-8", "utf-8-sig"}:
        file_tags.append(f"ENCODING {a_enc}->{b_enc}")
    if a_bytes.startswith(b"\xef\xbb\xbf") != b_bytes.startswith(b"\xef\xbb\xbf"):
        file_tags.append("BOM")
    if a_bytes.endswith(b"\n") != b_bytes.endswith(b"\n"):
        file_tags.append("FINAL-NEWLINE")

    a_lines = a_text.replace("\r\n", "\n").split("\n")
    b_lines = b_text.replace("\r\n", "\n").split("\n")
    prefixes = comment_prefixes_for(rel)
    sm = difflib.SequenceMatcher(a=a_lines, b=b_lines, autojunk=False)
    blocks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    out.append(f"\n=== {rel}  ({len(blocks)} change block(s))" + (f"  [file: {', '.join(file_tags)}]" if file_tags else ""))
    printed = 0
    for n, (tag, i1, i2, j1, j2) in enumerate(blocks, 1):
        removed, added = a_lines[i1:i2], b_lines[j1:j2]
        tags, notes = classify_block(removed, added, prefixes)
        kind = {"insert": "added", "delete": "removed", "replace": "changed"}[tag]
        loc = f"original {i1+1}-{i2}" if i2 > i1 else f"after original line {i1}"
        out.append(f"--- block {n} ({kind}): {loc} -> modified {j1+1}-{j2}  (-{len(removed)} +{len(added)})"
                   + (f"  <{', '.join(tags)}>" if tags else ""))
        for note in notes:
            out.append(f"    ! {note}")
        if printed >= max_lines:
            continue
        body = [f"   {l}" for l in a_lines[max(0, i1 - context):i1]]
        body += [f" - {l}" for l in removed] + [f" + {l}" for l in added]
        body += [f"   {l}" for l in a_lines[i2:i2 + context]]
        out += body
        printed += len(body)
        if printed >= max_lines:
            out.append("   [... further blocks listed without content; use --max-lines to see more]")
    return len(blocks) + (1 if file_tags else 0)


# ----------------------------------------------------------------- docx
def docx_paragraphs(z):
    root = ET.fromstring(z.read("word/document.xml"))
    paras = []
    for p in root.iter(W + "p"):
        style = ""
        ppr = p.find(W + "pPr")
        if ppr is not None:
            ps = ppr.find(W + "pStyle")
            if ps is not None:
                style = ps.get(W + "val", "")
        texts, fmt = [], []
        for r in p.iter(W + "r"):
            t = "".join(x.text or "" for x in r.iter(W + "t"))
            texts.append(t)
            rpr = r.find(W + "rPr")
            if rpr is not None and t.strip():
                fmt.append(ET.tostring(rpr))
        paras.append((style, "".join(texts), sha(b"".join(fmt)) if fmt else ""))
    return paras


def diff_docx(rel, a_bytes, b_bytes, out):
    za, zb = zipfile.ZipFile(io.BytesIO(a_bytes)), zipfile.ZipFile(io.BytesIO(b_bytes))
    pa, pb = docx_paragraphs(za), docx_paragraphs(zb)
    out.append(f"\n=== {rel}  (Word document: {len(pa)} -> {len(pb)} paragraphs)")
    changes = 0
    ka = [f"[{s or 'Normal'}] {t}" for s, t, _ in pa]
    kb = [f"[{s or 'Normal'}] {t}" for s, t, _ in pb]
    sm = difflib.SequenceMatcher(a=ka, b=kb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                if pa[i][2] != pb[j][2] and pa[i][1].strip():
                    changes += 1
                    out.append(f"  ~ para {j+1}: RUN-FORMATTING changed (bold/italic/font/size): {pb[j][1][:80]!r}")
            continue
        changes += 1
        rem, add = pa[i1:i2], pb[j1:j2]
        if len(rem) == len(add) and all(r[1] == a[1] for r, a in zip(rem, add)):
            for (rs, rt, _), (as_, _, _) in zip(rem, add):
                out.append(f"  ~ STYLE-ONLY: {rs or 'Normal'} -> {as_ or 'Normal'}: {rt[:80]!r}")
            continue
        for s, t, _ in rem:
            out.append(f"  - [{s or 'Normal'}] {t}")
        for s, t, _ in add:
            out.append(f"  + [{s or 'Normal'}] {t}")
    # other parts
    names = sorted(set(za.namelist()) | set(zb.namelist()))
    watched = re.compile(r"word/(styles|numbering|settings|header\d*|footer\d*|theme/.*|fontTable)\.xml|docProps/core\.xml|docProps/app\.xml")
    for n in names:
        if not watched.fullmatch(n):
            continue
        a = za.read(n) if n in za.namelist() else None
        b = zb.read(n) if n in zb.namelist() else None
        if a != b:
            changes += 1
            label = {"word/styles.xml": "STYLES changed", "docProps/core.xml": "DOCUMENT PROPERTIES (author/title/dates) changed"}.get(n, f"{n} changed")
            out.append(f"  ! {label}")
    # page setup (sectPr)
    def sect(z):
        root = ET.fromstring(z.read("word/document.xml"))
        return [ET.tostring(s) for s in root.iter(W + "sectPr")]
    if sect(za) != sect(zb):
        changes += 1
        out.append("  ! PAGE SETUP (margins/size/orientation/columns) changed")
    if changes == 0:
        out.append("  (only internal metadata differs)")
    return changes


# ----------------------------------------------------------------- xlsx
def xlsx_cells(z):
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.iter(S + "si"):
            shared.append("".join(t.text or "" for t in si.iter(S + "t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    sheets = {}
    for sh in wb.iter(S + "sheet"):
        name = sh.get("name")
        target = rmap.get(sh.get(R_NS + "id"), "")
        path = target.lstrip("/") if target.startswith("/") else "xl/" + target
        cells = {}
        if path in z.namelist():
            root = ET.fromstring(z.read(path))
            for c in root.iter(S + "c"):
                ref = c.get("r")
                f = c.find(S + "f")
                v = c.find(S + "v")
                t = c.get("t")
                val = None
                if t == "s" and v is not None:
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(S + "t"))
                elif v is not None:
                    val = v.text
                formula = ("=" + (f.text or "")) if f is not None else None
                cells[ref] = (formula or val, c.get("s"))
        sheets[name] = cells
    return sheets


def diff_xlsx(rel, a_bytes, b_bytes, out, max_lines):
    za, zb = zipfile.ZipFile(io.BytesIO(a_bytes)), zipfile.ZipFile(io.BytesIO(b_bytes))
    sa, sb = xlsx_cells(za), xlsx_cells(zb)
    out.append(f"\n=== {rel}  (spreadsheet)")
    changes = 0
    if list(sa) != list(sb):
        changes += 1
        out.append(f"  ! SHEETS changed: {list(sa)} -> {list(sb)}")
    shown = 0
    for name in sb:
        a, b = sa.get(name, {}), sb[name]
        for ref in sorted(set(a) | set(b), key=lambda r: (int(re.sub(r"\D", "", r) or 0), r)):
            av, bv = a.get(ref, (None, None)), b.get(ref, (None, None))
            if av == bv:
                continue
            changes += 1
            if shown < max_lines:
                if av[0] == bv[0]:
                    out.append(f"  ~ {name}!{ref}: FORMAT-ONLY change")
                else:
                    out.append(f"  {name}!{ref}: {av[0]!r} -> {bv[0]!r}")
                shown += 1
    if shown >= max_lines:
        out.append("  [... truncated]")
    for n in ("xl/styles.xml",):
        if (za.read(n) if n in za.namelist() else None) != (zb.read(n) if n in zb.namelist() else None):
            changes += 1
            out.append("  ! STYLES (number formats, fonts, fills, borders) changed")
    charts_a = [n for n in za.namelist() if n.startswith("xl/charts/")]
    charts_b = [n for n in zb.namelist() if n.startswith("xl/charts/")]
    if charts_a != charts_b or any(za.read(n) != zb.read(n) for n in charts_a if n in charts_b):
        changes += 1
        out.append("  ! CHARTS changed/added")
    return changes


# ----------------------------------------------------------------- pptx
def pptx_slides(z):
    names = sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                   key=lambda n: int(re.findall(r"\d+", n)[-1]))
    slides = []
    for n in names:
        root = ET.fromstring(z.read(n))
        paras = []
        for p in root.iter(A + "p"):
            t = "".join(x.text or "" for x in p.iter(A + "t"))
            if t.strip():
                paras.append(t)
        rel = n.replace("slides/", "slides/_rels/") + ".rels"
        layout = ""
        if rel in z.namelist():
            for r in ET.fromstring(z.read(rel)):
                if r.get("Type", "").endswith("/slideLayout"):
                    layout = os.path.basename(r.get("Target", ""))
        slides.append((layout, paras, sha(z.read(n))))
    return slides


def diff_pptx(rel, a_bytes, b_bytes, out):
    za, zb = zipfile.ZipFile(io.BytesIO(a_bytes)), zipfile.ZipFile(io.BytesIO(b_bytes))
    sa, sb = pptx_slides(za), pptx_slides(zb)
    out.append(f"\n=== {rel}  (presentation: {len(sa)} -> {len(sb)} slides)")
    changes = 0
    for i in range(max(len(sa), len(sb))):
        a = sa[i] if i < len(sa) else None
        b = sb[i] if i < len(sb) else None
        if a == b:
            continue
        changes += 1
        if a is None:
            out.append(f"  + slide {i+1} added (layout {b[0]}): {' | '.join(b[1])[:160]}")
        elif b is None:
            out.append(f"  - slide {i+1} removed: {' | '.join(a[1])[:160]}")
        else:
            if a[0] != b[0]:
                out.append(f"  ! slide {i+1}: LAYOUT {a[0]} -> {b[0]}")
            if a[1] != b[1]:
                for line in difflib.unified_diff(a[1], b[1], lineterm="", n=0):
                    if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                        out.append(f"    slide {i+1}: {line}")
            elif a[0] == b[0]:
                out.append(f"  ~ slide {i+1}: FORMAT/POSITION-ONLY change (text identical)")
    for n in sorted(set(za.namelist()) | set(zb.namelist())):
        if n.startswith(("ppt/slideMasters/", "ppt/slideLayouts/", "ppt/theme/")) and n.endswith(".xml"):
            if (za.read(n) if n in za.namelist() else None) != (zb.read(n) if n in zb.namelist() else None):
                changes += 1
                out.append(f"  ! {n} changed (master/layout/theme)")
    return changes


# ----------------------------------------------------------------- driver
def compare_file(rel, a_path, b_path, args, out):
    a, b = read_bytes(a_path), read_bytes(b_path)
    if a == b:
        return 0
    ext = os.path.splitext(rel)[1].lower()
    try:
        if ext in (".docx", ".dotx", ".docm"):
            return diff_docx(rel, a, b, out)
        if ext in (".xlsx", ".xlsm", ".xltx"):
            return diff_xlsx(rel, a, b, out, args.max_lines)
        if ext in (".pptx", ".potx"):
            return diff_pptx(rel, a, b, out)
    except Exception as e:  # malformed or unusual file: fall back to hash
        out.append(f"\n=== {rel}: could not parse as {ext} ({e}); hash {sha(a)} -> {sha(b)}")
        return 1
    return diff_text(rel, a, b, args.context, args.max_lines, out)


def walk(root):
    files = {}
    for d, dirs, fs in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(fs):
            if f in SKIP_FILES:
                continue
            p = os.path.join(d, f)
            files[os.path.relpath(p, root)] = p
    return files


def main():
    # Windows consoles default to cp1252; don't crash on accents or symbols.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original")
    ap.add_argument("modified")
    ap.add_argument("--context", type=int, default=3, help="context lines around each hunk")
    ap.add_argument("--max-lines", type=int, default=400, help="max diff lines printed per file")
    args = ap.parse_args()

    out = []
    total = 0
    if os.path.isfile(args.original) and os.path.isfile(args.modified):
        total += compare_file(os.path.basename(args.modified), args.original, args.modified, args, out)
        added = removed = []
    elif os.path.isdir(args.original) and os.path.isdir(args.modified):
        fa, fb = walk(args.original), walk(args.modified)
        removed = sorted(set(fa) - set(fb))
        added = sorted(set(fb) - set(fa))
        for rel in sorted(set(fa) & set(fb)):
            total += compare_file(rel, fa[rel], fb[rel], args, out)
    else:
        sys.exit("Give two files or two folders.")

    print("CHANGE REVIEW  (original: %s  ->  modified: %s)" % (args.original, args.modified))
    if added:
        print("\nNEW FILES (each must be required by the statement):")
        for r in added:
            print("  +", r)
    if removed:
        print("\nDELETED FILES (almost never justified):")
        for r in removed:
            print("  -", r)
    print("\n".join(out) if out else "\nNo content changes in shared files.")
    print("\n" + "-" * 70)
    print(f"Summary: {total} change block(s) in existing files, {len(added)} new file(s), {len(removed)} deleted file(s).")
    print("For each block: name the requirement (R#/N#) it serves, or revert it.")
    print("Usually unnecessary: WHITESPACE-ONLY, COMMENT-ONLY, rename-like or whitespace-only edits,")
    print("STYLE-ONLY / FORMAT-ONLY / RUN-FORMATTING, and file-level LINE-ENDINGS/ENCODING/BOM/FINAL-NEWLINE.")


if __name__ == "__main__":
    main()
