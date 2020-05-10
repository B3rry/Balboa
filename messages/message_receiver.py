""" Rule Parse """
import os
import json
import sys
from actions.action_request import ActionRequest

# ============= Message Receiver .py ============= #
# Currently, Message Receiver handles the retrieval of messages from the inbox
# of the bot's Reddit account using PRAW.
#
# The long term vision for this code is to handle the management of all incoming
# data. This solution will need to:
# [ ] Handle incoming messages sent via the Slack API by way of the flask
# [ ] Handle frequent, repeated requests to the Reddit API to check for messages
# [ ] Exist, or augment the current `bot.py` loop model. *Big implications*
#
# [TODO]: Standardize the handling of various messaging integrations within this dir. Treat message-receiver as the way to initiate a dispatch.

class MessageReceiver:
    def __init__(self, reddit):
        # passing a param and conditionally loads the data is maybe how we'd want do this. (+ a dict of service info?)
        self.reddit = reddit
        self.get_messages()

    def get_messages(self):
        # get all messages, and pocess each one in order
        for msg in self.reddit.inbox.unread():
            # interpret inboud traffic
            self.process_message(msg)

    def process_message(self, msg):
        # ensures message is properly encoded, as emoji and non utf characters will cause issues with the bot's ability to request actions
        request = msg.subject.encode('utf-8')
        ActionRequest(request, msg, self.reddit)
