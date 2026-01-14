#! /usr/bin/python3
# populates downloads directory with files and removes sub-directories
from pathlib import Path

download_dir = Path.home() / 'downloads' 
files = ('hi.txt', 'friend.txt', 'funny.mov', 'metallica.mp3','show_ep1.mov','dog.jpg','study.pdf', 'history.tar.gz')


for f in files:  #repopulate downloads with files
    file_path = download_dir / f
    file_path.touch()

with open('file_move_log.txt', 'w') as f:
    f.write("**Records older than 30 days will be deleted\n")
