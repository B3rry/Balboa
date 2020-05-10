""" Rule Parse """
import os
import sys
from slack import WebClient
from slack.errors import SlackApiError

# ============= Slack Message Dispatcher .py ============= #
class SlackMessageDispatcher:
    if os.getenv("SLACK_SIGNING_SECRET") is None:
        from os.path import join, dirname
        from dotenv import load_dotenv

        load_dotenv()

    # Initialize a Web API client
    slack_web_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

    def __init__(self, response, payload):
        print("response is")
        print(str(response))
        sys.stdout.flush()
        try:
            response = self.slack_web_client.chat_postMessage(
                channel=payload['channel'],
                text=response['subject']
            )
        except SlackMessageDispatcher as e:
            print(e)
            sys.stdout.flush()
