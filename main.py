import time

import functions as fun
from upload_process import process_files

config_data = fun.read_config_data()


def main(files_):
    # process files
    process_files(files_)


if __name__ == "__main__":
    path_to_watch = config_data.get("source_folder")
    while True:
        print("Checking files in Source Folder")
        time.sleep(config_data.get('refresh_time'))
        files = fun.get_files_in_folder((config_data.get("source_folder") + "*"))
        if files:
            print(f"{len(files)} found. Starting operation.")
            main(files)
        else:
            print(f"No files found. Will start operation in another {config_data.get('refresh_time')} seconds")
