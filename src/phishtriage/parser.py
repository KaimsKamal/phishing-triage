from __future__ import annotations

import re
from dataclasses import dataclass, field
from email import policy
from email.parser import BytesParser
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s<>\"')]+", re.IGNORECASE)


@dataclass
class ParsedEmail:
    subject: str
    sender: str
    reply_to: str
    auth_results: str
    body_text: str
    urls: list[str] = field(default_factory=list)


def parse_eml(path: Path) -> ParsedEmail:
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    body_part = msg.get_body(preferencelist=("plain", "html"))
    body = body_part.get_content() if body_part else ""
    urls = list(dict.fromkeys(URL_RE.findall(body)))  # dédoublonne, garde l'ordre

    return ParsedEmail(
        subject=str(msg["Subject"] or ""),
        sender=str(msg["From"] or ""),
        reply_to=str(msg["Reply-To"] or ""),
        auth_results=str(msg["Authentication-Results"] or ""),
        body_text=body,
        urls=urls,
    )
