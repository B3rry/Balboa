import os
import json
import sys

class Ping:

    def __init__(self, payload):
        author = str(payload.author)

        self.status = {
            'statusCode': 200,
            'subject': 'Pong',
            'message': author + ' sent ping, I sent pong'
        }

    @property
    def complete(self):
        return self.status
