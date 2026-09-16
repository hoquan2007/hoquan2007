# QUAN.OS // Profile Guide

This guide documents how the GitHub profile `hoquan2007` is built, how to
regenerate every visual locally, and how to safely change colors,
copy, or layout without breaking the contract.

---

## 1. Where everything lives

```
hoquan2007/
├── README.md                       # the profile itself (Markdown + image tags)
├── .github/workflows/              # 4 GitHub Actions
│   ├── profile-3d.yml              # yoshi389111/github-profile-3d-contrib nightly
│   ├── profile-telemetry.yml       # api.github.com → 4 SVG files (nightly + push)
│   ├── snake.yml                   # Platane/snk@v3 → output branch (nightly)
│   └── validate.yml                # scripts/validate_profile.py on push + PR
├── assets/
│   ├── scenes/                     # static, hand-authored scenes (01-12)
│   ├── generated/                  # CI-generated SVGs (4 files)
│   ├── static/scene-divider.svg    # reserved for future transitions
│   └── ...
├── profile-3d-contrib/             # CI-generated 3D skyline variants
├── config/
│   ├── profile.json                # identity / projects / mission / philosophy
│   └── theme.json                  # colors / motion timings / metadata
├── scripts/
│   ├── generate_profile_metrics.py # main SVG generator (uses config/*.json)
│   └── validate_profile.py         # linting on every push + PR
└── docs/
    ├── DESIGN_SYSTEM.md            # single source of truth for visuals
    ├── UX_UI_AUDIT_BEFORE.md       # 47 baseline issues
    ├── UX_UI_AUDIT_AFTER.md        # how each was fixed + score card
    └── PROFILE_GUIDE.md            # this file
```

## 2. The 12 scenes (in the order they appear)

| # | File | Purpose |
| --- | --- | --- |
| 01 | `assets/scenes/01-hero.svg` | Identity + boot sequence (high energy, slow) |
| 02 | `assets/scenes/02-whoami.svg` | Terminal-style `whoami` block (medium) |
| 03 | `assets/scenes/03-engineering-dna.svg` | Engineering DNA central node (calm) |
| 04 | `assets/scenes/04-tech-universe.svg` | Tech orbital system (medium) |
| 05 | `assets/scenes/05-domains.svg` | Hexagonal domain HUD (calm) |
| 06 | `assets/generated/projects.svg` | Top-5 project cards (high) — CI-generated |
| 07 | `assets/scenes/06-workflow.svg` | Engineering loop (medium) |
| 08 | `assets/scenes/08-skyline-frame.svg` | Header for the 3D skyline (calm) |
| 09 | `assets/generated/github-telemetry.svg` | Live profile metrics (medium) |
| 10 | `assets/scenes/09-mission.svg` | Current mission cards (high) |
| 11 | `assets/scenes/10-roadmap.svg` | Skill tree (medium) |
| 12 | `assets/scenes/11-contact.svg` | Final transmission (high) |
| (footer) | `assets/scenes/12-footer.svg` | Shutdown (calm) |

(Note: the scene numbers visible inside each SVG file are kept stable
even though file names are renumbered — `assets/scenes/01-hero.svg`
contains `SCENE 01 / HERO BOOT` and so on.)

## 3. How to run things locally

```bash
# regenerate all 4 dynamic SVGs into assets/generated/
python scripts/generate_profile_metrics.py

# lint the README + assets + workflows
python scripts/validate_profile.py
```

Both scripts are safe to run repeatedly; they are idempotent. The
generator only hits `api.github.com` for `github_user_name` resolved from
`GITHUB_USER` or `HNQuan`. Set `GITHUB_TOKEN` to raise the rate limit
(60 unauthenticated / 5000 authenticated requests/hour).

## 4. How to change colors

Open `config/theme.json` and edit any value. Re-run the generator. The
generator pulls every color from this file; the static scenes use the
same hex codes by hand and are kept in sync via the design-system doc.

If you want to change a static scene's color, also update
`docs/DESIGN_SYSTEM.md` to keep the documentation honest.

## 5. How to add a new scene

1. Author the SVG in `assets/scenes/NN-name.svg` using the existing
   palette + reduced-motion media query.
2. Add a README anchor (`<a id="..."></a>`) and an image tag.
3. Add the file to `scripts/validate_profile.py`'s expected list.
4. Re-run the validator.
5. Open a pull request — `validate.yml` will gate regressions.

## 6. How to update profile data

Open `config/profile.json` and edit the relevant section. Run
`python scripts/generate_profile_metrics.py` to refresh
`assets/generated/projects.svg`. Commit both files.

## 7. Common maintenance tasks

| Task | Steps |
| --- | --- |
| Bump palette | `config/theme.json` + static scenes (manually mirror changes) |
| Update featured projects | `config/profile.json` → run generator → commit |
| Update mission / roadmap | edit static scenes in `assets/scenes/` |
| Add a new workflow | `.github/workflows/*.yml` (use concurrency + permissions) |
| Change tagline | `config/theme.json` → static hero → docs |

## 8. Reduced-motion contract

Every animated SVG in this profile ships with:

```css
@media (prefers-reduced-motion: reduce){
  animate,animateTransform{display:none}
}
```

When the user enables reduced motion, every `<animate>` and
`<animateTransform>` is removed from layout, so the scene settles into
its resting state.

## 9. Accessibility contract

Every animated SVG ships with `role="img"`, a useful `aria-label`, an
SVG `<title>`, and an SVG `<desc>`. Body text outside of decorative
micro-labels uses at least `#94A3B8` on `#020617` (contrast > 7:1,
WCAG AAA).

## 10. Performance contract

- Static scenes are hand-authored under 10 KB each.
- Generated scenes are < 12 KB each.
- Hero uses no `feGaussianBlur` filters (those caused expensive paints).
- Animations are `transform`, `opacity`, and `stroke-dasharray` only.
- Particle counts never exceed 6 per scene.
- One slow orbit, not five overlapping orbits.

## 11. Trust / honesty contract

- No fake completion percentages.
- No "I am fluent in..." claims.
- No fake contact channels (only verified GitHub handle).
- Every mission card references either an actual repository or a
  planned study path in `profile.json`.

## 12. The 10-line "I want to ship QUAN.OS" recipe

```bash
git clone https://github.com/hoquan2007/hoquan2007
cd hoquan2007
python scripts/generate_profile_metrics.py
python scripts/validate_profile.py
git add -A
git commit -m "QUAN.OS / refresh"
git push origin main
```

That's the entire local workflow.