# RRATalog

The web version of the RRATalog is located at https://rratalog.github.io/rratalog/

The RRATalog is a comprehensive catalog of radio pulsars categorized as Rotating Radio Transients (RRATs). 
For clarity, we only include published pulsars which were discovered through their single pulses rather than a periodicity search.

This repository contains the published parameters of each RRAT in its own TOML file, located in the "rrats" directory. We also provide a machine-readable CSV version of the RRATalog.

## Generating the catalog

The script `make_rratalog.py` reads the individual TOML files and creates the
CSV and HTML versions of the catalog. Run it from the repository root with:

```bash
python make_rratalog.py --data-dir ./rrats
```

Omitting `--data-dir` defaults to `./rrats`, so the command above works
out-of-the-box.

The RRATalog is maintained by Evan Lewis (efl0003 (at) mix.wvu.edu) and Maura McLaughlin (maura.mclaughlin (at) mail.wvu.edu). 
We welcome additions, updates, and corrections to the RRATalog-- either in the form of GitHub pull requests (edit/add the TOML files and we'll take care of the rest), or you can email the maintainers.
If you use the RRATalog, please acknowledge the URL above, and cite Agarwal et al. (in prep).  
