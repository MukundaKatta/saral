"""Data models for Saral."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Domain(str, Enum):
    MEDICAL = "medical"
    LEGAL = "legal"
    TECH = "tech"
    FINANCE = "finance"


class ReadingLevel(str, Enum):
    ELEMENTARY = "elementary"   # Grade 3-5
    MIDDLE = "middle"           # Grade 6-8
    HIGH_SCHOOL = "high_school" # Grade 9-12
    COLLEGE = "college"         # College level
    EXPERT = "expert"           # Graduate/professional


class JargonMatch(BaseModel):
    """A detected jargon term and its plain-language equivalent."""

    term: str
    definition: str
    domain: Domain
    start: int = 0
    end: int = 0


class SimplificationResult(BaseModel):
    """Result of simplifying a text."""

    original_text: str
    simplified_text: str
    jargon_found: list[JargonMatch] = Field(default_factory=list)
    original_reading_level: Optional[str] = None
    target_reading_level: Optional[str] = None
    domains_detected: list[Domain] = Field(default_factory=list)


class TextStats(BaseModel):
    """Statistics about a piece of text."""

    word_count: int = 0
    avg_word_length: float = 0.0
    avg_sentence_length: float = 0.0
    jargon_density: float = 0.0
    estimated_grade_level: float = 0.0
