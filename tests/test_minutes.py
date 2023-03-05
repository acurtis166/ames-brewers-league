import tempfile
from pathlib import Path

from abl import minutes


def test_load():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        (temp_path / "2020").mkdir()
        (temp_path / "2020/2020-01.txt").write_text("test")
        mins = minutes.load(temp_path, "txt")
    assert len(mins) == 1
    assert mins[0].date.year == 2020
