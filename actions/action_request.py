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

    def __init__(self, request, payload, reddit):
        self.reddit = reddit

        # `requestCommand` (dict, string:string): defines a list of message subjects that will cause the bot to dispatch a matching action, as defined in action_dispatch.py
        requestCommand = {
            'Ping': 'PINGPONG',
            'Flair': 'UPDATE_FLAIR_TEXT',
            'Set Flair': 'UPDATE_FLAIR_WITH_RULES',
            'Update Rules': 'UPDATE_RULES',
            'Bulk Update Flair': 'BULK_UPDATE_FLAIRS'
        }

        # `knownExceptions` (list, string): defines a list of message subjects that will cause the bot to mark the message as read and take no action.
        knownExceptions = [
            'post reply',
            'comment reply'
        ]

        # Decoding the initial request aftern utf-8 sanitization
        decodedRequest = request.decode('utf-8')

        print('Message: /u/' + str(payload.author) + " sent '" + str(decodedRequest) + "': " + str(payload.body) )
        sys.stdout.flush()
        
        # Try to see if requestIdentifier (the subject line of the dispatched message) is in the requestCommand dict
        # TODO - JRB: Suppport the passing of args in the requestIdentifier line
        try:
            requestIdentifier = requestCommand[decodedRequest]

        # Except messages where requestIdentifier does not exist in the requestCommand dict
        except KeyError as e:
            exception = decodedRequest
            # If this is a non-actionable message (such as notifications about replies to posts or comments, mark them as read and take no action.)
            if exception in knownExceptions:
                print(str(decodedRequest) + " is on the list of known exceptions. Taking no action, marking message as read. ")
                sys.stdout.flush()
                payload.mark_read()
            # Else dispatch a message and mark as read if the provided requestIdentifier doesn't exist in the requestCommand or knownExceptions dicts
            else:
                print(str(decodedRequest) + " does not match a known action or known exception. Replying with error message...")
                sys.stdout.flush()
                # TODO - JRB: I think this message should be more generic(?)
                reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators: (Key Error: ' + str(e) + ')')
                payload.mark_read()
        # Catch all other excpetions
        except Exception as e:
            reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators: (Exception: ' + str(e) + ')')
            payload.mark_read()
        # If all conditions are met, dispatch the action.
        else:
            print(str(decodedRequest) + " matches action " + str(requestIdentifier) + ". Dispatching Action...")
            sys.stdout.flush()
            ActionDispatch(requestIdentifier, payload, self.reddit)
