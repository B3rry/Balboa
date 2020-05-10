""" Rule Parse """
import os
import json
import sys

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
    def __init__(self, payload, response, reddit):
        self.payload = payload
        self.response = response
        self.reddit = reddit

        print('responding')
        sys.stdout.flush()

        if response['statusCode'] == 200:
            reddit.redditor(str(payload.author)).message(response['subject'], response['message'])
            payload.mark_read()
        elif response['statusCode'] == 204:
            payload.mark_read()
        elif response['statusCode'] == 400:
            reddit.redditor('/r/' + os.getenv("SUBREDDIT")).message(response['subject'], response['message'])
            payload.mark_read()
        else: 
            payload.mark_read()