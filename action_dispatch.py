import os
import sys 
from update_flair_text import UpdateFlairText
from update_flair_text_by_user import UpdateFlairTextByUser
from update_flair_with_rules import UpdateFlairWithRules
from update_flair_with_rules_by_user import UpdateFlairWithRulesByUser
from bulk_update_from_csv import BulkUpdateFromCSV
from rule_parse import Rules

class ActionDispatch:

    def __init__(self, requestIdentifier, payload, reddit):
        # Maps action requests to executions
        functionDispatch = {
            # 'UPDATE_FLAIR_TEXT': lambda: UpdateFlairText(payload, reddit).complete,
            # 'UPDATE_FLAIR_TEXT_BY_USER': UpdateFlairTextByUser(payload, reddit).complete,
            'UPDATE_FLAIR_WITH_RULES': lambda: UpdateFlairWithRules(payload, reddit).complete,
            # 'UPDATE_FLAIR_WITH_RULES_BY_USER': UpdateFlairWithRulesByUser(payload, reddit).complete,
            # 'UPDATE_RULES': Rules(reddit).updateRules,
            # 'UPDATE_CONFIG': Rules(reddit).updateRules,
            # 'REBOOT': Rules(reddit).updateRules,
            # 'SHUTDOWN': Rules(reddit).updateRules,
            # 'STATUS': Rules(reddit).updateRules,
            # 'LOGS': Rules(reddit).updateRules,
            # 'LOGS_BY_USER': Rules(reddit).updateRules,
            # 'EXECUTE': BulkUpdateFromCSV(reddit).complete,
        }

        # Dispatches function, returns a response status code, response message subject, and response message body
        dispatch = functionDispatch[requestIdentifier]()

        # Catch for error handling of function execution
        if dispatch['response'] == 200:
            reddit.redditor(str(payload.author)).message(dispatch['subject'], dispatch['message'])
            payload.mark_read()
        # if dispatch['response'] == 200:
        #     reddit.redditor(str(payload.author)).message(dispatch['subject'], dispatch['message'])
        #     payload.mark_read()
        # else:
        #     reddit.redditor(str(payload.author)).message(dispatch['subject'], dispatch['message'])
        #     payload.mark_read()
