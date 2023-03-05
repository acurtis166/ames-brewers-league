import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FTPConfig:
    """Login information for FTP connections."""

    site: str
    username: str
    password: str


@dataclass(frozen=True)
class PathConfig:
    """File-system locations of data sources."""

    competitions: Path
    entries: Path
    minutes: Path
    sponsors: Path


@dataclass(frozen=True)
class Config:
    """Configuration information related to ABL maintenance."""

    ftp: FTPConfig
    paths: PathConfig


def load(file_path: Path) -> Config:
    data = json.loads(file_path.read_text())
    ftp_config = FTPConfig(**data["ftp"])
    paths = {k: Path(v) for k, v in data["paths"].items()}
    path_config = PathConfig(**paths)
    return Config(ftp_config, path_config)
