import os
import json
import sys
import praw
import re
import calendar
from time import gmtime, strftime

class ModeratorRelationship:

    def __init__(self, payload, reddit):
        userToCheck = str(payload.author)
        self.status = {
            'statusCode': 200,
            'subject': 'Moderator Relationship',
            'message': str(userToCheck)
        }

        target_sub = os.environ.get("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)
        callModeratorList = subreddit.moderator.__call__(redditor=userToCheck)
        self.is_moderator = userToCheck in callModeratorList

        self.status = {
            'statusCode': 200,
            'subject': 'Moderator Relationship',
            'message': '/u/' + str(userToCheck) + ' returned ' + str(self.is_moderator)
        }
        

    @property
    def isModerator(self):
        # print('isModerator')
        # print(self.isModerator)
        # sys.stdout.flush()
        return self.is_moderator

    @property
    def complete(self):
        # print('completed')
        # sys.stdout.flush()
        return self.status
