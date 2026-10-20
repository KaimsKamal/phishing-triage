import joblib

from pathlib import Path

from phishtriage.parser import parse_eml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


def load_dataset(folder: Path) -> tuple[list[str], list[int]]:
    texts = []
    labels = []
    for path in sorted(folder.glob("*.eml")):
        mail = parse_eml(path)
        texts.append(mail.subject + " " + mail.body_text)
        labels.append(1 if "phishing" in path.name else 0)
    return texts, labels


def train_and_evaluate(texts: list[str], labels: list[int]):
    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.3, random_state=42, stratify=labels
    )
    model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(classification_report(y_test, predictions, zero_division=0))
    return model


MODEL_PATH = Path("models/phishing_model.joblib")


def train_and_save(folder: Path, model_path: Path = MODEL_PATH) -> None:
    texts, labels = load_dataset(folder)
    model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    model.fit(texts, labels)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def predict_proba(subject: str, body: str, model_path: Path = MODEL_PATH) -> float:
    model = joblib.load(model_path)
    return float(model.predict_proba([subject + " " + body])[0][1])
