import requests
import json
import constants

urlParams = {
    'APIkey': constants.API_KEY
}

def queryAPI(action, params):
    urlParams['action'] = action
    for key in params:
        urlParams[key] = params[key]
    return requests.get(constants.API_URL, params=urlParams);
