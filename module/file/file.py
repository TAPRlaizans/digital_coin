

import os
import sys

class File:
    def __init__(self):
        pass

    def checkFileExists(path_file):
        if os.path.exists(path_file):
            return True
        else:
            print(f"{path_file} is not exits!")
            return False
    
    def mkdirFile(path_file):
        if not os.path.exists(path_file):
            os.makedirs(path_file)
        else:
            print(f"{path_file} is not exists!")