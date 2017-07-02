import requests
import json
import constants

def sendToSlack(data):
    r = requests.post(constants.SLACK_WEBHOOK, headers=constants.JSON_CONTENT, data=json.dumps(data));
    print r.text
