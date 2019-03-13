""" Rule Parse """
import os
import json
import sys

class Rules:

    def __init__(self, reddit):
        self.status = {
            'statusCode': 204,
            'subject': 'No Content',
            'message': 'No Content'
        }
        self.theseRules = None 
        self.rulesDirectory = {}
        self.reddit = reddit

        self.get_rules()

    def get_rules(self):
        try:
            path = os.environ.get("USERNAME") + '/rules'

            print "* Updating rulesets"
            print "  * Looking for ruleset at reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + path + "..."
            sys.stdout.flush()
            
            ruledef = self.reddit.subreddit(os.environ.get("SUBREDDIT")).wiki[path].content_md
        except Exception as e:
            self.status = {
                'statusCode': 400,
                'subject': 'Error: Flair Rules Not Found',
                'message': "Ruleset cannot be found. Confirm your ruleset is located at reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + path + " :"  + str(e)
            }
        else:
            self.parse_rules(ruledef)


    def parse_rules(self, ruledef):
        try:
            print "  * Loading ruleset..."
            sys.stdout.flush()

            ruledef = json.loads(ruledef)
        except Exception as e:
            self.status = {
                'statusCode': 400,
                'subject': 'Error: Flair Rules Not Loaded',
                'message': 'Ruleset not valid: ' + str(e)
            }
        else:
            self.store_rules(ruledef)

    def store_rules(self, ruledef):
        try:
            print "  * Storing ruleset..."
            sys.stdout.flush()

            json.dump(ruledef, open("rules.json", 'w'))
        except Exception as e:
            self.status = {
                'statusCode': 400,
                'subject': 'Error: Flair Rules Not Saved',
                'message': 'Ruleset cannot be saved: ' + str(e)
            }
        else:
            self.process_rules()

    def process_rules(self):
        print "  * Applying ruleset..."
        sys.stdout.flush()

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
                self.status = {
                    'statusCode': 400,
                    'subject': 'Error: Flair Rules Not Loaded',
                    'message': 'The following ruleset could not be loaded: ' + str(e)
                }
            else:
                print "* Rulesets " + ', '.join(loaded) + " now active"
                sys.stdout.flush()
                self.status = {
                    'statusCode': 400,
                    'subject': 'Success: New Rules Loaded',
                    'message': 'Enabled the following rulesets: ' + ', '.join(loaded)
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
