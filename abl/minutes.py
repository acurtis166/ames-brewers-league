from dataclasses import dataclass
import datetime as dt
from pathlib import Path


@dataclass
class Minutes:
    file_path: Path

    @property
    def date(self) -> dt.date:
        file_name_no_ext = self.file_path.name.split(".")[0]
        year, _, month = file_name_no_ext.partition("-")
        return dt.date(int(year), int(month), 1)


def load(minutes_dir: Path, extension: str = "pdf"):
    return [Minutes(p) for p in minutes_dir.glob(f"*/*.{extension}")]
