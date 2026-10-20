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
AUTH_RESULTS = [
    "spf=fail; dkim=none; dmarc=fail",
    "spf=softfail; dkim=none; dmarc=fail",
    "spf=pass; dkim=pass; dmarc=pass",
    "",
]
REPLY_TO_DOMAINS = ["autre-domaine.example", "collecte-infos.example", ""]

OUTPUT_DIR = Path("data/generated")

LEGIT_DOMAINS = ["exemple-asso.example", "mairie-ville.example", "club-sport.example", "reseau-pro.example"]
LEGIT_SUBJECTS = [
    "Compte rendu de la reunion",
    "Programme de la semaine",
    "Facture de novembre",
    "Piece jointe de la reunion",
]
LEGIT_BODIES = [
    "Bonjour, veuillez trouver ci-joint le compte rendu.",
    "Voici le programme de la semaine.",
    "Merci de traiter ces elements, c'est urgent.",
    "Merci de confirmer votre presence sous 48h.",
]


def build_eml(domain, subject, body, auth, reply_domain):
    lines = [
        f'From: "Service" <contact@{domain}>',
        "To: victime@example.org",
        f"Subject: {subject}",
    ]
    if reply_domain:
        lines.append(f"Reply-To: <retours@{reply_domain}>")
    if auth:
        lines.append(f"Authentication-Results: mx.example.org; {auth}")
    lines.append("Content-Type: text/plain; charset=utf-8")
    return "\n".join(lines) + "\n\n" + body + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    for i in range(1, 11):
        domain = random.choice(SENDER_DOMAINS)
        subject = random.choice(SUBJECTS)
        body = random.choice(BODIES)
        auth = random.choice(AUTH_RESULTS)
        reply_domain = random.choice(REPLY_TO_DOMAINS)
        path = OUTPUT_DIR / f"gen_phishing_{i:02d}.eml"
        path.write_text(
            build_eml(domain, subject, body, auth, reply_domain),
            encoding="utf-8",
        )

    for i in range(1, 11):
        domain = random.choice(LEGIT_DOMAINS)
        subject = random.choice(LEGIT_SUBJECTS)
        body = random.choice(LEGIT_BODIES)
        reply_domain = random.choice([domain, ""])
        path = OUTPUT_DIR / f"gen_legit_{i:02d}.eml"
        path.write_text(
            build_eml(domain, subject, body, "spf=pass; dkim=pass; dmarc=pass", reply_domain),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
