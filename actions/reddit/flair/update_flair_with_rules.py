import os
import json
import sys
import praw
import re
import calendar
from time import gmtime, strftime
from rule_parse import Rules

class UpdateFlairWithRules:

    def __init__(self, payload, reddit):
        author = str(payload.author)
        content = str(payload.body)
        # Set a default status to be overwritten
        self.status = {
            'statusCode': 0,
            'subject': 'Flair not set',
            'message': 'An error has occured. Please contact your moderator.',
            'notify': {
                'user': author,
                'log': True,
                'notifyUser': True,
                'notifyModerators': False
            }
        }
        current_class = ''
        new_class = ''
        target_sub = os.environ.get("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)

        for user in subreddit.flair.__call__(redditor=author):
            current_class = user['flair_css_class']
            if current_class == None:
                current_class = ''
            ruleset = Rules(reddit).findRuleset
        try:
            ruleset = ruleset[content]
        except KeyError:
            ruleset = False
            self.status['statusCode'] = 200
            self.status['subject'] = 'Invalid Flair for /r/' + os.environ.get("SUBREDDIT")
            self.status['message'] = '/u/' +  author + ',\n\nThe flair you requested ("' + content + '") is not valid. Please try again.\n\nPlease go to the [list of available flairs](https://www.reddit.com/r/survivor/wiki/available_flairs) and follow the instructions provided.\n\nIf you continue to experience errors, please [message the /r/' + os.environ.get("SUBREDDIT") + '  moderators](https://www.reddit.com/message/compose/?to=/r/Survivor&subject=Help%20with%20flair) for help.'
        else:
            process_rules = Rules(reddit).currentRules
            process_rules = process_rules[ruleset]

            for index, rule in enumerate(process_rules['set']['class']):
                will_apply_rule = True
                # Check to see if time on rule is valid
                if 'limit' in rule:
                    # Checks to see if rule has begun availability window
                    if 'available' in rule['limit']:
                        if calendar.timegm(gmtime()) < rule['limit']['available']:
                            will_apply_rule = False
                    # Checks to see if rule has passed availability window
                    if 'expires' in rule['limit']:
                        if calendar.timegm(gmtime()) >= rule['limit']['expires']:
                            will_apply_rule = False

                if will_apply_rule:
                    if rule['type'] == 'string':
                        new_class = new_class + str(rule['content'])
                    elif rule['type'] == 'regex':
                        regex = rule['content'].encode('ascii', 'ignore')
                        result = re.search(regex, current_class)
                        if result is None:
                            new_class = new_class
                        else:
                            new_class = new_class + result.group(1)
            try:
                subreddit.flair.set(author, content, new_class)
            except:
                self.status['statusCode'] = 200
                self.status['subject'] = 'An Error Occurred'
                self.status['message'] = author + ', your requested flair of "' + content + '" on /r/' + os.environ.get("SUBREDDIT") + ' is not valid. This bot is in beta. Is this an error? Please contact your moderator.'
            else:
                self.status['statusCode'] = 200
                self.status['subject'] = '/r/' + os.environ.get("SUBREDDIT") + ' Flair Updated'
                self.status['message'] = '/u/' +  author + ',\n\nYour flair has been updated to "' + content + '".\n\nIf your updated flair is incorrect, [message the /r/' + os.environ.get("SUBREDDIT") + '  moderators](https://www.reddit.com/message/compose/?to=/r/Survivor&subject=Help%20with%20flair) for help.'


    @property
    def complete(self):
        return self.status
