#!/usr/bin/env python3
"""Checks rules.json and pending.json before they reach the app.

Runs as a GitHub Action on every push and pull request in the public repo.
The limits mirror the app (src/rules.rs, src/rating.rs in the app repo): a file
the app would reject or that would match far too many programs fails here, so
it never goes online. Only standard library modules are used.

Usage: python3 .github/scripts/check_data.py [rules.json] [pending.json]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_RULES_BYTES = 2 * 1024 * 1024
MAX_PENDING_BYTES = 512 * 1024
MAX_PENDING_PROGRAMS = 500
MAX_PENDING_NAME_CHARS = 120
MAX_PENDING_DESCRIPTION_CHARS = 300
MAX_RULE_NAME_CHARS = 80
MAX_RULE_ALIASES = 20
MAX_RULE_CATEGORY_CHARS = 40
MAX_RULE_REASON_CHARS = 400
MAX_RULE_ALTERNATIVES = 10
MAX_RULE_ALTERNATIVE_CHARS = 80
GENERIC_TERMS = {
    "app", "application", "client", "driver", "drivers", "free", "microsoft", "program",
    "pro", "service", "setup", "software", "tool", "tools", "update", "updater", "windows",
    "x64", "x86",
}
DRAFT_MARKER = "TODO"
READINESS = {"green", "yellow", "red"}
RULES_VERSION = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\.\d{1,6}$")
CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f-\x9f]")


def is_clean_text(value, max_chars: int) -> bool:
    return isinstance(value, str) and len(value) <= max_chars and not CONTROL_CHARACTERS.search(value)


def load_json(path: Path, max_bytes: int, errors: list[str]):
    if not path.exists():
        errors.append(f"{path.name}: Datei fehlt")
        return None
    raw = path.read_bytes()
    if len(raw) > max_bytes:
        errors.append(f"{path.name}: {len(raw)} Bytes, erlaubt sind höchstens {max_bytes}")
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        errors.append(f"{path.name}: kein gültiges JSON ({error})")
        return None


def check_match_term(term, where: str, errors: list[str]) -> str | None:
    if not is_clean_text(term, MAX_RULE_NAME_CHARS):
        errors.append(f"{where}: zu lang, kein Text oder enthält Steuerzeichen")
        return None
    normalized = term.lower().strip()
    if sum(character.isalnum() for character in normalized) < 2:
        errors.append(f"{where}: „{term}“ braucht mindestens zwei Buchstaben oder Ziffern")
    if normalized in GENERIC_TERMS:
        errors.append(f"{where}: „{term}“ ist zu allgemein und würde viele Programme treffen")
    return normalized


def check_rules(path: Path) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    names: set[str] = set()
    data = load_json(path, MAX_RULES_BYTES, errors)
    if data is None:
        return errors, names
    if not isinstance(data, dict):
        return [f"{path.name}: erwartet wird ein Objekt mit schema_version, rules_version und rules"], names
    if data.get("schema_version") != 1:
        errors.append(f"{path.name}: schema_version muss 1 sein")
    if not isinstance(data.get("rules_version"), str) or not RULES_VERSION.match(data["rules_version"]):
        errors.append(f"{path.name}: rules_version muss das Format JJJJ-MM-TT.N haben")
    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append(f"{path.name}: rules muss eine nicht leere Liste sein")
        return errors, names

    for index, rule in enumerate(rules):
        where = f"{path.name}, Regel {index + 1}"
        if not isinstance(rule, dict):
            errors.append(f"{where}: kein Objekt")
            continue
        where = f"{where} ({rule.get('name', '?')})"
        name = check_match_term(rule.get("name"), f"{where}, name", errors)
        if name:
            if name in names:
                errors.append(f"{where}: Name kommt doppelt vor")
            names.add(name)
        aliases = rule.get("aliases", [])
        if not isinstance(aliases, list) or len(aliases) > MAX_RULE_ALIASES:
            errors.append(f"{where}: aliases muss eine Liste mit höchstens {MAX_RULE_ALIASES} Einträgen sein")
        else:
            for alias in aliases:
                normalized = check_match_term(alias, f"{where}, alias", errors)
                if normalized:
                    names.add(normalized)
        if rule.get("readiness") not in READINESS:
            errors.append(f"{where}: readiness muss green, yellow oder red sein")
        for field, max_chars in (("category", MAX_RULE_CATEGORY_CHARS), ("reason", MAX_RULE_REASON_CHARS)):
            value = rule.get(field)
            if not is_clean_text(value, max_chars) or not value.strip():
                errors.append(f"{where}: {field} fehlt, ist zu lang oder enthält Steuerzeichen")
            elif DRAFT_MARKER in value:
                errors.append(f"{where}: {field} enthält noch TODO, der Entwurf ist nicht fertig")
        if "reason_en" in rule:
            value = rule["reason_en"]
            if not is_clean_text(value, MAX_RULE_REASON_CHARS) or not value.strip():
                errors.append(f"{where}: reason_en ist leer, zu lang oder enthält Steuerzeichen")
            elif DRAFT_MARKER in value:
                errors.append(f"{where}: reason_en enthält noch TODO, der Entwurf ist nicht fertig")
        for field in ("alternatives", "alternatives_en"):
            alternatives = rule.get(field, [])
            if (
                not isinstance(alternatives, list)
                or len(alternatives) > MAX_RULE_ALTERNATIVES
                or not all(is_clean_text(item, MAX_RULE_ALTERNATIVE_CHARS) for item in alternatives)
            ):
                errors.append(f"{where}: {field} sind zu viele, zu lang oder kein Text")
        unknown = set(rule) - {
            "name", "aliases", "readiness", "category", "reason", "alternatives", "reason_en", "alternatives_en",
        }
        if unknown:
            errors.append(f"{where}: unbekannte Felder {sorted(unknown)} (Tippfehler?)")
    return errors, names


def check_pending(path: Path, rule_names: set[str]) -> list[str]:
    errors: list[str] = []
    data = load_json(path, MAX_PENDING_BYTES, errors)
    if data is None:
        return errors
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("programs"), list):
        return [f"{path.name}: erwartet wird {{\"schema_version\": 1, \"programs\": [...]}}"]
    programs = data["programs"]
    if len(programs) > MAX_PENDING_PROGRAMS:
        errors.append(f"{path.name}: {len(programs)} Programme, die App zeigt höchstens {MAX_PENDING_PROGRAMS}")
    seen: set[str] = set()
    for index, program in enumerate(programs):
        where = f"{path.name}, Eintrag {index + 1}"
        if not isinstance(program, dict):
            errors.append(f"{where}: kein Objekt")
            continue
        name = program.get("name")
        if not is_clean_text(name, MAX_PENDING_NAME_CHARS) or not name.strip():
            errors.append(f"{where}: name fehlt, ist zu lang oder enthält Steuerzeichen")
            continue
        key = name.strip().lower()
        if key in seen:
            errors.append(f"{where}: „{name}“ kommt doppelt vor")
        if key in rule_names:
            errors.append(f"{where}: „{name}“ steht schon in rules.json, bitte aus pending.json entfernen")
        seen.add(key)
        for field, max_chars in (
            ("category", MAX_PENDING_NAME_CHARS),
            ("description", MAX_PENDING_DESCRIPTION_CHARS),
            ("description_en", MAX_PENDING_DESCRIPTION_CHARS),
        ):
            if field in program and not is_clean_text(program[field], max_chars):
                errors.append(f"{where}: {field} ist zu lang oder enthält Steuerzeichen")
        unknown = set(program) - {"name", "category", "description", "description_en"}
        if unknown:
            errors.append(f"{where}: unbekannte Felder {sorted(unknown)} (Tippfehler?)")
    return errors


def main(argv: list[str]) -> int:
    rules_path = Path(argv[0]) if argv else Path("rules.json")
    pending_path = Path(argv[1]) if len(argv) > 1 else Path("pending.json")
    rule_errors, rule_names = check_rules(rules_path)
    errors = rule_errors + check_pending(pending_path, rule_names)
    for error in errors:
        print(f"::error::{error}")
    if errors:
        print(f"{len(errors)} Problem(e) gefunden. Die Dateien so nicht veröffentlichen.")
        return 1
    print(f"{rules_path.name} und {pending_path.name} sind in Ordnung.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
