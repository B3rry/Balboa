import os
import json
import sys
import praw
import re
import calendar
from time import gmtime, strftime
from .rule_parse import Rules

class UpdateFlairWithRules:

    def __init__(self, payload, reddit):
        author = str(payload.author)
        content = str(payload.body)
        print("CONTENT IS:")
        print(content)
        print("CONTENT ********")
        sys.stdout.flush()
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
        target_sub = os.getenv("SUBREDDIT")
        subreddit = reddit.subreddit(target_sub)

        # retrieve the current CSS class for the user's flair, otherwise set thier current css class to an empty string.
        for user in subreddit.flair.__call__(redditor=author):
            current_class = user['flair_css_class']
            if current_class == None:
                current_class = ''
            # todo: figure out why this is here.... it looks to set rules, but idk why it's in this "if" statement
            ruleset = Rules(reddit).findRuleset

        try:
            rulesetIndex = ruleset[content]
        except KeyError:
            ruleset = False
            self.status['statusCode'] = 200
            self.status['subject'] = 'Invalid Flair for /r/' + os.getenv("SUBREDDIT")
            self.status['message'] = '/u/' +  author + ',\n\nThe flair you requested ("' + content + '") is not valid. Please try again.\n\nPlease go to the [list of available flairs](https://www.reddit.com/r/survivor/wiki/available_flairs) and follow the instructions provided.\n\nIf you continue to experience errors, please [message the /r/' + os.getenv("SUBREDDIT") + '  moderators](https://www.reddit.com/message/compose/?to=/r/Survivor&subject=Help%20with%20flair) for help.'
        except Exception as e:
            print('exception: ' + str(e))
            sys.stdout.flush()
        else:
            print('Valid ruleset found for requested flair: ' + str(rulesetIndex))
            sys.stdout.flush()
            process_rules = Rules(reddit).currentRules
            process_rules = process_rules[rulesetIndex]

            print('process rules by ruleset: ' + str(process_rules))
            sys.stdout.flush()

            for index, rule in enumerate(process_rules['set']['class']):
                # enumerate through each class element to conditionally apply logic to the construction of a new css class
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
                # When rule is eligible, apply it via the method speified as the "type"
                if will_apply_rule:
                    if rule['type'] == 'string':
                        new_class = new_class + str(rule['content'])
                    elif rule['type'] == 'regex':
                        print("applying regex rule")
                        sys.stdout.flush()
                        # TODO: seems to be failing somewhere in here, probably due to python 3 encdoing shit
                        regex = rule['content'].encode('ascii', 'ignore')
                        decodedRegex = regex.decode('ascii')
                        result = re.search(decodedRegex, current_class)
                        if result is None:
                            new_class = new_class
                        else:
                            new_class = new_class + result.group(1)
            try:
                subreddit.flair.set(author, content, new_class)
            except:
                self.status['statusCode'] = 200
                self.status['subject'] = 'An Error Occurred'
                self.status['message'] = author + ', your requested flair of "' + content + '" on /r/' + os.getenv("SUBREDDIT") + ' is not valid. This bot is in beta. Is this an error? Please contact your moderator.'
            else:
                self.status['statusCode'] = 200
                self.status['subject'] = '/r/' + os.getenv("SUBREDDIT") + ' Flair Updated'
                self.status['message'] = '/u/' +  author + ',\n\nYour flair has been updated to "' + content + '".\n\nIf your updated flair is incorrect, [message the /r/' + os.getenv("SUBREDDIT") + '  moderators](https://www.reddit.com/message/compose/?to=/r/Survivor&subject=Help%20with%20flair) for help.'


    @property
    def complete(self):
        return self.status
