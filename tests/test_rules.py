from pathlib import Path

from phishtriage.parser import parse_eml
from phishtriage.rules import reply_to_mismatch


def test_reply_to_mismatch_detected():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    finding = reply_to_mismatch(mail)
    assert finding is not None
    assert finding.rule_id == "reply_to_mismatch"


def test_no_finding_when_same_domain():
    mail = parse_eml(Path("data/samples/legit_01.eml"))
    assert reply_to_mismatch(mail) is None
