import os
import sys
import time
import datetime
import praw
import flair_bot
from rule_parse import Rules
from message_receiver import MessageReceiver

class Bot:

    subject = None
    logging = None
    conf = None
    reddit = None
    flairs = {}

    def __init__(self):
        if os.environ.get("LOGGING"):
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.logging = False

        print ''
        print 'Initializing Bot : /u/' + os.environ.get("USERNAME") + ' for subreddit /r/' + os.environ.get("SUBREDDIT")
        sys.stdout.flush()

        self.login()
    def login(self):
        """ Log in via script/web app. """

        app_id = os.environ.get("APP_ID")
        app_secret = os.environ.get("APP_SECRET")
        user_agent = "Flair Updater for /r/" + os.environ.get("SUBREDDIT")

        username = os.environ.get("USERNAME")
        password = os.environ.get("USER_PASSWORD")
        self.reddit = praw.Reddit(client_id=app_id,\
                        client_secret=app_secret,\
                        username=username,\
                        password=password,\
                        user_agent=user_agent)
        self.run()

    def run(self):
        print ''
        print 'Bot: /u/' + os.environ.get("USERNAME") + 'has started. Initialized at: ' + str(datetime.datetime.now())
        sys.stdout.flush()
        # self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT") ).message('Bot: /u/' + os.environ.get("USERNAME") + 'has started', 'Initialized at: ' + str(datetime.datetime.now()))
        # GET RULES
        currentRules = Rules(self.reddit).currentRules
        
        # RUN LISTENER
        running = True
        while running:
            try:
                MessageReceiver(self.reddit)
                time.sleep(int(os.environ.get("REFRESH_INTERVAL")))
            except Exception as e:
                time.sleep(int(os.environ.get("REFRESH_INTERVAL")))
        return 0