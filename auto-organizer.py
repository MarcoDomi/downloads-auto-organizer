#! /usr/bin/python3

import shutil
import sys
from pathlib import Path

DOWNLOAD_DIR = Path.home() / "downloads"

'''def get_init_dir(): #NOTE i forgot why i added this :(
    if len(sys.argv) > 1 and sys.argv[1] == 'cwd': #set INIT_DIR to the current working directory
        INIT_DIR = Path.cwd()
    else:
        INIT_DIR = HOME_DIR #path where the download files will be moved to.

    return INIT_DIR'''

def create_path(path):
    try:
        path.mkdir()
    except FileExistsError:
        print(f"Directory {path} already exists")


def move_file(file): 
    # values as sets allow for efficient membership testing
    valid_extensions = {
        'documents': {'.txt', '.pdf', '.docx'},
        'archives': {'.zip', '.tar.gz'},
        'videos': {'.mp4', '.mkv', '.mov'},
        'images': {'.jpg', '.jpeg', '.png', '.gif'}
    }

    for file_type, f_extension in valid_extensions.items():
        type_path = DOWNLOAD_DIR.joinpath(file_type)
        if file.suffix in f_extension:
            create_path(type_path)
            


def scan_downloads():
    '''scan download directory for files'''

    for f in DOWNLOAD_DIR.iterdir():
        move_file(f)


def main():
    #INIT_DIR = get_init_dir()
    scan_downloads()


main()
