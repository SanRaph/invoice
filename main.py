import upload_process
import os, time


config_data = upload_process.read_config_data()


def main(files):
    # process files
    upload_process.process_files(files)


if __name__ == "__main__":
    path_to_watch = config_data.get("source_folder")
    while True:
        time.sleep(60)
        files = upload_process.get_files_in_folder((config_data.get("source_folder") + "*"))
        if files:
            main(files)
