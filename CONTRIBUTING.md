# Contributing to RRATalog

## What this repo is

RRATalog is a TOML-per-source catalog of Rotating Radio Transients (RRATs). Each RRAT lives in `rrats/<J-name>.toml`. The script `make_rratalog.py` reads all TOML files and generates `index.html` (interactive web table) and `rratalog.csv` (machine-readable CSV). See `README.md` for the full project description.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/rratalog/rratalog.git
cd rratalog
uv sync
```

## File layout and naming

- One TOML file per RRAT under `rrats/`.
- Filename = psrcat-style J-name: `J<HHMM><±DDMM>.toml` (e.g. `J0746+5514.toml`). The shorter form `J<HHMM><±DD>` is acceptable when coordinates are not yet precisely known.
- `title` at the top of the file **must** match `[Name].value`, which **must** match the filename stem (e.g. all three are `"J0746+5514"`).

## Schema reference

Start from `templates/template.toml`. Below is every field in use across the catalog.

### Required sections

| Section | Field | Type | Unit | Notes |
|---------|-------|------|------|-------|
| `[Name]` | `value` | string | — | psrcat J-name |
| `[Name]` | `error` | `false` | — | always `false` |
| `[Name]` | `ref` | string | — | DOI of discovery paper |
| `[RA]` | `value` | string | hh:mm:ss.ss | e.g. `"07:46:47.4"` |
| `[RA]` | `error` | `false` or string | hh:mm:ss.ss | e.g. `"00:00:00.2"` |
| `[RA]` | `ref` | string | — | DOI |
| `[Dec]` | `value` | string | (sign)dd:mm:ss.ss | e.g. `"+55:14:37"` |
| `[Dec]` | `error` | `false` or string | dd:mm:ss.ss | e.g. `"00:00:02"` |
| `[Dec]` | `ref` | string | — | DOI |
| `[DM]` | `value` | number | pc cm⁻³ | |
| `[DM]` | `error` | `false` or number | pc cm⁻³ | |
| `[DM]` | `ref` | string | — | DOI |

### Optional sections

| Section | Field | Type | Unit | Notes |
|---------|-------|------|------|-------|
| `[Period]` | `value` | number | s | strongly encouraged |
| `[Period]` | `error` | `false` or number | s | |
| `[Period]` | `ref` | string | — | |
| `[Pdot]` | `value` | number | s/s | use scientific notation: `5.5e-15` |
| `[Pdot]` | `error` | `false` or number | s/s | |
| `[Pdot]` | `ref` | string | — | |
| `[Pepoch]` | `value` | number | MJD | include when timing solution available |
| `[Pepoch]` | `error` | `false` | — | always `false` |
| `[Pepoch]` | `ref` | string | — | see `rrats/J0012+5431.toml` for example |
| `[Flux.<freqMHz>]` | `value` | number | mJy | repeat per band; e.g. `[Flux.150]`, `[Flux.1400]` |
| `[Flux.<freqMHz>]` | `error` | `false` or number | mJy | |
| `[Flux.<freqMHz>]` | `frequency` | number | MHz | must match sub-table key |
| `[Flux.<freqMHz>]` | `ref` | string | — | see `rrats/J1848+1516.toml` |
| `[Width.<freqMHz>]` | `value` | number | ms | |
| `[Width.<freqMHz>]` | `error` | `false` or number | ms | |
| `[Width.<freqMHz>]` | `frequency` | number | MHz | |
| `[Width.<freqMHz>]` | `ref` | string | — | |
| `[BurstRate.Discovery]` | `value` | number | hr⁻¹ | **required** when any `[BurstRate]` is present |
| `[BurstRate.Discovery]` | `error` | `false` or number | hr⁻¹ | |
| `[BurstRate.Discovery]` | `frequency` | number | MHz | |
| `[BurstRate.Discovery]` | `telescope` | string | — | e.g. `"GBT"`, `"CHIME"`, `"I-LOFAR"` |
| `[BurstRate.Discovery]` | `minflux` | `false` or number | mJy | minimum detectable flux |
| `[BurstRate.Discovery]` | `ref` | string | — | |
| `[BurstRate.<label>]` | (same fields) | | | extra sub-tables for other telescopes/epochs, e.g. `[BurstRate.LOFAR150]`; see `rrats/J0201+7005.toml` |

**Inline comment conventions** (add to value lines where helpful):
```
value = 1.09  # seconds
value = 26.924  # pc/cc
value = "23:55:48.62"  # hh:mm:ss.ss
value = "+15:23:19"  # (sign)dd:mm:ss.ss
value = 0.41e-15  # s/s
value = 6.0  # hour^-1
value = 4.5  # mJy
value = 17  # ms
frequency = 150  # MHz
```

## Add a new RRAT — worked example

This example uses `J0746+5514`, discovered and timed in McKenna et al. 2024 (doi:10.1093/mnras/stad2900).

**1. Copy the template:**

```bash
cp templates/template.toml rrats/J0746+5514.toml
```

**2. Fill in `title` and `[Name]`:**

```toml
title = "J0746+5514"

[Name]
value = "J0746+5514"
error = false
ref = "https://doi.org/10.1093/mnras/stad2900"
```

**3. Fill in coordinates (timing-solution precision):**

```toml
[RA]
value = "07:46:47.4"  # hh:mm:ss.ss
error = "00:00:00.2"
ref = "https://doi.org/10.1093/mnras/stad2900"

[Dec]
value = "+55:14:37"  # (sign)dd:mm:ss.ss
error = "00:00:02"
ref = "https://doi.org/10.1093/mnras/stad2900"
```

**4. Fill in dispersion measure, period, Pdot:**

```toml
[DM]
value = 10.318  # pc/cc
error = 0.007
ref = "https://doi.org/10.1093/mnras/stad2900"

[Period]
value = 2.8936675025  # seconds
error = 0.0000000004
ref = "https://doi.org/10.1093/mnras/stad2900"

[Pdot]
value = 10.19e-15  # s/s
error = 0.05e-15
ref = "https://doi.org/10.1093/mnras/stad2900"
```

**5. Add the timing epoch (when a timing solution is available):**

```toml
[Pepoch]
value = 59558
error = false
ref = "https://doi.org/10.1093/mnras/stad2900"
```

**6. Add burst rate and pulse width at the detection frequency:**

```toml
[BurstRate]
[BurstRate.Discovery]
value = 1.11  # hour^-1
error = 0.16
frequency = 150  # MHz
telescope = "I-LOFAR"
minflux = false  # mJy
ref = "https://doi.org/10.1093/mnras/stad2900"

[Width]
[Width.150]
value = 32  # ms
error = 20
frequency = 150  # MHz
ref = "https://doi.org/10.1093/mnras/stad2900"
```

**7. Add a reference comment at the bottom:**

```toml
# McKenna et al 2024: https://doi.org/10.1093/mnras/stad2900
```

The final file is `rrats/J0746+5514.toml`.

## Edit an existing RRAT

**Add a flux/width at a new frequency** — append a new sub-table anywhere after the parent table header:

```toml
[Flux.350]
value = 1.1  # mJy
error = 0.3
frequency = 350  # MHz
ref = "https://doi.org/..."
```

**Add a burst rate from a new telescope** — append a new `[BurstRate.<label>]` sub-table (choose a descriptive label):

```toml
[BurstRate.LOFAR150]
value = 9.0  # hour^-1
error = 0.5
frequency = 150  # MHz
telescope = "I-LOFAR"
minflux = false  # mJy
ref = "https://doi.org/..."
```

**Refine DM, RA, or Dec** — update `value`, `error`, and `ref` in the relevant section. When a more precise value supersedes an older one, update `ref` to the newer paper.

**Update the source name / rename the file:**

```bash
git mv rrats/J0054+66.toml rrats/J0054+6650.toml
# then update title and [Name].value inside the file
```

## Local checks (run before opening a PR)

```bash
# Schema validation
uv run python validate_rrats.py

# TOML formatting
uvx tombi format --check rrats/*.toml

# Python formatting
uvx ruff format --check .

# Build the site
uv run python make_rratalog.py
```

To auto-fix formatting issues: `uvx tombi format rrats/*.toml` and `uvx ruff format .`.

## CI expectations

- **Lint** (`lint.yml`): runs on every PR and push to `main`. Checks Python formatting (`ruff`), TOML formatting (`tombi`), and schema validation. All three must pass.
- **Build** (`build-pages.yml`): runs on push to `main` whenever source files change. Regenerates `index.html` and `rratalog.csv` via `make_rratalog.py` and commits them automatically. **Do not hand-edit `index.html` or `rratalog.csv`.**

## PR checklist

- [ ] One TOML file per source; one paper per PR (preferred)
- [ ] `title`, `[Name].value`, and filename stem all match
- [ ] Every `ref` field contains a full DOI URL (`https://doi.org/...`)
- [ ] `uv run python validate_rrats.py` passes with no errors
- [ ] `uvx tombi format --check rrats/*.toml` passes (or run `uvx tombi format rrats/*.toml` to auto-fix)
- [ ] Only edit `index.html` / `rratalog.csv` if CI is broken — otherwise let the build workflow regenerate them
