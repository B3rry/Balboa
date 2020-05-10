""" Rule Parse """
import os
import json
import sys
from actions.action_request import ActionRequest

# ============= Slack Message Receiver .py ============= #
# Currently, this is an exact copy of the reddit message reciever.
#
# The long term vision for this code is to
# [ ] 
#
# [TODO]: 

class SlackMessageReceiver:
    def __init__(self, reddit):
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
