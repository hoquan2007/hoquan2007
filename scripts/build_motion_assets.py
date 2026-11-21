#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_motion_assets.py - Hand-tuned animated SVG set for the profile README.

Outputs (into assets/motion/):
    hero.svg, about.svg, timeline.svg, divider.svg, footer.svg,
    project-<slug>.svg (one card per featured project)

Design rules:
    * One palette (deep navy + cyan -> violet accent), one signature move:
      a thin light that travels around every card border.
    * Motion is slow and quiet; every SVG honours prefers-reduced-motion.
    * Pure SVG + CSS/SMIL (no script) so GitHub's image proxy renders it.

Run:  python scripts/build_motion_assets.py
"""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "motion"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- tokens
BG0, BG1, CARD, INSET = "#070A13", "#0C1222", "#0E1526", "#0A101E"
LINE, TEXT, MUTED, DIM = "#1C2540", "#E6EDF7", "#8D9AB3", "#5B6782"
CYAN, VIOLET, BLUE, GREEN, PINK = "#22D3EE", "#A78BFA", "#60A5FA", "#34D399", "#F472B6"
SANS = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace"

BASE_CSS = """
  .sans{font-family:%(sans)s}
  .mono{font-family:%(mono)s}
  .fu{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}
  @keyframes fu{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
  .pulse{animation:pulse 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
  @keyframes pulse{0%%,100%%{opacity:.35;transform:scale(1)}50%%{opacity:1;transform:scale(1.15)}}
  .blink{animation:blink 1.05s steps(1) infinite}
  @keyframes blink{50%%{opacity:0}}
  @media (prefers-reduced-motion: reduce){
    *{animation:none!important}
    animate,animateTransform,animateMotion{display:none}
  }
""" % {"sans": SANS, "mono": MONO}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w: int, h: int, label: str, defs: str, css: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(label)}" fill="none">\n'
        f"<title>{esc(label)}</title>\n<defs>\n"
        f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>\n'
        f'<linearGradient id="cardbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{CARD}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>\n'
        f"{defs}\n</defs>\n<style><![CDATA[{BASE_CSS}{css}]]></style>\n{body}\n</svg>\n"
    )


def frame(x: float, y: float, w: float, h: float, rx: float = 18, delay: float = 0, dur: float = 9) -> str:
    """Card surface + the signature travelling border light."""
    return (
        f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#cardbg)" stroke="{LINE}"/>'
        f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{rx}" stroke="url(#accent)" '
        f'stroke-width="1.4" pathLength="1000" stroke-dasharray="90 910" stroke-linecap="round" opacity=".85">'
        f'<animate attributeName="stroke-dashoffset" values="1000;0" dur="{dur}s" begin="{-delay}s" repeatCount="indefinite"/>'
        f"</rect>"
        # soft top sheen
        f'<path d="M{x+rx} {y+1}H{x+w-rx}" stroke="#FFFFFF" stroke-opacity=".06"/>'
    )


def pill(x: float, y: float, w: float, label: str, color: str = MUTED, size: int = 12, h: int = 26) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{INSET}" stroke="{LINE}"/>'
        f'<text x="{x + w/2}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" class="mono" '
        f'font-size="{size}" fill="{color}">{esc(label)}</text>'
    )


def mono_w(text: str, size: float) -> float:
    return len(text) * size * 0.61


# ---------------------------------------------------------------- hero
def build_hero() -> str:
    W, H = 1200, 420
    cx, cy = 968, 212
    defs = f"""
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" fill="#2A3554"/></pattern>
<radialGradient id="fade" cx="60%" cy="45%" r="65%"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="dotmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="24"/></clipPath>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="#0D1428"/></linearGradient>
<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="620" y2="0">
  <stop offset="0" stop-color="{TEXT}"/><stop offset=".38" stop-color="{TEXT}"/>
  <stop offset=".5" stop-color="#A5F3FC"/><stop offset=".6" stop-color="#C4B5FD"/>
  <stop offset=".72" stop-color="{TEXT}"/><stop offset="1" stop-color="{TEXT}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-640 0;640 0;640 0" keyTimes="0;.45;1" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<radialGradient id="core" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<path id="orbitA" d="M{cx-150},{cy} a150,150 0 1,1 300,0 a150,150 0 1,1 -300,0"/>
"""
    css = """
  .role{opacity:0;animation:role 12s infinite both}
  .r2{animation-delay:3s}.r3{animation-delay:6s}.r4{animation-delay:9s}
  @keyframes role{0%{opacity:0;transform:translateY(14px)}3.5%{opacity:1;transform:none}
    22%{opacity:1;transform:none}25.5%{opacity:0;transform:translateY(-14px)}100%{opacity:0}}
  .float{animation:float 7s ease-in-out infinite}
  @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
  .tw{animation:tw 4s ease-in-out infinite}
  @keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}
"""
    stars = ""
    for i, (sx, sy) in enumerate([(140, 60), (420, 48), (690, 92), (760, 330), (560, 380), (1130, 70),
                                  (1150, 300), (330, 395), (820, 40), (40, 260)]):
        stars += f'<circle cx="{sx}" cy="{sy}" r="1.2" fill="#C7D2FE" class="tw" style="animation-delay:{i*0.45:.2f}s"/>'

    roles = ["Software Engineering Student", "Full-stack Web Developer",
             "AI &amp; Computer Vision Explorer", "Systems · C/C++ Enthusiast"]
    roles_svg = "".join(
        f'<g class="role r{i+1}"><text x="100" y="246" class="sans" font-size="25" font-weight="500" fill="{TEXT}">{r}</text></g>'
        for i, r in enumerate(roles)
    )

    # chips
    chips = []
    x = 72
    for label, w, kind in [("Open to collaborate", 206, "live"), ("Việt Nam · UTC+7", 178, "pin"),
                           ("41+ repos · 18 live demos", 236, "repo")]:
        chips.append(f'<rect x="{x}" y="326" width="{w}" height="34" rx="17" fill="{CARD}" stroke="{LINE}"/>')
        if kind == "live":
            chips.append(f'<circle cx="{x+20}" cy="343" r="8" fill="{GREEN}" opacity=".25" class="pulse"/>'
                         f'<circle cx="{x+20}" cy="343" r="4" fill="{GREEN}"/>')
        elif kind == "pin":
            chips.append(f'<path d="M{x+20} 352c-4-5-7-8-7-12a7 7 0 0 1 14 0c0 4-3 7-7 12z" stroke="{CYAN}" stroke-width="1.6"/>'
                         f'<circle cx="{x+20}" cy="340" r="2.2" fill="{CYAN}"/>')
        else:
            chips.append(f'<rect x="{x+13}" y="336" width="14" height="14" rx="3" stroke="{VIOLET}" stroke-width="1.6"/>'
                         f'<path d="M{x+17} 343h6" stroke="{VIOLET}" stroke-width="1.6"/>')
        chips.append(f'<text x="{x+36}" y="348" class="sans" font-size="14" fill="{TEXT}">{label}</text>')
        x += w + 12

    pills = ""
    for i, (label, w) in enumerate([("TypeScript", 104), ("C / C++", 82), ("Next.js", 82), ("AI · CV", 76)]):
        pills += (
            f'<g><rect x="{-w/2}" y="-14" width="{w}" height="28" rx="14" fill="{CARD}" stroke="{LINE}"/>'
            f'<text y="4.5" text-anchor="middle" class="mono" font-size="12" fill="{CYAN if i % 2 == 0 else VIOLET}">{label}</text>'
            f'<animateMotion dur="48s" begin="{-i*12}s" repeatCount="indefinite"><mpath href="#orbitA"/></animateMotion></g>'
        )

    body = f"""
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g filter="url(#blur)">
    <circle cx="900" cy="110" r="170" fill="{VIOLET}" opacity=".30">
      <animateTransform attributeName="transform" type="translate" values="0 0;-70 50;0 0" dur="20s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></circle>
    <circle cx="230" cy="380" r="170" fill="{CYAN}" opacity=".16">
      <animateTransform attributeName="transform" type="translate" values="0 0;90 -40;0 0" dur="24s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></circle>
    <circle cx="1120" cy="400" r="130" fill="{BLUE}" opacity=".22">
      <animateTransform attributeName="transform" type="translate" values="0 0;-40 -60;0 0" dur="18s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></circle>
  </g>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dotmask)" opacity=".7"/>
  {stars}
</g>
{frame(0, 0, W, H, rx=24, dur=12)}

<g class="fu" style="animation-delay:.1s"><text x="72" y="112" class="mono" font-size="15" fill="{CYAN}">&lt;/&gt;  xin chào, mình là</text></g>
<g class="fu" style="animation-delay:.25s"><text x="68" y="188" class="sans" font-size="70" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Hồ Ngọc Quân</text></g>
<g class="fu" style="animation-delay:.45s">
  <text x="72" y="246" class="sans" font-size="25" font-weight="600" fill="{CYAN}">▸</text>
  {roles_svg}
</g>
<g class="fu" style="animation-delay:.6s">
  <text x="72" y="288" class="sans" font-size="16.5" fill="{MUTED}">Xây sản phẩm Web, AI và hệ thống — từ C/C++ cấp thấp tới TypeScript full-stack.</text>
</g>
<g class="fu" style="animation-delay:.75s">{''.join(chips)}</g>

<g class="fu" style="animation-delay:.4s">
  <circle cx="{cx}" cy="{cy}" r="150" stroke="{LINE}" stroke-dasharray="2 7">
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="90s" repeatCount="indefinite"/></circle>
  <circle cx="{cx}" cy="{cy}" r="150" stroke="url(#accent)" stroke-width="1.6" pathLength="100" stroke-dasharray="10 90" stroke-linecap="round">
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="14s" repeatCount="indefinite"/></circle>
  <circle cx="{cx}" cy="{cy}" r="104" stroke="{LINE}"/>
  <g><circle cx="{cx}" cy="{cy-104}" r="3.5" fill="{PINK}"/>
    <animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="22s" repeatCount="indefinite"/></g>
  <circle cx="{cx}" cy="{cy}" r="92" fill="url(#core)" class="pulse" style="animation-duration:6s"/>
  <g class="float">
    <circle cx="{cx}" cy="{cy}" r="58" fill="{BG1}" stroke="url(#accent)" stroke-width="1.6"/>
    <text x="{cx}" y="{cy+14}" text-anchor="middle" class="sans" font-size="40" font-weight="800" letter-spacing="1" fill="url(#accent)">HQ</text>
  </g>
  {pills}
</g>
<text x="{W-36}" y="{H-24}" text-anchor="end" class="mono" font-size="12" fill="{DIM}">github.com/hoquan2007</text>
"""
    return svg(W, H, "Hồ Ngọc Quân — Software Engineering Student", defs, css, body)


# ---------------------------------------------------------------- about
def build_about() -> str:
    W, H = 1200, 440
    TW = 724  # terminal width
    lines: list[tuple[str, str, str]] = [
        ("cmd", "whoami", ""),
        ("out", "Hồ Ngọc Quân  ·  @hoquan2007", ""),
        ("cmd", "cat about.yml", ""),
        ("kv", "role", "Software Engineering Student"),
        ("kv", "based", "Việt Nam (UTC+7)"),
        ("kv", "focus", "Web · AI · Systems · Algorithms"),
        ("kv", "stack", "TypeScript · Next.js · Node.js · C/C++"),
        ("kv", "learning", "DSA nâng cao · Linux kernel · GPU computing"),
        ("kv", "speaks", "Tiếng Việt · English"),
        ("kv", "email", "hnquan2007@gmail.com"),
        ("end", "", ""),
    ]
    defs = ""
    rows = []
    t = 0.5
    y = 96
    cw = 9.15  # mono glyph width at 15px
    for i, (kind, a, b) in enumerate(lines):
        if kind == "cmd":
            n = len(a)
            step = 0.065
            widths = ";".join(f"{k*cw:.1f}" for k in range(n + 1))
            keys = ";".join(f"{k/n:.4f}" for k in range(n + 1))
            defs += (f'<clipPath id="type{i}"><rect x="58" y="{y-16}" height="24" width="0">'
                     f'<animate attributeName="width" values="{widths}" keyTimes="{keys}" calcMode="discrete" '
                     f'dur="{n*step:.2f}s" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>')
            rows.append(f'<text x="36" y="{y}" class="mono" font-size="15" fill="{GREEN}">❯</text>'
                        f'<text x="58" y="{y}" class="mono" font-size="15" fill="{TEXT}" clip-path="url(#type{i})">{esc(a)}</text>')
            t += n * step + 0.25
        elif kind == "out":
            rows.append(f'<text x="36" y="{y}" class="mono" font-size="15" font-weight="700" fill="url(#accent)" opacity="0">{esc(a)}'
                        f'<animate attributeName="opacity" values="0;1" dur=".4s" begin="{t:.2f}s" fill="freeze"/></text>')
            t += 0.45
        elif kind == "kv":
            rows.append(f'<g opacity="0"><text x="36" y="{y}" class="mono" font-size="15" fill="{VIOLET}">{a}<tspan fill="{DIM}">:</tspan></text>'
                        f'<text x="160" y="{y}" class="mono" font-size="15" fill="{TEXT}">{esc(b)}</text>'
                        f'<animate attributeName="opacity" values="0;1" dur=".35s" begin="{t:.2f}s" fill="freeze"/></g>')
            t += 0.16
        else:
            rows.append(f'<g opacity="0"><text x="36" y="{y}" class="mono" font-size="15" fill="{GREEN}">❯</text>'
                        f'<rect x="58" y="{y-14}" width="9" height="18" fill="{CYAN}" class="blink"/>'
                        f'<animate attributeName="opacity" values="0;1" dur=".2s" begin="{t+0.2:.2f}s" fill="freeze"/></g>')
        y += 29

    # right panel
    RX = TW + 22
    RW = W - RX
    now_rows = [
        ("BUILDING", "QEnglish · Chess online · Web-xem-phim", GREEN),
        ("LEARNING", "Cấu trúc dữ liệu & giải thuật nâng cao", CYAN),
        ("EXPLORING", "Edge AI · Computer Vision thời gian thực", VIOLET),
    ]
    now_svg = ""
    for i, (lbl, val, col) in enumerate(now_rows):
        yy = 104 + i * 66
        now_svg += (
            f'<g class="fu" style="animation-delay:{0.5 + i*0.2:.1f}s">'
            f'<circle cx="{RX+34}" cy="{yy-5}" r="9" fill="{col}" opacity=".25" class="pulse" style="animation-delay:{i*0.6:.1f}s"/>'
            f'<circle cx="{RX+34}" cy="{yy-5}" r="4" fill="{col}"/>'
            f'<text x="{RX+54}" y="{yy-1}" class="mono" font-size="11.5" letter-spacing="2" fill="{DIM}">{lbl}</text>'
            f'<text x="{RX+54}" y="{yy+22}" class="sans" font-size="16" fill="{TEXT}">{esc(val)}</text></g>'
        )
    stats = [("41+", "repositories"), ("18", "live demos"), ("2025", "on GitHub")]
    sw = (RW - 48) / 3
    stats_svg = f'<path d="M{RX+24} 318H{W-24}" stroke="{LINE}"/>'
    for i, (num, lbl) in enumerate(stats):
        sx = RX + 24 + sw * i + sw / 2
        stats_svg += (f'<g class="fu" style="animation-delay:{1.2 + i*0.15:.2f}s">'
                      f'<text x="{sx}" y="372" text-anchor="middle" class="sans" font-size="36" font-weight="800" fill="url(#accent)">{num}</text>'
                      f'<text x="{sx}" y="398" text-anchor="middle" class="mono" font-size="12" fill="{MUTED}">{lbl}</text></g>')
        if i:
            stats_svg += f'<path d="M{RX+24+sw*i} 344V398" stroke="{LINE}"/>'

    body = f"""
{frame(0, 0, TW, H, dur=10)}
<path d="M1 50H{TW-1}" stroke="{LINE}"/>
<circle cx="28" cy="25" r="6" fill="#FF5F57"/><circle cx="48" cy="25" r="6" fill="#FEBC2E"/><circle cx="68" cy="25" r="6" fill="#28C840"/>
<text x="{TW/2}" y="30" text-anchor="middle" class="mono" font-size="13" fill="{DIM}">quan@dev — ~/profile</text>
{''.join(rows)}

{frame(RX, 0, RW, H, dur=10, delay=5)}
<text x="{RX+24}" y="42" class="mono" font-size="12" letter-spacing="2.5" fill="{CYAN}">NOW // 2026</text>
<path d="M{RX+24} 56h44" stroke="url(#accent)" stroke-width="2"/>
{now_svg}
{stats_svg}
"""
    return svg(W, H, "About Hồ Ngọc Quân", defs, "", body)


# ---------------------------------------------------------------- project motifs (206 x 212 box)
def motif_chat() -> str:
    css_bubbles = ""
    out = ""
    bubbles = [(16, 22, 128, CYAN, 0.0), (62, 68, 128, VIOLET, 1.0), (16, 114, 74, CYAN, 2.0)]
    for i, (bx, by, bw, col, d) in enumerate(bubbles):
        inner = (f'<rect x="{bx}" y="{by}" width="{bw}" height="34" rx="12" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>')
        if i < 2:
            inner += (f'<rect x="{bx+12}" y="{by+11}" width="{bw-40}" height="4" rx="2" fill="{col}" opacity=".7"/>'
                      f'<rect x="{bx+12}" y="{by+20}" width="{bw-64}" height="4" rx="2" fill="{col}" opacity=".4"/>')
        else:
            for k in range(3):
                inner += (f'<circle cx="{bx+22+k*15}" cy="{by+17}" r="3.5" fill="{col}" class="dot" style="animation-delay:{k*0.18:.2f}s"/>')
        out += f'<g class="bub" style="animation-delay:{d}s">{inner}</g>'
    bars = ""
    for k in range(16):
        dur = 0.9 + (k * 37 % 7) / 10
        bars += (f'<rect x="{16 + k*11}" y="166" width="5" height="34" rx="2.5" fill="url(#accent)" class="eq" '
                 f'style="animation-duration:{dur:.1f}s;animation-delay:{-k*0.13:.2f}s"/>')
    return out + bars, """
  .bub{opacity:0;animation:bub 6s ease-out infinite both;transform-box:fill-box;transform-origin:left bottom}
  @keyframes bub{0%{opacity:0;transform:translateY(8px) scale(.94)}6%{opacity:1;transform:none}82%{opacity:1}92%,100%{opacity:0}}
  .dot{animation:dot 1s ease-in-out infinite}
  @keyframes dot{0%,100%{opacity:.3}50%{opacity:1}}
  .eq{transform-box:fill-box;transform-origin:center;animation:eq 1s ease-in-out infinite alternate}
  @keyframes eq{from{transform:scaleY(.15)}to{transform:scaleY(1)}}
"""


def motif_face() -> str:
    s = (f'<g stroke="{CYAN}" stroke-width="2.4" stroke-linecap="round">'
         f'<path d="M34 46V28h18M172 46V28h-18M34 166v18h18M172 166v18h-18"/></g>'
         f'<ellipse cx="103" cy="92" rx="34" ry="42" stroke="{TEXT}" stroke-opacity=".55" stroke-width="1.6"/>'
         f'<path d="M58 184c6-24 24-34 45-34s39 10 45 34" stroke="{TEXT}" stroke-opacity=".35" stroke-width="1.6"/>'
         f'<circle cx="90" cy="86" r="3" fill="{TEXT}"/><circle cx="116" cy="86" r="3" fill="{TEXT}"/>'
         f'<path d="M92 110q11 8 22 0" stroke="{TEXT}" stroke-width="1.6" stroke-linecap="round"/>')
    for k, (px, py) in enumerate([(78, 70), (128, 70), (103, 98), (84, 118), (122, 118), (103, 132), (70, 96), (136, 96)]):
        s += f'<circle cx="{px}" cy="{py}" r="2" fill="{VIOLET}" class="lm" style="animation-delay:{k*0.12:.2f}s"/>'
    s += (f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/></linearGradient>'
          f'<g class="scan"><rect x="36" y="0" width="134" height="26" fill="url(#scan)"/>'
          f'<rect x="36" y="25" width="134" height="1.5" fill="{CYAN}"/></g>'
          f'<g class="ok"><rect x="58" y="192" width="90" height="20" rx="10" fill="{GREEN}" fill-opacity=".15" stroke="{GREEN}" stroke-opacity=".6"/>'
          f'<text x="103" y="206" text-anchor="middle" class="mono" font-size="10.5" fill="{GREEN}">✓ VERIFIED</text></g>')
    return s, """
  .scan{animation:scan 3.2s cubic-bezier(.45,0,.55,1) infinite}
  @keyframes scan{0%{transform:translateY(24px);opacity:0}10%{opacity:1}70%{transform:translateY(160px);opacity:1}80%,100%{transform:translateY(160px);opacity:0}}
  .lm{animation:lm 3.2s ease-out infinite}
  @keyframes lm{0%,20%{opacity:0}35%,85%{opacity:1}100%{opacity:0}}
  .ok{animation:ok 3.2s ease-out infinite}
  @keyframes ok{0%,70%{opacity:0}78%,95%{opacity:1}100%{opacity:0}}
"""


def motif_chess() -> str:
    ox, oy, sq = 23, 18, 40
    s = ""
    for r in range(4):
        for c in range(4):
            col = "#18223D" if (r + c) % 2 == 0 else "#0F172B"
            s += f'<rect x="{ox+c*sq}" y="{oy+r*sq}" width="{sq}" height="{sq}" fill="{col}"/>'
    s += f'<rect x="{ox}" y="{oy}" width="{sq*4}" height="{sq*4}" stroke="{LINE}"/>'
    # knight tour (col,row), all legal L-moves
    tour = [(0, 3), (1, 1), (3, 0), (2, 2), (0, 3)]
    pos = [(ox + c*sq + sq/2, oy + r*sq + sq/2) for c, r in tour]
    vals, keys = [], []
    n = len(tour) - 1
    for i in range(n):
        x0, y0 = pos[i]
        vals += [f"{x0} {y0}", f"{x0} {y0}"]
        keys += [i / n, i / n + 0.6 / n]
    vals.append(f"{pos[-1][0]} {pos[-1][1]}")
    keys.append(1)
    splines = ";".join(["0 0 1 1" if k % 2 == 0 else ".5 0 .2 1" for k in range(len(vals) - 1)])
    for i in range(n):
        tx, ty = pos[i + 1]
        s += (f'<rect x="{tx-sq/2+3}" y="{ty-sq/2+3}" width="{sq-6}" height="{sq-6}" rx="6" stroke="{CYAN}" stroke-width="1.5" opacity="0">'
              f'<animate attributeName="opacity" values="0;0;.9;0;0" keyTimes="0;{(i+0.45)/n:.3f};{(i+0.6)/n:.3f};{(i+1)/n:.3f};1" dur="8s" repeatCount="indefinite"/></rect>')
    s += (f'<text x="{ox+3*sq+sq/2}" y="{oy+3*sq+sq/2+11}" text-anchor="middle" font-size="30" fill="{VIOLET}" opacity=".85">♚</text>'
          f'<g><text y="11" text-anchor="middle" font-size="32" fill="{TEXT}">♞</text>'
          f'<animateTransform attributeName="transform" type="translate" values="{";".join(vals)}" '
          f'keyTimes="{";".join(f"{k:.4f}" for k in keys)}" calcMode="spline" keySplines="{splines}" dur="8s" repeatCount="indefinite"/></g>'
          f'<text x="103" y="204" text-anchor="middle" class="mono" font-size="11" fill="{DIM}">knight · L-moves</text>')
    return s, ""


def motif_music() -> str:
    s = (f'<g transform="translate(78 82)"><g class="spin">'
         f'<circle r="58" fill="#0B0F1C" stroke="{LINE}"/>')
    for r in (50, 43, 36, 29):
        s += f'<circle r="{r}" stroke="#FFFFFF" stroke-opacity=".05"/>'
    s += (f'<path d="M0 0L-52 -18A55 55 0 0 1 -30 -46Z" fill="#FFFFFF" fill-opacity=".06"/>'
          f'<circle r="18" fill="url(#accent)"/><circle r="3" fill="{BG0}"/></g></g>'
          f'<path d="M176 22v14l-34 62" stroke="{MUTED}" stroke-width="3" stroke-linecap="round"/>'
          f'<circle cx="176" cy="22" r="6" fill="{CARD}" stroke="{MUTED}" stroke-width="2"/>')
    for k in range(14):
        dur = 0.7 + (k * 53 % 9) / 10
        s += (f'<rect x="{14 + k*13}" y="160" width="7" height="44" rx="3.5" fill="url(#accent)" class="eq" '
              f'style="animation-duration:{dur:.1f}s;animation-delay:{-k*0.17:.2f}s"/>')
    return s, """
  .spin{animation:spin 5s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}
  .eq{transform-box:fill-box;transform-origin:bottom;animation:eq 1s ease-in-out infinite alternate}
  @keyframes eq{from{transform:scaleY(.12)}to{transform:scaleY(1)}}
"""


def motif_gpu() -> str:
    s = (f'<text x="14" y="26" class="mono" font-size="10" letter-spacing="2" fill="{DIM}">JOB QUEUE</text>'
         f'<clipPath id="q"><rect x="14" y="36" width="178" height="22"/></clipPath><g clip-path="url(#q)"><g class="queue">')
    for k in range(12):
        col = CYAN if k % 3 else VIOLET
        s += f'<rect x="{14 + k*30}" y="38" width="24" height="18" rx="4" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-opacity=".6"/>'
    s += "</g></g>"
    loads = [("0.62;0.91;0.48;0.84;0.62", 4.2), ("0.35;0.58;0.88;0.4;0.35", 5.1),
             ("0.8;0.52;0.7;0.95;0.8", 3.7), ("0.2;0.66;0.44;0.3;0.2", 4.6)]
    for i, (vals, dur) in enumerate(loads):
        y = 88 + i * 30
        ws = ";".join(f"{float(v)*120:.0f}" for v in vals.split(";"))
        col = [CYAN, VIOLET, BLUE, PINK][i]
        s += (f'<text x="14" y="{y+8}" class="mono" font-size="11" fill="{MUTED}">GPU{i}</text>'
              f'<rect x="56" y="{y}" width="120" height="9" rx="4.5" fill="#141C33"/>'
              f'<rect x="56" y="{y}" width="60" height="9" rx="4.5" fill="{col}">'
              f'<animate attributeName="width" values="{ws}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" '
              f'keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></rect>'
              f'<circle cx="188" cy="{y+4.5}" r="3" fill="{GREEN}" class="pulse" style="animation-delay:{i*0.5}s"/>')
    s += f'<text x="14" y="206" class="mono" font-size="10.5" fill="{DIM}">scheduler · round-robin</text>'
    return s, """
  .queue{animation:queue 6s linear infinite}
  @keyframes queue{to{transform:translateX(-90px)}}
"""


def motif_dungeon() -> str:
    ox, oy, c = 13, 12, 20
    rooms = [(1, 1, 3, 3), (5, 1, 3, 2), (5, 5, 3, 3), (1, 6, 3, 2)]
    corr = [(4, 2, 1, 1), (6, 3, 1, 2), (4, 6, 1, 1)]
    s = f'<rect x="{ox}" y="{oy}" width="{c*9}" height="{c*9}" fill="#090D18" stroke="{LINE}"/>'
    for gx in range(1, 9):
        s += f'<path d="M{ox+gx*c} {oy}v{c*9}M{ox} {oy+gx*c}h{c*9}" stroke="#FFFFFF" stroke-opacity=".035"/>'
    for i, (x, y, w, h) in enumerate(rooms + corr):
        s += (f'<rect x="{ox+x*c}" y="{oy+y*c}" width="{w*c}" height="{h*c}" fill="#18223D" class="room" '
              f'style="animation-delay:{i*0.15:.2f}s"/>')
    p = lambda gx, gy: (ox + gx*c + c/2, oy + gy*c + c/2)  # noqa: E731
    pts = [p(2, 2), p(6, 2), p(6, 6), p(2, 6)]
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    s += (f'<path d="{d}" stroke="url(#accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
          f'pathLength="100" stroke-dasharray="100" class="draw"/>'
          f'<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="5" fill="{GREEN}"/>'
          f'<rect x="{pts[-1][0]-5}" y="{pts[-1][1]-5}" width="10" height="10" rx="2" fill="{PINK}" class="pulse"/>'
          f'<circle r="4" fill="#FFFFFF"><animateMotion dur="4s" repeatCount="indefinite" path="{d}" '
          f'keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="linear"/></circle>'
          f'<text x="103" y="208" text-anchor="middle" class="mono" font-size="10.5" fill="{DIM}">A* · seed 0x51AD</text>')
    return s, """
  .draw{animation:draw 4s ease-in-out infinite}
  @keyframes draw{0%{stroke-dashoffset:100}70%{stroke-dashoffset:0}90%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
  .room{animation:fu .6s ease-out both}
"""


PROJECTS = [
    {
        "slug": "qenglish", "no": "01", "tag": "AI · EDTECH", "title": "QEnglish",
        "desc": ["Luyện giao tiếp tiếng Anh với AI —", "hội thoại theo ngữ cảnh, phản xạ nhanh."],
        "chips": ["TypeScript", "Next.js", "AI"], "cta": "Source code", "motif": motif_chat,
    },
    {
        "slug": "face-attendance", "no": "02", "tag": "COMPUTER VISION", "title": "face-attendance",
        "desc": ["Điểm danh bằng nhận diện khuôn mặt", "ngay trên trình duyệt, độ trễ thấp."],
        "chips": ["TypeScript", "CV", "Web"], "cta": "Live demo", "motif": motif_face,
    },
    {
        "slug": "chess-online", "no": "03", "tag": "GAME · REALTIME", "title": "Chess Online",
        "desc": ["Cờ vua trực tuyến trên web — bàn cờ", "tương tác, xử lý luật đi quân."],
        "chips": ["TypeScript", "Game logic"], "cta": "Live demo", "motif": motif_chess,
    },
    {
        "slug": "qmusic", "no": "04", "tag": "MEDIA · UI", "title": "QMusic",
        "desc": ["Web nghe nhạc cá nhân — trình phát,", "playlist và giao diện tối giản."],
        "chips": ["TypeScript", "Audio", "UI"], "cta": "Live demo", "motif": motif_music,
    },
    {
        "slug": "gpu-server-manager", "no": "05", "tag": "SYSTEMS · C", "title": "GPU-Server-Manager",
        "desc": ["Quản lý & phân bổ tài nguyên máy chủ", "GPU — bài tập lớn lập trình C."],
        "chips": ["C", "Scheduling", "Memory"], "cta": "Source code", "motif": motif_gpu,
    },
    {
        "slug": "shadow-collapse", "no": "06", "tag": "ALGORITHMS · GAME", "title": "Shadow-Collapse",
        "desc": ["Procedural dungeon crawler — sinh", "bản đồ ngẫu nhiên, tìm đường A*."],
        "chips": ["Procedural", "A*", "Game loop"], "cta": "Source code", "motif": motif_dungeon,
    },
]


def build_project(p: dict, idx: int) -> str:
    W, H = 580, 260
    motif, mcss = p["motif"]()
    chips = ""
    x = 28
    for ch in p["chips"]:
        w = mono_w(ch, 11.5) + 22
        chips += pill(x, 168, w, ch, MUTED, size=11.5, h=24)
        x += w + 8
    cta_col = CYAN if p["cta"] == "Live demo" else VIOLET
    title_size = 26 if len(p["title"]) < 16 else 22
    body = f"""
{frame(0, 0, W, H, dur=9, delay=idx*1.5)}
<text x="28" y="44" class="mono" font-size="12" letter-spacing="2" fill="{CYAN}">{p['no']} <tspan fill="{DIM}">—</tspan> {p['tag']}</text>
<text x="28" y="86" class="sans" font-size="{title_size}" font-weight="700" fill="{TEXT}">{p['title']}</text>
<text x="28" y="118" class="sans" font-size="15" fill="{MUTED}">{esc(p['desc'][0])}</text>
<text x="28" y="140" class="sans" font-size="15" fill="{MUTED}">{esc(p['desc'][1])}</text>
{chips}
<text x="28" y="226" class="sans" font-size="14" font-weight="600" fill="{cta_col}">{p['cta']} <tspan class="arrow">↗</tspan></text>
<rect x="350" y="24" width="206" height="212" rx="14" fill="{INSET}" stroke="{LINE}"/>
<g transform="translate(350 24)">{motif}</g>
"""
    css = mcss + """
  .arrow{animation:arr 2.4s ease-in-out infinite}
  @keyframes arr{0%,100%{opacity:.6}50%{opacity:1}}
"""
    return svg(W, H, f"{p['title']} — project card", "", css, body)


# ---------------------------------------------------------------- timeline
def build_timeline() -> str:
    W, H = 1200, 250
    items = [
        ("07 · 2025", "Gia nhập GitHub", "Bắt đầu hành trình"),
        ("03 · 2026", "Nền tảng C / C++", "ProjectChess · Code_C"),
        ("05 · 2026", "GPU-Server-Manager", "Bài tập lớn lập trình C"),
        ("07 · 2026", "Web &amp; Next.js", "Shadow-Collapse · NextGPU"),
        ("09 · 2026", "AI &amp; Vision", "face-attendance · ResearchAI"),
        ("11 · 2026", "41+ repositories", "Chess online · Web-xem-phim"),
    ]
    x0, x1, ly = 100, 1100, 118
    step = (x1 - x0) / (len(items) - 1)
    nodes = ""
    for i, (date, title, sub) in enumerate(items):
        x = x0 + i * step
        last = i == len(items) - 1
        col = CYAN if i % 2 == 0 else VIOLET
        ring = (f'<circle cx="{x}" cy="{ly}" r="10" stroke="{GREEN}" stroke-width="1.5">'
                f'<animate attributeName="r" values="8;20" dur="2s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values=".9;0" dur="2s" repeatCount="indefinite"/></circle>') if last else ""
        nodes += (
            f'<g class="fu" style="animation-delay:{0.35 + i*0.32:.2f}s">'
            f'<text x="{x}" y="{ly-30}" text-anchor="middle" class="mono" font-size="13" fill="{GREEN if last else col}">{date}</text>'
            f'{ring}<circle cx="{x}" cy="{ly}" r="8" fill="{BG1}" stroke="{GREEN if last else col}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{ly}" r="3" fill="{GREEN if last else col}"/>'
            f'<text x="{x}" y="{ly+40}" text-anchor="middle" class="sans" font-size="16" font-weight="700" fill="{TEXT}">{title}</text>'
            f'<text x="{x}" y="{ly+62}" text-anchor="middle" class="sans" font-size="13.5" fill="{MUTED}">{sub}</text>'
            f"</g>"
        )
    css = """
  .line{stroke-dasharray:1000;stroke-dashoffset:1000;animation:ln 2.2s .2s cubic-bezier(.6,0,.2,1) forwards}
  @keyframes ln{to{stroke-dashoffset:0}}
"""
    body = f"""
{frame(0, 0, W, H, dur=14)}
<text x="36" y="40" class="mono" font-size="12" letter-spacing="2.5" fill="{CYAN}">JOURNEY // 2025 → NOW</text>
<path d="M{x0} {ly}H{x1}" stroke="{LINE}" stroke-width="2"/>
<path d="M{x0} {ly}H{x1}" stroke="url(#accent)" stroke-width="2" pathLength="1000" class="line"/>
<circle r="4" fill="#FFFFFF" opacity=".9"><animateMotion dur="7s" begin="2.4s" repeatCount="indefinite" path="M{x0} {ly}H{x1}"/>
  <animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.1;.9;1" dur="7s" begin="2.4s" repeatCount="indefinite"/></circle>
{nodes}
"""
    return svg(W, H, "Journey timeline", "", css, body)


# ---------------------------------------------------------------- divider / footer
def build_divider() -> str:
    W, H = 1200, 24
    defs = (f'<linearGradient id="fadeLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LINE}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#2B3760"/><stop offset="1" stop-color="{LINE}" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="glow"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>')
    body = (f'<path d="M0 12H{W}" stroke="url(#fadeLine)"/>'
            f'<ellipse cy="12" rx="60" ry="2.5" fill="url(#glow)">'
            f'<animate attributeName="cx" values="-80;1280" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1"/></ellipse>'
            f'<g transform="translate(600 12)"><rect x="-4" y="-4" width="8" height="8" transform="rotate(45)" fill="{BG0}" stroke="url(#accent)" stroke-width="1.4"/></g>')
    return svg(W, H, "divider", defs, "", body)


def build_footer() -> str:
    W, H = 1200, 230
    words = ["LEARN", "BUILD", "BREAK", "UNDERSTAND", "IMPROVE"]
    spans = ""
    for i, w in enumerate(words):
        if i:
            spans += f'<tspan fill="{DIM}">  ·  </tspan>'
        spans += f'<tspan class="w" style="animation-delay:{i*1.2:.1f}s">{w}</tspan>'
    waves = ""
    for i, (amp, col, dur, op) in enumerate([(14, CYAN, 9, .35), (20, VIOLET, 12, .28), (10, BLUE, 7, .22)]):
        base = 196 + i * 6
        a = f"M0 {base} C300 {base-amp} 600 {base+amp} 900 {base} S1200 {base-amp} 1200 {base}"
        b = f"M0 {base} C300 {base+amp} 600 {base-amp} 900 {base} S1200 {base+amp} 1200 {base}"
        waves += (f'<path d="{a}" stroke="{col}" stroke-opacity="{op}" stroke-width="1.5">'
                  f'<animate attributeName="d" values="{a};{b};{a}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" '
                  f'keySplines=".45 0 .55 1;.45 0 .55 1"/></path>')
    css = f"""
  .w{{fill:{DIM};animation:w 6s ease-in-out infinite}}
  @keyframes w{{0%,30%,100%{{fill:{DIM}}}10%,20%{{fill:{CYAN}}}}}
"""
    body = f"""
<defs><clipPath id="fc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="24"/></clipPath></defs>
{frame(0, 0, W, H, rx=24, dur=14)}
<g clip-path="url(#fc)">{waves}</g>
<text x="600" y="78" text-anchor="middle" class="mono" font-size="20" letter-spacing="3" font-weight="700">{spans}</text>
<text x="600" y="122" text-anchor="middle" class="sans" font-size="24" font-weight="700" fill="{TEXT}">Cảm ơn bạn đã ghé thăm</text>
<text x="600" y="154" text-anchor="middle" class="sans" font-size="17" fill="{MUTED}">Hẹn gặp ở commit tiếp theo <tspan fill="{PINK}" class="pulse">♥</tspan></text>
"""
    return svg(W, H, "Footer — thanks for visiting", "", css, body)


# ---------------------------------------------------------------- driver
def write(name: str, content: str) -> None:
    path = OUT / name
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({len(content):,} bytes)")


def main() -> None:
    write("hero.svg", build_hero())
    write("about.svg", build_about())
    write("timeline.svg", build_timeline())
    write("divider.svg", build_divider())
    write("footer.svg", build_footer())
    for i, p in enumerate(PROJECTS):
        write(f"project-{p['slug']}.svg", build_project(p, i))


if __name__ == "__main__":
    main()
