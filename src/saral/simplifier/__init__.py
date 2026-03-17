"""Text simplification modules."""

from saral.simplifier.detector import JargonDetector
from saral.simplifier.translator import JargonTranslator
from saral.simplifier.leveler import ReadingLevelAdapter

__all__ = ["JargonDetector", "JargonTranslator", "ReadingLevelAdapter"]
