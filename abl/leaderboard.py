"""Logic for creating brewing competition leaderboards."""

import collections
from dataclasses import dataclass

from abl.competition import Competition


@dataclass(frozen=True)
class LeaderboardEntry:
    """A brewer's point total and standing for a given competition year."""

    brewer: str
    points: float
    place: int


def create_leaderboards(
    competitions: list[Competition],
) -> dict[int, list[LeaderboardEntry]]:
    """Create annual leaderboards from a list of competitions."""
    comps_by_year = collections.defaultdict(list)
    for comp in competitions:
        comps_by_year[comp.date.year].append(comp)

    out = {}
    for year, comps in sorted(comps_by_year.items(), reverse=True):
        out[year] = _create_leaderboard(comps)
    return out


def _create_leaderboard(
    competitions: list[Competition],
) -> list[LeaderboardEntry]:
    """Create an annual leaderboard from a list of competitions."""
    totals = collections.defaultdict(float)
    for comp in competitions:
        for entry in comp.entries:
            totals[entry.brewer] += entry.points
    total_items = list(sorted(totals.items(), key=lambda t: t[1], reverse=True))

    out = []
    previous_points = None
    place = 0
    for i, (brewer, points) in enumerate(total_items):
        if previous_points is None or points < previous_points:
            # Only increment the place when points decreased
            place = i + 1
            previous_points = points
        lb_entry = LeaderboardEntry(brewer, points, place)
        out.append(lb_entry)
    return out
