import os
import sys 

from actions.system.ping import Ping
from actions.reddit.flair.update_flair_text import UpdateFlairText
from actions.reddit.flair.update_flair_text_by_user import UpdateFlairTextByUser
from actions.reddit.flair.update_flair_with_rules import UpdateFlairWithRules
from actions.reddit.flair.update_flair_with_rules_by_user import UpdateFlairWithRulesByUser
from actions.reddit.flair.bulk_update_from_csv import BulkUpdateFromCSV
from actions.reddit.flair.rule_parse import Rules
from actions.reddit.redditor.moderator_relationship import ModeratorRelationship
from actions.reddit.redditor.banned_relationship import BannedRelationship
from messages.message_dispatcher import MessageDispatcher

from actions.reddit.configuration.get_permissions import Permissions

class ActionDispatch:
    # ActionDispatch is triggered when action_request.py determines a request for action is valid.  This is where the bot will determine what to do when a user passes in a valid
    # command. Dispatch will determine if a user is authorized to tigger a command, and return a `status` object back to the MessageDispatcher.

    def __init__(self, requestIdentifier, payload, reddit):
        # `functionDispatch` (dict, string: `lambda:` function): defines a list of functions that can be preformed when the bot requests for an action to be preformed, as defined 
        # in action_request.py 
        functionDispatch = {
            'PINGPONG': lambda: Ping(payload).complete,
            'UPDATE_FLAIR_TEXT': lambda: UpdateFlairText(payload, reddit).complete,
            # 'UPDATE_FLAIR_TEXT_BY_USER': UpdateFlairTextByUser(payload, reddit).complete,
            'UPDATE_FLAIR_WITH_RULES': lambda: UpdateFlairWithRules(payload, reddit).complete,
            # 'UPDATE_FLAIR_WITH_RULES_BY_USER': UpdateFlairWithRulesByUser(payload, reddit).complete,
            'UPDATE_RULES': lambda: Rules(reddit).updateRules,
            'BULK_UPDATE_FLAIRS': lambda: BulkUpdateFromCSV(payload, reddit).complete,
            # 'REBOOT': Rules(reddit).updateRules,
            # 'SHUTDOWN': Rules(reddit).updateRules,
            # 'STATUS': Rules(reddit).updateRules,
            # 'LOGS': Rules(reddit).updateRules,
            # 'LOGS_BY_USER': Rules(reddit).updateRules,
        }

        activePermissions = Permissions(reddit).currentPermissions
        botPermissions = activePermissions['bot']
        requestPermissions = activePermissions['actions'][requestIdentifier]

        # Check to see if a user is in the list of users banned from using the bot, or is banned from the subreddit
        if (str(payload.author).lower() in botPermissions['restrictedUsers'] or BannedRelationship(payload, reddit).isBanned):
            print('* User is not authorized to use bot')
            sys.stdout.flush()
            response = {
            'statusCode': 200,
            'subject': 'Error: Not Authorized',
            'message': 'You are banned from using this bot.'
            }
        else:
            print('* User is authorized to use bot')
            sys.stdout.flush()
            if ('redditor' in requestPermissions['authorizedRelationships']):
                response = functionDispatch[requestIdentifier]()
            elif ('moderator' in requestPermissions['authorizedRelationships'] and ModeratorRelationship(payload, reddit).isModerator):
                response = functionDispatch[requestIdentifier]()
            else:
                response = {
                'statusCode': 200,
                'subject': 'Error: Not Authorized',
                'message': 'You are not authorized to preform this action'
                }

        MessageDispatcher(payload, response, reddit)

