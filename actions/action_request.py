import os
import sys
from action_dispatch import ActionDispatch

class ActionRequest:
    # ActionRequest is triggered _any_ time a message is recieved. In short, init defines the list of possible actions, and known exceptions, and determines if the request will 
    # fail or trigger an action to occur (which may or may not respond with a message). When a request exists, throws no errors, and has a matching entry in actionDispatch.py,
    # the action will be dispatched. 
    # TODO - JRB: Right now we trigger a message reply to be sent directly in this file. I think we'll want to eventually request a message (and logging, modmail, etc?) get 
    # dispatched through a generic channel that we can control. (Esepcially important for enabling different types of messaging services) 
    # TODO - JRB: We also should eventually use this as a place to reference a dynamically generated manifest of actions.

    def __init__(self, request, payload, reddit):
        self.reddit = reddit

        # `requestCommand` (dict, string:string): defines a list of message subjects that will cause the bot to dispatch a matching action, as defined in actionDispatch.py
        # Currently, only supports 'Set Flair', you can enable other items, but do so at your own risk. No permissions gate any user from executing any of these. (Yet. High 
        # priority contribution option if you're looking for a place to start. )
        requestCommand = {
            'Ping': 'PING',
            'Flair': 'UPDATE_FLAIR_TEXT',
            # 'User Flair': 'UPDATE_FLAIR_TEXT_BY_USER',
            'Set Flair': 'UPDATE_FLAIR_WITH_RULES',
            # 'Set User Flair': 'UPDATE_FLAIR_WITH_RULES_BY_USER',
            'Update Rules': 'UPDATE_RULES',
            # 'Update Config': 'UPDATE_CONFIG',
            # 'Reboot': 'REBOOT',
            # 'Shutdown': 'SHUTDOWN',
            # 'Status': 'STATUS',
            # 'Logs': 'LOGS',
            # 'User Logs': 'LOGS_BY_USER',
            # 'Execute': 'EXECUTE',
            # 'Unknown Command': 'ERR_UNKOWN_COMMAND'
        }

        # `knownExceptions` (list, string): defines a list of message subjects that will cause the bot to mark the message as read and take no action.
        knownExceptions = [
            'post reply',
            'comment reply'
        ]
        
        # Try to see if requestIdentifier (the subject line of the dispatched message) is in the requestCommand dict
        # TODO - JRB: Suppport the passing of args in the requestIdentifier line
        try:
            requestIdentifier = requestCommand[request]

        # Except messages where requestIdentifier does not exist in the requestCommand dict
        except KeyError:
            exception = request
            # If this is a non-actionable message (such as notifications about replies to posts or comments, mark them as read and take no action.)
            if exception in knownExceptions:
                payload.mark_read()
            # Else dispatch a message and mark as read if the provided requestIdentifier doesn't exist in the requestCommand or knownExceptions dicts
            else:
                # TODO - JRB: I think this message should be more generic(?)
                reddit.redditor(str(payload.author)).message('Error Updating Flair for /r/' + os.environ.get("SUBREDDIT"), '/u/' +  str(payload.author) + ',\n\nYour flair request could not be processed. Please try again.\n\nWhen sending a message created from a link in the [list of available flairs]( https://www.reddit.com/r/survivor/wiki/available_flairs), be sure to not edit the subject or body of the message before pressing \'send\'.\n\nIf you continue to experience errors, please [message the /r/' + os.environ.get("SUBREDDIT") + '  moderators](https://www.reddit.com/message/compose/?to=/r/Survivor&subject=Help%20with%20flair) for help.')
                payload.mark_read()
        # Catch all other excpetions
        except Exception as e:
            reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators.')
            payload.mark_read()
        # If all conditions are met, dispatch the action.
        # TODO - JRB: I think we'll want to use similar logic to `rule_parse.py` to check for permissions levels. Probably as a wrapper around the entire block. General strat 
        # would be to check against JSON pulled from subreddit wiki with kvp map of requestIdentifier to authorized roles
        else:
            ActionDispatch(requestIdentifier, payload, self.reddit)
