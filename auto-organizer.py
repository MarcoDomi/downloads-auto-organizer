#! /usr/bin/python3

import shutil
import sys
from pathlib import Path

HOME_DIR = Path.home()

'''def get_init_dir(): #NOTE i forgot why i added this :(
    if len(sys.argv) > 1 and sys.argv[1] == 'cwd': #set INIT_DIR to the current working directory
        INIT_DIR = Path.cwd()
    else:
        INIT_DIR = HOME_DIR #path where the download files will be moved to.

    return INIT_DIR'''


def move_file(file): 
    #values as sets allow for efficient membership testing
    valid_extensions = {
        'documents': set('.txt', '.pdf', '.docx'),
        'archives': set('.zip', '.tar.gz'),
        'videos': set('.mp4', '.mkv', '.mov'),
        'images': set('.jpg', '.jpeg', '.png', '.gif')
    }


def scan_downloads():
    '''scan download directory for files'''

    download_dir = HOME_DIR.joinpath('downloads')
    for f in download_dir.iterdir():
        move_file(f)


def main():
    #INIT_DIR = get_init_dir()
    scan_downloads()

main()