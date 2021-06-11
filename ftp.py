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

    for sub_path in path.iterdir():
        if sub_path.is_file():
            transfer_file(ftp_conn, sub_path)
        else:
            make_dir(ftp_conn, sub_path)
            transfer_dir(ftp_conn, sub_path)


def transfer_file(ftp_conn:ftplib.FTP, path:Path):
    web_path = windows_to_web_path(path)
    with path.open('rb') as fp:
        ftp_conn.storbinary('STOR {}'.format(web_path), fp)


def make_dir(ftp_conn:ftplib.FTP, path:Path):
    try:
        web_path = windows_to_web_path(path)
        ftp_conn.mkd(web_path)
    except ftplib.error_perm:
        pass


def windows_to_web_path(path:Path):
    return '/'.join(str(path).split('\\'))


def is_file(ftp_conn:ftplib.FTP, path:Path):
    try:
        ftp_conn.size(path)
        return True
    except ftplib.error_perm:
        return False


def clean():
    local_path = Path('www', 'static')
    with conn() as ftp:
        clean_dir(ftp, 'static', local_path)


def clean_dir(ftp:ftplib.FTP, dirname:str, local_path:Path):
    
    ftp.cwd(dirname)
    local_names = [p.name for p in local_path.iterdir()]

    for name in ftp.nlst():
        if name in local_names:
            if is_file(ftp, name):
                continue
            else:
                clean_dir(ftp, name, local_path / name)
        elif is_file(ftp, name):
            ftp.delete(name)
        else:
            ftp.rmd(name)

    ftp.cwd('..')


@contextmanager
def conn():
    ftp = ftplib.FTP(secrets.site)
    ftp.login(secrets.username, secrets.password)
    try:
        yield ftp
    finally:
        ftp.close()
    

if __name__ == '__main__':
    print('Transferring files to {}'.format(secrets.site))
    transfer()
    print('Success')

    print('Removing excess files and directories from server')
    clean()
    print('Success')