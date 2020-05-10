""" Rule Parse """
import os
import json
import sys
from actions.action_request import ActionRequest

# ============= Reddit Message Receiver .py ============= #
# Currently, 
#
# The long term vision for this code is to
# [ ] 
#
# [TODO]: 

class RedditMessageReceiver:
    def __init__(self, reddit):
        self.reddit = reddit
        self.get_messages()

    def get_messages(self):
        # Iterate through processing all inboxed messages.
        for msg in self.reddit.inbox.unread():
            self.process_message(msg)

    def process_message(self, msg):
        # Sanitize inbound request
        request = msg.subject.encode('utf-8')
        # Request Action
        ActionRequest(request, msg, self.reddit)
