"""Validate RRAT TOML files against the expected schema."""

import sys
import glob
import toml

ERRORS = []


def error(filename, msg):
    ERRORS.append(f"{filename}: {msg}")


def validate_file(path):
    try:
        data = toml.load(path)
    except toml.decoder.TomlDecodeError as e:
        error(path, f"TOML parse error: {e}")
        return

    # title
    if "title" not in data:
        error(path, "missing 'title'")

    # Required top-level sections
    for section in ("Name", "RA", "Dec", "DM"):
        if section not in data:
            error(path, f"missing required section [{section}]")
            continue

        s = data[section]

        if "value" not in s:
            error(path, f"[{section}] missing 'value'")

        if "error" not in s:
            error(path, f"[{section}] missing 'error'")

        if "ref" not in s:
            error(path, f"[{section}] missing 'ref'")

    # RA / Dec: value must be string, error must be false or string
    for coord in ("RA", "Dec"):
        if coord not in data:
            continue
        s = data[coord]
        if "value" in s and not isinstance(s["value"], str):
            error(path, f"[{coord}] 'value' must be a string (e.g. \"00:31:31.8\")")
        if "error" in s:
            err = s["error"]
            if err is not False and not isinstance(err, str):
                error(
                    path,
                    f"[{coord}] 'error' must be false or a string in hh:mm:ss / dd:mm:ss format, got {type(err).__name__} ({err!r})",
                )

    # Numeric error fields
    for section in ("DM", "Period", "Pdot"):
        if section not in data:
            continue
        s = data[section]
        if "error" in s:
            err = s["error"]
            if err is not False and not isinstance(err, (int, float)):
                error(
                    path,
                    f"[{section}] 'error' must be false or a number, got {type(err).__name__} ({err!r})",
                )

    # BurstRate: must have a Discovery sub-table
    if "BurstRate" in data:
        br = data["BurstRate"]
        if "Discovery" not in br:
            error(path, "[BurstRate] must contain a [BurstRate.Discovery] sub-table")
        else:
            for field in ("value", "telescope", "minflux", "ref"):
                if field not in br["Discovery"]:
                    error(path, f"[BurstRate.Discovery] missing '{field}'")


if __name__ == "__main__":
    patterns = sys.argv[1:] if len(sys.argv) > 1 else ["rrats/*.toml"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

    if not files:
        print("No TOML files found.")
        sys.exit(1)

    for f in sorted(files):
        validate_file(f)

    if ERRORS:
        for msg in ERRORS:
            print(f"ERROR: {msg}")
        sys.exit(1)

    print(f"All {len(files)} RRAT TOML files passed validation.")
