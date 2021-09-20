import time
import upload_process

config_data = upload_process.read_config_data()


def main(files_):
    # process files
    upload_process.process_files(files_)


if __name__ == "__main__":
    path_to_watch = config_data.get("source_folder")
    while True:
        print("Checking files in Source Folder")
        time.sleep(config_data.get('refresh_time'))
        files = upload_process.get_files_in_folder((config_data.get("source_folder") + "*"))
        if files:
            print(f"{len(files)} found. Starting operation.")
            main(files)
        else:
            print(f"No files found. Will start operation in another {config_data.get('refresh_time')}")
