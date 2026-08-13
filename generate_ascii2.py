#!/usr/bin/env python3
"""Generate ascii.svg (portrait #2) from asciiArt.js using the same
row-by-row typewriter reveal (SMIL <animate>) as the original ascii.svg.

No JS runs in a GitHub-rendered SVG, so the "typing" effect is baked in as
native SVG animation: each row is revealed by a clipPath whose width
animates 0 -> full over ROW_DUR seconds, staggered by row index, followed
by a small blinking-cursor rect. Font is embedded separately afterwards by
embed_portrait_font.py so this script only emits the markup + <style> stub.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

FONT_SIZE = 12.9
CHAR_W = round(FONT_SIZE * 0.6, 2)   # 7.74 - matches JetBrains Mono 600/1000 advance
ROW_H = 15
PAD_X = 14
PAD_TOP = 14
PAD_BOTTOM = 15
ROW_DUR = 0.09          # seconds per row reveal (matches original)
CURSOR_W = 6
CURSOR_H = 12


def load_art(path):
    js = open(path, encoding="utf-8").read()
    m = re.search(r"`(.*)`", js, re.S)
    if not m:
        raise SystemExit(f"{path}: no template literal found")
    lines = m.group(1).split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    maxlen = max(len(l) for l in lines)
    lines = [l.ljust(maxlen) for l in lines]
    return lines, maxlen


def esc(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_svg(lines, cols):
    rows = len(lines)
    text_w = round(cols * CHAR_W, 2)
    width = round(PAD_X + text_w + CURSOR_W + PAD_X - 0.8, 1)  # matches original's rounding
    height = PAD_TOP + rows * ROW_H + PAD_BOTTOM

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,\'Liberation Mono\',monospace">'
        f'<style>.a{{fill:#6e7681}}@media(prefers-color-scheme:dark){{.a{{fill:#c9d1d9}}}}</style>'
    )

    for i, line in enumerate(lines):
        rect_y = PAD_TOP + i * ROW_H
        text_y = round(rect_y + 11.2, 1)
        begin = round(i * ROW_DUR, 2)
        end = round(begin + ROW_DUR, 2)
        cursor_x_end = round(PAD_X + text_w, 1)

        parts.append(
            f'<clipPath id="c{i}"><rect x="{PAD_X}" y="{rect_y}" height="{ROW_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{text_w}" begin="{begin:.2f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<g clip-path="url(#c{i})"><text xml:space="preserve" x="{PAD_X}" y="{text_y}" class="a" '
            f'font-size="{FONT_SIZE}">{esc(line)}</text></g>'
            f'<rect y="{rect_y + 1}" width="{CURSOR_W}" height="{CURSOR_H}" class="a" opacity="0">'
            f'<animate attributeName="x" from="{PAD_X}" to="{cursor_x_end}" begin="{begin:.2f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{end:.2f}s"/>'
            f'</rect>'
        )

    parts.append("</svg>")
    return "".join(parts)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(HERE), "asciiArt.js")
    target = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(HERE), "ascii.svg")

    lines, cols = load_art(src)
    svg = build_svg(lines, cols)

    with open(target, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{target}: wrote {len(lines)} rows x {cols} cols ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
