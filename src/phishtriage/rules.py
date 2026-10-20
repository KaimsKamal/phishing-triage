from __future__ import annotations

from dataclasses import dataclass
from email.utils import parseaddr

from phishtriage.parser import ParsedEmail
from urllib.parse import urlparse


@dataclass
class Finding:
    rule_id: str
    points: int
    explanation: str


def get_domain(address_header: str) -> str:
    _, address = parseaddr(address_header)
    return address.split("@")[-1].lower()


def reply_to_mismatch(mail: ParsedEmail) -> Finding | None:
    if not mail.reply_to:
        return None

    sender_domain = get_domain(mail.sender)
    reply_domain = get_domain(mail.reply_to)

    if sender_domain != reply_domain:
        return Finding(
            rule_id="reply_to_mismatch",
            points=10,
            explanation=f"Reply-To ({reply_domain}) differs from sender ({sender_domain})",
        )
    return None


SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl"}


def shortened_url(mail: ParsedEmail) -> Finding | None:
    for url in mail.urls:
        domain = urlparse(url).hostname
        if domain in SHORTENERS:
            return Finding(
                rule_id="shortened_url",
                points=10,
                explanation=f"Shortened URL detected: {domain}",
            )
    return None


URGENCY_WORDS = {"urgent", "immédiatement", "suspendu"}


def urgency_language(mail: ParsedEmail) -> Finding | None:
    text = mail.body_text.lower().split()
    for word in text:
        if word in URGENCY_WORDS:
            return Finding(
                rule_id="urgency_language",
                points=10,
                explanation=f"Urgency wording detected: {word}",
            )
    return None


def auth_failed(mail: ParsedEmail) -> Finding | None:
    results = mail.auth_results.lower()
    if "fail" in results:
        return Finding(
            rule_id="auth_failed",
            points=25,
            explanation="SPF, DKIM or DMARC check failed",
        )
    return None
