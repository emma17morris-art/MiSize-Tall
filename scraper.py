"""Utilities for scraping brand sizing data from the MiSize demo site.

The script currently focuses on extracting the inline ``BRAND_SIZE_DATABASE``
JavaScript object from ``index.html`` and exporting it as JSON so it can be
consumed by other tooling (for instance the runtime loader that expects a
``uk_brands.json`` file).

Usage
-----
Run ``python scraper.py`` to extract the data from ``index.html`` in the
repository root and write it to ``uk_brands.json``. You can specify alternative
input or output paths via the ``--input`` and ``--output`` flags.
"""

from __future__ import annotations

import argparse
import ast
import datetime as _dt
import json
from pathlib import Path
from typing import Any, Dict


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("index.html"),
        help="HTML file that contains the BRAND_SIZE_DATABASE definition",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("uk_brands.json"),
        help="Destination JSON file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = extract_brand_database(args.input)
    write_brand_database(data, args.output)
    print(f"Extracted {len(data)} brands to {args.output}")


if __name__ == "__main__":
    main()
