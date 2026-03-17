"""Jargon detection using domain dictionaries."""

from __future__ import annotations

import re

from saral.models import Domain, JargonMatch
from saral.domains.medical import MEDICAL_JARGON
from saral.domains.legal import LEGAL_JARGON
from saral.domains.tech import TECH_JARGON
from saral.domains.finance import FINANCE_JARGON


DOMAIN_DICTS: dict[Domain, dict[str, str]] = {
    Domain.MEDICAL: MEDICAL_JARGON,
    Domain.LEGAL: LEGAL_JARGON,
    Domain.TECH: TECH_JARGON,
    Domain.FINANCE: FINANCE_JARGON,
}


class JargonDetector:
    """Identifies technical jargon terms using domain dictionaries."""

    def __init__(self, domains: list[Domain] | None = None) -> None:
        """Initialize with specific domains or all domains."""
        if domains:
            self._dicts = {d: DOMAIN_DICTS[d] for d in domains}
        else:
            self._dicts = DOMAIN_DICTS

    def detect(self, text: str) -> list[JargonMatch]:
        """Find all jargon terms in the text."""
        matches: list[JargonMatch] = []
        text_lower = text.lower()
        seen: set[str] = set()

        for domain, dictionary in self._dicts.items():
            # Sort by length descending to match longer phrases first
            sorted_terms = sorted(dictionary.keys(), key=len, reverse=True)
            for term in sorted_terms:
                if term in seen:
                    continue
                # Use word boundary matching for single words, substring for phrases
                if " " in term:
                    pattern = re.escape(term)
                else:
                    pattern = r"\b" + re.escape(term) + r"\b"

                match = re.search(pattern, text_lower)
                if match:
                    seen.add(term)
                    matches.append(
                        JargonMatch(
                            term=term,
                            definition=dictionary[term],
                            domain=domain,
                            start=match.start(),
                            end=match.end(),
                        )
                    )

        matches.sort(key=lambda m: m.start)
        return matches

    def detect_domains(self, text: str) -> list[Domain]:
        """Detect which domains are present in the text."""
        matches = self.detect(text)
        domain_counts: dict[Domain, int] = {}
        for m in matches:
            domain_counts[m.domain] = domain_counts.get(m.domain, 0) + 1
        return sorted(domain_counts, key=domain_counts.get, reverse=True)  # type: ignore[arg-type]
