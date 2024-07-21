import os
import pprint
import time

path_current_folder = os.path.dirname(os.path.abspath(__file__))
absolute_path_out_folder = os.path.join(path_current_folder, "calculate_correlations_output","only_pair")
file_name_list = os.listdir(absolute_path_out_folder)
file_object = []

for i in range(len(file_name_list)):
    print(i)
    data = {}

    with open(os.path.join(absolute_path_out_folder, file_name_list[i]), "r", encoding="utf-8") as file:
        file_path = file_name_list[i]
        for line in file.read().split('\n'):
            data[key.strip()] = value.strip()
        file_object.append()

        print(file_object)
        time.sleep(100)