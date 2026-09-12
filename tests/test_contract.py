from pathlib import Path


def test_contract_declares_counterfactual_and_calibration_rounds():
    source = Path('contracts/contract.py').read_text()
    assert "def illuminate" in source
    assert "def calibrate" in source
    assert "run_nondet_unsafe" in source
    assert "sha256" in source

def test_site_is_not_a_mock_dashboard():
    site = Path('docs/index.html').read_text()
    assert "writeContract" in site
    assert "Forklight" in site
    assert "hardcoded success" not in site.lower()

