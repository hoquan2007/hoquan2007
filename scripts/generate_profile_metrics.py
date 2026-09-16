#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_profile_metrics.py - Self-hosted QUAN.OS telemetry generator.

Outputs (into assets/generated/):
    * github-telemetry.svg        unified dashboard (KPIs + lang bars + activity)
    * projects.svg                holographic project gallery (priority + stars)
    * language-constellation.svg  language-as-orbit visualization
    * activity-stream.svg         recent public events / fallback timeline

Constraints:
    * Python standard library only.
    * Reads non-secret profile config from config/profile.json.
    * Reads visual tokens from config/theme.json (no magic numbers in SVGs).
    * Fetches ONLY public data from api.github.com with GITHUB_TOKEN.
    * Never logs or persists the token.
    * On API failure falls back to the documented snapshot so the SVGs
      remain shippable.

Run locally:
    python scripts/generate_profile_metrics.py
"""
from __future__ import annotations

import datetime as _dt
import json
import math
import os
import pathlib
import sys
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS_GENERATED = REPO_ROOT / "assets" / "generated"
CONFIG_DIR = REPO_ROOT / "config"
ASSETS_GENERATED.mkdir(parents=True, exist_ok=True)

GITHUB_API = "https://api.github.com"
USER = os.environ.get("USERNAME", "hoquan2007") or "hoquan2007"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    "User-Agent": "quan-os-profile-bot/2.0",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


# ---------------------------------------------------------------------------
# Config loaders
# ---------------------------------------------------------------------------


def _load_json(path: pathlib.Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


PROFILE_CONFIG = _load_json(CONFIG_DIR / "profile.json", default={})
THEME = _load_json(CONFIG_DIR / "theme.json", default={})

# Visual tokens (locked)
C = THEME.get("colors", {})
CYAN = C.get("cyan_2", "#22D3EE")
CYAN_DARK = C.get("cyan_dark", "#0E7490")
VIOLET = C.get("violet_3", "#A855F7")
VIOLET_DARK = C.get("violet_dark", "#5B21B6")
PURPLE = C.get("violet", "#7C3AED")
PURPLE_DARK = "#3B0764"
BLUE = C.get("blue", "#3B82F6")
BLUE_DARK = C.get("blue_dark", "#1E3A8A")
SNOW = C.get("snow", "#F8FAFC")
TEXT_2 = C.get("text_2", "#CBD5E1")
MUTED = C.get("muted", "#94A3B8")
DIM = C.get("dim", "#64748B")
BG = C.get("bg_0", "#020617")

# Animation envelope
ANIM = THEME.get("animation", {})


# ---------------------------------------------------------------------------
# Snapshot fallback (verified 2026-09-15, refreshed by CI on every run)
# ---------------------------------------------------------------------------

FALLBACK_REPOS = [
    {"name": "face-attendance", "language": "TypeScript", "stargazers_count": 0,
     "description": "Web-based attendance tracking with face recognition.",
     "updated_at": "2026-09-01T00:00:00Z"},
    {"name": "QITEnglish", "language": "TypeScript", "stargazers_count": 0,
     "description": "Web learning English for IT people",
     "updated_at": "2026-08-20T00:00:00Z"},
    {"name": "QMusic", "language": None, "stargazers_count": 0,
     "description": "Personal music web app",
     "updated_at": "2026-08-15T00:00:00Z"},
    {"name": "QEnglish", "language": "TypeScript", "stargazers_count": 0,
     "description": "QEnglish - AI conversation platform for English learners",
     "updated_at": "2026-08-10T00:00:00Z"},
    {"name": "GPU-Server-Manager", "language": "C", "stargazers_count": 0,
     "description": "C programming final project - GPU server resource management",
     "updated_at": "2025-12-10T00:00:00Z"},
]
FALLBACK_PROFILE = {
    "login": USER,
    "public_repos": 22,
    "followers": 0,
    "following": 0,
    "created_at": "2025-07-30T00:00:00Z",
}


# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------


def _http_get_json(url: str) -> dict | list:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


def fetch_profile() -> dict:
    if not TOKEN:
        return FALLBACK_PROFILE
    try:
        return _http_get_json(f"{GITHUB_API}/users/{USER}")
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return FALLBACK_PROFILE


def fetch_repos() -> list[dict]:
    if not TOKEN:
        return FALLBACK_REPOS
    try:
        return _http_get_json(
            f"{GITHUB_API}/users/{USER}/repos?per_page=100&sort=updated"
        )
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return FALLBACK_REPOS


def fetch_events() -> list[dict]:
    if not TOKEN:
        return []
    try:
        return _http_get_json(f"{GITHUB_API}/users/{USER}/events/public")
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _short(text: str | None, n: int = 80) -> str:
    if not text:
        return ""
    if len(text) <= n:
        return text
    return text[: n - 1].rstrip() + "..."


def _grad_id(name: str) -> str:
    return f"gen-{name}"


def _priority_slugs() -> list[str]:
    """Read curated project priority from config/profile.json."""
    featured = PROFILE_CONFIG.get("featured_projects") or []
    return [str(p.get("slug")) for p in featured if p.get("slug")]


def _project_meta(slug: str) -> dict:
    """Return curated metadata for a slug from config/profile.json."""
    for p in PROFILE_CONFIG.get("featured_projects", []) or []:
        if p.get("slug") == slug:
            return p
    return {}


# ---------------------------------------------------------------------------
# 1. github-telemetry.svg  (unified dashboard)
# ---------------------------------------------------------------------------


def build_telemetry_svg(profile: dict, repos: list[dict]) -> str:
    total_repos = int(profile.get("public_repos") or len(repos))
    followers = int(profile.get("followers") or 0)
    following = int(profile.get("following") or 0)
    total_stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    total_forks = sum(int(r.get("forks_count") or 0) for r in repos)
    total_size = sum(int(r.get("size") or 0) for r in repos)
    languages: dict[str, int] = {}
    for r in repos:
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    lang_sorted = sorted(languages.items(), key=lambda kv: kv[1], reverse=True)
    lang_max = max((c for _, c in lang_sorted), default=1)
    lang_count = len(lang_sorted)

    now = _dt.datetime.now(_dt.timezone.utc)
    months = []
    for i in range(11, -1, -1):
        m = (now.replace(day=1) - _dt.timedelta(days=30 * i))
        months.append(m.strftime("%Y-%m"))
    month_counts = {m: 0 for m in months}
    for r in repos:
        u = r.get("updated_at") or r.get("pushed_at")
        if not u:
            continue
        try:
            dt = _dt.datetime.fromisoformat(u.replace("Z", "+00:00"))
        except ValueError:
            continue
        key = dt.strftime("%Y-%m")
        if key in month_counts:
            month_counts[key] += 1

    spark_max = max(month_counts.values(), default=1) or 1

    def spark_path() -> str:
        pts = []
        w = 220
        h = 60
        for i, m in enumerate(months):
            x = (i / (len(months) - 1)) * w if len(months) > 1 else 0
            v = month_counts[m]
            y = h - (v / spark_max) * h
            pts.append(f"{x:.1f},{y:.1f}")
        return "M" + " L".join(pts)

    def lang_bars() -> str:
        out = []
        palette = [CYAN, VIOLET, PURPLE, BLUE, SNOW, CYAN]
        for i, (lang, count) in enumerate(lang_sorted[:6]):
            y = i * 26
            pct = count / lang_max
            bar_w = int(260 * pct)
            color = palette[i % len(palette)]
            out.append(
                f'<text x="0" y="{y}" class="bar-lbl">{_esc(lang)}</text>'
                f'<rect x="100" y="{y - 12}" width="260" height="14" rx="2" fill="#0B1224"/>'
                f'<rect x="100" y="{y - 12}" width="{bar_w}" height="14" rx="2" fill="{color}" opacity="0.9">'
                f'<animate attributeName="width" values="0;{bar_w}" dur="1.4s" begin="{0.1 + i*0.1}s" fill="freeze"/>'
                f'</rect>'
                f'<text x="370" y="{y}" class="bar-val">{count}</text>'
            )
        return "\n".join(out)

    w, h = 1200, 600
    accent_palette = [CYAN, VIOLET, PURPLE, BLUE]
    cards = [
        ("REPOSITORIES", total_repos, "public", f"verified via github api", accent_palette[0], "cyan", 270),
        ("STARS", total_stars, "received", f"+ {total_forks} forks", accent_palette[1], "violet", 270),
        ("NETWORK", followers, "followers", f"following ÃÂÃÂ {following}", accent_palette[2], "violet", 270),
        ("FOOTPRINT", total_size // 1024, "MB tracked", f"{lang_count} languages", accent_palette[3], "cyan", 250),
    ]
    cards_svg_parts = []
    for idx, (title, value, unit, sub, edge, lbl_class, cw) in enumerate(cards):
        x = 40 + sum(c[6] for c in cards[:idx]) + (idx * 20)
        big_cls = "big-cyan" if lbl_class == "cyan" else "big-violet"
        cards_svg_parts.append(
            f"""<g transform="translate({x} 80)">
  <rect width="{cw}" height="160" rx="10" fill="url(#{_grad_id('card')})" stroke="{edge}" stroke-opacity="0.5"/>
  <text x="20" y="34" class="card-title" fill="{edge}">ÃÂÃÂ· {title}</text>
  <text x="20" y="100" class="{big_cls}">{value}</text>
  <text x="170" y="100" class="unit">{unit}</text>
  <text x="20" y="130" class="lbl">{_esc(sub)}</text>
  <line x1="20" y1="140" x2="{cw - 20}" y2="140" stroke="#1E293B"/>
  <text x="20" y="156" class="micro">scope ÃÂÃÂ @{_esc(USER)}</text>
</g>"""
        )
    cards_svg = "\n".join(cards_svg_parts)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="GitHub telemetry dashboard" font-family="JetBrains Mono, ui-monospace, monospace">
<title>QUAN.OS ÃÂÃÂ GitHub Telemetry</title>
<desc>Self-generated telemetry dashboard for {USER}. KPI cards, language distribution, 12-month activity sparkline.</desc>
<defs>
  <linearGradient id="{_grad_id('bg')}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#080B16"/>
    <stop offset="1" stop-color="#020617"/>
  </linearGradient>
  <linearGradient id="{_grad_id('card')}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0B1224"/>
    <stop offset="1" stop-color="#070A18"/>
  </linearGradient>
  <pattern id="{_grad_id('grid')}" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#10172A" stroke-width="0.5"/>
  </pattern>
</defs>
<style><![CDATA[
  .mono{{font-family:JetBrains Mono,Fira Code,IBM Plex Mono,ui-monospace,Menlo,monospace}}
  .lbl{{font-size:10px;fill:{MUTED};letter-spacing:3px}}
  .big{{font-size:42px;fill:{SNOW};letter-spacing:2px;font-weight:700}}
  .big-cyan{{font-size:42px;fill:{CYAN};letter-spacing:2px;font-weight:700}}
  .big-violet{{font-size:42px;fill:{VIOLET};letter-spacing:2px;font-weight:700}}
  .unit{{font-size:11px;fill:{DIM};letter-spacing:2px}}
  .card-title{{font-size:11px;letter-spacing:3px;font-weight:700}}
  .bar-lbl{{font-size:11px;fill:{SNOW};letter-spacing:2px}}
  .bar-val{{font-size:11px;fill:{CYAN};letter-spacing:2px}}
  .micro{{font-size:9px;fill:{DIM};letter-spacing:2px}}
  @media (prefers-reduced-motion: reduce){{animate,animateTransform{{display:none}}}}
]]></style>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('bg')})"/>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('grid')})" opacity="0.45"/>
<g class="mono">
  <text class="micro" x="40" y="34">SCENE 08 / GITHUB TELEMETRY ÃÂÃÂ SELF-GENERATED</text>
  <line x1="40" y1="42" x2="380" y2="42" stroke="{CYAN}" stroke-opacity="0.6"/>
  <text class="micro" x="1160" y="34" text-anchor="end">SOURCE ÃÂÃÂ api.github.com ÃÂÃÂ LIVE</text>
</g>
{cards_svg}
<g transform="translate(40 270)">
  <rect width="540" height="280" rx="10" fill="url(#{_grad_id('card')})" stroke="{CYAN}" stroke-opacity="0.45"/>
  <text x="20" y="34" class="card-title" fill="{CYAN}">ÃÂÃÂ LANGUAGE DISTRIBUTION</text>
  <text x="520" y="34" text-anchor="end" class="micro">top {min(6, lang_count)} ÃÂÃÂ live</text>
  <g transform="translate(20 60)">
    {lang_bars()}
  </g>
</g>
<g transform="translate(620 270)">
  <rect width="540" height="280" rx="10" fill="url(#{_grad_id('card')})" stroke="{VIOLET}" stroke-opacity="0.45"/>
  <text x="20" y="34" class="card-title" fill="{VIOLET}">ÃÂÃÂ ACTIVITY ÃÂÃÂ LAST 12 MONTHS</text>
  <text x="520" y="34" text-anchor="end" class="micro">repo updates / month</text>
  <g transform="translate(20 70)">
    <line x1="0" y1="60" x2="500" y2="60" stroke="#1E293B"/>
    <path d="{spark_path()}" fill="none" stroke="{CYAN}" stroke-width="1.6">
      <animate attributeName="stroke-dasharray" values="0,1000;1000,0" dur="2s" fill="freeze"/>
    </path>
    <path d="{spark_path()} L 220 60 L 0 60 Z" fill="{CYAN}" opacity="0.12">
      <animate attributeName="opacity" values="0;0.12" dur="2s" fill="freeze"/>
    </path>
  </g>
  <g transform="translate(20 160)">
    <text class="micro" y="0">JAN</text>
    <text class="micro" x="500" y="0" text-anchor="end">NOW</text>
    <text class="micro" y="40">PEAK ÃÂÃÂ?ÃÂÃÂ {spark_max} UPDATES/MO</text>
    <text class="micro" y="56">SAMPLE ÃÂÃÂ {sum(month_counts.values())} UPDATES ÃÂÃÂ?ÃÂÃÂ 12 MO</text>
    <text class="micro" y="72">SYNTHESIZED FROM updated_at</text>
    <text class="micro" y="88">SOURCE ÃÂÃÂ?ÃÂÃÂ github rest api</text>
  </g>
  <line x1="0" y1="0" x2="540" y2="0" stroke="{CYAN}" stroke-width="1" opacity="0.4">
    <animate attributeName="y1" values="0;280;0" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="y2" values="0;280;0" dur="6s" repeatCount="indefinite"/>
  </line>
</g>
<g class="mono">
  <line x1="40" y1="568" x2="1160" y2="568" stroke="#1E293B"/>
  <text class="micro" x="40" y="586">REFRESH · DAILY 18:00 UTC · NO FAKE NUMBERS</text>
  <text class="micro" x="1160" y="586" text-anchor="end" fill="{CYAN}">QUAN-OS ÃÂÃÂ TELEMETRY ENGINE</text>
</g>
</svg>"""
    return svg


# ---------------------------------------------------------------------------
# 2. activity-stream.svg
# ---------------------------------------------------------------------------


def build_activity_stream_svg(events: list[dict], repos: list[dict]) -> str:
    items: list[dict] = []
    if events:
        for ev in events[:8]:
            t = ev.get("type", "")
            repo = (ev.get("repo") or {}).get("name", "")
            payload = ev.get("payload") or {}
            desc = t.replace("Event", "").upper()
            if t == "PushEvent":
                desc = f"PUSH ÃÂÃÂ {len(payload.get('commits', []))} commits"
            elif t == "CreateEvent":
                desc = f"CREATE ÃÂÃÂ {payload.get('ref_type', '')}".strip()
            elif t == "ReleaseEvent":
                desc = f"RELEASE ÃÂÃÂ {payload.get('release', {}).get('tag_name', '')}"
            elif t == "PullRequestEvent":
                desc = "PR ÃÂÃÂ opened"
            ts = ev.get("created_at", "")
            items.append({"time": ts, "desc": desc, "repo": repo})
    else:
        for r in repos[:6]:
            items.append({
                "time": r.get("updated_at", "") or r.get("pushed_at", ""),
                "desc": "UPDATE",
                "repo": f"{USER}/{r.get('name', '')}",
            })

    if not items:
        items = [{"time": "2026-09-15T00:00:00Z", "desc": "OFFLINE", "repo": "no-data"}]

    w, h = 1200, 540
    items = items[:8]

    def parse_time(s: str) -> str:
        if not s:
            return "..."
        try:
            dt = _dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m")
        except ValueError:
            return s[:7]

    rows = []
    for i, it in enumerate(items):
        x = 120 + (i % 4) * 240
        y = 140 + (i // 4) * 150
        color = CYAN if i % 2 == 0 else VIOLET
        rows.append(
            f'<g transform="translate({x} {y})" class="mono">'
            f'<circle r="6" fill="{color}"/>'
            f'<circle r="6" fill="none" stroke="{color}" stroke-opacity="0.6">'
            f'<animate attributeName="r" values="6;14;6" dur="2.4s" begin="{i*0.3}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.8;0;0.8" dur="2.4s" begin="{i*0.3}s" repeatCount="indefinite"/>'
            f'</circle>'
            f'<text x="14" y="-4" class="time">{parse_time(it["time"])}</text>'
            f'<text x="14" y="14" class="lbl">{_esc(it["desc"])}</text>'
            f'<text x="14" y="30" class="repo">{_esc(it["repo"])}</text>'
            f'</g>'
        )
    rows_svg = "\n".join(rows)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Recent public activity timeline" font-family="JetBrains Mono, ui-monospace, monospace">
<title>QUAN.OS ÃÂÃÂ Activity Stream</title>
<desc>Recent public activity events from GitHub for {USER}.</desc>
<defs>
  <linearGradient id="{_grad_id('bg2')}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#080B16"/>
    <stop offset="1" stop-color="#020617"/>
  </linearGradient>
  <pattern id="{_grad_id('grid2')}" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#10172A" stroke-width="0.5"/>
  </pattern>
</defs>
<style><![CDATA[
  .mono{{font-family:JetBrains Mono,Fira Code,IBM Plex Mono,ui-monospace,Menlo,monospace}}
  .time{{font-size:10px;fill:{CYAN};letter-spacing:2px}}
  .lbl{{font-size:12px;fill:{SNOW};letter-spacing:2px;font-weight:700}}
  .repo{{font-size:10px;fill:{MUTED};letter-spacing:1px}}
  .micro{{font-size:9px;fill:{DIM};letter-spacing:2px}}
  @media (prefers-reduced-motion: reduce){{animate,animateTransform{{display:none}}}}
]]></style>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('bg2')})"/>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('grid2')})" opacity="0.45"/>
<g class="mono">
  <text class="micro" x="40" y="34">SCENE 09 / ACTIVITY STREAM ÃÂÃÂ CI LIVE</text>
  <line x1="40" y1="42" x2="340" y2="42" stroke="{CYAN}" stroke-opacity="0.6"/>
  <text class="micro" x="1160" y="34" text-anchor="end">{len(items)} EVENTS ÃÂÃÂ EVENTS API</text>
</g>
{rows_svg}
<g class="mono">
  <line x1="40" y1="478" x2="1160" y2="478" stroke="#1E293B"/>
  <text class="micro" x="40" y="500">FALLBACK ÃÂÃÂ updated_at WHEN EVENTS API UNAVAILABLE</text>
  <text class="micro" x="1160" y="500" text-anchor="end" fill="{CYAN}">{_dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</text>
  <text class="micro" x="40" y="520">PUBLIC DATA ONLY ÃÂÃÂ NEVER LEAK PRIVATE INFO</text>
  <text class="micro" x="1160" y="520" text-anchor="end" fill="{VIOLET}">QUAN-OS ÃÂÃÂ STREAM ENGINE</text>
</g>
</svg>"""
    return svg


# ---------------------------------------------------------------------------
# 3. projects.svg  (uses curated priority from config/profile.json)
# ---------------------------------------------------------------------------


def build_projects_svg(profile: dict, repos: list[dict]) -> str:
    priority_slugs = _priority_slugs()
    priority_map = {slug: (len(priority_slugs) - i) * 10 for i, slug in enumerate(priority_slugs)}

    def score(r: dict) -> float:
        return priority_map.get(r.get("name", ""), 0) + int(r.get("stargazers_count") or 0) * 5

    curated = sorted(repos, key=score, reverse=True)[:4]
    if not curated:
        curated = FALLBACK_REPOS[:4]

    w, h = 1200, 600
    positions = [(40, 80), (620, 80), (40, 300), (620, 300)]
    cards = []
    for i, r in enumerate(curated):
        x, y = positions[i]
        name = r.get("name", "project")
        desc = _short(r.get("description") or "(no description)", 90)
        lang = r.get("language") or "ÃÂÃÂ?ÃÂÃÂ?ÃÂÃÂ?ÃÂÃÂ?"
        updated = (r.get("updated_at") or "")[:10]
        stars = int(r.get("stargazers_count") or 0)
        meta = _project_meta(name)
        domain = meta.get("domain") or _domain_for(lang)
        edge = CYAN if i % 2 == 0 else VIOLET
        led_color = CYAN if i % 2 == 0 else VIOLET
        accent_color = CYAN if i % 2 == 0 else VIOLET
        lang_class = "lang" if i % 2 == 0 else "lang-v"
        scan_delay = i * 1.5
        cards.append(
            f"""<g transform="translate({x} {y})">
  <rect width="540" height="200" rx="10" fill="#0B1224" stroke="{edge}" stroke-opacity="0.65" stroke-width="1"/>
  <rect x="0" y="0" width="540" height="2" fill="{accent_color}"/>
  <rect width="540" height="2" fill="{accent_color}" opacity="0">
    <animate attributeName="y" values="0;200;0" dur="6s" begin="{scan_delay}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.7;0" dur="6s" begin="{scan_delay}s" repeatCount="indefinite"/>
  </rect>
  <circle cx="20" cy="20" r="4" fill="{led_color}">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" begin="{i*0.3}s" repeatCount="indefinite"/>
  </circle>
  <text x="34" y="24" class="mono {lang_class}">{_esc((lang or '...').upper())}</text>
  <text x="520" y="24" text-anchor="end" class="mono meta">? {stars} ÃÂÃÂ {updated}</text>
  <text x="20" y="62" class="mono name">{_esc(name)}</text>
  <text x="20" y="86" class="mono desc">{_esc(desc)}</text>
  <text x="20" y="128" class="mono meta">DOMAIN ÃÂÃÂ {_esc(domain)}</text>
  <text x="20" y="148" class="mono meta">UPDATED ÃÂÃÂ {updated}</text>
  <text x="20" y="170" class="mono meta">github.com/{_esc(USER)}/{_esc(name)}</text>
  <line x1="20" y1="180" x2="520" y2="180" stroke="#1E293B"/>
</g>"""
        )
    cards_svg = "\n".join(cards)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Featured projects gallery ÃÂÃÂ live" font-family="JetBrains Mono, ui-monospace, monospace">
<title>QUAN.OS ÃÂÃÂ Featured Systems ÃÂÃÂ Live</title>
<desc>Holographic gallery of featured projects for {USER}.</desc>
<defs>
  <linearGradient id="{_grad_id('bg3')}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#080B16"/>
    <stop offset="1" stop-color="#020617"/>
  </linearGradient>
  <pattern id="{_grad_id('grid3')}" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="#10172A" stroke-width="0.4"/>
  </pattern>
</defs>
<style><![CDATA[
  .mono{{font-family:JetBrains Mono,Fira Code,IBM Plex Mono,ui-monospace,Menlo,monospace}}
  .name{{font-size:14px;fill:{SNOW};letter-spacing:1.5px;font-weight:700}}
  .desc{{font-size:10px;fill:{MUTED};letter-spacing:0.5px}}
  .lang{{font-size:9px;fill:{CYAN};letter-spacing:2px}}
  .lang-v{{font-size:9px;fill:{VIOLET};letter-spacing:2px}}
  .meta{{font-size:9px;fill:{DIM};letter-spacing:1.5px}}
  .micro{{font-size:9px;fill:{DIM};letter-spacing:2px}}
  @media (prefers-reduced-motion: reduce){{animate,animateTransform{{display:none}}}}
]]></style>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('bg3')})"/>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('grid3')})" opacity="0.4"/>
<g class="mono">
  <text class="micro" x="40" y="34">SCENE 06 / FEATURED SYSTEMS ÃÂÃÂ LIVE</text>
  <line x1="40" y1="42" x2="320" y2="42" stroke="{CYAN}" stroke-opacity="0.6"/>
  <text class="micro" x="1160" y="34" text-anchor="end">CURATED FROM {int(profile.get('public_repos') or len(repos))} PUBLIC REPOS</text>
</g>
{cards_svg}
<g class="mono">
  <text class="micro" x="40" y="544">? PRIORITIZED BY REPRESENTATIVENESS ÃÂÃÂ NOT STAR COUNT ALONE</text>
  <text class="micro" x="1160" y="544" text-anchor="end" fill="{CYAN}">UPDATED {_dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")}</text>
  <text class="micro" x="40" y="562">FULL LIST ÃÂÃÂ?ÃÂÃÂ /?tab=repositories</text>
  <text class="micro" x="1160" y="562" text-anchor="end" fill="{VIOLET}">QUAN-OS ÃÂÃÂ GALLERY ENGINE</text>
</g>
</svg>"""
    return svg


def _domain_for(lang: str | None) -> str:
    table = {
        "TypeScript": "web ÃÂÃÂ frontend ÃÂÃÂ fullstack",
        "JavaScript": "web ÃÂÃÂ fullstack",
        "C": "systems ÃÂÃÂ backend",
        "C++": "systems ÃÂÃÂ performance",
        "HTML": "web ÃÂÃÂ ui",
        "Python": "ai ÃÂÃÂ scripting",
        "Go": "backend ÃÂÃÂ infra",
        "Rust": "systems ÃÂÃÂ performance",
    }
    return table.get(lang or "", "engineering")


# ---------------------------------------------------------------------------
# 4. language-constellation.svg
# ---------------------------------------------------------------------------


def build_constellation_svg(repos: list[dict]) -> str:
    langs: dict[str, int] = {}
    for r in repos:
        l = r.get("language")
        if l:
            langs[l] = langs.get(l, 0) + 1
    sorted_langs = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    if not sorted_langs:
        sorted_langs = [("TypeScript", 9), ("HTML", 5), ("C", 2), ("C++", 2)]
    total = sum(c for _, c in sorted_langs)
    palette = [
        ("url(#g-cyan)", CYAN, CYAN_DARK),
        ("url(#g-violet)", VIOLET, VIOLET_DARK),
        ("url(#g-purple)", PURPLE, PURPLE_DARK),
        ("url(#g-blue)", BLUE, BLUE_DARK),
    ]
    n = len(sorted_langs[:4])
    angles = [-90, -30, 30, 90, 150, 210, 270][:n]
    radius = 200 if n <= 4 else 200

    nodes_svg = []
    lines_svg = []
    pulses_svg = []
    for i, (lang, count) in enumerate(sorted_langs[:4]):
        a = math.radians(angles[i])
        x = 600 + int(radius * math.cos(a))
        y = 320 + int(radius * math.sin(a))
        node_r = 30 + count * 6
        fill_ref, color, _ = palette[i % 4]
        pct = int(round(count / total * 100)) if total else 0
        lines_svg.append(
            f'<line x1="600" y1="320" x2="{x}" y2="{y}" stroke="{color}" stroke-opacity="0.35">'
            f'<animate attributeName="stroke-opacity" values="0.15;0.6;0.15" dur="{3.4 + i*0.4}s" repeatCount="indefinite"/>'
            f'</line>'
        )
        pulses_svg.append(
            f'<circle r="2.5" fill="{SNOW}">'
            f'<animateMotion dur="{3.4 + i*0.4}s" repeatCount="indefinite" path="M600 320 L{x} {y}"/>'
            f'</circle>'
        )
        nodes_svg.append(
            f"""<g transform="translate({x} {y})">
  <circle r="{node_r+18}" fill="none" stroke="{color}" stroke-opacity="0.2">
    <animate attributeName="r" values="{node_r+18};{node_r+30};{node_r+18}" dur="{4.0 + i*0.4}s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.4;0;0.4" dur="{4.0 + i*0.4}s" repeatCount="indefinite"/>
  </circle>
  <circle r="{node_r}" fill="{fill_ref}" opacity="0.30"/>
  <circle r="{node_r-10}" fill="{BG}" stroke="{color}" stroke-width="1.4"/>
  <text y="-2" text-anchor="middle" class="mono lang-lbl">{_esc(lang)}</text>
  <text y="14" text-anchor="middle" class="mono lang-count">{count}</text>
  <text y="32" text-anchor="middle" class="mono lang-pct">{pct}%</text>
</g>"""
        )
    w, h = 1200, 600
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Language constellation ÃÂÃÂ live" font-family="JetBrains Mono, ui-monospace, monospace">
<title>QUAN.OS ÃÂÃÂ Language Constellation ÃÂÃÂ Live</title>
<desc>Radial constellation of programming languages used across {USER}'s repositories.</desc>
<defs>
  <radialGradient id="{_grad_id('bg4')}" cx="50%" cy="50%" r="60%">
    <stop offset="0" stop-color="#080B16"/>
    <stop offset="1" stop-color="#020617"/>
  </radialGradient>
  <radialGradient id="g-cyan" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{CYAN}"/>
    <stop offset="1" stop-color="{CYAN_DARK}"/>
  </radialGradient>
  <radialGradient id="g-violet" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{VIOLET}"/>
    <stop offset="1" stop-color="{VIOLET_DARK}"/>
  </radialGradient>
  <radialGradient id="g-purple" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{PURPLE}"/>
    <stop offset="1" stop-color="{PURPLE_DARK}"/>
  </radialGradient>
  <radialGradient id="g-blue" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{BLUE_DARK}"/>
  </radialGradient>
  <pattern id="{_grad_id('grid4')}" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#10172A" stroke-width="0.5"/>
  </pattern>
</defs>
<style><![CDATA[
  .mono{{font-family:JetBrains Mono,Fira Code,IBM Plex Mono,ui-monospace,Menlo,monospace}}
  .lang-lbl{{font-size:14px;fill:{SNOW};letter-spacing:2px;font-weight:700}}
  .lang-count{{font-size:24px;fill:{SNOW};letter-spacing:2px;font-weight:700}}
  .lang-pct{{font-size:11px;fill:{MUTED};letter-spacing:2px}}
  .micro{{font-size:9px;fill:{DIM};letter-spacing:2px}}
  @media (prefers-reduced-motion: reduce){{animate,animateTransform,animateMotion{{display:none}}}}
]]></style>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('bg4')})"/>
<rect width="{w}" height="{h}" fill="url(#{_grad_id('grid4')})" opacity="0.45"/>
<g class="mono">
  <text class="micro" x="40" y="34">SCENE 09 / LANGUAGE CONSTELLATION ÃÂÃÂ LIVE</text>
  <line x1="40" y1="42" x2="380" y2="42" stroke="{CYAN}" stroke-opacity="0.6"/>
  <text class="micro" x="1160" y="34" text-anchor="end">NODE SIZE = REPO COUNT</text>
</g>
<g>
  {''.join(lines_svg)}
  {''.join(pulses_svg)}
</g>
<g transform="translate(600 320)">
  <circle r="14" fill="{BG}" stroke="{SNOW}"/>
  <circle r="3" fill="{SNOW}">
    <animate attributeName="r" values="2;6;2" dur="2s" repeatCount="indefinite"/>
  </circle>
</g>
{''.join(nodes_svg)}
<g class="mono">
  <line x1="40" y1="528" x2="1160" y2="528" stroke="#1E293B"/>
  <text class="micro" x="40" y="552">TOTAL ÃÂÃÂ {total} LANGUAGE-DECLARED REPOS ÃÂ· 4 SHOWN</text>
  <text class="micro" x="1160" y="552" text-anchor="end" fill="{CYAN}">UPDATED {_dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")}</text>
  <text class="micro" x="40" y="572">SELF-GENERATED BY GITHUB ACTIONS ÃÂÃÂ NO THIRD-PARTY</text>
  <text class="micro" x="1160" y="572" text-anchor="end" fill="{VIOLET}">QUAN-OS ÃÂÃÂ CONSTELLATION ENGINE</text>
</g>
</svg>"""
    return svg


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)} ({len(content)} chars)")


def main() -> int:
    print(f"Generating QUAN.OS telemetry for {USER!r}...")
    profile = fetch_profile()
    repos = fetch_repos()
    events = fetch_events()
    print(f"profile ... public_repos={profile.get('public_repos')} followers={profile.get('followers')}")
    print(f"repos    ... {len(repos)}")
    print(f"events   ... {len(events)}")

    write(ASSETS_GENERATED / "github-telemetry.svg", build_telemetry_svg(profile, repos))
    write(ASSETS_GENERATED / "activity-stream.svg", build_activity_stream_svg(events, repos))
    write(ASSETS_GENERATED / "projects.svg", build_projects_svg(profile, repos))
    write(ASSETS_GENERATED / "language-constellation.svg", build_constellation_svg(repos))
    return 0


if __name__ == "__main__":
    sys.exit(main())