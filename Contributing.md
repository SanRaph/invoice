# Python Image to Text Program

## Project Description

We need to scan an average of 2000 printed invoices and upload the scanned copies of them to NetSuite which is our ERP system. 
In NetSuite, we need to attach the scanned invoice to the corresponding invoice record.

To do that, we need:
    • A scanner that has a scanning speed of at least 60ppm (60 pages per minute). 
    Here is the one we will use: https://www.usa.canon.com/internet/portal/us/home/products/details/scanners/document-scanner/imageformula-dr-m160ii
    • A Desktop program:
        ◦ That will read the barcode in the scanned invoice. 
        ◦ That will create an API that will upload each document from the local computer to NetSuite.
    • A NetSuite API:
        ◦ That will receive the scanned document from the image-to-text software.
        ◦ That will attach the scanned document to the corresponding NetSuite invoice records.
        ◦ That will upload the files from the file cabinet to AWS.

A Desktop Program

Use Case:
    • The employee scans 2000 invoices at one time using the ultra-fast scanner (60 pages per minute)
    • The scanner creates PDF, PNG or JPEG files of the 2000 invoices in the local computer.
    • The desktop program reads each of the PDF, PNG or JPEG files to know the Invoice number based on the barcode of every file.
    • The desktop program triggers a REST Api call to NetSuite, the ERP system, to upload the files.
    • The desktop program moves the PDF, PNG or JPEG files of the 2000 invoices to other folder.

Requirements:
    • It should be easily installed to any local computer.
    • It should have a setting where the user can change the folder location where the scanned invoices are located.
    • It should be able to read PDF, PNG or JPEG files.
    • It should have a setting where the user can change the URL of the REST Api of NetSuite.





REST API

Python – http.client

import http.client

conn = http.client.HTTPSConnection("5774630.restlets.api.netsuite.com")
payload = "{\n    \"recordType\": \"invoice\",\n    \"recordNumber\": \"INV190251\",\n    \"fileType\": \"PDF\",\n    \"fileName\": \"test1.pdf\",\n    \"fileContent\": \"file content\"\n}"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'OAuth realm="5774630",oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1630602678",oauth_nonce="qQ4n9hdz96u",oauth_version="1.0",oauth_signature="cHoxq5NenUCGIIXDoeYzxkHpzY0%3D"',
  'Cookie': 'NS_ROUTING_VERSION=LAGGING'
}
conn.request("POST", "/app/site/hosting/restlet.nl?deploy=1&script=1878", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


Python – Requests

import requests

url = "https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878"

payload="{\n    \"recordType\": \"invoice\",\n    \"recordNumber\": \"INV190251\",\n    \"fileType\": \"PDF\",\n    \"fileName\": \"test1.pdf\",\n    \"fileContent\": \"file content\"\n}"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'OAuth realm="5774630",oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1630602678",oauth_nonce="qQ4n9hdz96u",oauth_version="1.0",oauth_signature="cHoxq5NenUCGIIXDoeYzxkHpzY0%3D"',
  'Cookie': 'NS_ROUTING_VERSION=LAGGING'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


cURL

curl --location --request POST 'https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878' \
--header 'Content-Type: application/json' \
--header 'Authorization: OAuth realm="5774630",oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1630602678",oauth_nonce="qQ4n9hdz96u",oauth_version="1.0",oauth_signature="cHoxq5NenUCGIIXDoeYzxkHpzY0%3D"' \
--header 'Cookie: NS_ROUTING_VERSION=LAGGING' \
--data-raw '{
    "recordType": "invoice",
    "recordNumber": "INV190251",
    "fileType": "PDF",
    "fileName": "test1.pdf",
    "fileContent": "file content"
}'


Parameters:

	recordType – Always “invoice”
	recordNumber – The barcode value
	filetype – PDF, JPGIMAGE, or PNGIMAGE
	filename – The filename of the file with file extension.
	fileContent – File content of the file.



REMINDER: In your testing, don’t upload more than 10 files.
