import os
import sys
from .action_dispatch import ActionDispatch

# ============= Action Request .py ============= #
# Currently, is triggered _any_ time a message is recieved. In short, it identifes
# actions, validates they can be performed, and triggers the relevant request when
# valid. When a request exists, throws no errors, and has a matching entry in 
# action_dispatch.py, the action will be dispatched.
# 
# The long term vision for this code is to transition to requesting "scripts" of
# multiple actions.
#
# TODO - JRB: Right now we trigger a message reply to be sent directly in this file.
# I think we'll want to eventually request a message (and logging, modmail, etc?)
# get dispatched through a generic channel that we can control. (Esepcially 
# important for enabling different types of messaging services) 
# TODO - JRB: We also should eventually use this as a place to reference a 
# dynamically generated manifest of actions.

class ActionRequest:

    # `requestCommand` (dict, string:string): defines a list of message subjects that will cause the bot to dispatch a matching action, as defined in action_dispatch.py
    requestCommand = {
            'system': {
                'Ping': 'PINGPONG',
            },
            'reddit': {
                'Flair': 'UPDATE_FLAIR_TEXT',
                'Set Flair': 'UPDATE_FLAIR_WITH_RULES',
                'Update Rules': 'UPDATE_RULES',
                'Bulk Update Flair': 'BULK_UPDATE_FLAIRS'
            },
            'slack': {
                'make channel': 'CREATE_CHANNEL',
                'hi': 'SAY_HELLO',
                'vote': 'VOTE',
            }
        }

    def __init__(self, protocol: str, request: str, payload, reddit):
        self.reddit = reddit
        
        # Decoding the initial request aftern utf-8 sanitization
        decodedRequest = request.decode('utf-8')
        
        # `knownExceptions` (list, string): defines a list of message subjects that will cause the bot to mark the message as read and take no action.
        knownExceptions = [
            'post reply',
            'comment reply'
        ]
        
        # Get the identifier for the request made. Returns None when request has no match.
        requestIdentifier = self.getRequestIdentifier(protocol=protocol, request=decodedRequest)

        # Dispatch an action for valid requests.
        if requestIdentifier is not None:
            print(str(decodedRequest) + " matches action " + str(requestIdentifier) + ". Dispatching Action...")
            sys.stdout.flush()
            ActionDispatch(protocol, requestIdentifier, payload, self.reddit)
        elif decodedRequest in knownExceptions:
            print(str(decodedRequest) + " is on the list of known exceptions. Taking no action, marking message as read. ")
            sys.stdout.flush()
            if protocol == "reddit":
                payload.mark_read()
        else:
            print(str(decodedRequest) + " does not match a known action or known exception. Replying with error message...")
            sys.stdout.flush()
            if protocol == "reddit":
                reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators.')
                payload.mark_read()

    # Parses requestCommand dict and returns the command identifier for valid requests.
    # Prioritizes global commands 
    def getRequestIdentifier(self, protocol: str, request: str):
        identifier = None
        if request in self.requestCommand['system']:
            identifier = self.requestCommand['system'][request]
        elif request in self.requestCommand[protocol]:
            identifier = self.requestCommand[protocol][request]
        else:
            identifier = None
        return identifier
