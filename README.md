# Python Image to Text Program

## Project Description

We need to scan an average of 2000 printed invoices and upload the scanned copies of them to NetSuite which is our ERP system. 
In NetSuite, we need to attach the scanned invoice to the corresponding invoice record.

To do that, we need:
    • A scanner that has a scanning speed of at least 60ppm (60 pages per minute). 
    Here is the one we will use: https://www.usa.canon.com/internet/portal/us/home/products/details/scanners/document-scanner/imageformula-dr-m160ii
    • A Desktop program:
        ◦ That will read the barcode in the scanned invoice. 
        ◦ That will create an API that will upload each document from the local computer to NetSuite.
    • A NetSuite API:
        ◦ That will receive the scanned document from the image-to-text software.
        ◦ That will attach the scanned document to the corresponding NetSuite invoice records.
        ◦ That will upload the files from the file cabinet to AWS.

## A Desktop Program

#### Use Case:
    • The employee scans 2000 invoices at one time using the ultra-fast scanner (60 pages per minute)
    • The scanner creates PDF, PNG or JPEG files of the 2000 invoices in the local computer.
    • The desktop program reads each of the PDF, PNG or JPEG files to know the Invoice number based on the barcode of every file.
    • The desktop program triggers a REST Api call to NetSuite, the ERP system, to upload the files.
    • The desktop program moves the PDF, PNG or JPEG files of the 2000 invoices to other folder.

#### Requirements:
    • It should be easily installed to any local computer.
    • It should have a setting where the user can change the folder location where the scanned invoices are located.
    • It should be able to read PDF, PNG or JPEG files.
    • It should have a setting where the user can change the URL of the REST Api of NetSuite.





## REST API

### Python – http.client

	import http.client
        conn = http.client.HTTPSConnection("5774630.restlets.api.netsuite.com")
        payload = "{\n    \"recordType\": \"invoice\",\n    \"recordNumber\": \"INV190251\",\n    \"fileType\": \"PDF\",\n    \"fileName\": \"test1.pdf\",\n    
	 \"fileContent\": \"file content\"\n}"
        headers = {
             'Content-Type': 'application/json',
             'Authorization': 'OAuth  realm="5774630",
	     oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",
	     oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",
	     oauth_signature_method="HMACSHA1",
	     oauth_timestamp="1630602678",
	     oauth_nonce="qQ4n9hdz96u",
	     oauth_version="1.0",
	     oauth_signature="cHoxq5NenUCGIIXDoeYzxkHpzY0%3D"',
             'Cookie': 'NS_ROUTING_VERSION=LAGGING'
         }
         conn.request("POST", "/app/site/hosting/restlet.nl?deploy=1&script=1878", payload, headers)
         res = conn.getresponse()
         data = res.read()
         print(data.decode("utf-8"))


### Python – Requests

	import requests

        url = "https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878"

        payload="{
	         \n\"recordType\": \"invoice\",
	         \n\"recordNumber\": \"INV190251\",
	         \n\"fileType\": \"PDF\",
	         \n\"fileName\": \"test1.pdf\",
	         \n\"fileContent\": \"file content\"\n
		 }"
        headers = {
                  'Content-Type': 'application/json',
                  'Authorization': 'OAuth   realm="5774630",
		  oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",
		  oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",
		  oauth_signature_method="HMAC-SHA1",
		  oauth_timestamp="1630602678",
		  oauth_nonce="qQ4n9hdz96u",
		  oauth_version="1.0",
		  oauth_signature="cHoxq5NenUCGIIXDoeYzxkHpzY0%3D"',
                  'Cookie': 'NS_ROUTING_VERSION=LAGGING'
                  }

       response = requests.request("POST", url, headers=headers, data=payload)

       print(response.text)


### cURL

	curl --location --request POST 'https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878'
	\--header 'Content-Type: application/json' \--header 'Authorization: OAuth realm="5774630",
        oauth_consumer_key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",
        oauth_token="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",oauth_signature_method="HMAC-SHA1",
	oauth_timestamp="1630602678",
	oauth_nonce="qQ4n9hdz96u",
	oauth_version="1.0",
	oauth_signature="cHoxq5NenUCGIIXDoeYzxkHpzY0%3D"'\--header 'Cookie: NS_ROUTING_VERSION=LAGGING' \--data-raw 
	'{
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


## Contributing

If you want to contribute to this project and make it better, your help is very welcome. 
Adding new features or making constructive, helpful bug reports and feature requests is how we get this project to where it should be.

### How to make a clean pull request

Take these steps to be part of this projects' contribution.

- Create a personal fork of the project on Github.
- Clone the fork on your local machine.
- Add the original repository as a remote called `upstream`.
- If you created your fork a while ago be sure to pull upstream changes into your local repository.
- Create a new branch to work on! Branch from `develop` if it exists, else from `master`.
- Implement/fix your feature, comment your code.
- Follow the code style of the project, including indentation.
- If the project has tests run them although, there are no test scripts at the moment!
- Write or adapt tests as needed.
- Add or change the documentation as needed.
- Squash your commits into a single commit with git's [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.
- Push your branch to your fork on Github, the remote `origin`.
- From your fork open a pull request in the correct branch. Target the project's `develop` branch if there is one, else go for `master`!
- ...
- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete
your extra branch(es).

And last but not least: Always write your commit messages in the present tense. 
Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.


REMINDER: In your testing, don’t upload more than 2 files.

Thank you for HACKING this project with us.
