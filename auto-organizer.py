#! /usr/bin/python3

import shutil
import sys
from pathlib import Path


if len(sys.argv) > 1 and sys.argv[1] == 'cwd': #set INIT_DIR to the current working directory
    INIT_DIR = Path.cwd()
else:
    INIT_DIR = Path.home() #path where the download files will be moved to.


def main():
    print(INIT_DIR)

main()