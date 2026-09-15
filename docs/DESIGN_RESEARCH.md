# QUAN.OS // Design Research

> Research notes for rebuilding the GitHub Profile of **Hồ Ngọc Quân** as a futuristic AI engineering command center.
> All claims below are derived from public sources and the verified GitHub API snapshot of `hoquan2007` on 2026-09-15.

---

## 1. Verified Identity Facts (DO NOT fabricate beyond this)

| Field | Value |
| --- | --- |
| GitHub handle | `hoquan2007` |
| Display name | `Hồ Ngọc Quân` |
| Public repos | 22 |
| Followers | 0 |
| Following | 0 |
| Account created | 2025-07-30 |
| Total stars across owned repos | 0 |
| Total tracked size | ~671 KB |

**Repository languages (non-forked, with declared `language`):**

| Language | Repo count |
| --- | --- |
| TypeScript | 9 |
| HTML | 5 |
| C | 2 |
| C++ | 2 |

**Notable repositories (verified, descending `updated_at`):**

- `hoquan2007` (profile repo)
- `face-attendance` — TypeScript
- `6651071056.BTLT2` — HTML
- `ResearchAI` — (no language declared)
- `QITEnglish` — TypeScript — *Web học tiếng Anh dành cho dân IT*
- `QMusic` — (no language declared) — *Web nghe nhạc cá nhân*
- `QEnglish` — TypeScript — *QEnglish - Nền tảng học tiếng Anh giao tiếp với AI*
- `HQ-English` — TypeScript
- `Web-xem-phim` — TypeScript — *Tạo một web để xem phim*
- `SOLO-GAME` — HTML
- `HQEnglish` — TypeScript — *WE*
- `EnglishHNQ` — TypeScript — *Web học tiếng Anh*
- `Test-Game-3`, `Test-Game-2`, `Test_game` — HTML (small tests)
- `NEXTGPU-COPY` — TypeScript
- `Shadow-Collapse` — *Procedural Dungeon Crawler*
- `Test-Next-GPU` — TypeScript — *test Git va lenh*
- `GPU-Server-Manager` — C — *Bài tập lớn Kỹ thuật Lập trình C - Hệ thống quản lý tài nguyên máy chủ GPU*
- `ProjectChess` — C
- `Code_C_2` — C++
- `Code_C` — C++

> **Rule:** Any other tech (company, role, certification, achievement, education institution) MUST NOT appear in the profile unless verified through additional public sources during implementation.

---

## 2. GitHub README Hard Limitations (must respect)

GitHub sanitizes profile READMEs heavily. Forbidden techniques:

- `<script>` tags of any kind (including inline)
- Custom stylesheet `<link>` tags
- JavaScript (`onclick`, `onerror`, etc. attributes are stripped)
- Most CSS `position: fixed`, `position: sticky`, parallax, custom cursors
- `<iframe>` (most forms blocked / sandboxed; some still allowed but unreliable)
- `<canvas>`, WebGL, Three.js
- `foreignObject`-based HTML injection
- Mouse / pointer / scroll-driven interactions
- Background audio, video autoplay above 10s
- Embedded `@import` from arbitrary origins
- `style` attribute on most SVG containers is stripped
- `prefers-color-scheme: dark` works on `<picture>` and `<img>` only — not on CSS in HTML

Allowed & encouraged:

- Inline SVG with `<style>` blocks (per-element CSS scoped to that SVG)
- SVG `<animate>`, `<animateTransform>`, `<animateMotion>` (SMIL)
- SVG gradients, filters (`feGaussianBlur`, `feColorMatrix`, `feTurbulence`), `clipPath`, `mask`
- `<picture>` for light/dark variants
- Native Markdown tables, headings, lists, links
- HTML `<img>`, `<picture>`, `<details>`, `<table>`, `<sup>`, `<sub>`
- GitHub Actions for asset generation
- Asset URLs served from the same repo (`raw.githubusercontent.com/...`)

---

## 3. Inspiration Catalog

The following public projects influenced the design language. None of them are copied; only patterns are extracted.

| Reference | Pattern adopted | License / credit |
| --- | --- | --- |
| `Platane/snk` | Snake animation on contribution graph | MIT, credit `Platane/snk` |
| `yoshi389111/github-profile-3d-contrib` | Isometric contribution skyline | MIT, credit `yoshi389111` |
| `DenverCoder1/readme-typing-svg` | Typing / caret rhythm (rebuilt locally as SMIL) | MIT |
| `abhisheknaiidu/awesome-github-profile-readme` | Curated scene taxonomy | CC0 |
| `kautukkundan/Awesome-Profile-README-templates` | Card / divider vocabulary | CC0 |
| Concept reference: Linear / Raycast / Vercel / Nothing OS / NASA mission control HUD | Aesthetic vocabulary (chromatic palette, micro-typography, grid backgrounds) | — visual language only |

**Extracted patterns we will adopt:**

- Hero scene with a moving aurora + grid behind large identity typography.
- Glassmorphism terminal card for `whoami` (frosted tint via `feGaussianBlur` on a copy of the background, not a real backdrop-filter).
- Orbital tech-universe with slow rotation and individually-pulsing tech nodes.
- Hexagonal HUD radar for domains (decorative; no fake %).
- Holographic project cards with moving border scan.
- Engineering loop with traveling packet.
- Self-generated GitHub telemetry SVG driven by a Python script in CI.
- Language constellation (force-directed layout approximation, deterministic seed).
- Activity timeline as a signal monitor.
- 3D contribution skyline wrapped in a local neon frame.
- Snake game with cyan/violet palette integration.

**Explicitly avoided:**

- Fake stats percentages without backing data.
- Rainbow badge walls (`https://img.shields.io/...` chaos).
- Heavy 3D third-party services with no fallback.
- `mousemove` parallax effects (won't render).
- Custom web fonts via `@font-face` (blocked on `style` attribute; safer to rely on system monospace).
- Embedding third-party iframe widgets.
- Screenshots inside SVGs of copyrighted dashboards.

---

## 4. Animation Patterns

To stay smooth and reliable, we use:

- **SMIL** (`<animate>`, `<animateTransform>`, `<animateMotion>`) inside SVG. Compatible with GitHub's sanitizer because SMIL is parsed, not executed JS.
- **CSS `@keyframes`** scoped per-SVG inside an inline `<style>` block. GitHub preserves `<style>` *inside* `<svg>` elements.
- **Looped durations** chosen to share factors (e.g. 4s, 6s, 12s) so all loops resync smoothly when the user scrolls back to the top.
- **Reduced motion**: every SVG includes a `<style>` rule

  ```css
  @media (prefers-reduced-motion: reduce) {
    animate, animateTransform, animateMotion { display: none; }
  }
  ```

  so users who request reduced motion see a static composition.

- **Loop seamlessness**: gradient `gradientTransform` rotations are continuous (not snap-back). Stars and particles use `<animateMotion>` along closed `<path>`s.

---

## 5. Performance Budget

| Metric | Budget |
| --- | --- |
| Total visual payload (sum of SVG files referenced by README) | < 3.5 MB |
| Each individual SVG | < 350 KB |
| One workflow run / day maximum for metric regen | 1 |
| Workflow concurrency | single-job serialized |
| Permissions | `contents: write` only |
| External runtime deps (Python) | standard library only — no `pip install` inside the action |
| External network calls from generator | only `api.github.com` over HTTPS with `GITHUB_TOKEN` |

---

## 6. Architecture Decisions

```
hoquan2007/
├── README.md                      ← Top-level scene assembly
├── .github/
│   └── workflows/
│       ├── profile-telemetry.yml  ← generates local GitHub metrics SVG
│       ├── snake.yml              ← unchanged (third-party)
│       └── profile-3d.yml         ← unchanged (third-party)
├── assets/
│   ├── scenes/                    ← hand-crafted SVG scenes (01..17)
│   ├── static/                    ← icons, frames, decorations
│   └── generated/                 ← CI-produced SVGs (telemetry, projects, language-constellation, activity-stream)
├── scripts/
│   └── generate_profile_metrics.py
├── docs/
│   ├── DESIGN_RESEARCH.md         ← this file
│   └── PROFILE_GUIDE.md           ← human-readable explanation of the scenes
└── .gitignore
```

**Why this layout:**

- 80% self-hosted — every scene SVG is committed in-repo. Only the snake and 3D skyline rely on third-party actions.
- One script (`generate_profile_metrics.py`) regenerates all dynamic SVGs atomically. No node_modules, no TypeScript build step.
- Generated SVGs are force-added by CI (`git add -f`) but live under `assets/generated/` so they're easy to inspect.

---

## 7. Color System (locked)

| Token | Hex | Use |
| --- | --- | --- |
| `--bg-0` | `#020617` | Page-equivalent fill for SVG backgrounds |
| `--bg-1` | `#050816` | Layered panels |
| `--bg-2` | `#080B16` | Card surfaces |
| `--bg-3` | `#0D1117` | GitHub dark fallback |
| `--cyan` | `#00E5FF` | Primary accent |
| `--cyan-2` | `#22D3EE` | Secondary accent |
| `--violet` | `#7C3AED` | Brand violet |
| `--violet-2` | `#8B5CF6` | Mid violet |
| `--violet-3` | `#A855F7` | Highlight violet |
| `--blue` | `#3B82F6` | Cool info |
| `--snow` | `#F8FAFC` | Rare highlight |
| `--muted` | `#94A3B8` | Body text |

Gradients: linear 135° between `--cyan` and `--violet`; radial glows use `--bg-1` → `--bg-0`.

---

## 8. Typography

We do NOT embed web fonts (GitHub strips `@font-face` from inline styles). All text uses `font-family` stacks:

- Primary mono: `"JetBrains Mono", "Fira Code", "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace`
- Display sans: `"Inter", "Segoe UI", system-ui, -apple-system, sans-serif`

These resolve on GitHub to `ui-monospace` / `system-ui` on every OS — perfectly legible, no external dependency.

---

## 9. Accessibility & Safety

- Every dynamic SVG has `aria-label` describing the scene.
- No essential information lives *only* inside an SVG; every data point also appears in plain Markdown.
- Reduced-motion users see static compositions.
- No analytics, no tracking pixels, no third-party fonts.
- `GITHUB_TOKEN` is read only by CI; never logged.

---

## 10. Implementation Phases (Cursor will execute these)

1. Phase A — Backup verification ✅ (current commit `e96e7d5`).
2. Phase B — Remove old assets/decoration (preserves `.git`, keeps workflows intact at first).
3. Phase C — Rebuild scene SVGs (01..17) + static assets.
4. Phase D — Build telemetry Python script + workflow.
5. Phase E — Compose `README.md`.
6. Phase F — Local validation (size budget, lint, dry-run generator with mocked API).
7. Phase G — Documentation (`docs/PROFILE_GUIDE.md`).
8. Phase H — Stop. No push. Report status to user with handoff instructions.

Cursor should NOT push unless the user explicitly asks.
