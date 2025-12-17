#! /usr/bin/python3
# populates downloads directory with files
from pathlib import Path

download_dir = Path.home() / 'downloads' 
files = ('hi.txt', 'friend.txt', 'funny.mov', 'metallica.mp3','show_ep1.mov','dog.jpg','study.pdf', 'history.tar.gz')


def clear_dir(parent_dir):  # NOTE be very careful when deleting multiple directories
    '''delete all files w/i directory'''
    for file in parent_dir.iterdir():
        file.unlink()
        print(f"{file.name} deleted")


for f in Path.iterdir(download_dir): #remove all directories w/i the submitted directory
    if f.is_dir():
        clear_dir(f)
        f.rmdir()

for f in files:  #repopulate downloads with files
    file_path = download_dir / f
    file_path.touch()

open('file_move_log.txt', 'w').close() #clear content in file_move_log.txt
