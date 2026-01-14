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
        self.default_msg = "**Records older than 30 days will be deleted\n" #this message appears in first line of the log file


    def update_logfile(self,file_path:Path):
        '''updates log file with new records'''
        new_log = self._create_log(file_path)
        new_log_list = self._prepend_new_log(new_log)

        self._write_to_file(new_log_list) 


    def print_log(self):
        '''print log file to console'''
        record_list = self._create_record_list()
        record_list.insert(0, self.default_msg)
        print(*record_list, sep='') #default value of sep adds an extra space before each record so i removed this


    def delete_old_records(self):
        '''deletes all records from file they are at least 30 days old and updates log file'''
        record_list = self._create_record_list()

        dt_now = datetime.datetime.now()
        #NOTE by checking most recent records first you can stop searching when you find a record older than 30 days, remove that record and all records past that 
        for i in range(len(record_list)):
            dt_move = self._extract_date_time(record_list[i]) #datetime of when the file was moved
            if (dt_now - dt_move).days >= 30: 
                record_list = record_list[:i] #remove current record and all records after current from list
                break
        
        self._write_to_file(record_list)


    def _write_to_file(self, record_list:list[str]):
        '''writes directly to log file'''
        record_list.insert(0, self.default_msg) #insert default message to start of list
        record_str = "".join(record_list)

        with open(self.log_file, 'w') as f:
            f.write(record_str)
        

    def _extract_date_time(self,record:str):
        '''extract the date and time portion of a record and return a datetime object'''
        date_time = record.split('] ')[0] #obtain date-time portion of the record 
        date_time = date_time[1:]   #remove '[' from start of date_time
        date, time = date_time.split('--')

        dt_str = f"{date} {time}" 

        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %I:%M %p") #convert str to datetime object
    

    def _get_file_datetime(self, file_path:Path):
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

        return new_log_list
    

    def _create_record_list(self):
        '''create a list of records read from file_move_log.txt'''
        with open(self.log_file, 'r') as f:
            fileline_list = f.readlines()

        record_list = fileline_list[1:] #remove the default message from record list
        return record_list


logger = log_manager()


def create_dir(dir_path:Path):
    '''creates a directory'''
    try:
        dir_path.mkdir()
    except FileExistsError:
        print(f"Directory {dir_path} already exists")


def get_file_suffix(file_path:Path): #NOTE must account for object with no extensions
    '''return extension of a file'''
    #some file extensions will have 2 dots(example.tar.gz) so using .suffix attribute will not work in those cases
    file_name = file_path.name
    index =  file_name.find('.')

    if index == -1:
        extension = ""
    else:
        extension = file_name[index:]

    return extension


def dir_setup(file_type:str):
    '''create the proper path directories and return a valid path'''
    type_path = DOWNLOAD_DIR.joinpath(file_type)  # create path object using the file
    create_dir(type_path)  # create new directory using the file type

    curr_date_str = str(datetime.date.today())
    date_path = type_path.joinpath(curr_date_str)
    create_dir(date_path)

    return date_path

def create_format_str(file_str:str):
    '''creates and returns format string for duplicate file name'''
    
    str_list = file_str.split('.', 1)
    join_str = "({num})." #used to insert values by using .format()

    return join_str.join(str_list)

def get_valid_dupl(format_str:str, dst_path:Path):
    '''return a duplicate name that does not exist in destination path'''
    duplicate_num = 1
    duplicate_name = format_str.format(num=duplicate_num)

    while (dst_path / duplicate_name).exists():
        duplicate_num += 1
        duplicate_name = format_str.format(num=duplicate_num)
    
    return duplicate_name

def rename_duplicate(file_path:Path, duplicate_name: str):
    '''renames the duplicate file within the filesystem'''
    
    duplicate_path = file_path.parent / duplicate_name
    os.rename(file_path, duplicate_path)

def move_duplicate(duplicate_name:str, dst_path:Path):
    '''move duplicate file to destination path'''
    duplicate_path = DOWNLOAD_DIR.joinpath(duplicate_name)
    try:
        shutil.move(duplicate_path, dst_path)
    except shutil.Error:
        print("ERROR: moving duplicate file failed.")


def duplicate_handler(file:Path, dst_path:Path):
    '''handles various tasks related to duplicate files'''

    # file_sorter() handles the case where a file has no extension so no need to worry about that here
    dupl_format_str = create_format_str(file.name)
    duplicate_name = get_valid_dupl(dupl_format_str, dst_path)

    rename_duplicate(file, duplicate_name)
    move_duplicate(duplicate_name, dst_path)


def move_file(file:Path, dst_path:Path):
    '''moves file to specified directory '''
    try:
        shutil.move(file, dst_path)
    except shutil.Error:
        print(f'DUPLICATE FILE: {file.name}')
        duplicate_handler(file, dst_path)


def file_sorter(file:Path): 
    '''move file from parent dir to new dir based on file type'''
    for file_type, f_extension in valid_extensions.items():
        file_suffix = get_file_suffix(file)

        if file_suffix in f_extension:
            date_dir_path = dir_setup(file_type) 
            move_file(file, date_dir_path) 
            logger.update_logfile(date_dir_path / file.name) #send updated file path to log_manager write method
            break


def remove_dir(dir):
    '''deletes empty directory'''
    try:
        os.rmdir(dir)
    except OSError:
        print(f"{dir} is not empty")

def cleanup_dirs():
    '''remove any empty directories and sub-directories in downloads'''
    for dir in DOWNLOAD_DIR.iterdir(): 
        if dir.name not in valid_extensions.keys(): #prevents accidentally removing other directories in downloads that dont have file type name
            continue
        for sub_dir in dir.iterdir(): #iterate thru sub-directories in dir
            remove_dir(sub_dir)
                
        remove_dir(dir)

def main():
    logger.delete_old_records()
    for f in DOWNLOAD_DIR.iterdir():
        file_sorter(f)

    logger.print_log()

if __name__ == "__main__":
    main()
    cleanup_dirs()
