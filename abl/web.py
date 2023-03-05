import collections
import datetime as dt
from pathlib import Path

from abl.competition import Competition


def create_competition_dicts(competitions: list[Competition]) -> list[dict]:
    out = []
    for comp in competitions:
        entries = []
        for e in sorted(comp.entries, key=lambda e: e.points, reverse=True):
            new_entry = {"Name": e.brewer, "Beer": e.beer, "Points": e.points}
            entries.append(new_entry)
        new_comp = {
            "Style": comp.style,
            "Category": comp.category,
            "Year": comp.date.year,
            "Month": comp.date.strftime("%B"),
            "Entries": entries,
            "Winner": entries[0] if entries else {},
        }
        out.append(new_comp)
    return out


def create_minutes_dicts(minutes_dir: Path) -> list[dict]:
    """Create dictionaries for each meeting minutes file.

    Args:
        minutes_dir (Path): The directory where the minutes files are stored.

    Returns:
        list[dict]: Dictionaries for each minutes file.
    """
    minutes = []
    for minutes_path in minutes_dir.glob("*.pdf"):
        date = dt.datetime.strptime(minutes_path.name[:-4], r"%Y-%m")
        record = {
            "FileName": minutes_path.name,
            "FormattedDate": date.strftime(r"%B %Y"),
        }
        minutes.append(record)
    return minutes


def create_leaderboard_dicts(competitions: list[Competition]) -> list[dict]:
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
        record = {
            "Name": brewer,
            "Points": points,
            "Place": place,
        }
        out.append(record)
    return out


def create_years_list(directory: Path) -> list[int]:
    return [int(p.name) for p in directory.glob("[0-9][0-9][0-9][0-9]")]
