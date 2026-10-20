# Limits

This project is a learning and portfolio tool, not a production filter.
Do not rely on it to protect a real mailbox.

## Authentication headers

- SPF, DKIM and DMARC cannot be verified from a standalone `.eml` file.
  The tool reads the verdict written by the receiving server in the
  `Authentication-Results` header. If that header is missing or forged,
  the rule has nothing to say.
- The rule looks for the text `fail`, so it also matches `softfail`
  (a weaker signal) and any other occurrence of the word.

## Rules

- `urgency_language` uses substring matching on a short word list.
  It is blind to accents ("immediatement" without accent is missed)
  and can match inside other words ("urgent" in "non urgent").
  Legitimate mails with "urgent" or "sous 48h" trigger false positives.
- `shortened_url` only knows four shortener domains. Others
  (including the synthetic `tinyurl.example`) are not detected.
- `reply_to_mismatch` flags legitimate newsletters sent through a
  provider, and misses attackers who simply omit `Reply-To`.
- Only the body is analysed for urgency, not the subject.
- Weights and thresholds are judgment calls, not tuned on data.

## Classifier

- Trained on about 20 template-generated mails: it learns template
  phrases, not phishing in general. Scores are optimistic.
- Test sets are tiny (6 and 10 mails), so metrics are indicative only.
- The model outputs a weak signal (about 0.55 on phishing_05).
- The factor 50 in the combined score is arbitrary.

## Security

- The model is saved with joblib, which uses pickle. Loading a file
  from an unknown source can execute code. Only load models you
  trained yourself.
- The tool never opens
