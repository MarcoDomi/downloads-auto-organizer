#! /usr/bin/python3

import shutil
import sys
from pathlib import Path

DOWNLOAD_DIR = Path.home() / "downloads"

 # values as sets allow for efficient membership testing
valid_extensions = {
    'documents': {'.txt', '.pdf', '.docx'},
    'archives': {'.zip', '.tar.gz'},
    'videos': {'.mp4', '.mkv', '.mov'},
    'images': {'.jpg', '.jpeg', '.png', '.gif'},
    'audio' : {'.mp3'}
}

'''def get_init_dir(): #NOTE i forgot why i added this :(
    if len(sys.argv) > 1 and sys.argv[1] == 'cwd': #set INIT_DIR to the current working directory
        INIT_DIR = Path.cwd()
    else:
        INIT_DIR = HOME_DIR #path where the download files will be moved to.

    return INIT_DIR'''


def create_dir(dir_path):
    '''creates a directory'''
    try:
        dir_path.mkdir()
    except FileExistsError:
        print(f"Directory {dir_path} already exists")


def get_file_suffix(file_path):
    '''return extension of a file'''
    #some files will have 2 dots(.) so using .suffix will not work in those cases
    file_name = file_path.name
    index =  file_name.find('.')

    return file_name[index:]


def move_file(file): 
    '''move file from parent dir to new dir based on file type'''
    for file_type, f_extension in valid_extensions.items():
        file_suffix = get_file_suffix(file)

        if file_suffix in f_extension:
            type_path = DOWNLOAD_DIR.joinpath(file_type) #create path for new file type directory
            create_dir(type_path) #create new file type directory
            shutil.move(file, type_path) 


def main():
    for f in DOWNLOAD_DIR.iterdir():
        move_file(f)


main()