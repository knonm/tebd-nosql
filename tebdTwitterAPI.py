import requests
import hashlib
import json
import base64
import ast
from pathlib import Path

class HTTPError(Exception):
    def __init__(self, method, urlReq, reqResponse):
        self.method = method
        self.urlReq = urlReq
        self.reqResponse = reqResponse
        
    def __str__(self):
        sep = "===================================================="
        return "\n%s\nMethod: %s\nURL: %s\nResponse Code: %d\n\nResponse Header:\n%s\n\nResponse:\n%s\n%s\n" % (sep, self.method, 
        self.urlReq, self.reqResponse.status_code, self.reqResponse.headers, self.reqResponse.text, sep)

class HTTPTooManyError(HTTPError):
    pass

def getTwitterAPI(endpoint, endParams, twitterToken):
    apiUrl = "https://api.twitter.com/1.1/%s.json?%s" % (endpoint, endParams)
    reqResponse = requests.get(apiUrl,
        headers = {
        "host":"api.twitter.com","accept":"application/json",
        "authorization":"Bearer %s" % (twitterToken),
        "accept-encoding":"UTF-8"})
        
    if reqResponse.status_code == requests.codes.ok:
        return reqResponse.json()
    elif reqResponse.status_code == requests.codes.too_many:
        raise HTTPTooManyError("getTwitterAPI", apiUrl, reqResponse)
    else:
        raise HTTPError("getTwitterAPI", apiUrl, reqResponse)

def getTwitterToken():
    apiUrl = "https://api.twitter.com/oauth2/token"
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
    elif reqResponse.status_code == requests.codes.too_many:
        raise HTTPTooManyError("getTwitterAPI", apiUrl, reqResponse)
    else:
        raise HTTPError("getTwitterAPI", apiUrl, reqResponse)

def requestAPI(endpoint, endParams):
    jsonFileName = hashlib.md5(("%s%s" % (endpoint, endParams)).encode('utf-8')).hexdigest()
    jsonFile = Path("./cache/twitter/%s.json" % (jsonFileName))
    jsonContent = None
    if jsonFile.is_file():
        jsonContent = jsonFile.read_text(encoding='utf-8')
        jsonContent = json.loads(jsonContent)
    else:
        twitterToken = getTwitterToken()
        jsonContent = getTwitterAPI(endpoint, endParams, twitterToken)
        jsonFile.write_text(json.dumps(jsonContent), encoding='utf-8')
    return jsonContent
