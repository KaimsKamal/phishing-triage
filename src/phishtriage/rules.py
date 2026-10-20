from __future__ import annotations

from dataclasses import dataclass
from email.utils import parseaddr

from phishtriage.parser import ParsedEmail


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
