import os
import sys
import csv
import praw

class BulkUpdateFromCSV:

    def __init__(self, reddit):
        self.status = {
            'statusCode': 0,
            'subject': 'Error: Flair not set',
            'message': 'An error has occured. Please contact your moderator.'
        }

        target_sub = os.environ.get("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)

        flair_dicts = []

        keys = ['user', 'flair_text', 'flair_css_class']

        with open('bulk_update_flairs.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                flair_dicts.append(dict(zip(keys, row)))

        subreddit.flair.update(flair_dicts)


        self.status['statusCode'] = 200
        self.status['subject'] = 'Flair Changed'
        self.status['message'] = 'Batch process complete.'


    @property
    def complete(self):
        return self.status
