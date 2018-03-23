import requests
import hashlib
import json
import base64
import ast
from pathlib import Path

def getInstagramAPI(endpoint, endParams, instagramToken):
    apiUrl = "https://api.twitter.com/1.1/%s.json?%s" % (endpoint, endParams)
    reqResponse = requests.get(apiUrl,
        headers = {
        "host":"api.twitter.com","accept":"application/json",
        "authorization":"Bearer %s" % (instagramToken),
        "accept-encoding":"UTF-8"})
        
    if reqResponse.status_code == requests.codes.ok:
        return reqResponse.json()
    else:
        print("getInstagramAPI\nError code (%s):\n\n%s\n\n%s\n" % (reqResponse.status_code, reqResponse.headers, reqResponse.text))
        return None

def getInstagramToken():
    apiUrl = "https://api.instagram.com/oauth/authorize?client_id=2fb1a13a803d4f07b9d99d43f250e528&redirect_uri=http://127.0.0.1&response_type=token"
    apiKey = "API_KEY"
    apiSecret = "API_SECRET"
    bTokenCreden = "%s:%s" % (apiKey, apiSecret)
    b64TokenCreden = base64.b64encode(bTokenCreden.encode("utf-8"))
    reqResponse = requests.post(apiUrl, data = "grant_type=client_credentials",
        headers =
        {"host":"api.twitter.com",
         "accept":"application/json",
         "authorization":"Basic %s" % (b64TokenCreden.decode("utf-8")),
         "content-type":"application/x-www-form-urlencoded;charset=UTF-8",
         "content-length":"29",
         "accept-encoding":"UTF-8"})
         
    if reqResponse.status_code == requests.codes.ok:
        return reqResponse.json()["access_token"]
    else:
        print("getInstagramToken\nError code (%s):\n\n%s\n\n%s\n" % (reqResponse.status_code, reqResponse.headers, reqResponse.text))
        return None

def requestAPI(endpoint, endParams):
    jsonFileName = hashlib.md5(("%s%s" % (endpoint, endParams)).encode('utf-8')).hexdigest()
    jsonFile = Path("./cache/instagram/%s.json" % (jsonFileName))
    jsonContent = None
    if jsonFile.is_file():
        jsonContent = jsonFile.read_text(encoding='utf-8')
        jsonContent = json.loads(jsonContent)
    else:
        instagramToken = getInstagramToken()
        if twitterToken is not None:
            jsonContent = getInstagramAPI(endpoint, endParams, instagramToken)
            if jsonContent is not None:
                jsonFile.write_text(json.dumps(jsonContent), encoding='utf-8')
    return jsonContent
