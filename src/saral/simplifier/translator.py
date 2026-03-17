"""Jargon translation - replacing terms with plain language."""

from __future__ import annotations

import re

from saral.models import Domain, JargonMatch, SimplificationResult
from saral.simplifier.detector import JargonDetector


class JargonTranslator:
    """Replaces jargon with plain-language equivalents."""

    def __init__(self, domains: list[Domain] | None = None) -> None:
        self._detector = JargonDetector(domains)

    def translate(self, text: str) -> SimplificationResult:
        """Translate jargon terms to plain language."""
        matches = self._detector.detect(text)
        simplified = text

        # Replace from end to start to preserve positions
        for match in sorted(matches, key=lambda m: m.start, reverse=True):
            # Find the actual case-preserved text in the original
            original_span = simplified[match.start:match.end]
            simplified = (
                simplified[:match.start]
                + match.definition
                + simplified[match.end:]
            )

        domains = list({m.domain for m in matches})

        return SimplificationResult(
            original_text=text,
            simplified_text=simplified,
            jargon_found=matches,
            domains_detected=domains,
        )

    def translate_with_glossary(self, text: str) -> tuple[str, dict[str, str]]:
        """Translate text and return a glossary of terms found."""
        result = self.translate(text)
        glossary = {m.term: m.definition for m in result.jargon_found}
        return result.simplified_text, glossary
