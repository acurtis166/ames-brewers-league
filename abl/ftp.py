"""FTP file handling."""

import ftplib
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def connect(site_name: str, username: str, password: str):
    """Create an FTP connection.

    Yields:
        ftplib.FTP: The FTP connection to use for server management.
    """
    with ftplib.FTP(site_name) as ftp:
        try:
            ftp.login(username, password)
            yield ftp
        except ftplib.error_perm as ex:
            msg = f"""
                Error occurred when trying to log in to the FTP server.
                Error message: {ex}
            """
            raise ftplib.error_perm(msg)


class FTPSession:
    def __init__(self, ftp: ftplib.FTP, root_dir: Path):
        self._ftp = ftp
        self._root_dir = root_dir

    def transfer_dir(self, path: Path):
        """Transfer files from a specific directory via FTP.

        Recursively call the function for subdirectories.

        Args:
            path (Path): Path to the directory in the local filesystem.
        """
        print(f"Transferring directory {path}")
        for sub_path in path.iterdir():
            if sub_path.is_file():
                # if the item is a file, transfer it
                self.transfer_file(sub_path)
            else:
                # otherwise, make sure the subdirectory exists
                self.make_dir(sub_path)
                # and recursively call this function on the subdirectory
                self.transfer_dir(sub_path)

    def transfer_file(self, path: Path):
        """Transfer the file at the given path via FTP.

        Args:
            path (Path): Path to the file in the local filesystem.
        """
        print(f"Transferring file {path}")
        with path.open("rb") as fp:
            posix = path.relative_to(self._root_dir).as_posix()
            self._ftp.storbinary(f"STOR {posix}", fp)

    def make_dir(self, path: Path):
        """Create or ignore a directory on the web server.

        Args:
            path (Path): Path to the directory in the local filesystem.
        """
        print(f"Creating directory {path}")
        try:
            posix = path.relative_to(self._root_dir).as_posix()
            self._ftp.mkd(posix)
        except ftplib.error_perm as ex:
            if "550 Cannot create a file" not in str(ex):
                # Only raise exception if the error isn't that the directory exists
                raise ex

    def is_file(self, filename: str) -> bool:
        """Determine the type of object at the given `filename` argument.

        Requires that the current directory has been changed to reference the
        filename directly.

        Args:
            filename (str): Path to the item.

        Returns:
            bool: Whether the entity at the provided filename is a file or not.
        """
        try:
            self._ftp.size(filename)
            return True
        except ftplib.error_perm:
            # Must be a directory
            return False

    def clean_dir(self, dirname: str, local_path: Path):
        """Remove files from web server that do not exist locally.

        Recursively calls itself when subdirectories are found.

        Args:
            dirname (str): The web server directory name to clean.
            local_path (Path): Local-equivalent Path to the `dirname` directory.
        """
        print(f"Cleaning directory {local_path}")
        local_files = [(p.name, p.is_file()) for p in local_path.iterdir()]

        self._ftp.cwd(dirname)
        for name in self._ftp.nlst():
            is_file = self.is_file(name)

            if (name, is_file) in local_files:
                # Web server match local file system.
                if is_file:
                    continue
                self.clean_dir(name, local_path / name)
            elif is_file:
                # File exists on web server but not in local file system.
                print(f"Deleting file {name}")
                self._ftp.delete(name)
            else:
                # Directory exists on web server but not in local file system.
                print(f"Deleting directory {name}")
                # TODO Error message: 550 The directory is not empty.
                self._ftp.rmd(name)

        self._ftp.cwd("..")
