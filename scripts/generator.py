import datetime as dt
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from abl import competition, config, leaderboard, minutes, sponsor

ROOT_DIR = Path(__file__).parents[1]
PUBLIC_DIR = ROOT_DIR / "public"
TEMPLATE_DIR = ROOT_DIR / "templates"

CONFIG = config.load(ROOT_DIR / "config.json")


def empty_public_dir():
    """Clear out existing content from the publish directory."""
    shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir()


def copy_static_files():
    shutil.copytree(TEMPLATE_DIR / "static", PUBLIC_DIR / "static")


def copy_minutes(minutes_dir: Path):
    shutil.copytree(minutes_dir, PUBLIC_DIR / "minutes")


def render(env: Environment, filename: str, **kwargs):
    template = env.get_template(filename)
    html = template.render(**kwargs)
    (PUBLIC_DIR / filename).write_text(html)


def main():
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    comps = competition.load(CONFIG.paths.competitions, CONFIG.paths.entries)
    history, upcoming = competition.split_competition_list(
        comps, dt.date.today()
    )

    lboards = leaderboard.create_leaderboards(comps)

    mins = minutes.load(CONFIG.paths.minutes)
    mins = list(sorted(mins, key=lambda m: m.date, reverse=True))

    sponsors = sponsor.load(CONFIG.paths.sponsors)
    sponsor_rows = sponsor.batch(sponsors, 3)

    empty_public_dir()
    copy_static_files()
    copy_minutes(CONFIG.paths.minutes)
    render(env, "index.html")
    render(env, "minutes.html", minutes=mins)
    render(env, "leaderboard.html", leaderboards=lboards)
    render(env, "results.html", competitions=history)
    render(env, "upcoming.html", competitions=upcoming)
    render(env, "raffle.html", sponsor_rows=sponsor_rows)


if __name__ == "__main__":
    main()
