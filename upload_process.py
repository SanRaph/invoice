import json

import cv2
import requests
from pdf2image import convert_from_path
from pyzbar import pyzbar

import functions as fun
from get_headers import get_headers


def upload_barcode(file_path):
    config_data = fun.read_config_data()
    url = config_data.get('api_link')
    file_split = file_path.split('/')[-1].split('.')
    file_name, file_extension = file_split[0], file_split[1]
    file = file_name + '.' + file_extension

    print("Trying for file ", file)

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
        payload = {}

        if file_extension.lower() == "pdf":
            payload = {
                "recordType": "invoice",
                "recordNumber": b_data,
                "fileType": file_extension.upper(),
                "fileName": file,
                "fileContent": fun.get_file_content(file_path).decode('utf-8')
            }
        elif file_extension.lower() == "png":
            payload = {
                "recordType": "invoice",
                "recordNumber": b_data,
                "fileType": "PNGIMAGE",
                "fileName": file,
                "fileContent": fun.get_image_content(file_path).decode('utf-8')
            }
        elif file_extension.lower() == "jpg":
            payload = {
                "recordType": "invoice",
                "recordNumber": b_data,
                "fileType": "JPGIMAGE",
                "fileName": file,
                "fileContent": fun.get_image_content(file_path).decode('utf-8')
            }

        headers = get_headers()

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200 and "success" in response.text:
            fun.move_file_to_folder(file)
        fun.write_log(payload['recordNumber'], file, response.text)


def process_files(files):
    for file in files:
        upload_barcode(file)
