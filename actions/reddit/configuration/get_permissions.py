""" Permissions Parse """
import os
import json
import sys

class Permissions:

    def __init__(self, reddit):
        self.status = {
            'statusCode': 204,
            'subject': 'No Content',
            'message': 'No Content'
        }
        self.thesePermissions = None 
        self.permissionsDirectory = {}
        self.reddit = reddit

        self.get_permissions()

    def get_permissions(self):
        try:
            documentPath = os.environ.get("USERNAME") + '/config/permissions'
            print("* Updating permissions")
            print("  * Looking for permissions at reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + documentPath + '...')
            sys.stdout.flush()
            permissionsDefinition = self.reddit.subreddit(os.environ.get("SUBREDDIT")).wiki[documentPath].content_md
        except Exception as e:
            print("  * No permissions found at reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + documentPath + "")
            print("* Updating permissionss failed. Continuing with no active permissionss.")
            sys.stdout.flush()
            self.status = {
                'statusCode': 400,
                'subject': 'Error: Permissions Not Found',
                'message': "Permissions definition cannot be found. Confirm your permissions definition is located at reddit.com/r/" + os.environ.get("SUBREDDIT") + '/wiki/' + path + " :"  + str(e)
            }
        else:
            self.parse_permissions(permissionsDefinition)

    def parse_permissions(self, permissionsdef):
        try:
            print("  * Loading permissions...")
            sys.stdout.flush()
            permissionsdef = json.loads(permissionsdef)
        except Exception as e:
            print("  * Permissions definition contains invalid JSON: " + str(e))
            print("* Updating permissions failed. Continuing with no active permissions.")
            sys.stdout.flush()
            self.status = {
                'statusCode': 400,
                'subject': 'Error: Permissions Not Loaded',
                'message': 'Permissions not valid: ' + str(e)
            }
        else:
            self.store_permissions(permissionsdef)

    def store_permissions(self, permissionsdef):
        try:
            print("  * Storing permissions...")
            sys.stdout.flush()
            json.dump(permissionsdef, open("permissions.json", 'w'))
        except Exception as e:
            print("  * Permissions could not be saved: " + str(e))
            print("* Updating permissions failed. Continuing with no active permissions.")
            sys.stdout.flush()
            self.status = {
                'statusCode': 400,
                'subject': 'Error: Permissions Not Saved',
                'message': 'Permissions cannot be saved: ' + str(e)
            }
        else:
            self.process_permissions()

    def process_permissions(self):
        print("  * Applying permissions...")
        sys.stdout.flush()
        with open('permissions.json') as botconfig:
            self.thesePermissions = json.load(botconfig)
        print("* Updating permissions completed.")
        sys.stdout.flush()

    @property
    def currentPermissions(self):
        return self.thesePermissions

    @property
    def updatePermissions(self):
        self.get_permissions()
        return self.status

    @property
    def findPermissions(self):
        self.process_permissions()
        return self.permissionsDirectory
