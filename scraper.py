"""Utilities for managing the MiSize brand dataset.

The ``extract`` command re-exports the inline ``BRAND_SIZE_DATABASE`` from
``index.html`` so you can bootstrap the JSON dataset. Use the ``manual`` command
to enter authoritative measurements sourced from official brand guides. Each
mode supports the ``--output`` flag to control where the resulting JSON file is
saved.
"""

from __future__ import annotations

import argparse
import ast
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


ISO_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _read_file(path: Path) -> str:
    """Return the contents of *path* as UTF-8 text."""

    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:  # pragma: no cover - defensive guard
        raise SystemExit(f"Input file '{path}' was not found") from exc


def _extract_js_object(source: str, variable: str) -> str:
    """Extract the object literal assigned to ``variable`` from *source*.

    This walks the source code starting from the ``const <variable> =``
    declaration and returns the text inside the matching curly braces.
    """

    marker = f"const {variable}"
    try:
        decl_start = source.index(marker)
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise SystemExit(f"Unable to find declaration for '{variable}'") from exc

    brace_start = source.index("{", decl_start)
    depth = 0
    for position in range(brace_start, len(source)):
        char = source[position]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace_start : position + 1]

    raise SystemExit(f"Unable to locate the end of '{variable}' object literal")


def _normalise_js_object(js_object: str) -> Dict[str, Any]:
    """Convert a JavaScript object literal into a Python dictionary.

    The ``BRAND_SIZE_DATABASE`` definition mixes bare identifiers (``name``) and
    string keys (``'S'``) and contains ``new Date().toISOString()`` calls.  The
    transformation below converts the snippet into a shape ``ast.literal_eval``
    can parse reliably.
    """

    # Replace the dynamic date helper with an ISO timestamp so we can parse it.
    timestamp = _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    pythonish = js_object.replace("new Date().toISOString()", f"'{timestamp}'")

    # Quote bare identifiers that appear directly before a colon. We anchor the
    # regex so quoted keys (e.g. `'S':`) remain untouched.
    def _replacer(match: "re.Match[str]") -> str:
        prefix, whitespace, identifier = match.groups()
        return f"{prefix}{whitespace}'{identifier}':"

    import re

    pattern = re.compile(r"(\{|,)(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:")
    pythonish = pattern.sub(_replacer, pythonish)

    try:
        return ast.literal_eval(pythonish)
    except (ValueError, SyntaxError) as exc:  # pragma: no cover - defensive guard
        raise SystemExit("Failed to parse brand database into Python data") from exc


def extract_brand_database(source_path: Path) -> Dict[str, Any]:
    """Load ``source_path`` and return the ``BRAND_SIZE_DATABASE`` mapping."""

    raw_source = _read_file(source_path)
    js_object = _extract_js_object(raw_source, "BRAND_SIZE_DATABASE")
    return _normalise_js_object(js_object)


def write_brand_database(data: Dict[str, Any], destination: Path) -> None:
    """Serialise *data* to *destination* with stable formatting."""

    destination.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


DEMO_NOTE_MARKERS = {
    "Excellent size inclusivity, detailed size guides, online exclusive",
    "Fast fashion, trend-focused, size up recommended",
    "Sustainable lines run differently, budget-friendly",
    "Reliable consistent sizing across seasons",
}


def _find_demo_markers(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return brands whose note fields still contain demo copy."""

    hits: Dict[str, Any] = {}
    for brand, payload in data.items():
        notes = payload.get("notes", {})
        for key, value in notes.items():
            if isinstance(value, str) and value in DEMO_NOTE_MARKERS:
                hits.setdefault(brand, {})[key] = value
    return hits


def _prompt(message: str) -> str:
    """Return ``input`` stripped of surrounding whitespace."""

    return input(message).strip()


def _prompt_number(message: str) -> float:
    """Prompt until the user supplies a numeric measurement."""

    while True:
        raw = _prompt(message)
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a numeric value (e.g. 32 or 27.5).")
            continue
        return int(value) if value.is_integer() else value


def _load_existing_dataset(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive guard
        raise SystemExit(
            f"Unable to load existing dataset from '{path}': {exc}"
        ) from exc


def _manual_entry(destination: Path) -> None:
    """Collect brand data interactively and save it to *destination*."""

    print("Entering manual data entry mode. Press Ctrl+C at any time to abort.\n")
    data = _load_existing_dataset(destination)
    if data:
        print(
            f"Loaded {len(data)} existing brand(s) from {destination}. "
            "You can add new entries or overwrite an existing one.\n"
        )

    try:
        while True:
            brand_name = _prompt("Brand name (leave blank to finish): ")
            if not brand_name:
                break
            if brand_name in data:
                confirm = _prompt(
                    f"'{brand_name}' already exists. Overwrite? [y/N]: "
                ).lower()
                if confirm not in {"y", "yes"}:
                    print("  Skipping existing brand.\n")
                    continue

            brand_payload: Dict[str, Any] = {"name": brand_name}
            categories: Dict[str, Any] = {}
            print("Enter categories for this brand. Examples: Women's Jeans, Men's Shirts.")
            while True:
                category_name = _prompt("  Category (leave blank to finish categories): ")
                if not category_name:
                    break
                sizes: Dict[str, Any] = {}
                while True:
                    size_label = _prompt("    Size label (leave blank to finish sizes): ")
                    if not size_label:
                        break
                    measurements: Dict[str, float] = {}
                    print(
                        "    Enter measurements for this size. Examples: bust, waist, hips."
                    )
                    while True:
                        measurement_name = _prompt(
                            "      Measurement name (leave blank to finish measurements): "
                        )
                        if not measurement_name:
                            break
                        measurement_value = _prompt_number("      Measurement value: ")
                        measurements[measurement_name] = measurement_value
                    if not measurements:
                        print("      No measurements recorded; skipping this size.")
                        continue
                    sizes[size_label] = measurements
                if not sizes:
                    print("    No sizes recorded; skipping this category.")
                    continue
                categories[category_name] = sizes
            if not categories:
                print("  No categories recorded for this brand; discarding entry.\n")
                continue
            brand_payload["categories"] = categories

            default_timestamp = _dt.datetime.utcnow().strftime(ISO_TIMESTAMP_FORMAT)
            timestamp = _prompt(
                f"  Last updated timestamp [{default_timestamp}]: "
            )
            brand_payload["lastUpdated"] = timestamp or default_timestamp

            source_url = _prompt("  Source URL (optional): ")
            if source_url:
                brand_payload["sourceUrl"] = source_url

            source_date = _prompt("  Source publication date (optional): ")
            if source_date:
                brand_payload["sourceDate"] = source_date

            notes: Dict[str, str] = {}
            print("  Add any notes (fit guidance, inclusivity info, etc.).")
            while True:
                note_key = _prompt("    Note label (leave blank to finish notes): ")
                if not note_key:
                    break
                note_value = _prompt("    Note text: ")
                if note_value:
                    notes[note_key] = note_value
            if notes:
                brand_payload["notes"] = notes

            data[brand_name] = brand_payload
            print(f"Recorded data for '{brand_name}'.\n")
    except KeyboardInterrupt:
        print("\nAborted by user; keeping collected data.")

    if not data:
        print("No brand data captured. Nothing written.")
        return

    write_brand_database(data, destination)
    print(f"Saved {len(data)} brand(s) to {destination}.")


def parse_args(raw_args: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    extract_parser = subparsers.add_parser(
        "extract", help="Re-export the inline BRAND_SIZE_DATABASE from index.html"
    )
    extract_parser.add_argument(
        "--input",
        type=Path,
        default=Path("index.html"),
        help="HTML file that contains the BRAND_SIZE_DATABASE definition",
    )
    extract_parser.add_argument(
        "--output",
        type=Path,
        default=Path("uk_brands.json"),
        help="Destination JSON file",
    )
    extract_parser.add_argument(
        "--check-demo-data",
        action="store_true",
        help="Warn if the export still matches known demo placeholder copy",
    )

    manual_parser = subparsers.add_parser(
        "manual", help="Enter brand data interactively and write it to JSON"
    )
    manual_parser.add_argument(
        "--output",
        type=Path,
        default=Path("uk_brands.json"),
        help="Destination JSON file",
    )

    if raw_args is None:
        raw_args = sys.argv[1:]

    help_flags = {"-h", "--help"}
    if raw_args and raw_args[0] in help_flags:
        return parser.parse_args(raw_args)

    if not raw_args or raw_args[0].startswith("-"):
        # Maintain backwards compatibility with ``python scraper.py`` plus
        # optional flags (``--input``/``--output``/``--check-demo-data``) by
        # routing to the ``extract`` sub-command when no explicit action is
        # provided.
        raw_args = ["extract", *raw_args]

    return parser.parse_args(raw_args)


def _run_extract(args: argparse.Namespace) -> None:
    data = extract_brand_database(args.input)
    write_brand_database(data, args.output)
    print(f"Extracted {len(data)} brands to {args.output}")
    if args.check_demo_data:
        demo_hits = _find_demo_markers(data)
        if demo_hits:
            print("Detected demo placeholder copy in the following brands:")
            for brand, markers in sorted(demo_hits.items()):
                marker_list = ", ".join(f"{key}: {value}" for key, value in markers.items())
                print(f"  - {brand}: {marker_list}")
            print(
                "Replace these values with measurements sourced from official size guides "
                "before distributing the dataset."
            )
        else:
            print("No demo placeholder copy detected; dataset appears to be updated.")


def main() -> None:
    args = parse_args()

    if args.command == "manual":
        _manual_entry(args.output)
    else:
        _run_extract(args)


if __name__ == "__main__":
    main()
