import sys
from pathlib import Path

sys.path.insert(0, "src")

from phishtriage.classifier import load_dataset, train_and_evaluate

texts, labels = load_dataset(Path("data/generated"))
train_and_evaluate(texts, labels)
