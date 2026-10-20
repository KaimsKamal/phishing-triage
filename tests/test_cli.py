import subprocess
import sys
import json


def test_cli_phishing_mail():
    result = subprocess.run(
        [sys.executable, "-m", "phishtriage", "data/samples/phishing_01.eml"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": "src"},
    )
    assert result.returncode == 0
    assert "Verdict: phishing" in result.stdout


def test_cli_legit_mail():
    result = subprocess.run(
        [sys.executable, "-m", "phishtriage", "data/samples/legit_01.eml"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": "src"},
    )
    assert result.returncode == 0
    assert "Verdict: legit" in result.stdout


def test_cli_json_output():
    result = subprocess.run(
        [sys.executable, "-m", "phishtriage", "data/samples/phishing_01.eml", "--json"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": "src"},
    )
    data = json.loads(result.stdout)
    assert data["score"] == 55
    assert data["verdict"] == "phishing"
    assert len(data["findings"]) == 4
