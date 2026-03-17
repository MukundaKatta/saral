"""Tests for jargon translation."""

from saral.simplifier.translator import JargonTranslator
from saral.models import Domain


def test_translates_medical_terms():
    result = JargonTranslator(domains=[Domain.MEDICAL]).translate(
        "The patient has hypertension."
    )
    assert "high blood pressure" in result.simplified_text
    assert "hypertension" not in result.simplified_text


def test_preserves_non_jargon():
    result = JargonTranslator().translate("I went for a walk today.")
    assert result.simplified_text == "I went for a walk today."


def test_returns_glossary():
    text, glossary = JargonTranslator(domains=[Domain.LEGAL]).translate_with_glossary(
        "The defendant filed an appeal."
    )
    assert "defendant" in glossary
    assert "appeal" in glossary


def test_multiple_terms_replaced():
    result = JargonTranslator(domains=[Domain.TECH]).translate(
        "Deploy the container to the cloud."
    )
    assert len(result.jargon_found) >= 2
