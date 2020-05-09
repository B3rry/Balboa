import os
import json
import sys
import praw

class UpdateFlairTextByUser:

    def __init__(self, payload, reddit):
        self.status = {
            'statusCode': 0,
            'subject': 'Error: Flair not set',
            'message': 'An error has occured. Please contact your moderator.'
        }
        author = str(payload.author)
        content = str(payload.body)
        current_class = None
        target_sub = os.getenv("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)

        for user in subreddit.flair.__call__(redditor=author):
            current_class = user['flair_css_class']

        subreddit.flair.set(author, content, current_class)

        self.status['statusCode'] = 200
        self.status['subject'] = 'Flair Changed'
        self.status['message'] = author + ', your flair on /r/' + os.getenv("SUBREDDIT") + ' has been updated to: ' + content + '. This bot is in beta. Not seeing your flair update? Please contact your moderator.'


    @property
    def complete(self):
        return self.status
