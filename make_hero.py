"""Builds assets/hero.svg: halftone portrait + SYSTEM.INFO panel (GitHub-safe static SVG)."""
import base64, io
from PIL import Image, ImageDraw, ImageOps, ImageFilter

PHOTO = "/mnt/user-data/uploads/1000118688.jpg"

# --- halftone portrait ---
img = Image.open(PHOTO).convert("L")
w, h = img.size
img = img.crop((170, 1000, 930, 1760))                         # face + collar
img = ImageOps.autocontrast(img, cutoff=1)
img = ImageOps.autocontrast(img.point(lambda p: int(255*((p/255)**0.9))))
mask = Image.new("L", img.size, 0)
ImageDraw.Draw(mask).ellipse((20, 10, 740, 750), fill=255)
img = Image.composite(img, Image.new("L", img.size, 0), mask.filter(ImageFilter.GaussianBlur(60)))
CELL = 7
cols, rows = 62, 60
small = img.resize((cols, rows), Image.LANCZOS)
out = Image.new("RGB", (cols*CELL, rows*CELL), (5, 10, 26))
d = ImageDraw.Draw(out)
for y in range(rows):
    for x in range(cols):
        v = small.getpixel((x, y)) / 255
        r = v * CELL * 0.62
        if r > 0.6:
            cx, cy = x*CELL + CELL/2, y*CELL + CELL/2
            d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(200, 215, 255))
buf = io.BytesIO(); out.save(buf, "PNG", optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()
out.save("assets/visual-map.png")

# --- SVG card ---
info = [
 ("Subject", "Nishchay Puri"),
 ("Role", "Full-Stack & AI/ML Engineer"),
 ("Origin", "New Delhi, India"),
 ("Education", "B.Tech AI & ML - VIPS (GGSIPU)"),
 ("Status", "1st of 4,413 teams - Japan 2025"),
 ("ToolChain", "Python / TypeScript / React"),
]
core = [("Core.Lang", "Python | JS | TS | SQL"),
        ("Core.Frontend", "React | TS | Tailwind"),
        ("Core.Backend", "FastAPI | Node.js | Flask"),
        ("Core.Infra", "Docker | GH Actions | AWS")]
grid = ["Grid.Mail", "Grid.LinkedIn", "Grid.GitHub"]

rowsvg = ""
y = 70
for k, v in info:
    rowsvg += f'<text x="520" y="{y}" class="k">{k}</text><text x="650" y="{y}" class="v">{v}</text>'
    y += 26
y += 14
for k, v in core:
    rowsvg += f'<text x="520" y="{y}" class="c">{k}</text><text x="650" y="{y}" class="v">{v}</text>'
    y += 24
y += 14
rowsvg += f'<text x="520" y="{y}" class="k">- Contact</text>'; y += 24
for g in grid:
    rowsvg += f'<text x="520" y="{y}" class="g">{g}</text>'; y += 22

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="980" height="520" viewBox="0 0 980 520">
<style>
 text{{font-family:'SFMono-Regular',Consolas,Menlo,monospace}}
 .k{{fill:#6ee7ff;font-size:14px;letter-spacing:1px}}
 .v{{fill:#e6edff;font-size:14px}}
 .c{{fill:#a78bfa;font-size:14px}}
 .g{{fill:#34d399;font-size:13px}}
 .t{{fill:#e6edff;font-size:13px}}
 .dim{{fill:#64748b;font-size:11px;letter-spacing:2px}}
 .glow{{animation:p 2.4s ease-in-out infinite}} @keyframes p{{50%{{opacity:.45}}}}
</style>
<rect width="980" height="520" rx="14" fill="#050a1a"/>
<rect x="1" y="1" width="978" height="518" rx="14" fill="none" stroke="#22d3ee" stroke-opacity=".55" class="glow"/>
<circle cx="24" cy="22" r="6" fill="#ff5f57"/><circle cx="44" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>
<text x="956" y="26" text-anchor="end" class="t">nishchaypuri034@gmail.com - ~/nishchaypuri1</text>
<text x="40" y="58" class="dim">VISUAL.MAP</text>
<rect x="38" y="68" width="440" height="430" fill="none" stroke="#22d3ee" stroke-opacity=".6"/>
<image x="40" y="70" width="436" height="426" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/png;base64,{b64}"/>
<text x="520" y="48" class="dim">SYSTEM.INFO</text>
{rowsvg}
</svg>'''
open("assets/hero.svg", "w").write(svg)
print("ok", len(svg)//1024, "KB")
