import os
import sys
from action_dispatch import ActionDispatch

class ActionRequest:
    # ActionRequest is triggered _any_ time a message is recieved. In short, init defines the list of possible actions, and known exceptions, and determines if the request will 
    # fail or trigger an action to occur (which may or may not respond with a message). When a request exists, throws no errors, and has a matching entry in action_dispatch.py,
    # the action will be dispatched. 
    # TODO - JRB: Right now we trigger a message reply to be sent directly in this file. I think we'll want to eventually request a message (and logging, modmail, etc?) get 
    # dispatched through a generic channel that we can control. (Esepcially important for enabling different types of messaging services) 
    # TODO - JRB: We also should eventually use this as a place to reference a dynamically generated manifest of actions.

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

        print('Message: /u/' + str(payload.author) + " sent '" + str(request) + "': " + str(payload.body) )
        sys.stdout.flush()
        
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
                reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators.')
                payload.mark_read()
        # Catch all other excpetions
        except Exception as e:
            reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators.')
            payload.mark_read()
        # If all conditions are met, dispatch the action.
        else:
            ActionDispatch(requestIdentifier, payload, self.reddit)
