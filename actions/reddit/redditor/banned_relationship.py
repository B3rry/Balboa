import os
import json
import sys
import praw
import re
import calendar
from time import gmtime, strftime

class BannedRelationship:

    def __init__(self, payload, reddit):
        userToCheck = str(payload.author)
        self.status = {
            'statusCode': 200,
            'subject': 'Banned Relationship',
            'message': str(userToCheck)
        }

        target_sub = os.getenv("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)
        callBannedList = subreddit.banned.__call__(redditor=userToCheck)
        self.is_banned = userToCheck in callBannedList

        self.status = {
            'statusCode': 200,
            'subject': 'Banned Relationship',
            'message': '/u/' + str(userToCheck) + ' returned ' + str(self.is_banned)
        }
        

    @property
    def isBanned(self):
        return self.is_banned

    @property
    def complete(self):
        return self.status
