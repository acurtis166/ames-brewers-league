import datetime as dt
import tempfile
from pathlib import Path

from abl.competition import load

COMPETITION_CSV = [
    "date,style,category,bjcp_year",
    "2018-01-09,Open to All Styles,All,2015",
]
ENTRY_CSV = [
    "date,brewer,beer,points",
    '2018-01-09,Ron Nelson,"English Porter, 13C",3.0',
]


def test_load():
    with tempfile.TemporaryDirectory() as temp_dir:
        comp_path = Path(temp_dir) / "comp.csv"
        comp_path.write_text("\n".join(COMPETITION_CSV))
        entry_path = Path(temp_dir) / "entry.csv"
        entry_path.write_text("\n".join(ENTRY_CSV))

        competitions = load(comp_path, entry_path)
    assert competitions[0].date == dt.date(2018, 1, 9)
    assert len(competitions[0].entries) == 1
