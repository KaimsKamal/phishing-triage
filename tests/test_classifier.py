from pathlib import Path

from phishtriage.classifier import predict_proba, train_and_save


def test_train_save_and_predict(tmp_path):
    model_file = tmp_path / "model.joblib"
    train_and_save(Path("data/samples"), model_path=model_file)
    assert model_file.exists()

    proba = predict_proba(
        "Action requise",
        "Cliquez ici pour confirmer vos informations.",
        model_path=model_file,
    )
    assert 0.0 <= proba <= 1.0
    