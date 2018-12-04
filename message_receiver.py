""" Rule Parse """
import os
import json
import sys
from action_request import ActionRequest

class MessageReceiver:
    def __init__(self, reddit):
        self.reddit = reddit
        self.get_messages()

    def get_messages(self):
        for msg in self.reddit.inbox.unread():
            self.process_message(msg)

    def process_message(self, msg):
        request = msg.subject.encode('utf-8')
        ActionRequest(request, msg, self.reddit)
