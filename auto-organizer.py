#! /usr/bin/python3

import shutil
import datetime
import os
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

class log_manager:
    def __init__(self):
        self.log_file = 'file_move_log.txt'
        self.curr_date = datetime.date.today()

    def write(self,file_path:Path):
        print(file_path)

        file_name = file_path.name
        with open(self.log_file, 'a') as f:
            move_time = os.stat(file_path).st_ctime #time file was moved
            f.write(f"{file_name} moved to {DOWNLOAD_DIR} at {self.curr_date}-{move_time}\n")
        #NOTE i may need to pass the entire path of the file to write method so i can use os.stat and get metadata timestampe

    def print_log(self):
        log_list = []
        with open(self.log_file) as f:
            for line in f:
                log_list.append(line)
        
        print("".join(log_list))

    def _convert_timestamp(self, f_ctime):
        '''convert 24 hour datetime obj to a 12 hour datetime obj'''
        pass


logger = log_manager()


def create_dir(dir_path):
    '''creates a directory'''
    try:
        dir_path.mkdir()
    except FileExistsError:
        print(f"Directory {dir_path} already exists")


def get_file_suffix(file_path):
    '''return extension of a file'''
    #some file extensions will have 2 dots(.) so using .suffix attribute will not work in those cases
    file_name = file_path.name
    index =  file_name.find('.')

    return file_name[index:]


def move_file(file): 
    '''move file from parent dir to new dir based on file type'''
    for file_type, f_extension in valid_extensions.items():
        file_suffix = get_file_suffix(file)

        if file_suffix in f_extension:
            type_path = DOWNLOAD_DIR.joinpath(file_type) #create path object for new file type directory
            create_dir(type_path) #create new file type directory
            shutil.move(file, type_path) 
            logger.write(file)


def main():
    for f in DOWNLOAD_DIR.iterdir():
        move_file(f)


main()
