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
    '''manages a log file to track the date-time files were moved'''
    def __init__(self):
        self.log_file = 'file_move_log.txt'
        self.curr_date = datetime.date.today()

    def write(self,file_path:Path):
        '''write to file_move_log.txt when a file was moved to a different directory'''

        with open(self.log_file, 'a') as f:

            move_date, move_time = self._get_file_datetime(file_path)

            file_name = file_path.name
            file_parent = file_path.parent.name

            f.write(f"{file_name} moved to {file_parent} at {move_date} -- {move_time}\n") #convert timestamp time to 12-hour format

    def print_log(self):
        '''print log file to console'''
        log_list = []
        with open(self.log_file) as f:
            for line in f:
                log_list.append(line)

        print("".join(log_list))

    def _get_file_datetime(self, file_path):
        '''get a human readable date and time of the last metadata change for a file in a 12-hour format'''
        metadata_timeStamp = os.stat(file_path).st_ctime #timestamp of when the file was moved to different directory
        move_datetime = datetime.datetime.fromtimestamp(metadata_timeStamp) #convert timestamp to human readable format

        move_date = move_datetime.date() 
        move_time12hr = move_datetime.time().strftime("%I:%M %p") #12 hour format time

        return move_date, move_time12hr


logger = log_manager()


def create_dir(dir_path):
    '''creates a directory'''
    try:
        dir_path.mkdir()
    except FileExistsError:
        print(f"Directory {dir_path} already exists")


def get_file_suffix(file_path):
    '''return extension of a file'''
    #some file extensions will have 2 dots(example.tar.gz) so using .suffix attribute will not work in those cases
    file_name = file_path.name
    index =  file_name.find('.')

    return file_name[index:]


def move_file(file): 
    '''move file from parent dir to new dir based on file type'''
    for file_type, f_extension in valid_extensions.items():
        file_suffix = get_file_suffix(file)

        if file_suffix in f_extension:
            type_path = DOWNLOAD_DIR.joinpath(file_type) #create path object for new file type directory
            create_dir(type_path) #create new directory using the file type
            shutil.move(file, type_path) 
            logger.write(type_path / file.name) #send updated file path to log_manager write method


def main():
    for f in DOWNLOAD_DIR.iterdir():
        move_file(f)


if __name__ == "__main__":
    main()
    logger.print_log()
