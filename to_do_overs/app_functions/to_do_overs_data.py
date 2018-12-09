"""
App controller functions for the Habitica To Do Over tool.
"""

__author__ = "Katie Patterson kirska.com"
__license__ = "MIT"

from cipher_functions import encrypt_text, decrypt_text
import requests


class ToDoOversData:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.hab_user_id = ''
        self.api_token = ''

    def login(self):
        req = requests.post('https://habitica.com/api/v3/user/auth/local/login',
                            data={'username': self.username, 'password': self.password})
        if req.status_code == 200:
            req_json = req.json()
            self.hab_user_id = req_json['data']['id']
            self.api_token = req_json['data']['apiToken']
            return True
        else:
            return False
