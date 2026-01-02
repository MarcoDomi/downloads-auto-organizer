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
        new_log = self._create_log(file_path)
        new_log_list = self._prepend_new_log(new_log)

        with open(self.log_file, 'w') as f:
            f.write(new_log_list) 


    def print_log(self):
        '''print log file to console'''
        record_list = self._create_record_list()
        print(*record_list, sep='') #default value of sep adds an extra space before each record so i removed this


    def delete_old_records(self):
        '''deletes all records from file they are at least 30 days old'''
        record_list = self._create_record_list()

        dt_now = datetime.datetime.now()
        #NOTE by checking most recent records first you can stop searching when you find a 30 day old record and remove all records past that 
        for i in range(len(record_list)):
            dt_move = self._extract_date_time(record_list[i]) #datetime of when the file was moved
            if (dt_now - dt_move).days >= 30: 
                record_list = record_list[:i] #remove current record and all records after current from list
                break
        
        with open(self.log_file, 'w') as f:
            f.write("".join(record_list))
        

    def _extract_date_time(self,record):
        '''extract the date and time portion of a record and return a datetime object'''
        date_time = record.split('] ')[0] #obtain date-time portion of the record 
        date_time = date_time[1:]   #remove '[' from start of date_time
        date, time = date_time.split('--')

        dt_str = f"{date} {time}" 

        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %I:%M %p") #convert str to datetime object
    

    def _get_file_datetime(self, file_path):
        '''get a human readable date and time of the last metadata change for a file in a 12-hour format'''
        metadata_timeStamp = os.stat(file_path).st_ctime #timestamp of when the file was moved to different directory
        move_datetime = datetime.datetime.fromtimestamp(metadata_timeStamp) #convert timestamp to human readable format

        move_date = move_datetime.date() 
        move_time12hr = move_datetime.time().strftime("%I:%M %p") #convert time to 12 hour format 

        return move_date, move_time12hr


    def _create_log(self, file_path:Path):
        '''creates a new log using the file path'''
        move_date, move_time = self._get_file_datetime(file_path)
        file_name = file_path.name
        type_dir = file_path.parent.parent.name #skip over date-directory to extract file type directory

        return f"[{move_date}--{move_time}] {file_name} moved to {type_dir}\n"


    def _prepend_new_log(self, new_log:str):
        '''prepend a new log to a list of logs so the order is most recent to oldest'''
        file_logs = self._create_record_list()

        new_log_list = [new_log] #extend method modifies list in place so must store new log in its own variable
        new_log_list.extend(file_logs)

        return "".join(new_log_list)
    

    def _create_record_list(self):
        '''create a list of records read from file_move_log.txt'''
        with open(self.log_file, 'r') as f:
            record_list = f.readlines()

        return record_list


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

def path_setup(file_type):
    '''create the proper path directories and return a valid path'''
    type_path = DOWNLOAD_DIR.joinpath(file_type)  # create path object using the file
    create_dir(type_path)  # create new directory using the file type
    curr_date_str = str(datetime.date.today())
    date_path = type_path.joinpath(curr_date_str)
    create_dir(date_path)

    return date_path


def move_file(file): 
    '''move file from parent dir to new dir based on file type'''
    for file_type, f_extension in valid_extensions.items():
        file_suffix = get_file_suffix(file)

        if file_suffix in f_extension:
            
            date_path = path_setup(file_type) 
            shutil.move(file, date_path) 
            logger.write(date_path / file.name) #send updated file path to log_manager write method


def main():
    logger.delete_old_records()
    for f in DOWNLOAD_DIR.iterdir():
        move_file(f)


if __name__ == "__main__":
    main()
    logger.print_log()
