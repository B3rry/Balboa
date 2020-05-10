import os
import json
import sys

class Ping:

    def __init__(self, payload):

        self.status = {
            'statusCode': 200,
            'subject': 'Pong',
            'message': 'You sent ping, I sent pong'
        }

    @property
    def complete(self):
        return self.status
