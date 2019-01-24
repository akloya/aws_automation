
import json
import requests

webhook = "https://hooks.slack.com/services/xxxxxxxxxxxxxxxxxxxxxxxxx"

def send_slack_message(color, pretext, title, message):
    payload = {
        "attachments": [
            {
                "color": color,
                "pretext": pretext,
                "title": title,
                "text": message,
                "footer": "AWS AUTOMATION ALERTS"
            }
        ]
    }
    requests.post(webhook,
                  json.dumps(payload),
                  headers={'content-type': 'application/json'})
