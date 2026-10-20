import sys
from pathlib import Path

sys.path.insert(0, "src")

from phishtriage.classifier import predict_proba
from phishtriage.parser import parse_eml

mail = parse_eml(Path("data/samples/phishing_05.eml"))
print(predict_proba(mail.subject, mail.body_text))
