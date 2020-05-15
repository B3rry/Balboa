import os
import sys
import random
from slack import WebClient
from slack.errors import SlackApiError

class CreateChannel:
    if os.getenv("SLACK_SIGNING_SECRET") is None:
        from os.path import join, dirname
        from dotenv import load_dotenv

        load_dotenv()

    # Initialize a Web API client
    # slack_web_client = WebClient(os.getenv("SLACK_BOT_TOKEN"))
    slack_web_client = WebClient(os.getenv("SLACK_OAUTH_ACCESS_TOKEN"))

    def __init__(self, payload):
        self.status = {
            'statusCode': 0,
            'subject': 'Make tribe action',
            'message': ''
        }

        channel_name = str("tribe" + str(random.randint(0, 1000)))
        # run through the operations here
        try:
            response = self.slack_web_client.conversations_create(name=channel_name)
            self.status['statusCode'] = 200
            self.status['subject'] = 'Ok. #' + channel_name + ' was created.'
            print("response is")
            print(str(response))
            sys.stdout.flush()
        # pylint: disable=catching-non-exception
        except Exception as e:
        # pylint: enable=catching-non-exception
            print(e)
            sys.stdout.flush()
            self.status['statusCode'] = 200
            self.status['subject'] = str(e)

    @property
    def complete(self):
        return self.status
