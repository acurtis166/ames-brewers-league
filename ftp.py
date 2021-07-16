"""Transfers files from the "www" directory to the web server."""

import ftplib
from pathlib import Path
import os
from contextlib import contextmanager

import secrets


def transfer():
    """Transfer all files in "www" directory to site via FTP.
    """

    # change directory to web root
    os.chdir('www')

    with conn() as ftp:
        transfer_dir(ftp, Path())

    # revert active directory to original state
    os.chdir('..')


def transfer_dir(ftp_conn:ftplib.FTP, path:Path):
    """Transfer files from a specific directory via FTP. Recursively call the function for subdirectories.

    Args:
        ftp_conn (ftplib.FTP): The FTP connection to use for the transfer.
        path (Path): Path to the directory in the local filesystem.
    """

    # loop through all the items in the directory as "Path" instances
    for sub_path in path.iterdir():
        if sub_path.is_file():
            # if the item is a file, transfer it
            transfer_file(ftp_conn, sub_path)
        else:
            # otherwise, make sure the subdirectory exists
            make_dir(ftp_conn, sub_path)
            # and recursively call this function on the subdirectory
            transfer_dir(ftp_conn, sub_path)


def transfer_file(ftp_conn:ftplib.FTP, path:Path):
    """Transfer the file at the given path via FTP.

    Args:
        ftp_conn (ftplib.FTP): The FTP connection to use for the transfer.
        path (Path): Path to the file in the local filesystem.
    """

    # get the web equivalent filepath
    web_path = windows_to_web_path(path)
    # open the file and transfer it
    with path.open('rb') as fp:
        ftp_conn.storbinary('STOR {}'.format(web_path), fp)


def make_dir(ftp_conn:ftplib.FTP, path:Path):
    """Create or ignore a directory on the web server.

    Args:
        ftp_conn (ftplib.FTP): The FTP connection to use to create the directory.
        path (Path): Path to the directory in the local filesystem.
    """

    # get the web equivalent filepath
    web_path = windows_to_web_path(path)

    try:
        # make the directory
        ftp_conn.mkd(web_path)
    except ftplib.error_perm as ex:
        e_str = str(ex)
        if '550 Cannot create a file when that file already exists' not in e_str:
            # only raise the exception if the error isn't that the directory exists
            raise ex


def windows_to_web_path(path:Path):
    """Convert a Path to a string with forward slashes replaced with back slashes.

    Args:
        path (Path): Path to the file or directory.

    Returns:
        str: File path to use for the web server.
    """

    return str(path).replace('\\', '/')


def is_file(ftp_conn:ftplib.FTP, filename:str):
    """Determine whether the item designated by the given path is a file or not. 
    
    Requires that the current directory has been changed to reference the filename directly.

    Args:
        ftp_conn (ftplib.FTP): The FTP connection to use.
        path (str): Path to the item.

    Returns:
        bool: Whether the item is a file or not
    """

    try:
        ftp_conn.size(filename)
        return True
    except ftplib.error_perm:
        # the file doesn't exist because it couldn't be found in the size method
        return False


def clean():
    """Remove files from the web server that do not exist in the local filesystem.

    Ignores the root directory, as some files are autogenerated (?).
    """

    local_path = Path('www', 'static')
    with conn() as ftp:
        clean_dir(ftp, 'static', local_path)


def clean_dir(ftp:ftplib.FTP, dirname:str, local_path:Path):
    """Remove files from a directory on the web server that do not exist in the local filesystem.

    Recursively calls itself when subdirectories are found.

    Args:
        ftp (ftplib.FTP): The FTP connection to use.
        dirname (str): The directory to clean.
        local_path (Path): Local-equivalent Path to the `dirname` directory.
    """
    
    # change the current directory to the dirname
    ftp.cwd(dirname)
    # get all valid filenames that should be in the directory (as well as a file marker)
    local_names = [(p.name, p.is_file()) for p in local_path.iterdir()]

    # loop through the items in the directory
    for name in ftp.nlst():
        isfl = is_file(ftp, name)

        # check server file name and isfile marker existence in the local path
        if (name, isfl) in local_names:
            # valid. move on if file, go next level deeper if directory
            if is_file(ftp, name):
                continue
            else:
                clean_dir(ftp, name, local_path / name)
        elif isfl:
            # invalid. remove file
            ftp.delete(name)
        else:
            # invalid. remove subdirectory
            ftp.rmd(name)

    # revert the current directory back to the starting point
    ftp.cwd('..')


@contextmanager
def conn():
    """Create an FTP connection.

    Yields:
        ftplib.FTP: The FTP connection to use for server management.
    """

    # create and provide credentials for the connection
    ftp = ftplib.FTP(secrets.site)
    ftp.login(secrets.username, secrets.password)
    try:
        yield ftp
    finally:
        # close the connection when the context is complete
        ftp.close()
    

def main():
    """Run the program:

    1. Transfer new and updated files from the "www" local directory to the web server.\n
    2. Remove files and directories that do not exist in the local "www" directory.
    """
    
    # transfer files from the local filesystem to the web server
    print('Transferring files to {}'.format(secrets.site))
    transfer()
    print('Success')

    # remove unnecessary items from the web server (ignoring the root directory)
    print('Removing excess files and directories from server')
    clean()
    print('Success')


if __name__ == '__main__':
    main()