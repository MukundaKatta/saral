"""Rich console report for Saral."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from saral.models import SimplificationResult, TextStats


def print_report(
    result: SimplificationResult,
    stats_before: TextStats | None = None,
    stats_after: TextStats | None = None,
    console: Console | None = None,
) -> None:
    """Print a formatted simplification report."""
    console = console or Console()

    console.print(Panel("[bold]Saral - Jargon Simplification Report[/bold]", style="blue"))

    # Jargon found
    if result.jargon_found:
        table = Table(title=f"Jargon Detected ({len(result.jargon_found)} terms)", show_lines=True)
        table.add_column("Term", style="red")
        table.add_column("Plain Meaning", style="green")
        table.add_column("Domain", style="cyan")
        for m in result.jargon_found:
            table.add_row(m.term, m.definition, m.domain.value)
        console.print(table)
    else:
        console.print("[green]No jargon detected![/green]")

    # Domains
    if result.domains_detected:
        domains = ", ".join(d.value for d in result.domains_detected)
        console.print(f"\n[bold]Domains detected:[/bold] {domains}")

    # Reading level stats
    if stats_before:
        console.print(f"\n[bold]Original reading level:[/bold] Grade {stats_before.estimated_grade_level}")
        console.print(f"  Words: {stats_before.word_count}, Avg sentence length: {stats_before.avg_sentence_length}")
    if stats_after:
        console.print(f"[bold]Simplified reading level:[/bold] Grade {stats_after.estimated_grade_level}")
        console.print(f"  Words: {stats_after.word_count}, Avg sentence length: {stats_after.avg_sentence_length}")

    # Simplified text
    console.print(Panel(result.simplified_text, title="Simplified Text", style="green"))
