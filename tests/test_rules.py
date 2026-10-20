from pathlib import Path

from phishtriage.parser import parse_eml
from phishtriage.rules import (
    auth_failed,
    reply_to_mismatch,
    run_rules,
    shortened_url,
    total_score,
    urgency_language,
    verdict,
)


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


def test_auth_failed_detected():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    finding = auth_failed(mail)
    assert finding is not None
    assert finding.rule_id == "auth_failed"


def test_no_auth_failed_in_legit_mail():
    mail = parse_eml(Path("data/samples/legit_01.eml"))
    assert auth_failed(mail) is None


def test_run_rules_on_phishing_mail():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    findings = run_rules(mail)
    assert len(findings) == 4


def test_run_rules_on_legit_mail():
    mail = parse_eml(Path("data/samples/legit_01.eml"))
    assert run_rules(mail) == []


def test_total_score_on_phishing_mail():
    mail = parse_eml(Path("data/samples/phishing_01.eml"))
    assert total_score(run_rules(mail)) == 55


def test_verdict_phishing():
    assert verdict(55) == "phishing"


def test_verdict_suspicious():
    assert verdict(25) == "suspicious"


def test_verdict_legit():
    assert verdict(0) == "legit"


def test_verdict_at_phishing_threshold():
    assert verdict(45) == "phishing"


def test_verdict_just_below_threshold():
    assert verdict(44) == "suspicious"


def test_phishing_02_findings():
    mail = parse_eml(Path("data/samples/phishing_02.eml"))
    findings = run_rules(mail)
    ids = {f.rule_id for f in findings}
    assert ids == {"reply_to_mismatch", "urgency_language", "auth_failed"}
    assert "shortened_url" not in ids
    assert verdict(total_score(findings)) == "phishing"
