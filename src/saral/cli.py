"""CLI interface for Saral."""

from __future__ import annotations

import sys

import click
from rich.console import Console

from saral.models import Domain, ReadingLevel
from saral.simplifier.detector import JargonDetector
from saral.simplifier.translator import JargonTranslator
from saral.simplifier.leveler import ReadingLevelAdapter
from saral.report import print_report


@click.group()
def main() -> None:
    """Saral - AI Jargon Simplifier."""


@main.command()
@click.option("--text", "-t", default=None, help="Text to simplify. Reads from stdin if not provided.")
@click.option("--domain", "-d", multiple=True, type=click.Choice([d.value for d in Domain]),
              help="Limit to specific domains.")
@click.option("--level", "-l", type=click.Choice([r.value for r in ReadingLevel]),
              default="middle", help="Target reading level.")
def simplify(text: str | None, domain: tuple[str, ...], level: str) -> None:
    """Simplify jargon in text."""
    if text is None:
        if sys.stdin.isatty():
            click.echo("Enter text (Ctrl+D to finish):")
        text = sys.stdin.read()

    domains = [Domain(d) for d in domain] if domain else None
    target_level = ReadingLevel(level)

    translator = JargonTranslator(domains)
    leveler = ReadingLevelAdapter()

    stats_before = leveler.estimate_level(text)
    result = translator.translate(text)
    result.simplified_text = leveler.adapt(result.simplified_text, target_level)
    stats_after = leveler.estimate_level(result.simplified_text)

    result.original_reading_level = f"Grade {stats_before.estimated_grade_level}"
    result.target_reading_level = target_level.value

    print_report(result, stats_before, stats_after)


@main.command()
@click.option("--text", "-t", required=True, help="Text to scan for jargon.")
@click.option("--domain", "-d", multiple=True, type=click.Choice([d.value for d in Domain]))
def detect(text: str, domain: tuple[str, ...]) -> None:
    """Detect jargon terms without replacing them."""
    domains = [Domain(d) for d in domain] if domain else None
    detector = JargonDetector(domains)
    matches = detector.detect(text)

    console = Console()
    if matches:
        for m in matches:
            console.print(f"  [{m.domain.value}] [red]{m.term}[/red] -> {m.definition}")
    else:
        console.print("[green]No jargon found.[/green]")


if __name__ == "__main__":
    main()
