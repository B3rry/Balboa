""" Rule Parse """
import os
import json
import sys
from actions.action_request import ActionRequest
from .recievers.reddit_message_receiver import RedditMessageReceiver
from .recievers.slack_message_receiver import SlackMessageReceiver

# ============= Message Receiver .py ============= #
# Currently, Message Receiver handles the retrieval of messages from the inbox
# of the bot's Reddit account using PRAW. We treat _all_ incoming requests that
# could potentially trigger an action as a "message." Right now, each individual
# "reciever" handles the dispatching of its own action requests. This should be
# a workflow of standardization and "pass-along" to the `ActionRequest` process.
# Note that `ActionRequest` should define the protocol for handling messages as
# it relates to determination of action, autorization and negotiated response…
# this work should only facilitate that handoff.
#
# The long term vision for this code is to handle the management of all incoming
# data. This solution will need to:
# [ ] Handle incoming messages sent via the Slack API by way of the flask
#     > Do we achieve this by just instantiating the flask API under its reciever?
# [ ] Handle frequent, repeated requests to the Reddit API to check for messages
# [ ] Exist, or augment the current `bot.py` loop model. *Big implications*
#
# [TODO]: Standardize the handling of various messaging integrations within this dir. Treat message-receiver as the way to initiate a dispatch.

class MessageReceiver:
    def __init__(self, reddit):
        # this should run through present protocols, look for presence and check for messages
        self.reddit = reddit
        self.check_service("reddit")

    def check_service(self, protocol):
        if protocol == "reddit":
            RedditMessageReceiver(self.reddit)
        if protocol == "slack":
            SlackMessageReceiver(self.reddit)
