"""
App controller functions for the Habitica To Do Over tool.
"""

__author__ = "Katie Patterson kirska.com"
__license__ = "MIT"

from cipher_functions import encrypt_text, decrypt_text
import requests
from to_do_overs.models import Users, Tasks
from datetime import datetime, timedelta


class ToDoOversData:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.hab_user_id = ''
        self.api_token = ''
        self.logged_in = False

        self.task_name = ''
        self.task_days = 0
        self.task_id = ''
        self.priority = ''
        self.notes = ''

    def login(self):
        req = requests.post('https://habitica.com/api/v3/user/auth/local/login',
                            data={'username': self.username, 'password': self.password})
        if req.status_code == 200:
            req_json = req.json()
            print req_json
            self.hab_user_id = req_json['data']['id']
            self.api_token = req_json['data']['apiToken']
            self.username = req_json['data']['username']

            enc_token = encrypt_text(self.api_token.encode('utf-8'))

            Users.objects.update_or_create(user_id=self.hab_user_id, defaults={
                'api_key': enc_token,
                'username': self.username,
            })

            self.logged_in = True

            return True
        else:
            return False

    def login_api_key(self):
        headers = {'x-api-user': self.hab_user_id.encode('utf-8'), 'x-api-key': self.api_token.encode('utf-8')}

        req = requests.get('https://habitica.com/api/v3/user', headers=headers, data={
            'userFields': 'profile.name'
        })
        if req.status_code == 200:
            req_json = req.json()
            self.username = req_json['data']['profile']['name']
            enc_token = encrypt_text(self.api_token.encode('utf-8'))

            Users.objects.update_or_create(user_id=self.hab_user_id, defaults={
                'api_key': enc_token,
                'username': self.username,
            })

            self.logged_in = True

            return True
        else:
            return False

    def create_task(self):
        headers = {'x-api-user': self.hab_user_id.encode('utf-8'), 'x-api-key': self.api_token.encode('utf-8')}

        if int(self.task_days) > 0:
            due_date = datetime.now() + timedelta(days=int(self.task_days))

            req = requests.post('https://habitica.com/api/v3/tasks/user', headers=headers, data={
                'text': self.task_name,
                'type': 'todo',
                'notes': self.notes,
                'date': due_date,
                'priority': self.priority,
            })
            if req.status_code == 201:
                req_json = req.json()
                self.task_id = req_json['data']['id']
                return True
            else:
                return False
        else:
            req = requests.post('https://habitica.com/api/v3/tasks/user', headers=headers, data={
                'text': self.task_name,
                'type': 'todo',
                'notes': self.notes,
                'priority': self.priority,
            })
            if req.status_code == 201:
                req_json = req.json()
                self.task_id = req_json['data']['id']
                return True
            else:
                return False
