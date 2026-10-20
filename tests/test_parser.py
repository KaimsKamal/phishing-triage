from pathlib import Path
from phishtriage.parser import parse_eml

SAMPLE = Path("data/samples/phishing_01.eml")


def test_extracts_basic_headers():
    mail = parse_eml(SAMPLE)
    assert "suspendu" in mail.subject
    assert "secure-banque-verif.example" in mail.sender


def test_extracts_urls():
    mail = parse_eml(SAMPLE)
    assert mail.urls == ["http://bit.ly/abc123"]


def test_reply_to_differs_from_sender_domain():
    mail = parse_eml(SAMPLE)
    assert "autre-domaine.example" in mail.reply_to
