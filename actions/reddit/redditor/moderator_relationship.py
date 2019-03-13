import os
import json
import sys
import praw
import re
import calendar
from time import gmtime, strftime

class ModeratorRelationship:

    def __init__(self, payload, reddit):
        author = str(payload.author)
        # content = str(payload.body)
        # Set a default status to be overwritten
        self.status = {
            'statusCode': 200,
            'subject': 'Flair not set',
            'message': 'An error has occured. Please contact your moderator.',
            'notify': {
                'user': author,
                'log': True,
                'notifyUser': True,
                'notifyModerators': False
            }
        }
        target_sub = os.environ.get("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)
        moderators = subreddit.moderator()

        print(moderators)
        sys.stdout.flush()

    @property
    def complete(self):
        return self.status
