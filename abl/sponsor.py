"""Raffle sponsor schema and loading logic."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Sponsor:
    """An Ames Brewers League annual raffle sponsor."""

    name: str
    url: str
    logo_url: str


def load(file_path: Path) -> list[Sponsor]:
    """Load sponsor data from a JSON file."""
    data = json.loads(file_path.read_text())
    return [Sponsor(**s) for s in data]


def batch(sponsors: list[Sponsor], size: int) -> list[list[Sponsor]]:
    """Create a 2-dimensional list of sponsors to organize them for display."""
    out = []
    num_sponsors = len(sponsors)
    for n in range(0, num_sponsors, size):
        out.append(sponsors[n : min(n + size, num_sponsors)])
    return out
