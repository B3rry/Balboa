import os
import sys
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
from actions.action_request import ActionRequest

# ============= Slack Message Receiver .py ============= #
# Currently, this is an exact copy of the reddit message reciever.
#
# The long term vision for this code is to
# [ ] 
#
# [TODO]: 
class SlackMessageReceiver:
    if os.getenv("SLACK_SIGNING_SECRET") is None:
        from os.path import join, dirname
        from dotenv import load_dotenv

        load_dotenv()
    
    app = Flask(__name__)
    slack_events_adapter = SlackEventAdapter(os.getenv("SLACK_SIGNING_SECRET"), "/slack/events", app)

    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
        self.app.run(port=3000)

    # pylint: disable=no-self-argument, no-member
    @slack_events_adapter.on("message")
    def message(payload):
        event = payload.get("event", {})
        channel_id = event.get("channel")
        user_id = event.get("user")
        print(payload)
        print(event)
        print(event['text'])
        print(channel_id)
        print(user_id)
        sys.stdout.flush()
    # pylint: enable=no-self-argument, no-member
