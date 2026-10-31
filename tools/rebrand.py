#!/usr/bin/env python3
"""Rebrand the upstream aerial-tv working copy at build time (CI only, never committed).

- app.orchard.tv -> com.dangbei.tvlauncher. Covers everything derived from the
  package name: applicationId/namespace, package/import statements, the guard
  component and broadcast action strings, accountType, Updates.kt's PACKAGE
  constant, and docs/site text. Three spellings need separate rules:
    app.orchard.tv          plain dotted form
    app\\.orchard\\.tv        regex-escaped form (lite/build.gradle.kts rewrite filter)
    HSPLapp/orchard/tv/...  slash form in the baseline profile (Lapp/... too)
  Source *directory* names (app/src/main/java/app/orchard/tv/...) are kept:
  Kotlin does not require directories to match packages, and keeping them lets
  upstream file additions always merge without conflicts. The OrchardDream
  legacy-check in GuardSetup.kt builds on context.packageName and follows along.
- Update source URLs -> this fork's GitHub releases. The version check reads a
  plain-text version.txt (uploaded as a release asset by build.yml); the APK
  download sources resolve to the latest release's assets.
- Left as upstream: aerial.qust.me/icons/ (static icon CDN, no need to fork it).
"""
from pathlib import Path

REPLACEMENTS = [
    ("https://aerial.qust.me/download/", "https://github.com/guoyb98/aerial-tv/releases/latest/download/"),
    ("pengchujin/aerial-tv", "guoyb98/aerial-tv"),
    ("aerial.qust.me/update", "github.com/guoyb98/aerial-tv/releases"),
    ("app\\\\.orchard\\\\.tv", "com\\\\.dangbei\\\\.tvlauncher"),
    ("HSPLapp/orchard/tv/", "HSPLcom/dangbei/tvlauncher/"),
    ("Lapp/orchard/tv/", "Lcom/dangbei/tvlauncher/"),
    ("app.orchard.tv", "com.dangbei.tvlauncher"),
]

self_path = Path(__file__).resolve()
root = self_path.parent.parent
changed = hits = 0
for path in sorted(root.rglob("*")):
    if not path.is_file() or ".git" in path.parts or path.resolve() == self_path:
        continue
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        continue
    new = text
    count = 0
    for old, replacement in REPLACEMENTS:
        count += new.count(old)
        new = new.replace(old, replacement)
    if new != text:
        path.write_bytes(new.encode("utf-8"))
        changed += 1
    hits += count
print(f"rebrand: {hits} replacement(s) across {changed} file(s)")
if hits == 0:
    raise SystemExit("rebrand: nothing replaced - upstream moved? review tools/rebrand.py")
