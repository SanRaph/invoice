import base64
import glob
import json
import shutil


import cv2
import pdfplumber
import requests
from pdf2image import convert_from_path
from pyzbar import pyzbar


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


def upload_barcode(file_path):
    config_data = read_config_data()
    url = config_data.get('api_link')
    consumer_key = config_data.get('consumer_key')
    consumer_key = f'"{consumer_key}"'
    access_token = config_data.get("access_token")
    access_token = f'"{access_token}"'
    file_split = file_path.split('/')[-1].split('.')
    file_name, file_extension = file_split[0], file_split[1]
    file = file_name + '.' + file_extension

    headers = {
        'Authorization': f'OAuth realm="5774630",'
                         f'oauth_consumer_key={consumer_key},'
                         f'oauth_token={access_token},'
                         f'oauth_signature_method="HMAC-SHA1",oauth_timestamp="1631997167",oauth_nonce="sVPRo7oyi0K",'
                         f'oauth_version="1.0",oauth_signature="Jd6xwEsubdlBOluQmsExUkF7TgI%3D"',
        'Content-Type': 'application/json',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    if file_extension.lower() == "pdf":
        pdf_page = convert_from_path(file_path)
        for page in pdf_page:
            page.save('bar_code.png', 'PNG')
        image = cv2.imread("bar_code.png")
    else:
        image = cv2.imread(file_path)
    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        x, y, w, h = barcode.rect

        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 4)

        # convert into string
        b_data = barcode.data.decode("utf-8")

        if file_extension.lower() == "pdf":
            payload = {
                "recordType": "invoice",
                "recordNumber": b_data,
                "fileType": file_extension.upper(),
                "fileName": file,
                "fileContent": get_file_content(file_path).decode('utf-8')
            }
        else:
            payload = {
                "recordType": "invoice",
                "recordNumber": b_data,
                "fileType": file_extension.upper(),
                "fileName": file,
                "fileContent": get_image_content(file_path).decode('utf-8')
            }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            if "success" in response.text:
                move_file_to_folder(file)
            else:
                print(file, "failed to upload to Netsuite with 200 status")
        else:
            print(file, "failed to upload without 200 status")


def process_files(files):
    for file in files:
        upload_barcode(file)
