#!/usr/bin/env python3
"""Dolly's comparison-table builder (dolly_build.py has no table format). Reuses its brand and footer readers.

Spec JSON: {"title","subtitle","columns":["Option 1",...],"rows":[["Row label",[cell,cell,cell]],...]}
Usage: python execution/dolly_table.py spec.json out_dir  -> out_dir/options_table-primary.svg, -alternate.svg
Copy comes from Mark; this script only lays it out.
"""
import json, os, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dolly_build as d
from xml.sax.saxutils import escape

W = 1600
LABEL_W, PAD, WRAP, SIZE, LEAD = 230, 22, 31, 22, 30


def soft():
    m = re.search(r"^\| Soft background \| (#[0-9A-Fa-f]{6})", open(os.path.join(d.ROOT, "config", "brand.md"), encoding="utf-8").read(), re.M)
    return m.group(1) if m else "#F5F3EE"


def build(spec, variant, b):
    dark = variant == "alternate"
    bg, fg = (b["Primary color"], "#FFFFFF") if dark else ("#FFFFFF", "#1A1A1A")
    band = b["Accent color"] if dark else b["Primary color"]
    bandfg = "#1A1A1A" if dark else "#FFFFFF"
    hf, bf = b["Heading font"], b["Body font"]
    n = len(spec["columns"])
    cw = (W - 120 - LABEL_W) // n
    el = [f'<rect width="{W}" height="@H@" fill="{bg}"/>', f'<rect width="{W}" height="36" fill="{band}"/>',
          d.text(60, 110, "The AI Agency Blueprint", 34, fg, hf, "bold"),
          d.text(60, 190, spec["title"], 46, fg, hf, "bold"),
          d.text(60, 235, spec.get("subtitle", ""), 24, fg, bf)]
    y = 270
    hh = 70
    el.append(f'<rect x="60" y="{y}" width="{W - 120}" height="{hh}" fill="{band}"/>')
    for i, c in enumerate(spec["columns"]):
        el.append(d.text(60 + LABEL_W + i * cw + PAD, y + 44, c, 26, bandfg, hf, "bold"))
    y += hh
    for r, (label, cells) in enumerate(spec["rows"]):
        lines = max(len(d.wrap(c, WRAP)) for c in cells)
        rh = lines * LEAD + 36
        shade = ("#2B4C7A" if dark else soft()) if r % 2 == 0 else bg
        el.append(f'<rect x="60" y="{y}" width="{W - 120}" height="{rh}" fill="{shade}"/>')
        el.append(d.text(60 + PAD, y + 38, label, SIZE, fg, bf, "bold"))
        for i, c in enumerate(cells):
            el.append(d.text(60 + LABEL_W + i * cw + PAD, y + 38, c, SIZE, fg, bf, wrap_at=WRAP, lead=LEAD / SIZE))
        y += rh
    el.append(f'<rect x="60" y="{y}" width="{W - 120}" height="3" fill="{band}"/>')
    h = y + 60 + 110 + 20
    fy = h - 60
    el.append(f'<rect x="0" y="{fy - 50}" width="{W}" height="110" fill="{band}"/>')
    el.append(d.text(W // 2, fy + 8, d.footer(), 22, bandfg, bf, anchor="middle"))
    body = "".join(el).replace("@H@", str(h))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">' + body + "</svg>"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    spec = json.load(open(sys.argv[1]))
    b, placeholder = d.brand()
    os.makedirs(sys.argv[2], exist_ok=True)
    files = []
    for v in ("primary", "alternate"):
        p = os.path.join(sys.argv[2], f"options_table-{v}.svg")
        open(p, "w", encoding="utf-8").write(build(spec, v, b)); files.append(p)
    rep = {"files": files, "placeholder_brand_settings": placeholder, "footer_source": "config/footer.md"}
    json.dump(rep, open(os.path.join(sys.argv[2], "options_table-build-report.json"), "w"), indent=2)
    print(json.dumps(rep, indent=2))
