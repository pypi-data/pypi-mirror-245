import requests

import json

class API:
    def __init__(self):
        self.documentation = ''
        self.post_api = ''
        self.api_key = None

    def auth(self, api_key):
        self.api_key = api_key

    def track(self, txn):
        try:
            if self.api_key is None:
                return {'status_code': 400, 'message': f'You must authorize your request first!  See documentation: {self.documentation}'}

            headers = {'api-key': self.api_key, 'Content-type': 'application/json'}

            if not isinstance(txn, dict): return {'message': 'You must pass a dictionary!'}

            r = requests.post(self.post_api, headers=headers, json=txn)

            response = json.loads(r.content)

            if r.status_code != 201:
                message = f'Could not complete send because {response}.  Visit {self.documentation} for help.'
                return {'status_code': r.status_code, 'message': message}

            return {'status_code': r.status_code, 'usd_amount': response['usd_amount'], 'message': response['message']}

        except Exception as e:
            return {'status_code': 500, 'message': f'Curia SDK event tracking failed because {e}'}