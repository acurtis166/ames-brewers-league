from pathlib import Path

from abl import config, ftp

ROOT_DIR = Path(__file__).parents[1]
CONFIG = config.load(ROOT_DIR / "config.json").ftp


def main():
    with ftp.connect(CONFIG.site, CONFIG.username, CONFIG.password) as conn:
        sess = ftp.FTPSession(conn, ROOT_DIR / "public")
        print("Transferring files to web server")
        sess.transfer_dir(ROOT_DIR / "public")
        print("Removing unnecessary files from web server")
        sess.clean_dir("static", ROOT_DIR / "public/static")


if __name__ == "__main__":
    main()
