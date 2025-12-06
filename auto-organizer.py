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

def create_path(dir_path):
    try:
        dir_path.mkdir()
    except FileExistsError:
        print(f"Directory {dir_path} already exists")


def move_file(file): 
    # values as sets allow for efficient membership testing
    valid_extensions = {
        'documents': {'.txt', '.pdf', '.docx'},
        'archives': {'.zip', '.tar.gz'},
        'videos': {'.mp4', '.mkv', '.mov'},
        'images': {'.jpg', '.jpeg', '.png', '.gif'},
        'audio' : {'.mp3'}
    }

    for file_type, f_extension in valid_extensions.items():
        type_path = DOWNLOAD_DIR.joinpath(file_type)
        if file.suffix in f_extension:
            create_path(type_path)
            shutil.move(file, type_path)


def main():
    for f in DOWNLOAD_DIR.iterdir():
        move_file(f)


main()
