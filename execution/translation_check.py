#!/usr/bin/env python3
"""Angelina's pre-handoff check on a translation (sops/angelina-sop.md step 5).

Compares an approved English source with its translation (text, markdown or JSON). Fails on:
numbers, prices, dates, URLs, emails, phone numbers or {{merge fields}} that changed or went missing;
footer, unsubscribe or signature lines from config/footer.md (when in the source) that are not exact;
the brand name altered; a JSON source whose translation is not valid JSON with the same keys;
a length ratio outside 0.8-1.6 words; text that does not look like the target language
(too few target-language function words, or too many English ones); retired brand names.
This is a safety net for what must not change. It does not judge translation quality: a person
should review Spanish before any live send.

Usage: python execution/translation_check.py source translation [--lang es] [--root DIR]
Exit 0 = PASS, 1 = FAIL.
"""
import json
import os
import re
import sys
from collections import Counter

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "execution"))
from brand_scrub import PATTERNS  # noqa: E402

BRAND = "The AI Agency Blueprint"
PROTECTED = [
    ("merge field", r"\{\{[^}]+\}\}"),
    ("url", r"https?://[^\s)>\]\"']+|www\.[^\s)>\]\"']+"),
    ("email", r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    ("phone", r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"),
    ("money", r"\$\s?\d[\d,]*(?:\.\d+)?"),
    ("percent", r"\d+(?:\.\d+)?\s?%"),
    ("number", r"\b\d+(?:[.,]\d+)*\b"),
]
ES_WORDS = set("de la el en y que los las del se por un una con para es su al lo como más pero sus le ya o este si porque esta entre cuando muy sin sobre también me hasta hay donde quien desde todo nos durante todos uno les ni contra otros ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo nosotros usted ustedes nuestro nuestra su sus".split())
EN_WORDS = set("the and of to in is that for it with as was on are be this by at or from your you we our will have has not but they their which can an if about more".split())
LANG_WORDS = {"es": ES_WORDS}
LENGTH_RATIO = (0.8, 1.6)
MIN_TARGET_SHARE = 0.12      # share of words that must be target-language function words
MAX_ENGLISH_SHARE = 0.20     # share of words allowed to be English function words


def footer_lines(root):
    path = os.path.join(root, "config", "footer.md")
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        content = f.read()
    for block in re.findall(r"```\n(.*?)\n```", content, re.S):
        out += [ln.strip() for ln in block.splitlines() if ln.strip() and not ln.strip().startswith("From:")]
    return out


def tokens(text):
    """Counts of protected tokens by kind, longest kinds first so a url's digits are not re-counted."""
    found, remaining = {}, text
    for kind, pat in PROTECTED:
        hits = [h.strip() for h in re.findall(pat, remaining)]
        if hits:
            found[kind] = Counter(hits)
        remaining = re.sub(pat, " ", remaining)
    return found


def keys(obj, prefix=""):
    if isinstance(obj, dict):
        return {k: keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [keys(v) for v in obj]
    return None


def words(text):
    return re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ']+", text)


def check(source, translation, lang="es", root=ROOT):
    fails, warns = [], []
    # JSON structure
    try:
        sj = json.loads(source)
    except ValueError:
        sj = None
    if sj is not None:
        try:
            tj = json.loads(translation)
        except ValueError:
            tj = None
            fails.append("source is JSON but the translation is not valid JSON")
        if tj is not None and keys(sj) != keys(tj):
            fails.append("JSON keys or list lengths differ from the source")

    foot = set(footer_lines(root))
    foot_in_src = [ln for ln in foot if ln in source]
    for ln in foot_in_src:
        if ln not in translation:
            fails.append(f"footer/signature line not exact: '{ln[:60]}'")
    if BRAND in source and BRAND not in translation:
        fails.append(f"brand name '{BRAND}' missing or altered")

    st, tt = tokens(source), tokens(translation)
    for kind, vals in st.items():
        for v, n in vals.items():
            if tt.get(kind, Counter())[v] < n:
                fails.append(f"{kind} '{v}' from the source is missing or changed in the translation")
    for kind, vals in tt.items():
        for v, n in vals.items():
            if st.get(kind, Counter())[v] < n:
                fails.append(f"{kind} '{v}' appears in the translation but not in the source")

    def strip_footer(t):
        for ln in foot:
            t = t.replace(ln, " ")
        return t
    sw, tw = words(strip_footer(source)), words(strip_footer(translation))
    if sw:
        ratio = len(tw) / len(sw)
        if not (LENGTH_RATIO[0] <= ratio <= LENGTH_RATIO[1]):
            fails.append(f"length ratio {ratio:.2f} outside {LENGTH_RATIO[0]}-{LENGTH_RATIO[1]} (content added or dropped?)")
    target = LANG_WORDS.get(lang)
    if target is None:
        fails.append(f"language '{lang}' is not supported yet [PENDING: languages, Joaquin]")
    elif tw:
        lw = [w.lower() for w in tw]
        share = sum(w in target for w in lw) / len(lw)
        en = sum(w in EN_WORDS for w in lw) / len(lw)
        if share < MIN_TARGET_SHARE:
            fails.append(f"only {share:.0%} of words look like {lang} function words (min {MIN_TARGET_SHARE:.0%}); untranslated?")
        if en > MAX_ENGLISH_SHARE:
            fails.append(f"{en:.0%} of words are English function words (max {MAX_ENGLISH_SHARE:.0%}); partly untranslated?")
    for p in PATTERNS:
        if p.search(translation):
            fails.append("retired brand name present (see execution/brand_scrub.py)")
            break
    warns.append("AI translation, not certified: a native-speaker review is recommended before any live send")
    if foot_in_src:
        warns.append("footer/unsubscribe lines are left in English; Spanish opt-out wording needs Joaquin's approval")
    return {"pass": not fails, "fails": fails, "warns": warns}


if __name__ == "__main__":
    args = sys.argv[1:]
    lang, root = "es", ROOT
    for flag in ("--lang", "--root"):
        if flag in args:
            i = args.index(flag)
            val = args[i + 1]
            del args[i:i + 2]
            lang, root = (val, root) if flag == "--lang" else (lang, val)
    if len(args) != 2:
        print(__doc__)
        sys.exit(2)
    with open(args[0], encoding="utf-8") as fa, open(args[1], encoding="utf-8") as fb:
        res = check(fa.read(), fb.read(), lang, root)
    print("PASS" if res["pass"] else "FAIL")
    for f in res["fails"]:
        print("  FAIL:", f)
    for w in res["warns"]:
        print("  WARN:", w)
    sys.exit(0 if res["pass"] else 1)
