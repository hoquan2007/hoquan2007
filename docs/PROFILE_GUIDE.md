# QUAN.OS // Profile Guide

> A scene-by-scene walkthrough of the `hoquan2007` GitHub profile.
> Read this if you want to understand, edit, or extend the design system.

---

## 1. Repository layout

```
hoquan2007/
├── README.md                       17-scene sequence
├── .github/workflows/
│   ├── profile-telemetry.yml       self-hosted GitHub metrics (daily + manual)
│   ├── snake.yml                   third-party snake (output branch)
│   └── profile-3d.yml              third-party 3D skyline
├── assets/
│   ├── scenes/                     hand-crafted SVG scenes (01..17)
│   ├── static/                     icons.svg + scene-divider.svg
│   └── generated/                  produced by profile-telemetry.yml
├── scripts/
│   ├── generate_profile_metrics.py standard-library-only telemetry generator
│   └── check_paths.py              validates README asset paths exist
└── docs/
    ├── DESIGN_RESEARCH.md          research notes & source decisions
    └── PROFILE_GUIDE.md            this file
```

## 2. The 17 scenes

| # | Scene | File | Source of truth |
| --- | --- | --- | --- |
| 01 | Cinematic boot / hero | `assets/scenes/01-hero.svg` | Hand-crafted |
| 02 | Identity terminal | `assets/scenes/02-identity.svg` | Hand-crafted |
| 03 | Neural core | `assets/scenes/03-neural-core.svg` | Hand-crafted |
| 04 | Tech universe | `assets/scenes/04-tech-orbit.svg` | Verified repos |
| 05 | Domain HUD | `assets/scenes/05-domains.svg` | Hand-crafted |
| 06 | Featured projects (LIVE) | `assets/generated/projects.svg` | GitHub API |
| 06b| Featured projects (FALLBACK) | `assets/scenes/06-projects.svg` | Snapshot 2026-09-15 |
| 07 | Engineering loop | `assets/scenes/07-engineering-loop.svg` | Hand-crafted |
| 08 | GitHub telemetry | `assets/generated/github-telemetry.svg` | GitHub API |
| 09 | Language constellation | `assets/generated/language-constellation.svg` | GitHub API |
| 10 | Activity stream | `assets/generated/activity-stream.svg` | Events API |
| 11 | 3D skyline | `profile-3d-contrib/profile-night-rainbow.svg` | yoshi389111 action |
| 12 | Snake | `output/github-snake[-dark].svg` | Platane/snk |
| 13 | Current mission | `assets/scenes/13-mission.svg` | Verified repos |
| 14 | Skill tree | `assets/scenes/14-roadmap.svg` | Verified repos |
| 15 | Philosophy | `assets/scenes/15-philosophy.svg` | Hand-crafted |
| 16 | Contact | `assets/scenes/16-contact.svg` | GitHub handle |
| 17 | Shutdown / footer | `assets/scenes/17-footer.svg` | Hand-crafted |

## 3. Color tokens (locked)

| Token | Hex | Use |
| --- | --- | --- |
| BG0 | `#020617` | SVG background base |
| BG1 | `#050816` | Layered panels |
| BG2 | `#080B16` | Card surfaces |
| BG3 | `#0D1117` | GitHub-dark fallback |
| CYAN | `#22D3EE` | Primary accent |
| CYAN2 | `#0E7490` | Cyan dark |
| VIOLET | `#A855F7` | Brand violet |
| VIOLET2 | `#5B21B6` | Violet dark |
| PURPLE | `#7C3AED` | Mid violet |
| BLUE | `#3B82F6` | Cool info |
| SNOW | `#F8FAFC` | Rare highlight |
| MUTED | `#94A3B8` | Body text |
| DIM | `#64748B` | Micro labels |

Never use rainbow colors. Never use red/green/yellow unless used for status indicators (LEDs).

## 4. Typography

- Mono stack: `JetBrains Mono, Fira Code, IBM Plex Mono, ui-monospace, Menlo, monospace`
- Sans stack: `Inter, Segoe UI, system-ui, -apple-system, sans-serif`
- No `@font-face` is used. GitHub strips custom font loading; system fallbacks resolve cleanly.

## 5. Animation rules

- Loops resync (no snap-back): `gradientTransform` rotations and `<animateMotion>` paths are closed.
- Reduced motion: every SVG contains the snippet
  ```css
  @media (prefers-reduced-motion: reduce){
    animate,animateTransform,animateMotion{display:none}
  }
  ```
- Loops are 2.4s, 3.4s, 4.0s, etc. — share factors where possible.
- Pulse strokes use `stroke-opacity` not `stroke`, so the line color stays constant.

## 6. CI workflows

### profile-telemetry.yml

Runs daily at 18:00 UTC + on every push to `scripts/`. Generates:

- `assets/generated/github-telemetry.svg`
- `assets/generated/projects.svg`
- `assets/generated/language-constellation.svg`
- `assets/generated/activity-stream.svg`

Uses only the GitHub REST API. No `pip install`. No third-party services. No fake metrics.

### snake.yml (unchanged)

Generates the snake animation and publishes it to the `output` branch.

### profile-3d.yml (unchanged)

Generates the 3D contribution skyline and commits it under `profile-3d-contrib/`.

## 7. Editing safely

1. Edit an SVG in `assets/scenes/`.
2. Validate: `python -c "import xml.etree.ElementTree as ET; ET.parse('path/to/file.svg')"`
3. (Optional) Use `scripts/check_paths.py` to ensure README references still resolve.
4. Commit and push. The README loads everything from this repository, so GitHub will pick up the changes automatically.

## 8. Performing a clean rebuild

If you ever want to reset:

```bash
git checkout main
git pull
git log --oneline | head
# baseline commits available:
#   cedb5e9 chore(profile): wipe legacy implementation, scaffold QUAN.OS research
#   e96e7d5 feat(profile): fix workflows, add 3D cube SVG, slim README to animated-only
#   35418e6 feat(profile): custom cyber-terminal SVG header & footer
```

## 9. Non-goals (intentional)

- No fake stats (`AI 95%`). The HUD uses `LEARNING / BUILDING / EXPLORING / ACTIVE`.
- No rainbow badges. No `shields.io` cluster.
- No JS, no iframes, no canvas, no WebGL.
- No fabricated companies, schools, certifications, or email.
- No hard-coded stars beyond what the GitHub API returns.

## 10. License

This is a personal profile repository. You are welcome to read and learn from
the structure; please do not lift the personal information (name, repos,
descriptions) for unrelated purposes.
