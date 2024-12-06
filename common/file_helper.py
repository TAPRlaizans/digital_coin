#///////////////////////////////////////////////////////////////////////////////
#
# (c) 2019-2022 Toolsensing, Inc. All rights reserved.
# Unless otherwise permitted, no distribution or use is permitted.
#
#///////////////////////////////////////////////////////////////////////////////


# coding=utf-8
import os
import re
import sys
import time
import shutil
from loguru import logger
from common.logger import Logger, LogLevel

class FileHelper():
    @staticmethod
    def remove_folder(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f"無法刪除 {file_path}: {e}")
                return False
        return True
    
    @staticmethod
    def check_folder_exist(self, folder_path, flag_recreate=False):
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                logger.info(f"output directory created!")
            except Exception as e:
                logger.error(f"failed to create {folder_path}: {e}")
                return False
        else:
            if flag_recreate == True:
                if self.remove_folder(folder_path):
                    logger.info(f"output directory is not empty, has been removed!")
                else:
                    logger.error(f"failed to remove {folder_path}")
                    return False
        return True
    
    @staticmethod
    def check_file_exist(self, file_path, flag_recreate=False):
        if not os.path.exists(file_path):
            open(file_path, 'w').close()
            logger.info(f"output file created!")
        else:
            if flag_recreate == True:
                os.remove(file_path)
                logger.info(f"output file is not empty, has been removed!")
        return True

    @staticmethod
    def replace_file_content(self, file_name, old_content, new_content):
        all_lines = self.read_all_lines(file_name)
        new_all_lines = []
        for line in all_lines:
            if re.search(old_content, line) is None:
                new_all_lines.append(line)
                continue

            new_all_lines.append(line.replace(old_content, new_content))

        self.write_all_lines(file_name, new_all_lines)

    @staticmethod
    def rm_files(directory, pattern, recursion=False):
        rm_file_list = []
        if recursion:
            for (root, dirs, files) in os.walk(directory):
                for f in files:
                    if re.search(pattern, f):
                        rm_file_list.append(os.path.join(root, f))
        else:
            for f in os.listdir(directory):
                if re.search(pattern, f):
                    rm_file_list.append(os.path.join(directory, f))

        for rm_file in rm_file_list:
            os.remove(rm_file)

    @staticmethod
    def read_all_data(filename):
        file_object = open(filename, r"rb")
        try:
            all_data = file_object.read()
            return all_data
        finally:
            file_object.close()

    @staticmethod
    def get_all_files_name_list(directory, abs_name=True):
        """
            get all files in the specified directory recursively
        :param directory:
        :return:
        """
        if not directory.endswith(r"/"):
            directory += r"/"

        all_files_abs_name_list = []
        for (root, dirs, files) in os.walk(directory):
            for file_name in files:
                name = os.path.join(root, file_name)
                if not abs_name:
                    name = name[len(directory):]

                all_files_abs_name_list.append(name)

        return all_files_abs_name_list

    @staticmethod
    def write_all_lines(filename, alllines, mode="w"):
        file_object = open(filename, "%s" % mode)
        try:
            file_object.writelines(alllines)
        finally:
            file_object.close()


    @staticmethod
    def read_all_lines(filename):
        if not os.path.isfile(filename):
            print("error: '%s' is not a file" % filename)
            return None

        file_object = open(filename)
        try:
            all_lines = file_object.readlines()
            return all_lines
        finally:
            file_object.close()

def main(): 
    pass

if __name__ == "__main__":
    main()
