import base64
import datetime
import glob
import json
import shutil

import pdfplumber


def read_config_data():
    with open('config.txt', 'r') as config_file:
        config_data = json.load(config_file)
    return config_data


def get_files_in_folder(folder):
    return glob.glob(folder)


def convert_pdf_to_text(file_path):
    pdf = pdfplumber.open(file_path)
    pages = pdf.pages
    full_text = ""
    for page in pages:
        text = page.extract_text()
        full_text += text
    pdf.close()
    return full_text


def write_log(barcode, file_name, response):
    now = datetime.datetime.now()
    file = open(f'logs/{now.strftime("%b-%d-%Y")}.log', 'a+')
    log = "Date: " + str(now) + " | Barcode: " + barcode + " | File name: " + file_name + " : Status: " + response
    file.write(f"{log}\n")


def move_file_to_folder(file_name):
    config_data = read_config_data()
    current_folder = config_data.get('source_folder')
    new_folder = config_data.get('destination_folder')
    shutil.move(current_folder + file_name, new_folder + file_name)


def get_file_content(file_path):
    with open(file_path, 'rb') as file:
        encode = base64.b64encode(file.read())
    return encode


def get_image_content(file_path):
    with open(file_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string
