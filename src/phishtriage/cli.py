import argparse
import json
from pathlib import Path

from phishtriage.classifier import MODEL_PATH, predict_proba
from phishtriage.parser import parse_eml
from phishtriage.rules import combined_score, run_rules, total_score, verdict


def main() -> None:
    parser = argparse.ArgumentParser(description="Triage a suspicious e-mail")
    parser.add_argument("eml_file", type=Path, help="path to a .eml file")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args()

    mail = parse_eml(args.eml_file)
    findings = run_rules(mail)
    rule_points = total_score(findings)

    proba = None
    score = rule_points
    if MODEL_PATH.exists():
        proba = predict_proba(mail.subject, mail.body_text)
        score = combined_score(rule_points, proba)

    if args.json:
        report = {
            "subject": mail.subject,
            "rule_points": rule_points,
            "model_proba": proba,
            "score": score,
            "verdict": verdict(score),
            "findings": [
                {"rule_id": f.rule_id, "points": f.points, "explanation": f.explanation}
                for f in findings
            ],
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    print(f"Subject: {mail.subject}")
    print(f"From: {mail.sender}")
    print()
    for finding in findings:
        print(f"  [+{finding.points}] {finding.explanation}")
    print()
    print(f"Rule points: {rule_points}")
    if proba is not None:
        print(f"Model probability: {proba:.2f}")
    print(f"Score: {score}")
    print(f"Verdict: {verdict(score)}")


if __name__ == "__main__":
    main()
