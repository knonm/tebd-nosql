import requests
import requests.auth
import hashlib
import json
from pathlib import Path

def getRedditAPI(endpoint, endParams, redditToken):
    if endParams is not None and len(endParams) > 0:
        apiUrl = "https://oauth.reddit.com/%s.json?%s" % (endpoint, endParams)
    else:
        apiUrl = "https://oauth.reddit.com/%s.json" % (endpoint)
    
    reqResponse = requests.get(apiUrl,
        headers =
        {"user-agent":"python:br.usp.tebd:v0.1",
         "accept":"application/json",
         "authorization":"bearer %s" % (redditToken),
         "accept-encoding":"UTF-8"})
    
    if reqResponse.status_code == requests.codes.ok:
        return reqResponse.json()
    else:
        print("getRedditAPI\nError code (%s):\n\n%s\n\n%s\n" % (reqResponse.status_code, reqResponse.headers, reqResponse.text))
        return None

def getRedditToken():
    apiUrl = "https://www.reddit.com/api/v1/access_token"
    apiKey = "API_KEY"
    apiSecret = "API_SECRET"
    clientAuth = requests.auth.HTTPBasicAuth(apiKey, apiSecret)
    reqResponse = requests.post(apiUrl, auth = clientAuth, data = "grant_type=client_credentials",
        headers =
        {"user-agent":"python:br.usp.tebd:v0.1",
         "accept":"application/json",
         "accept-encoding":"UTF-8"})
    
    if reqResponse.status_code == requests.codes.ok:
        return reqResponse.json()["access_token"]
    else:
        print("getRedditToken\nError code (%s):\n\n%s\n\n%s\n" % (reqResponse.status_code, reqResponse.headers, reqResponse.text))
        return None

def requestRedditAPI(endpoint, endParams):
    jsonFileName = hashlib.md5(("%s%s" % (endpoint, endParams)).encode('utf-8')).hexdigest()
    jsonFile = Path("./cache/reddit/%s.json" % (jsonFileName))
    jsonContent = None
    if jsonFile.is_file():
        jsonContent = jsonFile.read_text(encoding='utf-8')
        jsonContent = json.loads(jsonContent)
    else:
        redditToken = getRedditToken()
        if redditToken is not None:
            jsonContent = getRedditAPI(endpoint, endParams, redditToken)
            if jsonContent is not None:
                jsonFile.write_text(json.dumps(jsonContent), encoding='utf-8')
    return jsonContent
