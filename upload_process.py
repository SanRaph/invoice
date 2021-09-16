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
    return full_text


def set_url(url_path):
    if not url_path:
        return "https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878"
    return url_path


def upload_barcode(file_path, url_path):
    url = set_url(url_path)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth realm="5774630",oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1631817578",oauth_nonce="x0x3CDHPGKn",oauth_version="1.0",oauth_signature="edvx9rZXLGKWQBSP5BU6pFepm1U%3D"',
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
            "fileType": "PNGIMAGE",
            "fileName": "",
            "fileContent": convert_pdf_to_text(file_path)
        }

        print(payload)

        response = requests.post(url=url, headers=headers, data=payload)
        print(response.text)
