import sys
from pathlib import Path

sys.path.insert(0, "src")

from phishtriage.classifier import train_and_save

train_and_save(Path("data/generated"))
print("Modèle sauvegardé.")
