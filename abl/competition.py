"""Define schema for competition data. Load competitions from file."""

import collections
import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Entry:
    """A single brewer's beer submission to a competition."""

    brewer: str
    beer: str | None
    points: float


@dataclass(frozen=True)
class Competition:
    """A monthly brewing competition."""

    date: dt.date
    style: str
    category: str
    bjcp_year: int
    entries: list[Entry]


def _read_csv(path: Path) -> list[dict]:
    """Parse a CSV file and return a list of dictionary records."""
    with path.open() as fp:
        return [l for l in csv.DictReader(fp)]


def _groupby(data: list[dict], key: str) -> dict:
    """Group a list of dictionaries by the specified key."""
    out = collections.defaultdict(list)
    for item in data:
        out[item[key]].append(item)
    return out


def load(competitions_path: Path, entries_path: Path) -> list[Competition]:
    """Load and compile competition data to create Competition objects"""
    all_competitions = _read_csv(competitions_path)
    all_entries = _groupby(_read_csv(entries_path), "date")

    out = []
    for competition in all_competitions:
        entries = all_entries.get(competition["date"], [])
        # Sort entries from most points to least points
        entries = list(sorted(entries, key=lambda e: e["points"], reverse=True))
        comp = Competition(
            dt.date.fromisoformat(competition["date"]),
            competition["style"],
            competition["category"],
            int(competition["bjcp_year"]),
            [
                Entry(e["brewer"], e["beer"], float(e["points"]))
                for e in entries
            ],
        )
        out.append(comp)
    return out


def split_competition_list(
    competitions: list[Competition], date: dt.date
) -> tuple[list[Competition], list[Competition]]:
    """Split a list of competitions on a given date.

    Returns:
        tuple[list[Competition], list[Competition]]: Competitions before the
            date (sorted descending) and competitions on or after the date
            (sorted ascending).
    """
    before = []
    after = []
    for comp in competitions:
        if comp.date >= date:
            after.append(comp)
        else:
            before.append(comp)

    before = list(sorted(before, key=lambda c: c.date, reverse=True))
    after = list(sorted(after, key=lambda c: c.date))
    return before, after
