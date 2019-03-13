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
from messages.message_dispatcher import MessageDispatcher

class ActionDispatch:

    def __init__(self, requestIdentifier, payload, reddit):
        # Maps action requests to executions
        functionDispatch = {
            'PING': lambda: Ping(payload).complete,
            'UPDATE_FLAIR_TEXT': lambda: UpdateFlairText(payload, reddit).complete,
            # 'UPDATE_FLAIR_TEXT_BY_USER': UpdateFlairTextByUser(payload, reddit).complete,
            'UPDATE_FLAIR_WITH_RULES': lambda: UpdateFlairWithRules(payload, reddit).complete,
            # 'UPDATE_FLAIR_WITH_RULES_BY_USER': UpdateFlairWithRulesByUser(payload, reddit).complete,
            'UPDATE_RULES': lambda: Rules(reddit).updateRules,
            'MODERATOR_RELATIONSHIP': lambda: ModeratorRelationship(payload, reddit).complete
            # 'UPDATE_CONFIG': Rules(reddit).updateRules,
            # 'REBOOT': Rules(reddit).updateRules,
            # 'SHUTDOWN': Rules(reddit).updateRules,
            # 'STATUS': Rules(reddit).updateRules,
            # 'LOGS': Rules(reddit).updateRules,
            # 'LOGS_BY_USER': Rules(reddit).updateRules,
            # 'EXECUTE': BulkUpdateFromCSV(reddit).complete,
        }

        # Dispatches function, returns a response object
        response = functionDispatch[requestIdentifier]()

        MessageDispatcher(payload, response, reddit)

