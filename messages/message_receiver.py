""" Rule Parse """
import os
import json
import sys
from actions.action_request import ActionRequest

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
