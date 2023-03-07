"""Schema and loading logic for meeting minutes."""

import datetime as dt
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Minutes:
    """File reference for Ames Brewers League meeting minutes."""

    file_path: Path

    @property
    def date(self) -> dt.date:
        """The year/month that the minutes were recorded."""
        file_name_no_ext = self.file_path.name.split(".")[0]
        year, _, month = file_name_no_ext.partition("-")
        return dt.date(int(year), int(month), 1)


def load(minutes_dir: Path, extension: str = "pdf"):
    """Load PDF file references from the provided directory."""
    return [Minutes(p) for p in minutes_dir.glob(f"*/*.{extension}")]
