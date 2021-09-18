import upload_process


def main():
    config_data = upload_process.read_config_data()
    files = upload_process.get_files_in_folder((config_data.get("source_folder") + "*"))

    # process files
    upload_process.process_files(files)


if __name__ == "__main__":
    main()
