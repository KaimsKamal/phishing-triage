import sys
from pathlib import Path

sys.path.insert(0, "src")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline

from phishtriage.classifier import load_dataset

gen_texts, gen_labels = load_dataset(Path("data/generated"))
hand_texts, hand_labels = load_dataset(Path("data/samples"))

model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(gen_texts, gen_labels)
predictions = model.predict(hand_texts)

print(classification_report(hand_labels, predictions, zero_division=0))
print("Matrice de confusion (lignes = réalité, colonnes = prédiction) :")
print(confusion_matrix(hand_labels, predictions))

hand_paths = sorted(Path("data/samples").glob("*.eml"))
for path, real, pred in zip(hand_paths, hand_labels, predictions):
    if real != pred:
        print("Erreur :", path.name, "réalité =", real, "prédiction =", pred)
