import os
import sys
import csv
import urllib
import praw

class BulkUpdateFromCSV:

    def __init__(self, payload, reddit):
        self.status = {
            'statusCode': 0,
            'subject': 'Error: Flair not set',
            'message': 'An error has occured. Please contact your moderator.'
        }

        remoteURL = str(payload.body)

        target_sub = os.getenv("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)

        flair_dicts = []

        keys = ['user', 'flair_text', 'flair_css_class']
        print('starting bulk update')
        sys.stdout.flush()
        remoteFile = urllib.urlretrieve(remoteURL)
        # fileData = remoteFile.read()

        print(remoteFile[0])
        sys.stdout.flush()

        try:
            with open(remoteFile[0]) as file:
                reader = csv.reader(file)
                for row in reader:
                    flair_dicts.append(dict(zip(keys, row)))
        except Exception as e:
            print(e)
            sys.stdout.flush()

        print(flair_dicts)
        sys.stdout.flush()
        subreddit.flair.update(flair_dicts)


        self.status['statusCode'] = 200
        self.status['subject'] = 'Flair Changed'
        self.status['message'] = 'Batch process complete.'


    @property
    def complete(self):
        return self.status
