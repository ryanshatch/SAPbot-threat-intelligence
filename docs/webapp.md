# Read-only investigation explorer

The web app displays the repository's generated SQLite index. Dedicated case `addresses.csv` files remain authoritative. The app never writes labels or transactions, fetches chain data, or updates case reports.

## Run locally

Use Python 3.12 or newer from the repository root:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-web.txt
python -m threatintel validate
python scripts/prepare_web_db.py
python webapp.py
```

Visit `http://127.0.0.1:8000`. To place the derived database elsewhere, set `THREATINTEL_DB` to a writable path before preparing and starting the app. `python -m unittest discover -s tests -v` runs importer and web tests. The web process opens SQLite in read-only mode and `/healthz` reports 503 if the generated database is unavailable.

## Deploy on Render

The root [`render.yaml`](../render.yaml) describes one Python web service on the free plan. Its startup command rebuilds the disposable index from checked-in case CSVs, then starts Gunicorn on `0.0.0.0:$PORT`. There is no external database, persistent disk, API key, or scheduled collection job. A new deployment picks up reviewed CSV changes. The generated `.sqlite` file is ignored by Git.

After this change is merged, create a Render Blueprint from this GitHub repository, or create a Python web service with the build and start commands in `render.yaml`. Render health checks use `/healthz`. If you use a paid instance or custom domain later, update the service configuration separately.

## Current scope

- Home shows counts of **indexed** cases and observations, not totals for the repository.
- Cases and indicators are searchable. Indicator filters use network IDs and the case observation's explicit threat label. Case pages show the original role, confidence, notes, source CSV row, and evidence links.
- Legacy address layouts and sweep recap CSVs are still excluded by the importer. Some narrative-only cases have no compatible address CSV and will not appear until the data-model roadmap is extended.
- Confidence and priority are source fields, not computed scores. Shared addresses on separate networks remain separate observations. A false threat label can be a victim, recovery, or service pivot; it should not be reclassified by association.

The later [roadmap](roadmap.md) items—legacy migration, sourced flow events, optional collectors, and graph reports—can be added without blocking this read-only release.
