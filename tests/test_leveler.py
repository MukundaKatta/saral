"""Tests for reading level adaptation."""

from saral.simplifier.leveler import ReadingLevelAdapter
from saral.models import ReadingLevel


def test_estimate_level():
    text = "The cat sat on the mat. It was a good day."
    stats = ReadingLevelAdapter().estimate_level(text)
    assert stats.word_count > 0
    assert stats.estimated_grade_level > 0


def test_adapt_simplifies_words():
    text = "We need to utilize this methodology to facilitate the process."
    result = ReadingLevelAdapter().adapt(text, ReadingLevel.ELEMENTARY)
    assert "use" in result
    assert "help" in result


def test_adapt_no_change_at_expert():
    text = "We must utilize this methodology to facilitate the process."
    result = ReadingLevelAdapter().adapt(text, ReadingLevel.EXPERT)
    assert result == text


def test_syllable_count():
    adapter = ReadingLevelAdapter()
    assert adapter._count_syllables("cat") == 1
    assert adapter._count_syllables("computer") >= 2


def test_domain_term_count():
    """Verify we have 400+ total jargon terms across all domains."""
    from saral.domains import MEDICAL_JARGON, LEGAL_JARGON, TECH_JARGON, FINANCE_JARGON
    total = len(MEDICAL_JARGON) + len(LEGAL_JARGON) + len(TECH_JARGON) + len(FINANCE_JARGON)
    assert total >= 400, f"Only {total} terms, expected 400+"
