import oauth2 as oauth
import time


def get_headers():
    url = "https://5774630.restlets.api.netsuite.com/app/site/hosting/restlet.nl?deploy=1&script=1878"
    token = oauth.Token(key="b9195e93e272c7fd63ab47df3404b8688ed907827febe408208f1933b58e3f35",
                        secret="07e82f74e617dcd5c34854f805542dd4cce6c555d145212da3763dc7fc5d86f2")
    consumer = oauth.Consumer(key="a5cadba7533c1f5b1a6bcecd088c1de1cf2c6442044250859fdaf5d6a3327fd4",
                              secret="7c08803c96f15d54df63208c196008ba263a84f2e08a1dcdc64e8a8938f00582")

    http_method = "POST"
    realm = "5774630"

    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': str(int(time.time())),
        'oauth_token': token.key,
        'oauth_consumer_key': consumer.key
    }

    req = oauth.Request(method=http_method, url=url, parameters=params)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token)
    header = req.to_header(realm)
    headery = header['Authorization'].encode('ascii', 'ignore')
    return {"Authorization": headery, "Content-Type": "application/json"}
