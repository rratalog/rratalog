# RRATalog

The web version of the RRATalog is located at https://rratalog.github.io/rratalog/

The RRATalog is a comprehensive catalog of radio pulsars categorized as Rotating Radio Transients (RRATs). For clarity, we only include published pulsars which were discovered through their single pulses rather than a periodicity search.

## Repository structure

```
rrats/              TOML file for each RRAT (source of truth)
templates/
  template.html     Jinja2 template for the web page
make_rratalog.py    Generates index.html and rratalog.csv from TOML files
sigfig.py           Significant figures formatting utilities
index.html          Generated web page (do not edit directly)
rratalog.csv        Generated machine-readable CSV (do not edit directly)
```

## TOML format

Each RRAT has its own file in `rrats/` (e.g. `J0012+5431.toml`). Parameters follow this structure:

```toml
[Name]
value = "J0012+5431"
error = false
ref = "https://doi.org/..."

[Period]
value = 3.0253007099     # seconds
error = 0.0000000002
ref = "https://doi.org/..."

[DM]
value = 131.3            # pc/cc
error = 0.7
ref = "https://doi.org/..."
```

- `value` — the parameter value
- `error` — uncertainty, or `false` if not reported
- `ref` — DOI or URL of the publication

Nested parameters (BurstRate, Flux, Width) use sub-tables keyed by context:

```toml
[BurstRate.Discovery]
value = 2.7              # hour^-1
ref = "https://doi.org/..."

[Flux.1400]
value = 100              # mJy at 1400 MHz
ref = "https://doi.org/..."
```

## Building

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv run python make_rratalog.py
```

This generates:
- **`index.html`** — the web page with an interactive DataTables table, dark mode, search highlighting, and sticky headers
- **`rratalog.csv`** — machine-readable CSV with separate `_val` and `_err` columns for precise values

## Output columns

| Column | Description |
|--------|-------------|
| Name | Pulsar J-name |
| RA, Dec | Equatorial coordinates |
| DM | Dispersion measure (pc cm⁻³) |
| Period | Spin period (s) |
| Ṗ | Period derivative (10⁻¹⁵ s/s) |
| P_epoch | Period epoch (MJD) |
| Frequency, Ḟ | Spin frequency and derivative (derived from Period/Ṗ) |
| B_surf | Surface magnetic field (10¹² G, derived) |
| Ė | Spin-down luminosity (10³¹ erg/s, derived) |
| τ | Characteristic age (Myr, derived) |
| l, b | Galactic coordinates (derived from RA/Dec) |
| Burst Rate | Single-pulse rate at discovery (hr⁻¹) |
| S₁₄₀₀ | Peak single-pulse flux density at 1.4 GHz (mJy) |
| Width | Pulse width at 1.4 GHz (ms) |

## Contributing

We welcome additions, updates, and corrections — either as GitHub pull requests (edit/add the TOML files and we'll take care of the rest), or email the maintainers.

## Citation

If you use the RRATalog, please acknowledge https://rratalog.github.io/rratalog/ and cite:

Agarwal et al. (2026), *The RRATalog: a Galactic census of rotating radio transients*, MNRAS. https://doi.org/10.1093/mnras/stag787

```bibtex
@article{10.1093/mnras/stag787,
    author = {Agarwal, Devansh and Lewis, Evan F and Lorimer, Duncan R and McLaughlin, Maura A and Cui, Bingyi and Turner, Anna and McMann, Natasha},
    title = {The RRATalog: a Galactic census of rotating radio transients},
    journal = {Monthly Notices of the Royal Astronomical Society},
    pages = {stag787},
    year = {2026},
    month = {04},
    issn = {0035-8711},
    doi = {10.1093/mnras/stag787},
    url = {https://doi.org/10.1093/mnras/stag787},
    eprint = {https://academic.oup.com/mnras/advance-article-pdf/doi/10.1093/mnras/stag787/68156439/stag787.pdf},
}
```

## Maintainers

- Evan Lewis (efl0003 (at) mix.wvu.edu)
- Maura McLaughlin (maura.mclaughlin (at) mail.wvu.edu)
