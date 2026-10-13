# CYP Induction, Inhibition and Time-Dependent Inactivation

A small, open-source collection of CYP time-dependent inactivation calculations and legacy rule-based audit workflows.

## What works

- **Browser calculator:** calculate apparent inactivation rate (`k_obs`), remaining enzyme activity, inactivation half-life, and `k_inact/K_I` efficiency from supplied kinetic parameters. Interactive curve with local CSV export.
- **Python model:** the same one-site saturable equations in `cyp_kinetics.tdi.calculate_tdi`.
- **CLI and REST:** separate commands for TDI calculations and the original heuristic audit workflows; FastAPI exposes `POST /api/kinetics` and the existing `POST /api/audit`.
- **Legacy audit workflows:** two preserved implementations in `agents/` and `cyp_kinetics/`. Their configurable-looking metric names are generic thresholds, **not fitted CYP parameters or validated DDI classifications**.

## Kinetic model and scope

```text
k_obs = k_inact × [I] / (K_I + [I])
remaining activity (%) = 100 × exp(−k_obs × time)
inactivation half-life = ln(2) / k_obs   (defined only when k_obs > 0)
```

`k_inact` and `k_obs` have units min⁻¹; `K_I` and inhibitor concentration `[I]` are in µM; time is in minutes. Values are finite and nonnegative; `K_I` must be greater than zero.

**Important limitations:** this is a single-site, constant-inhibitor-concentration model for illustrative in vitro kinetics. It does not fit `k_inact` or `K_I` from experiments, model induction or enzyme turnover, quantify in vivo exposure, or predict clinical DDI magnitude. The existing `enrichment.py` modules are threshold-based placeholders, not implementations of the feature names they describe. Do not use the outputs for clinical decisions.

## Browser usage

Open the GitHub Pages app once deployed, or serve the checked-out folder locally using `python -m http.server 8080 --directory web` and visit `http://localhost:8080/`. Opening the file directly using `file://` is not supported because browser JavaScript modules require HTTP(S). Enter `k_inact`, `K_I`, inhibitor concentration and preincubation time. The calculated values and activity curve update when you select **Calculate activity**. **Export curve (CSV)** generates 101 locally computed samples.

The standalone site is pure JavaScript, not Python or Pyodide; this avoids a large runtime download for four simple equations. The model results are cross-checked by independent Python and JavaScript tests.

## Python usage

Requires Python 3.9 or newer.

```bash
git clone https://github.com/abusuraihsakhri/cyp-induction-inhibition-tdi.git
cd cyp-induction-inhibition-tdi
python -m pip install -e ".[server,test]"

# Numerical TDI calculation (fitted input parameters)
cyp-induction-inhibition-tdi tdi --kinact 0.2 --ki 5 --inhibitor 5 --time 10

# Preserved heuristic audit and CSV processing
python cli.py audit --primary 28.5 --secondary 14.2 --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv

# Local server with browser app at http://127.0.0.1:8000/
python cli.py serve
```

### REST API

The FastAPI application serves the browser UI at `/`, docs at `/docs`, and a kinetic endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/kinetics \
  -H 'Content-Type: application/json' \
  -d '{"kinact_per_min":0.2,"ki_um":5,"inhibitor_um":5,"time_min":10}'
```

`/api/audit`, `/api/chat`, `/api/audit/logs`, `/health`, and the JSON `/metrics` endpoint remain available. The installed CLI also provides an alternate `cyp_kinetics` API server implementation. These server endpoints are not available on GitHub Pages.

## Data privacy and audit trails

- The browser calculator performs calculations and creates CSV downloads locally. It has no network requests and does not persist inputs.
- The Python audit workflow uses an in-memory HMAC-SHA256 chain; the verifier recomputes signatures. The chain itself is **not durable across restarts**.
- Set a unique `AUDIT_SECRET_KEY` in the environment if needed. If omitted, an ephemeral random signing key is generated. Never commit a signing key to version control.
- A regex-based identifier guard is present in the legacy audit path. It does **not** establish de-identification or HIPAA compliance; avoid submitting protected health information.
- Do not expose the FastAPI server publicly without adding authentication, TLS, access controls, and persistence appropriate to your deployment.

## Verification and deployment

```bash
python -m pytest -v
python -m build
node --check web/app.mjs
node --test web/kinetics.test.mjs
docker compose up --build
```

CI covers Python 3.10–3.12, builds, API smoke tests, and browser-model unit tests. A GitHub Actions workflow publishes the static `web/` directory to GitHub Pages on updates to `master`. Current browsers with JavaScript modules are supported; obsolete browsers are not.

## License

MIT — see [LICENSE](LICENSE).
