# Evaluation

All numbers below come from a very small, synthetic dataset.
They are indicative only and must not be read as real-world performance.

## Dataset

- 10 hand-written e-mails in `data/samples/` (5 phishing, 5 legitimate)
- 20 generated e-mails in `data/generated/` (10 phishing, 10 legitimate),
  produced by `scripts/generate_samples.py` from templates (seed 42)
- Only reserved domains (`.example`), no real data

## Rules only (hand-written samples)

| Mail | Score | Verdict | Reality |
|---|---|---|---|
| phishing_01 | 55 | phishing | phishing |
| phishing_02 | 45 | phishing | phishing |
| phishing_03 | 35 | suspicious | phishing |
| phishing_04 | 45 | phishing | phishing |
| phishing_05 | 0 | legit | phishing (missed) |

All 5 legitimate samples stay `legit` (scores 0 or 10), including
false positives on "urgent" (legit_02), "sous 48h" (legit_04) and a
Reply-To via a provider (legit_03).

Thresholds: phishing >= 45, suspicious >= 20. They are a judgment call,
not tuned on data.

## Classifier (TF-IDF + logistic regression)

- Random split of generated mails (6 test mails): 1.00 everywhere.
  This is misleading: templates overlap, so the model recognises
  template phrases rather than phishing.
- Trained on generated mails, tested on the 10 hand-written mails:
  accuracy 0.90, recall (phishing) 1.00, precision (phishing) 0.83,
  1 false positive. Confusion matrix: [[4, 1], [0, 5]].
  Still only 10 mails: indicative, not generalisable.

## Combined score

`score = rule_points + round(probability * 50)`.
phishing_05 goes from 0 (legit) to 28 (suspicious): the model rescues
a mail with no technical indicator. The factor 50 is arbitrary.

## Known biases

- Same author wrote hand-written and generated mails (similar style).
- Generated phishing templates were adjusted to include urgency words,
  to avoid the model learning "urgent = legitimate".
