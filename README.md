# phishing-triage

![tests](https://github.com/KaimsKamal/phishing-triage/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/badge/license-MIT-blue.svg)

Explainable phishing e-mail triage. Give it a `.eml` file: it extracts
headers and links, applies transparent rules, adds a small scikit-learn
classifier, and prints a report with the indicators, a score and a verdict.

Free, local, no API keys, synthetic data only.

> Learning and portfolio project, not a production filter.
> See [docs/limits.md](docs/limits.md).

## Features

- `.eml` parser (headers, body, URLs) built on the standard `email` package
- Four explainable rules: authentication failure, Reply-To mismatch,
  shortened URL, urgency wording
- TF-IDF + logistic regression classifier that catches mails with no
  technical indicator
- Combined score and three-level verdict: `legit`, `suspicious`, `phishing`
- Text or JSON output
- pytest suite and GitHub Actions CI

## Quick start

```bash
git clone https://github.com/KaimsKamal/phishing-triage.git
cd phishing-triage
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# optional: generate synthetic data and train the model
python scripts/generate_samples.py
python scripts/train_model.py

PYTHONPATH=src python -m phishtriage data/samples/phishing_01.eml
PYTHONPATH=src python -m phishtriage data/samples/phishing_01.eml --json
pytest
```

Without a trained model, the tool falls back to rules only.

## Example report

```
Subject: Action requise : compte suspendu sous 24h
From: Support Banque <alerte@secure-banque-verif.example>

  [+10] Reply-To (autre-domaine.example) differs from sender (secure-banque-verif.example)
  [+10] Shortened URL detected: bit.ly
  [+10] Urgency wording detected: immédiatement
  [+25] SPF, DKIM or DMARC check failed

Rule points: 55
Score: 55
Verdict: phishing
```

With a trained model, the report also shows `Model probability` and the
score includes `round(probability * 50)`.

## How it works

```
.eml -> parser -> rules (points) ----+
                \-> classifier (p) --+-> score -> verdict -> report
```

Details in [docs/architecture.md](docs/architecture.md).

## Evaluation and limitations

On 10 hand-written mails, rules alone miss one phishing (score 0). The
classifier, trained on generated mails, reaches 0.90 accuracy on those
10 mails. That is a tiny sample: indicative only. A perfect score on
generated data is misleading because templates overlap.

See [docs/evaluation.md](docs/evaluation.md) and
[docs/limits.md](docs/limits.md).

## Ethics: synthetic data only

All e-mails use reserved domains (`.example`). No real personal data, keys
or secrets are in the repository.

## License

MIT, see [LICENSE](LICENSE).
