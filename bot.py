import os
import sys
import time
import datetime
import praw
from actions.reddit.flair.rule_parse import Rules
from actions.reddit.configuration.get_permissions import Permissions
from messages.message_receiver import MessageReceiver

class Bot:

    logging = None
    conf = None
    reddit = None
    flairs = {}

    def __init__(self):
        # Initializtion.
        if os.getenv("LOGGING"):
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.logging = False

        print('')
        print('Bot: Starting /u/' + os.getenv("USERNAME") + ' for subreddit /r/' + os.getenv("SUBREDDIT"))
        sys.stdout.flush()

        self.login()
    def login(self):
        print('* Authenticating /u/' + os.getenv("USERNAME") + ' on reddit.com')
        sys.stdout.flush()

        app_id = os.getenv("APP_ID")
        app_secret = os.getenv("APP_SECRET")
        user_agent = "Flair Updater for /r/" + os.getenv("SUBREDDIT")

        username = os.getenv("USERNAME")
        password = os.getenv("USER_PASSWORD")

        try:
            print('  * Signing in...')
            sys.stdout.flush()
            self.reddit = praw.Reddit(client_id=app_id,\
                            client_secret=app_secret,\
                            username=username,\
                            password=password,\
                            user_agent=user_agent)
        except Exception as e:
            print('  * Failed to authenticate: ' + str(e))
            sys.stdout.flush()
        else:
            print('* Authenticated /u/' + os.getenv("USERNAME") + ' on reddit.com')
            sys.stdout.flush()
            self.run()

        # print('* Authenticated /u/' + os.getenv("USERNAME") + ' on reddit.com')
        # self.run()

    def run(self):
        print('Bot: Started /u/' + os.getenv("USERNAME") + ' at ' + str(datetime.datetime.now()))
        print('')
        sys.stdout.flush()
        # Get the initial set of rules. This should probaby be split out into a separate initilization lifecycle script.

        print('Bot: Initializing /u/' + os.getenv("USERNAME") + ' for subreddit /r/' + os.getenv("SUBREDDIT"))
        sys.stdout.flush()
        currentPermissions = Permissions(self.reddit).currentPermissions
        currentRules = Rules(self.reddit).currentRules

        print('Bot: /u/' + os.getenv("USERNAME") + ' successfully initialized at ' + str(datetime.datetime.now()))
        sys.stdout.flush()
        
        # Starts running the bot...
        running = True

        print('')
        print('Bot: /u/' + os.getenv("USERNAME") + " running from " + str(datetime.datetime.now()))
        sys.stdout.flush()
        while running:
            try:
                MessageReceiver(self.reddit)
                time.sleep(int(os.getenv("REFRESH_INTERVAL")))
            except Exception as e:
                time.sleep(int(os.getenv("REFRESH_INTERVAL")))
        return 0
