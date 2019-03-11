import os
import sys
from action_dispatch import ActionDispatch

class ActionRequest:

    def __init__(self, request, payload, reddit):
        self.reddit = reddit
        # Maps subject commands to action requests, as defined in action_dispatch.py
        # Currently, only supports 'Set Flair', you can enable other items, but do so at your own risk.
        # No permissions gate any user from executing any of these.
        requestCommand = {
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
        # Defines subject strings exceptions that do not return an error message.
        knownExceptions = [
            'post reply',
            'comment reply'
        ]

        try:
            requestIdentifier = requestCommand[request]
        except KeyError:
            exception = request
            if exception in knownExceptions:
                payload.mark_read()
            else:
                reddit.redditor(str(payload.author)).message('Error Updating Flair for /r/' + os.environ.get("SUBREDDIT"), '/u/' +  str(payload.author) + ',\n\nYour flair request could not be processed. Please try again.\n\nWhen sending a message created from a link in the [list of available flairs]( https://www.reddit.com/r/survivor/wiki/available_flairs), be sure to not edit the subject or body of the message before pressing \'send\'.\n\nIf you continue to experience errors, please [message the /r/' + os.environ.get("SUBREDDIT") + '  moderators](https://www.reddit.com/message/compose/?to=/r/Survivor&subject=Help%20with%20flair) for help.')
                payload.mark_read()
        except Exception as e:
            reddit.redditor(str(payload.author)).message('An Error Occurred', 'An error occured. Please contact the subreddit moderators.')
            payload.mark_read()
        else:
            ActionDispatch(requestIdentifier, payload, self.reddit)
