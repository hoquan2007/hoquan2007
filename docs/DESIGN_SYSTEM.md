# QUAN.OS // Design System

> Single source of truth for the visual language of `hoquan2007`'s GitHub
> profile. Every custom SVG, generator script, and Markdown block must
> reuse these tokens. If something is not in this file, it is a bug.

---

## 1. Brand

| | |
| --- | --- |
| Codename | **QUAN.OS** |
| Tagline | NEURAL ENGINEERING COMMAND CENTER |
| Operator | HỒ NGỌC QUÂN · `@hoquan2007` |
| Voice | Technical, calm, futuristic, never boastful |
| Feel | Mission control, AI engineering HUD, sci-fi OS |

---

## 2. Color tokens (locked)

### Surface
| Token | Hex | Use |
| --- | --- | --- |
| `bg-0` | `#020617` | Page-equivalent fill (SVG root backgrounds) |
| `bg-1` | `#050816` | Layered panels |
| `bg-2` | `#080B16` | Card surfaces |
| `bg-3` | `#0D1117` | GitHub-dark fallback only |
| `panel` | `#0B1224` | Mid-card fills |

### Accent
| Token | Hex | Use |
| --- | --- | --- |
| `cyan` | `#00E5FF` | Primary accent (text highlight, scanlines, focus) |
| `cyan-2` | `#22D3EE` | Secondary accent (panel borders, glow) |
| `cyan-3` | `#0E7490` | Cyan dark (progress bars, status base) |
| `violet` | `#7C3AED` | Brand violet (alts, frame stroke) |
| `violet-2` | `#8B5CF6` | Mid violet (rare) |
| `violet-3` | `#A855F7` | Highlight violet (LEDs, links, status pulses) |
| `violet-4` | `#5B21B6` | Violet dark (filled bars, sub-strokes) |
| `blue` | `#3B82F6` | Cool info (NEXT badge, queue marker) |
| `blue-2` | `#1E3A8A` | Blue dark |

### Text
| Token | Hex | Use |
| --- | --- | --- |
| `snow` | `#F8FAFC` | Rare highlight only (large headings, key numbers) |
| `text` | `#F8FAFC` | Default text on dark (same as snow for simplicity) |
| `text-2` | `#CBD5E1` | Body text |
| `muted` | `#94A3B8` | Description text |
| `dim` | `#64748B` | Micro labels |
| `faint` | `#475569` | Lowest-priority labels |

### Borders / dividers
| Token | Hex | Use |
| --- | --- | --- |
| `line` | `#1E293B` | Thin static dividers |
| `line-2` | `#10172A` | Pattern grid lines |

### Distribution rule (must hold across the README)
- 70 % dark navy (bg-0 / bg-1 / bg-2)
- 15 % cyan (cyan-2 family)
- 10 % violet (violet family)
- 5 % white / highlights (`snow`)

> Never use red / green / yellow unless communicating status (LEDs).

---

## 3. Typography

### Stacks
- **Mono**: `"JetBrains Mono", "Fira Code", "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace`
- **Display**: `"Inter", "Segoe UI", system-ui, -apple-system, sans-serif`
- Never embed `@font-face`. GitHub strips it from inline SVG.

### Type scale
| Role | Size | Weight | Tracking |
| --- | --- | --- | --- |
| Hero display name | 62 px | 700 | 8 px |
| Footer headline | 28 px | 700 | 6 px |
| Section title (h3 in markdown) | 16 px | 600 | 2 px |
| Card title | 14 px | 700 | 1.5 px |
| Card value / big number | 42 px | 700 | 2 px |
| Card label | 11 px | 700 | 3 px |
| Body | 13 px | 400 | 1 px |
| Description | 10 px | 400 | 0.5 px |
| Micro label | 9 px | 400 | 2 px |
| Glyph-only tag | 9 px | 700 | 2 px |

> Sizes are nominal; SVGs use `viewBox` so they scale. Test at 1440 / 768
> / 390 / 360 viewport widths to confirm readability.

---

## 4. Spacing & shape

| Token | Value |
| --- | --- |
| `space-1` | 4 px |
| `space-2` | 8 px |
| `space-3` | 12 px |
| `space-4` | 16 px |
| `space-5` | 24 px |
| `space-6` | 32 px |
| `space-7` | 48 px |
| `radius` | 10 px (cards) |
| `radius-sm` | 6 px (inner cards) |
| `radius-pill` | 16 px (chips) |
| `border-thin` | 1 px |
| `border-strong` | 1.4 px |

---

## 5. Effects

| Token | Value | When to use |
| --- | --- | --- |
| `glow-soft` | radial gradient, opacity 0.18 → 0 | Behind primary headings |
| `glow-strong` | radial gradient, opacity 0.45 → 0 | Behind hero name only |
| `blur-2` | `feGaussianBlur stdDeviation="2"` | Localized halos |
| `blur-6` | `feGaussianBlur stdDeviation="6"` | Hero aurora ONLY, on `rx≥900` ellipse |
| `scan-line` | 2 px cyan line, 0.55 opacity, 6 s sweep | Card borders |
| `crt-scan` | 1 px cyan line, 0.4 opacity, 7 s sweep | Hero only |

> Never apply `blur-6` to anything smaller than 600 px wide. Never
> apply any blur to text.

---

## 6. Animation rhythm

| Level | Allowed duration | Use |
| --- | --- | --- |
| A — Hero | 14–18 s | aurora drift, grid scroll |
| A — Hero scan | 7 s | scanline |
| B — Primary scene | 30–90 s | orbital, snake, radar |
| B — Chart draw | 1.4–2 s | bar/sweep fill, on push only |
| C — Micro motion | 1.2–3 s | LED pulse, caret blink |
| D — Static | infinite (no animation) | labels, project text |

### Reduced motion contract
Every animated SVG **must** include:

```svg
<style>
  @media (prefers-reduced-motion: reduce) {
    animate, animateTransform, animateMotion { display: none; }
  }
</style>
```

Static fallback must remain visually complete (text readable, gradients
intact, layout intact).

---

## 7. Information density

- Max 5 separate data points per scene card.
- Card density: title, value, sub-label, micro-footer. Anything more
  belongs in a separate scene.

---

## 8. The "WOAH" checklist

For each scene ask:

1. Does it fit the QUAN.OS identity?
2. Is there **one** primary focal point?
3. Does it communicate real, verified information?
4. Is it readable at 360 px viewport?
5. Does the animation support information hierarchy, not fight it?
7. Does it duplicate information from another scene?
8. Would removing the scene make the README worse? (if no, delete)

If 4/8 is "no", the scene must be redesigned or removed.

---

## 9. Repository metadata

```
description:
  QUAN.OS — Futuristic AI engineering GitHub profile
topics:
  github-profile, profile-readme, animated-svg,
  developer-profile, github-actions, svg-animation
website:
  https://github.com/hoquan2007
```

These are recommended but **only the repository owner should apply them**
via the GitHub web UI. The Cursor agent does not modify them
automatically.

---

## 10. File system map

```
hoquan2007/
├── README.md                       17-scene + Markdown hybrid
├── .github/
│   └── workflows/
│       ├── profile-3d.yml          3D skyline generator
│       ├── snake.yml               snake generator
│       ├── profile-telemetry.yml   metrics generator
│       └── validate.yml            asset path / SVG XML linter (new)
├── assets/
│   ├── scenes/                     hand-crafted scenes 01..17
│   │   ├── 01-hero.svg
│   │   ├── 02-whoami.svg
│   │   ├── 03-engineering-dna.svg
│   │   ├── 04-tech-universe.svg
│   │   ├── 05-domains.svg
│   │   ├── 06-projects.svg         static fallback (deprecated; CI version used)
│   │   ├── 07-engineering-loop.svg
│   │   ├── 08-telemetry-frame.svg  decorative frame around generated dashboard
│   │   ├── 09-mission.svg
│   │   ├── 10-roadmap.svg
│   │   ├── 11-philosophy.svg
│   │   ├── 12-contact.svg
│   │   └── 13-footer.svg
│   ├── generated/                  CI-produced
│   │   ├── github-telemetry.svg
│   │   ├── projects.svg
│   │   ├── language-constellation.svg
│   │   └── activity-stream.svg
│   └── static/
│       ├── scene-divider.svg       used between scenes
│       └── icons.svg               inline glyph set
├── config/
│   ├── profile.json                non-secret profile data
│   └── theme.json                  visual tokens
├── scripts/
│   ├── generate_profile_metrics.py  Python stdlib only
│   └── check_paths.py              asset validator
└── docs/
    ├── DESIGN_SYSTEM.md            this file
    ├── DESIGN_RESEARCH.md          historical research
    ├── PROFILE_GUIDE.md            human-readable scene guide
    ├── UX_UI_AUDIT_BEFORE.md       baseline
    └── UX_UI_AUDIT_AFTER.md        results (filled at end)
```