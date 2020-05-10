""" Rule Parse """
import os
import json
import sys
from messages.dispatchers.reddit_message_dispatcher import RedditMessageDispatcher
from messages.dispatchers.slack_message_dispatcher import SlackMessageDispatcher


# ============= Message Dispatcher .py ============= #
# Currently, Message Dispatcher handles the sending of responses to messages sent
# to the bot's Reddit account using PRAW.
#
# The long term vision for this code is to handle the sending of all outgoing
# messages. This solution will need to:
# [ ] Standardize the data model for the definition of distribution with enough flexibility to support abstract response types 
#     [ ]: Reddit compose new message
#     [ ]: Reddit reply to existing message
#     [ ]: Reddit send modmail
#     [ ]: Slack reply in channel
#     [ ]: Slack reply in dm
#     [ ]: Slack set channel status
# [ ] Manage the distribution of messages to varous response processes.
#
# [TODO]: Standardize the handling of various messaging integrations within this dir. Treat message-dispatcher as the way to route to a response type.
# [TODO]: Templating!
# [TODO]: Dynamic composure of messages, (headers, footers for different types, etc)

class MessageDispatcher:
    def __init__(self, protocol, response, payload, reddit):
        self.protocol = protocol
        self.payload = payload
        self.response = response
        self.reddit = reddit

        print('responding via ' + protocol)
        sys.stdout.flush()

        if protocol == 'reddit':
            RedditMessageDispatcher(response=response, payload=payload, reddit=reddit)
        elif protocol == 'slack':
            SlackMessageDispatcher(response=response, payload=payload)
