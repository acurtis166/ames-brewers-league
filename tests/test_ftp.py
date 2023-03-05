import ftplib
from pathlib import Path

import pytest

from abl import config, ftp

ROOT_DIR = Path(__file__).parents[1]
CONFIG = config.load(ROOT_DIR / "config.json")


@pytest.fixture
def conn():
    with ftp.connect(CONFIG.site, CONFIG.username, CONFIG.password) as conn:
        yield conn


@pytest.fixture
def session(conn: ftplib.FTP):
    return ftp.FTPSession(conn)


def test_connect(conn: ftplib.FTP):
    assert isinstance(conn, ftplib.FTP)


def test_is_file_on_file(session: ftp.FTPSession):
    assert session.is_file("index.html")


def test_is_file_on_dir(session: ftp.FTPSession):
    assert not session.is_file("static")
