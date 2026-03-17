"""Reading level adaptation."""

from __future__ import annotations

import re
import math

from saral.models import ReadingLevel, TextStats


# Approximate target grade levels
LEVEL_GRADES: dict[ReadingLevel, float] = {
    ReadingLevel.ELEMENTARY: 4.0,
    ReadingLevel.MIDDLE: 7.0,
    ReadingLevel.HIGH_SCHOOL: 10.0,
    ReadingLevel.COLLEGE: 13.0,
    ReadingLevel.EXPERT: 16.0,
}

# Words to use as simpler replacements at lower reading levels
SIMPLIFICATIONS: dict[str, dict[ReadingLevel, str]] = {
    "utilize": {ReadingLevel.ELEMENTARY: "use", ReadingLevel.MIDDLE: "use"},
    "facilitate": {ReadingLevel.ELEMENTARY: "help", ReadingLevel.MIDDLE: "help"},
    "implement": {ReadingLevel.ELEMENTARY: "do", ReadingLevel.MIDDLE: "set up"},
    "subsequent": {ReadingLevel.ELEMENTARY: "next", ReadingLevel.MIDDLE: "next"},
    "approximately": {ReadingLevel.ELEMENTARY: "about", ReadingLevel.MIDDLE: "about"},
    "demonstrate": {ReadingLevel.ELEMENTARY: "show", ReadingLevel.MIDDLE: "show"},
    "indicate": {ReadingLevel.ELEMENTARY: "show", ReadingLevel.MIDDLE: "point to"},
    "sufficient": {ReadingLevel.ELEMENTARY: "enough", ReadingLevel.MIDDLE: "enough"},
    "additional": {ReadingLevel.ELEMENTARY: "more", ReadingLevel.MIDDLE: "extra"},
    "commence": {ReadingLevel.ELEMENTARY: "start", ReadingLevel.MIDDLE: "begin"},
    "terminate": {ReadingLevel.ELEMENTARY: "end", ReadingLevel.MIDDLE: "stop"},
    "endeavor": {ReadingLevel.ELEMENTARY: "try", ReadingLevel.MIDDLE: "effort"},
    "necessitate": {ReadingLevel.ELEMENTARY: "need", ReadingLevel.MIDDLE: "require"},
    "previously": {ReadingLevel.ELEMENTARY: "before", ReadingLevel.MIDDLE: "earlier"},
    "regarding": {ReadingLevel.ELEMENTARY: "about", ReadingLevel.MIDDLE: "about"},
    "therefore": {ReadingLevel.ELEMENTARY: "so", ReadingLevel.MIDDLE: "so"},
    "consequently": {ReadingLevel.ELEMENTARY: "so", ReadingLevel.MIDDLE: "as a result"},
    "nevertheless": {ReadingLevel.ELEMENTARY: "still", ReadingLevel.MIDDLE: "even so"},
    "furthermore": {ReadingLevel.ELEMENTARY: "also", ReadingLevel.MIDDLE: "also"},
    "comprehend": {ReadingLevel.ELEMENTARY: "understand", ReadingLevel.MIDDLE: "understand"},
    "anticipate": {ReadingLevel.ELEMENTARY: "expect", ReadingLevel.MIDDLE: "expect"},
    "accommodate": {ReadingLevel.ELEMENTARY: "fit", ReadingLevel.MIDDLE: "make room for"},
    "incorporate": {ReadingLevel.ELEMENTARY: "include", ReadingLevel.MIDDLE: "include"},
    "modification": {ReadingLevel.ELEMENTARY: "change", ReadingLevel.MIDDLE: "change"},
    "acquisition": {ReadingLevel.ELEMENTARY: "getting", ReadingLevel.MIDDLE: "purchase"},
    "predominant": {ReadingLevel.ELEMENTARY: "main", ReadingLevel.MIDDLE: "main"},
    "methodology": {ReadingLevel.ELEMENTARY: "method", ReadingLevel.MIDDLE: "approach"},
    "substantiate": {ReadingLevel.ELEMENTARY: "prove", ReadingLevel.MIDDLE: "back up"},
    "exacerbate": {ReadingLevel.ELEMENTARY: "make worse", ReadingLevel.MIDDLE: "worsen"},
    "ameliorate": {ReadingLevel.ELEMENTARY: "improve", ReadingLevel.MIDDLE: "improve"},
}


class ReadingLevelAdapter:
    """Adjusts text to a target reading grade level."""

    def estimate_level(self, text: str) -> TextStats:
        """Estimate the reading level of text using Flesch-Kincaid."""
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        words = text.split()
        if not words or not sentences:
            return TextStats()

        num_words = len(words)
        num_sentences = len(sentences)
        num_syllables = sum(self._count_syllables(w) for w in words)

        avg_word_len = sum(len(w) for w in words) / num_words
        avg_sent_len = num_words / num_sentences

        # Flesch-Kincaid Grade Level
        grade = 0.39 * avg_sent_len + 11.8 * (num_syllables / num_words) - 15.59
        grade = max(1.0, min(grade, 20.0))

        return TextStats(
            word_count=num_words,
            avg_word_length=round(avg_word_len, 2),
            avg_sentence_length=round(avg_sent_len, 2),
            estimated_grade_level=round(grade, 1),
        )

    def adapt(self, text: str, target: ReadingLevel) -> str:
        """Adapt text to the target reading level."""
        result = text
        if target in (ReadingLevel.COLLEGE, ReadingLevel.EXPERT):
            return result

        for word, replacements in SIMPLIFICATIONS.items():
            if target in replacements:
                pattern = r"\b" + re.escape(word) + r"\b"
                result = re.sub(pattern, replacements[target], result, flags=re.IGNORECASE)

        # For elementary level, also try to break long sentences
        if target == ReadingLevel.ELEMENTARY:
            result = self._shorten_sentences(result)

        return result

    def _shorten_sentences(self, text: str) -> str:
        """Break very long sentences into shorter ones."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        result_parts: list[str] = []
        for sent in sentences:
            words = sent.split()
            if len(words) > 20:
                # Try splitting at conjunctions
                for conj in [", and ", ", but ", ", however ", "; "]:
                    if conj in sent:
                        parts = sent.split(conj, 1)
                        sent = parts[0] + ". " + parts[1].capitalize()
                        break
            result_parts.append(sent)
        return " ".join(result_parts)

    @staticmethod
    def _count_syllables(word: str) -> int:
        """Approximate syllable count for a word."""
        word = word.lower().strip(".,!?;:'\"")
        if len(word) <= 2:
            return 1
        vowels = "aeiouy"
        count = 0
        prev_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith("e") and count > 1:
            count -= 1
        return max(1, count)
