import base64
import glob
import json
import os
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


def changes_in_folder(folder):
    saved_set = set()
    my_path = folder

    name_set = set()
    for file in os.listdir(my_path):
        full_path = os.path.join(my_path, file)
        if os.path.isfile(full_path):
            name_set.add(file)

    retrieved_set = set()
    for name in name_set:
        stat = os.stat(os.path.join(my_path, name))
        time = stat.ST_CTIME
        size = stat.ST_SIZE
        last_modified = stat.ST_MTIME
        retrieved_set.add((name, time, size, last_modified))

        new_set = retrieved_set - saved_set

        return new_set


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
    print(file_name)
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


def set_url(url_path):
    if not url_path:
        return "https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878"
    return url_path


def upload_barcode(file_path):
    config_data = read_config_data()
    api_link = config_data.get('api_link')
    url = set_url(api_link)
    file_split = file_path.split('/')[-1].split('.')
    file_name, file_extension = file_split[0], file_split[1]
    file = file_name + '.' + file_extension

    headers = {
        'Authorization': 'OAuth realm="5774630",'
                         'oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",'
                         'oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",'
                         'oauth_signature_method="HMAC-SHA1",oauth_timestamp="1631905608",oauth_nonce="DV1Eh3yLCf6",'
                         'oauth_version="1.0",oauth_signature="UA67Drt1XGESJ6Ygc9nW9B8Fe6E%3D"',
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
        print(response.text)
        if "success" not in response.text:
            move_file_to_folder(file)
        else:
            print("failed")


def process_files(files):
    for file in files:
        upload_barcode(file)
