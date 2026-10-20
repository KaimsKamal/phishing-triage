import subprocess
import sys


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
