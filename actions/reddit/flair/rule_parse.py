""" Rule Parse """
import os
import json
import sys

class Rules:

    def __init__(self, reddit):
        self.status = {
            'response': 400,
            'subject': 'Error: Rules not parsed',
            'message': 'An error has occured. Please contact your moderator.'
        }
        self.theseRules = None 
        self.rulesDirectory = {}
        self.reddit = reddit

        self.get_rules()

    def get_rules(self):
        try:
            path = os.environ.get("USERNAME") + '/rules'
            ruledef = self.reddit.subreddit(os.environ.get("SUBREDDIT")).wiki[path].content_md
        except Exception as e:
            self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Ruleset cannot be found. Confirm your ruleset is located at 'reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + os.environ.get("USERNAME") + "/rules':"  + str(e))
        else:
            self.parse_rules(ruledef)


    def parse_rules(self, ruledef):
        try:
            ruledef = json.loads(ruledef)
        except Exception as e:
            self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Ruleset cannot be read. Confirm your ruleset is valid JSON:" + str(e))
        else:
            self.store_rules(ruledef)

    def store_rules(self, ruledef):
        try:
            json.dump(ruledef, open("rules.json", 'w'))
        except Exception as e:
            self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Rulset cannot be saved:" + str(e))
        else:
            self.process_rules()

    def process_rules(self):
        with open('rules.json') as botconfig:
            self.theseRules = json.load(botconfig)['rules']
            loaded = []
            try:
                for index, rule in enumerate(self.theseRules):
                    ruleset = self.theseRules[index]['set']
                    ruletext = ruleset['text']

                    loaded.append(self.theseRules[index]['set']['setname'])

                    for option in ruletext:
                        self.rulesDirectory[option] = index

            except Exception as e:
                self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Rulset cannot be processed:" + str(e))
            else:
                self.status = {
                    'response': 200,
                    'subject': 'Success: New Rules Loaded',
                    'message': 'Loaded the following rulesets: ' + ', '.join(loaded)
                }

    @property
    def currentRules(self):
        return self.theseRules

    @property
    def updateRules(self):
        self.get_rules()
        return self.status

    @property
    def findRuleset(self):
        self.process_rules()
        return self.rulesDirectory
