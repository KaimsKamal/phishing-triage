import argparse
from pathlib import Path

from phishtriage.parser import parse_eml
from phishtriage.rules import run_rules, total_score, verdict


def main() -> None:
    parser = argparse.ArgumentParser(description="Triage a suspicious e-mail")
    parser.add_argument("eml_file", type=Path, help="path to a .eml file")
    args = parser.parse_args()

    mail = parse_eml(args.eml_file)
    findings = run_rules(mail)
    score = total_score(findings)

    print(f"Subject: {mail.subject}")
    print(f"From: {mail.sender}")
    print()
    for finding in findings:
        print(f"  [+{finding.points}] {finding.explanation}")
    print()
    print(f"Score: {score}")
    print(f"Verdict: {verdict(score)}")


if __name__ == "__main__":
    main()
