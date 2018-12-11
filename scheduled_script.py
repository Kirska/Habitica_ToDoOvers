"""Daily maintenance script - Habitica To Do Over tool

This script is run once a day to add repeats of tasks.
"""

__author__ = "Katie Patterson kirska.com"
__license__ = "MIT"

import sys
from Habitica_ToDoOvers.wsgi import application

from to_do_overs.models import Tasks
import requests
from to_do_overs.app_functions.cipher_functions import decrypt_text, CIPHER_FILE
from to_do_overs.app_functions.to_do_overs_data import ToDoOversData

CIPHER_FILE_SCRIPT = CIPHER_FILE

tasks = Tasks.objects.all()

for task in tasks:
    tdo_data = ToDoOversData()

    url = 'https://habitica.com/api/v3/tasks/' + str(task.task_id)
    headers = {'x-api-user': str(task.owner.user_id),
               'x-api-key': decrypt_text(task.owner.api_key.encode('utf-8'), CIPHER_FILE_SCRIPT)}

    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        req_json = req.json()
        if req_json['data']['completed']:
            # Task was completed to recreate it
            tdo_data.hab_user_id = task.owner.user_id
            tdo_data.priority = task.priority
            tdo_data.api_token = task.owner.api_key
            tdo_data.notes = task.notes
            tdo_data.task_name = task.name
            tdo_data.task_days = task.days

            if tdo_data.create_task():
                task.task_id = tdo_data.task_id
                task.save()
            else:
                pass


