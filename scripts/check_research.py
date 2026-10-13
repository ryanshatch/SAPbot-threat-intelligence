#!/usr/bin/env python3
"""Dependency-free structural checks for the public research repository."""
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []


def fail(path, message):
    errors.append(f"{path}: {message}")


def local_target(document, raw):
    raw = raw.replace("&amp;", "&").strip().strip("<>")
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:", "data:")):
        return None
    if raw.startswith("/"):
        # Site-root links do not resolve reliably on GitHub.
        fail(document.relative_to(ROOT), f"site-root link {raw!r}; use a relative link")
        return None
    return (document.parent / unquote(parsed.path)).resolve() if parsed.path else None


def check_links():
    pattern = re.compile(r"""(?:!?(?:\[[^\]]*\])\(([^)]+)\)|(?:href|src)=["']([^"']+)["'])""")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            raw = match.group(1) or match.group(2)
            target = local_target(path, raw)
            if target is not None and (not target.is_relative_to(ROOT) or not target.exists()):
                fail(path.relative_to(ROOT), f"missing local link {raw!r}")


def check_csv():
    layouts = {}
    for path in ROOT.rglob("*.csv"):
        if ".git" in path.parts:
            continue
        with path.open(encoding="utf-8-sig", newline="") as stream:
            try:
                reader = csv.reader(stream, strict=True)
                header = next(reader, None)
                if not header or any(not col.strip() for col in header) or len(set(header)) != len(header):
                    fail(path.relative_to(ROOT), "missing, blank, or duplicate CSV column")
                    continue
                layouts.setdefault(tuple(header), []).append(path)
                for line, row in enumerate(reader, 2):
                    if not row:
                        continue
                    if len(row) != len(header):
                        fail(path.relative_to(ROOT), f"row {line}: {len(row)} fields; expected {len(header)}")
                        continue
                    record = dict(zip(header, row))
                    if "threat_label" in record:
                        label = record["threat_label"].strip().lower()
                        if label not in {"true", "false"}:
                            fail(path.relative_to(ROOT), f"row {line}: threat_label must be true/false")
                        if label == "true":
                            role = " ".join(record.get(k, "") for k in
                                            ("role", "analyst_role", "classification", "current_classification"))
                            if re.search(r"\b(victim|recovery)\b", role, re.I):
                                fail(path.relative_to(ROOT), f"row {line}: review threat label on victim/recovery role")
            except (csv.Error, UnicodeError) as exc:
                fail(path.relative_to(ROOT), f"CSV parse error: {exc}")
    print(f"Checked {sum(map(len, layouts.values()))} CSV files across {len(layouts)} column layouts")


def check_json():
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeError) as exc:
            fail(path.relative_to(ROOT), f"JSON parse error: {exc}")
    manifest = ROOT / "assets" / "visuals.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for item in data.get("headers", []):
            for key in ("readme", "image"):
                value = item.get(key, "")
                if not value or not (ROOT / value).is_file():
                    fail(manifest.relative_to(ROOT), f"missing {key}: {value!r}")


if __name__ == "__main__":
    check_links()
    check_csv()
    check_json()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print("Research structure checks passed")
