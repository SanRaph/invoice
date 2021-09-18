import base64
import json

import cv2
from pyzbar import pyzbar
import requests
import pdfplumber
from pdf2image import convert_from_path


def convert_pdf_to_text(file_path):
    pdf = pdfplumber.open(file_path)
    pages = pdf.pages
    full_text = ""
    for page in pages:
        text = page.extract_text()
        full_text += text
    pdf.close()
    return full_text


def get_file_content(file_path):
    with open(file_path, 'rb') as file:
        encode = base64.b64encode(file.read())
    return encode


def set_url(url_path):
    if not url_path:
        return "https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878"
    return url_path


def upload_barcode(file_path, url_path):
    url = set_url(url_path)
    file_name = file_path.split('/')[-1]

    headers = {
        'Authorization': 'OAuth realm="5774630",oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1631905608",oauth_nonce="DV1Eh3yLCf6",oauth_version="1.0",oauth_signature="UA67Drt1XGESJ6Ygc9nW9B8Fe6E%3D"',
        'Content-Type': 'application/json',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    pdf_page = convert_from_path(file_path)
    for page in pdf_page:
        page.save('out.png', 'PNG')

    image = cv2.imread("out.png")
    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        x, y, w, h = barcode.rect

        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 4)

        # convert into string
        b_data = barcode.data.decode("utf-8")

        payload = {
            "recordType": "invoice",
            "recordNumber": b_data,
            "fileType": "PDF",
            "fileName": file_name,
            "fileContent": get_file_content(file_path).decode('utf-8')
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.text)
