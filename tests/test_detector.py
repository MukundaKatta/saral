"""Tests for jargon detection."""

from saral.simplifier.detector import JargonDetector
from saral.models import Domain


def test_detects_medical_jargon():
    text = "The patient has hypertension and tachycardia."
    matches = JargonDetector(domains=[Domain.MEDICAL]).detect(text)
    terms = [m.term for m in matches]
    assert "hypertension" in terms
    assert "tachycardia" in terms


def test_detects_legal_jargon():
    text = "The plaintiff filed a subpoena during litigation."
    matches = JargonDetector(domains=[Domain.LEGAL]).detect(text)
    terms = [m.term for m in matches]
    assert "plaintiff" in terms
    assert "subpoena" in terms


def test_detects_tech_jargon():
    text = "We need to refactor the API and deploy to the cloud."
    matches = JargonDetector(domains=[Domain.TECH]).detect(text)
    terms = [m.term for m in matches]
    assert "api" in terms
    assert "refactor" in terms


def test_detects_finance_jargon():
    text = "The portfolio shows strong diversification with good liquidity."
    matches = JargonDetector(domains=[Domain.FINANCE]).detect(text)
    terms = [m.term for m in matches]
    assert "portfolio" in terms
    assert "diversification" in terms


def test_multi_domain_detection():
    text = "The API endpoint needs authentication. The plaintiff filed a motion."
    matches = JargonDetector().detect(text)
    domains = {m.domain for m in matches}
    assert Domain.TECH in domains
    assert Domain.LEGAL in domains


def test_detect_domains():
    text = "The patient has acute anemia and chronic edema."
    domains = JargonDetector().detect_domains(text)
    assert Domain.MEDICAL in domains


def test_no_jargon_in_plain_text():
    text = "I went to the store and bought some apples."
    matches = JargonDetector().detect(text)
    assert len(matches) == 0
