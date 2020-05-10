import os
import json
import sys

class SayHello:

    def __init__(self, payload):

        self.status = {
            'statusCode': 200,
            'subject': 'hello',
            'message': None
        }

    @property
    def complete(self):
        return self.status
