import argparse
import json

class ArgsParse:
    def read_json_file_to_object(json_file_path, string_encoding='utf-8'):
        try:
            # Open the JSON file for reading
            with open(json_file_path, 'r', encoding=string_encoding) as file:
                # Parse the JSON content into a dictionary
                json_object = json.load(file)
                return json_object
        except FileNotFoundError:
            print(f"The file at path '{json_file_path}' was not found.")
            exit(-1)
        except json.JSONDecodeError:
            print(f"The file at path '{json_file_path}' does not contain valid JSON.")
            exit(-1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(-1)

