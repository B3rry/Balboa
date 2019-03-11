import os
import json
import sys
import praw
import re
import calendar
from time import gmtime, strftime
from rule_parse import Rules

class UpdateFlairWithRulesByUser:

    def __init__(self, payload, reddit):
        self.status = {
            'response': 0,
            'subject': 'Error: Flair not set',
            'message': 'An error has occured. Please contact your moderator.'
        }
        author = str(payload.author)
        content = str(payload.body)
        current_class = None
        new_class = ''
        target_sub = os.environ.get("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)

        for user in subreddit.flair.__call__(redditor=author):
            current_class = user['flair_css_class']

        ruleset = Rules(reddit).findRuleset
        ruleset = ruleset[content]
        process_rules = Rules(reddit).currentRules
        process_rules = process_rules[ruleset]

        for index, rule in enumerate(process_rules['set']['class']):
            will_apply_rule = True
            if 'limit' in rule:
                if 'available' in rule['limit']:
                    if calendar.timegm(gmtime()) < rule['limit']['available']:
                        will_apply_rule = False
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
                        new_class = new_class + result.group(0)

        subreddit.flair.set(author, content, new_class)

        self.status['response'] = 200
        self.status['subject'] = 'Flair Changed'
        self.status['message'] = author + ', your flair on /r/' + os.environ.get("SUBREDDIT") + ' has been updated to: ' + content + '. This bot is in beta. Not seeing your flair update? Please contact your moderator.'


    @property
    def complete(self):
        return self.status
