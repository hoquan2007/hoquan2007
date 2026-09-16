#!/usr/bin/env python3
"""validate_profile.py - Lightweight lint pass for the QUAN.OS profile.

Checks:
  * All local asset paths referenced by README.md exist.
  * Every .svg under assets/ parses as XML.
  * No SVG contains <script>, foreignObject, javascript:, or iframe.
  * profile.json / theme.json parse as JSON with the expected keys.
  * All .github/workflows/*.yml parse as YAML (when PyYAML is available).

Run from the repository root:  python scripts/validate_profile.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORBIDDEN_SVG_PATTERNS = [
    re.compile(r"<script", re.IGNORECASE),
    re.compile(r"foreignObject", re.IGNORECASE),
    re.compile(r"javascript:", re.IGNORECASE),
    re.compile(r"<iframe", re.IGNORECASE),
    re.compile(r"\bonclick\s*=", re.IGNORECASE),
    re.compile(r"\bonerror\s*=", re.IGNORECASE),
    re.compile(r"\bonload\s*=", re.IGNORECASE),
    re.compile(r"<canvas", re.IGNORECASE),
]


def _ok(msg: str) -> None:
    print(f"  ok   {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL {msg}")


def check_readme_paths() -> int:
    """Ensure every local src/href in README.md resolves."""
    readme = REPO_ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    refs = re.findall(r'(?:src|href)=["\'](?!https?://|mailto:|#)([^"\']+)["\']', text)
    failures = 0
    for r in refs:
        # ignore markdown anchors / mailto / http
        if r.startswith("#") or r.startswith("?"):
            continue
        target = (REPO_ROOT / r).resolve()
        # account for ./ prefix
        try:
            target.relative_to(REPO_ROOT)
        except ValueError:
            _fail(f"path escapes repo: {r}")
            failures += 1
            continue
        if not target.exists():
            # CI-generated files may be missing locally; only warn
            if "profile-3d-contrib" in r or "generated" in r:
                _ok(f"expected CI file present later: {r}")
                continue
            _fail(f"missing local asset: {r}")
            failures += 1
        else:
            _ok(f"asset present: {r}")
    return failures


def check_svg_files() -> int:
    """Validate every .svg in assets/ and profile-3d-contrib/."""
    failures = 0
    svg_paths = list((REPO_ROOT / "assets").rglob("*.svg"))
    svg_paths += list((REPO_ROOT / "profile-3d-contrib").rglob("*.svg"))
    svg_paths = [p for p in svg_paths if p.is_file()]
    if not svg_paths:
        _fail("no SVG files found under assets/")
        return 1
    for p in svg_paths:
        rel = p.relative_to(REPO_ROOT)
        text = p.read_text(encoding="utf-8", errors="replace")
        for pat in FORBIDDEN_SVG_PATTERNS:
            if pat.search(text):
                _fail(f"{rel}: forbidden pattern matched ({pat.pattern})")
                failures += 1
                break
        else:
            try:
                ET.fromstring(text)
            except ET.ParseError as e:
                _fail(f"{rel}: XML parse error ({e})")
                failures += 1
                continue
            _ok(f"parses cleanly: {rel}")
    return failures


def check_json_config() -> int:
    """profile.json + theme.json must parse and contain core keys."""
    failures = 0
    expected = {
        "config/profile.json": ["identity", "interests", "tech_stack", "featured_projects"],
        "config/theme.json": ["colors", "animation", "distribution"],
    }
    for path, keys in expected.items():
        f = REPO_ROOT / path
        if not f.exists():
            _fail(f"missing config file: {path}")
            failures += 1
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            _fail(f"{path}: invalid JSON ({e})")
            failures += 1
            continue
        missing = [k for k in keys if k not in data]
        if missing:
            _fail(f"{path}: missing keys {missing}")
            failures += 1
        else:
            _ok(f"config ok: {path}")
    return failures


def check_workflows() -> int:
    """Lightweight YAML lint — only run if PyYAML available."""
    try:
        import yaml  # type: ignore
    except ImportError:
        _ok("PyYAML not installed; skipping workflow YAML parse check")
        return 0
    failures = 0
    wf_dir = REPO_ROOT / ".github" / "workflows"
    for yml in sorted(wf_dir.glob("*.yml")):
        rel = yml.relative_to(REPO_ROOT)
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            _fail(f"{rel}: invalid YAML ({e})")
            failures += 1
            continue
        if not isinstance(data, dict) or "name" not in data:
            _fail(f"{rel}: missing top-level 'name'")
            failures += 1
        else:
            _ok(f"workflow ok: {rel}")
    return failures


def main() -> int:
    print("== QUAN.OS profile validator ==")
    failures = 0
    for label, fn in [
        ("README asset paths", check_readme_paths),
        ("SVG XML + forbidden content", check_svg_files),
        ("JSON config", check_json_config),
        ("Workflow YAML", check_workflows),
    ]:
        print(f"\n[{label}]")
        failures += fn()
    print()
    if failures:
        print(f"!! {failures} check(s) failed")
        return 1
    print("all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())