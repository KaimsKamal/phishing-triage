from pathlib import Path

from phishtriage.parser import parse_eml
from phishtriage.rules import reply_to_mismatch, shortened_url,  urgency_language



def test_reply_to_mismatch_detected():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    finding = reply_to_mismatch(mail)
    assert finding is not None
    assert finding.rule_id == "reply_to_mismatch"


def test_no_finding_when_same_domain():
    mail = parse_eml(Path("data/samples/legit_01.eml"))
    assert reply_to_mismatch(mail) is None


def test_shortened_url_detected():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    finding = shortened_url(mail)
    assert finding is not None
    assert finding.rule_id == "shortened_url"


def test_no_shortened_url_in_legit_mail():
    mail = parse_eml(Path("data/samples/legit_01.eml"))
    assert shortened_url(mail) is None


def test_urgency_language_detected():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    finding = urgency_language(mail)
    assert finding is not None
    assert finding.rule_id == "urgency_language"


def test_no_urgency_in_legit_mail():
    mail = parse_eml(Path("data/samples/legit_01.eml"))
    assert urgency_language(mail) is None
