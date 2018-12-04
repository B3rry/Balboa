""" Rule Parse """
import os
import json

class Rules:


    def __init__(self, reddit):
        self.theseRules = None
        self.reddit = reddit
        
        if os.path.isfile('rules.json') is False:
            self.get_rules()
        else:
            self.process_rules()

    def get_rules(self):
        """ Read flairs from CSV. """
        try:
            path = os.environ.get("USERNAME") + '/rules'
            ruledef = self.reddit.subreddit(os.environ.get("SUBREDDIT")).wiki[path].content_md
        except:
            self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Ruleset cannot be found. Confirm your ruleset is located at reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + os.environ.get("USERNAME") + '/rules')
        else:
            self.parse_rules(ruledef)


    def parse_rules(self, ruledef):
        try:
            ruledef = json.loads(ruledef)
        except:
            self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Ruleset cannot be read. Confirm your ruleset is valid JSON.")
        else:
            self.store_rules(ruledef)

    def store_rules(self, ruledef):
        try:
            json.dump(ruledef, open("rules.json", 'w'))
        except:
            self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Rulset cannot be saved. Contact your system administrator.")
        else:
            self.process_rules()

    def process_rules(self):
        with open('rules.json') as botconfig:
            rules = json.load(botconfig)['rules']
            loaded = []
            try:
                for index, rule in enumerate(rules):
                    loaded.append(rules[index]['set']['setname'])
            except:
                self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Error Loading Flair Rules', "ERROR - Ruleset is not valid.")
            else:
                self.reddit.redditor('/r/' + os.environ.get("SUBREDDIT")).message('Success Loading Flair Rules', 'Loaded the following rulesets: ' + ', '.join(loaded))
                self.theseRules = rules

    @property
    def currentRules(self):
        return self.theseRules
