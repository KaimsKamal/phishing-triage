# Architecture

phishing-triage reads one `.eml` file and produces a report with
indicators, a score and a verdict. Everything runs locally.

## Flow
.eml file
|
v
parser.py -> ParsedEmail (subject, sender, reply_to,
| auth_results, body_text, urls)
|
+--> rules.py -> list of Finding (rule_id, points, explanation)
| -> rule_points (sum)
|
+--> classifier.py -> probability of phishing (0 to 1)
(only if models/phishing_model.joblib exists)
|
v
combined_score = rule_points + round(probability * 50)
|
v
verdict: phishing (>= 45), suspicious (>= 20), legit
|
v
cli.py -> text report or JSON (--json)

## Modules

| File | Role |
|---|---|
| `src/phishtriage/parser.py` | Reads a `.eml` file with the standard `email` package |
| `src/phishtriage/rules.py` | Four rules, scoring, verdict, combined score |
| `src/phishtriage/classifier.py` | Dataset loading, training, evaluation, model save/load |
| `src/phishtriage/cli.py` | Command line entry point |
| `scripts/generate_samples.py` | Generates synthetic e-mails (seed 42) |
| `scripts/train_model.py` | Trains and saves the model |
| `scripts/eval_handwritten.py` | Trains on generated mails, tests on hand-written ones |
| `data/samples/` | 10 hand-written synthetic e-mails |
| `data/generated/` | Generated e-mails (not versioned) |
| `tests/` | pytest tests, run by GitHub Actions |

## Design choices

- **Rules first, model second.** Rules are explainable: each one
  returns a `Finding` with a reason. The model catches mails that
  have no technical indicator, but explains nothing.
- **Graceful fallback.** Without a model file, the CLI uses rules
  only. This also keeps CI independent of local artifacts.
- **Reproducibility.** Fixed seeds for data generation and for the
  train/test split. File lists are sorted.
- **No network, no secrets.** The tool only reads text; it never
  opens links or attachments.

## Planned

- Streamlit interface (`app/`)
- URL analysis (`urls.py`): punycode, IP addresses, risky TLDs
- Optional local LLM (Ollama) to rephrase the explanation
