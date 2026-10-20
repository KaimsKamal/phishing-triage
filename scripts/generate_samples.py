SENDER_DOMAINS = ["banque-alerte.example", "colis-express.example", "impots-remb.example", "facture-impaye.example"]
SUBJECTS = ["Action requise sur votre compte", "Colis en attente", "Remboursement disponible", "Lettre recommandee a retirer", "Est-ce bien vous ?"]
BODIES = ["Cliquez ici pour confirmer vos informations.", "Reglez les frais pour recevoir votre colis.", "ne laissez pas passer votre bon d'achat", "Cliquez pour recevoir votre remboursement."]

import random
from pathlib import Path

SENDER_DOMAINS = [
    "banque-alerte.example",
    "colis-express.example",
    "impots-remb.example",
    "facture-impaye.example",
]
SUBJECTS = [
    "Action requise sur votre compte",
    "Colis en attente",
    "Remboursement disponible",
    "Lettre recommandee a retirer",
    "Est-ce bien vous ?",
]
BODIES = [
    "Cliquez ici pour confirmer vos informations.",
    "Reglez les frais pour recevoir votre colis.",
    "Ne laissez pas passer votre bon d'achat.",
    "Cliquez pour recevoir votre remboursement.",
]

OUTPUT_DIR = Path("data/generated")


def build_eml(domain: str, subject: str, body: str) -> str:
    return (
        f'From: "Service" <contact@{domain}>\n'
        f"To: victime@example.org\n"
        f"Subject: {subject}\n"
        f"Content-Type: text/plain; charset=utf-8\n"
        f"\n"
        f"{body}\n"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    for i in range(1, 11):
        domain = random.choice(SENDER_DOMAINS)
        subject = random.choice(SUBJECTS)
        body = random.choice(BODIES)
        path = OUTPUT_DIR / f"gen_phishing_{i:02d}.eml"
        path.write_text(build_eml(domain, subject, body), encoding="utf-8")


if __name__ == "__main__":
    main()
