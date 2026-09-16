# QUAN.OS // UX/UI Audit — Before Refactor

> Snapshot of the `hoquan2007` GitHub profile repository captured at
> commit `fc97a78 feat(profile): rebuild as QUAN.OS neural command center`.
> This audit records every UX, UI, animation, accessibility and workflow
> issue discovered during the inspection phase, **before** any code changes.

---

## 1. Repository State Snapshot

| Item | Value |
| --- | --- |
| Branch | `main` |
| HEAD commit | `fc97a78` |
| Working tree | clean |
| Remote | `origin` (not pushed during this refactor) |
| Identity | Hồ Ngọc Quân / `@hoquan2007` |
| Public repos | 22 |
| Followers | 0 |
| Following | 0 |
| Account created | 2025-07-30 |
| Total stars across owned repos | 0 |
| Tracked size | ~671 KB |

### Verified repository inventory (used for ground truth)

- `face-attendance` — TypeScript
- `6651071056.BTLT2` — HTML
- `ResearchAI` — (no language declared)
- `QITEnglish` — TypeScript — *Web học tiếng Anh dành cho dân IT*
- `QMusic` — (no language declared) — *Web nghe nhạc cá nhân*
- `QEnglish` — TypeScript — *QEnglish - Nền tảng học tiếng Anh giao tiếp với AI*
- `HQ-English` — TypeScript
- `Web-xem-phim` — TypeScript — *Tạo một web để xem phim*
- `SOLO-GAME` — HTML
- `HQEnglish` — TypeScript
- `EnglishHNQ` — TypeScript — *Web học tiếng Anh*
- `Test-Game-3`, `Test-Game-2`, `Test_game` — HTML
- `NEXTGPU-COPY` — TypeScript
- `Shadow-Collapse` — *Procedural Dungeon Crawler*
- `Test-Next-GPU` — TypeScript
- `GPU-Server-Manager` — C — *Bài tập lớn Kỹ thuật Lập trình C - Hệ thống quản lý tài nguyên máy chủ GPU*
- `ProjectChess` — C
- `Code_C_2` — C++
- `Code_C` — C++

---

## 2. UX Problems Found

### 2.1 Information architecture
- README opens with a 17-scene SVG sequence; the first 320 pixels are
  almost pure decoration. The visitor does **not** learn who Hồ Ngọc Quân is
  until deep inside the file.
- The `<table>` immediately after the hero (`Software-Engineering Student
  / currently focused on`) duplicates identity content that already exists
  in `02-identity.svg`. Result: information is repeated inconsistently in
  Markdown vs SVG.
- "About / engineering dna" section is split across two visual containers
  (Markdown table + neural-core SVG). Reading order is broken because the
  visitor alternates between reading text and inspecting a graphic.
- "Featured systems" relies on `assets/generated/projects.svg` (CI) but
  also reuses `assets/scenes/06-projects.svg` (static fallback). Both
  cards exist, leading to two near-identical visuals with different bug
  surfaces (frozen vs dynamic).

### 2.2 Discoverability
- No quick-navigation table-of-contents. A visitor scrolls through the
  entire profile before finding the section they want.
- No CTA in the hero pointing to `/tab=repositories` or to the GitHub
  handle.
- Project descriptions live *inside* SVGs (e.g. `06-projects.svg` text).
  If the SVG fails to render, the user gets a blank box and zero context.

### 2.3 Markdown readability
- Many Unicode characters in `01-hero.svg`, `06-projects.svg`,
  `13-mission.svg`, `16-contact.svg`, `17-footer.svg`, `02-identity.svg`
  are stored as raw bytes (`?`). When viewed from a Windows shell or a
  non-UTF8-aware editor they render as `?`. The actual files do encode
  Vietnamese (`H? Ng?c Qu?`) and arrow glyphs (`?`, `?`) correctly inside
  `<title>` and `aria-label`, but decorative micro-text inside the SVG
  loses the characters entirely (e.g. `URL ? ...` shows as `URL ? ...`).
  This is a **content quality bug**, not a render bug.
- The `<sub>` lines around `assets/generated/...` embed `<code>...</code>`
  without escaping, which GitHub sometimes auto-corrects in surprising
  ways.
- README mixes HTML tables (`<table>`) and SVG scenes for the same logical
  region, producing inconsistent visual rhythm.

### 2.4 Redundancy
- `assets/scenes/09-language-constellation.svg` and
  `assets/generated/language-constellation.svg` both exist but only the
  generated one is referenced.
- `assets/scenes/10-activity-stream.svg` likewise shadows the generated
  activity stream. Confusing for maintainers.
- `11-city-frame.svg` and `12-snake-frame.svg` are decorative frames around
  third-party assets. They double the visual weight without adding
  information.

### 2.5 Accessibility
- All SVGs have `role="img"` + `aria-label` + `<title>` ✓
- But `scene-divider.svg` has no `aria-hidden="true"` ✓ (it does, good)
- Reduced-motion media query is present in every SVG ✓
- However the **README** has no language anchor for the hero, no
  skip-link, and no `<main>` / `<article>` structure.

### 2.6 Contact
- `16-contact.svg` only advertises the GitHub handle, which is correct.
  But the README contact table appears *after* the contact SVG, not as
  part of it. The visual handshake is split.
- No mention of repository metadata (description, topics).

---

## 3. UI Problems Found

### 3.1 Color discipline
- Most scenes respect the `#020617 → #0B1224` palette. However:
  - `04-tech-orbit.svg` uses `#0B1530` (hero-specific), `#0B1224` and
    `#10172A` interchangeably, creating inconsistent panel fills.
  - `02-identity.svg` uses a three-stop `#22D3EE → #7C3AED → #A855F7`
    border gradient — fine, but no other scene replicates this gradient.
- Border colors mix `stroke="#22D3EE" stroke-opacity="0.45"` in some
  scenes and `stroke="#1E293B"` in others. No single "thin separator"
  token.

### 3.2 Typography
- Hero uses `font-family="Inter,system-ui,sans-serif"` for the name but
  every other scene uses JetBrains Mono. Intentional, but inconsistent —
  no documentation in `docs/` calls this out.
- Letter-spacing varies: `letter-spacing:8px` for the hero name, `2px`
  for labels, `3px` for category titles, `1px` for descriptions. No scale
  table in `docs/DESIGN_RESEARCH.md`.

### 3.3 Card visuals
- All four project cards are `540×200`. On a 1440 viewport with two
  cards side-by-side, the grid is fine. On a 390 viewport, each card is
  180px wide with 12px font — text becomes microscopic.
- Card mini-diagrams (right column) use 9-10px text. On mobile they are
  unreadable.

### 3.4 Hero issues
- `01-hero.svg` includes two large `<filter id="blur6">` blur filters
  applied to 900×140 ellipses. That's expensive at full screen.
- The terminal boot lines have fixed `fill="freeze"` reveals but the
  cursor keeps blinking forever, which is intentional but draws focus.
- The label `?` (`?`) is used for both arrow and bullet purposes in
  different scenes.

### 3.5 Footer
- `17-footer.svg` ends with `QUAN.OS ? EOL ? 2026-09-15`. The "EOL"
  wording is a bit cold for a personal profile. The date is also frozen
  to commit time.

### 3.6 Scene dividers
- `scene-divider.svg` is **never referenced** by the README. It's dead
  weight, but a great idea for unifying the rhythm of the document.

---

## 4. Responsive Problems

### 4.1 49% side-by-side layouts
- `02-identity.svg` has a 640px left terminal + 380px right diagram.
  At 1440 viewport → readable. At 1024 viewport → readable. At 768 →
  the terminal still fits but micro-text gets tight.
- `assets/scenes/05-domains.svg` uses a 4-card 270-px row. On 390 width
  each card is ~85px wide; text wraps awkwardly.
- Project cards (4×540×200 in a 2×2 grid) scale linearly with the
  parent. The README sets `width="100%"`, so on 390 the cards are ~170px
  wide and **10-px desc text becomes 4-5 px after scaling**.

### 4.2 Hero
- Hero is 1200×560. Scales fine. But the corner brackets at `(24,24)`
  collapse to `(8,8)` on mobile, eating border space.

### 4.3 Mission timeline
- `13-mission.svg` mission timeline is fixed at `cx="280,560,840,1120"`.
  On 1024 width these cluster near the right edge.

---

## 5. Animation Problems

### 5.1 Motion overload
At any given moment the README has up to **17 animated SVG scenes**
visible off-screen but loaded. SMIL runs in the background even when
scrolled away. Battery cost on mobile is non-trivial.

### 5.2 Heavy filters
- Hero uses two `<feGaussianBlur stdDeviation="6">` filters applied to
  900×140 ellipses. The `04-tech-orbit.svg` core uses
  `<feGaussianBlur stdDeviation="2">` on the halo.
- `06-projects.svg` defines `p-glow` as a vertical gradient — cheap, but
  each of four cards also carries an animated scanline (`y` over 6s) +
  blinking LED (`opacity` over 1.6–2.4s).

### 5.3 Excessive rotation
- `04-tech-orbit.svg` has **five** `animateTransform rotate` groups
  running at 40s, 50s, 60s, 70s, 90s. All five rotate simultaneously —
  high background-motion cost.

### 5.4 Stale frames
- `01-hero.svg` scan line uses `dur="7s"` `values="0;560;0"`. The "from
  0 to 560 to 0" motion is jarring — better as a one-way sweep.
- `02-identity.svg` terminal prompt caret blinks at 1s forever.
- `06-projects.svg` scanlines loop every 6s with `fill="freeze"` cycles
  → smooth. OK.

### 5.5 Missing prefers-reduced-motion coverage
- All scene SVGs respect it. Good.
- However the **snake SVG** (third-party) does not guarantee reduced
  motion. Out of scope to control.

---

## 6. Performance Problems

| File | Size | Notes |
| --- | --- | --- |
| `profile-3d-contrib/profile-night-rainbow.svg` | ~221 KB | Largest single SVG referenced |
| `profile-3d-contrib/profile-south-season-animate.svg` | ~201 KB | Unused, but still in repo |
| `profile-3d-contrib/profile-season-animate.svg` | ~201 KB | Unused |
| `profile-3d-contrib/profile-season.svg` | ~186 KB | Unused |
| `profile-3d-contrib/profile-south-season.svg` | ~186 KB | Unused |
| `profile-3d-contrib/profile-gitblock.svg` | ~209 KB | Unused |
| `profile-3d-contrib/profile-green-animate.svg` | ~184 KB | Unused |
| `profile-3d-contrib/profile-green.svg` | ~169 KB | Unused |
| `profile-3d-contrib/profile-night-green.svg` | ~184 KB | Unused |
| `profile-3d-contrib/profile-night-view.svg` | ~184 KB | Unused |
| **Total unused 3D themes** | ~1.7 MB | Should be deleted |
| Scene SVGs (avg ~9 KB) | ~140 KB total | OK |
| Generated SVGs (avg ~6 KB) | ~24 KB total | OK |
| **Total repo payload (excluding unused themes)** | ~340 KB | OK |

Hero filter cost dominates. Hero has two `feGaussianBlur(6)` filters on
`900×140` ellipses — these run on every frame on a non-cached paint.

---

## 7. Accessibility Problems

- ✅ All SVGs have `<title>` and `aria-label`.
- ✅ All SVGs respect `prefers-reduced-motion`.
- ❌ Hero alt text mentions only "engineering command center"; doesn't
  name the developer in the alt.
- ❌ Section `<img>` tags inside the README rarely use the developer's
  name in alt text.
- ❌ `06-projects.svg` cards encode project descriptions inside the SVG
  text layer. If SMIL or font fallback breaks, descriptions vanish with
  no Markdown fallback.
- ❌ Color contrast on dim `#64748B` text over `#020617` is ~3.6:1
  (below WCAG AA 4.5:1 for small text).

---

## 8. Workflow Problems

| Workflow | Issues |
| --- | --- |
| `profile-3d.yml` | Uses `yoshi389111/github-profile-3d-contrib@latest` — unpinned. Adds `profile-3d-contrib/` even though only `profile-night-rainbow.svg` is referenced. |
| `snake.yml` | Healthy. |
| `profile-telemetry.yml` | Healthy. Uses `concurrency:` block, `permissions: contents: write`, `timeout-minutes: 5`. |
| (none) | No `validate.yml` for path/lint checks. |
| (none) | No concurrency group on `profile-3d.yml` or `snake.yml`. |

---

## 9. Documentation Gaps

- `docs/DESIGN_RESEARCH.md` exists but the 17-scene table at the bottom is
  out of sync with current files.
- `docs/PROFILE_GUIDE.md` exists but lacks:
  - Quick navigation rules
  - Motion hierarchy explanation
  - Reduced motion contract
  - Color tokens table (only in DESIGN_RESEARCH.md)
- No `docs/UX_UI_AUDIT_BEFORE.md` (this file).
- No `docs/UX_UI_AUDIT_AFTER.md`.
- No `docs/DESIGN_SYSTEM.md` lock file for visual tokens.
- No `config/profile.json` central config.
- No `config/theme.json` central config.

---

## 10. File inventory

```
.github/workflows/
├── profile-3d.yml          ✓ keep
├── profile-telemetry.yml   ✓ keep
└── snake.yml               ✓ keep

assets/
├── generated/              ✓ keep (CI output)
├── scenes/                 ⚠ remove duplicates (09, 10), keep 01..08, 11..17
└── static/                 ⚠ scene-divider unused, icons unused in README

docs/
├── DESIGN_RESEARCH.md      ✓ keep, refresh
├── PROFILE_GUIDE.md        ✓ keep, refresh
└── UX_UI_AUDIT_BEFORE.md   ✓ created by this audit

scripts/
├── check_paths.py          ✓ keep, evolve
└── generate_profile_metrics.py ✓ keep, expand

profile-3d-contrib/         ⚠ 9/10 themes unused; delete or move to /legacy
```

---

## 11. Summary of Issues (count)

| Category | Count |
| --- | --- |
| UX problems | 12 |
| UI problems | 8 |
| Responsive problems | 6 |
| Animation problems | 5 |
| Performance problems | 4 |
| Accessibility problems | 4 |
| Workflow problems | 3 |
| Documentation gaps | 5 |
| **Total** | **47** |

This audit is the baseline against which the refactor will be measured.