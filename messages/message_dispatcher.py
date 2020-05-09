""" Rule Parse """
import os
import json
import sys

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