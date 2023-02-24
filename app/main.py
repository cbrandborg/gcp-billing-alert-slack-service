import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request

from helper_functions import *

# Token used by the Slack Bot
SLACK_TOKEN = os.environ['SLACK_TOKEN']

# ID of the channel you want to send the message to
CHANNEL_ID = os.environ['CHANNEL_ID']

client = WebClient(token=SLACK_TOKEN)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    
    # Parsing request as object
    envelope = request.get_json()

    verify_request(envelope)

    # Creating dictionary containing pubsub message
    print(envelope)
    pubsub_message = envelope["message"]

    print(pubsub_message)

    notification_attr, notification_data = parse_message_content(pubsub_message)

    if not ('alertThresholdExceeded' in notification_data) and not ('forecastThresholdExceeded' in notification_data):
        
        return ("No threshold exceeded - Slack channel not notified.", 204)

    print('gets past this one fucker')

    slack_blocks = format_blocks(pubsub_message, notification_attr, notification_data)

    print(slack_blocks)

    try:
        print('Try statement entered')

        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            text="A request was received, but it did not send correctly - Consult logs.",
            blocks=slack_blocks

        )

        print(response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"] 


    return ("Threshold exceeded - Slack channel has been alerted.", 204)
