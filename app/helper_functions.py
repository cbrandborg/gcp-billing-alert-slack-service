import base64
import json
from datetime import datetime


# If empty, no data is received, respond with 400
def verify_request(envelope):
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    # If not in dict format or does not contain message key, respond with 400
    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    return envelope


# If in dictionary format, check if it contains attributes and data, store values, otherwise catch key errors
def parse_message_content(message):

    if isinstance(message, dict):
        try:
            notification_attr = message['attributes']
            #notification_attr = {key.replace(' ', ''): value for key, value in notification_attr.items()}
        except KeyError:
            notification_attr = "No attributes passed in"
        #print(notification_attr)
        try:
            print(message["data"])
            notification_data = base64.b64decode(message["data"]).decode("utf-8").strip()
            print(f'After B64: {notification_data}')
            #print(f'After Replacement: {notification_data}')

            notification_data = json.loads(notification_data)

        except KeyError:
            notification_data = "No data passed in"
    
    return notification_attr, notification_data


def format_blocks(pubsub_message: dict, notification_attr: dict, notification_data: dict):

    alert_increase=round(float(notification_data['costAmount'])/float(notification_data['budgetAmount'])*100,2)

    alert_type = 'Unknown'

    if "alertThresholdExceeded" in notification_data.keys() and "forecastThresholdExceeded" in notification_data.keys():
        alert_type = "Actual and Forecast"
    elif "alertThresholdExceeded" in notification_data.keys():
        alert_type = "Actual"
        notification_data['forecastThresholdExceeded'] = 'N/A'
    elif "forecastThresholdExceeded" in notification_data.keys():
        alert_type = "Forecast"
        notification_data['alertThresholdExceeded'] = 'N/A'

    blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"New {alert_type} Billing Alert: {notification_attr['billingAccountId']}",
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "text": f"*{datetime.now().strftime('%B %d %Y ')}*  |  Billing Alert",
                        "type": "mrkdwn"
                    }
                ]
		    },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey everyone  :sunglasses:  \n At {format_str_date(pubsub_message['publishTime'])} I've noticed that <https://console.cloud.google.com/billing/{notification_attr['billingAccountId']}|{notification_attr['billingAccountId']}> has exceeded {str(alert_increase)}% of the current budget of {notification_data['budgetAmount']} counting from {format_str_date(notification_data['costIntervalStart'])}  :chart_with_upwards_trend:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Anyone @here who would like to assist me in determining the cause and notify the customer? \n The budget details can be seen below:",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Cost Amount:* {str(notification_data['costAmount'])}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Budget Amount:* {str(notification_data['budgetAmount'])}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Budget type:* {notification_data['budgetAmountType']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Alert threshold exceeded:* {str(notification_data['alertThresholdExceeded'])}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Forecast threshold exceeded:* {str(notification_data['forecastThresholdExceeded'])}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Currency code:* {notification_data['currencyCode']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Start of current cost interval:* {format_str_date(notification_data['costIntervalStart'])}",
                    },
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Issue handling status:"
                },
                "accessory": {
                    "type": "radio_buttons",
                    "initial_option": 
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Not resolved",
                                },
                                "value": "value-0"
                            },
                    "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Not resolved",
                                },
                                "value": "value-0"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Resolved",
                                },
                                "value": "value-1"
                            },
                        ],
                    "action_id": "radio_buttons-issue-handled"
			    }
            }
    ]

    blocks = str(blocks)

    return blocks

def format_str_date(date_string):

    # Parse the date string into a datetime object using ISO8601 format with timezone offset 
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Parse the date string into a datetime object using ISO8601 format without timezone offset
    except ValueError:
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")

    new_date_string = date_object.strftime("%B %d %Y %H:%M")

    return new_date_string
