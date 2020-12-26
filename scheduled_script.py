"""Daily maintenance script - Habitica To Do Over tool

This script is run once a day to add repeats of tasks.
"""
from __future__ import print_function

from builtins import str
__author__ = "Katie Patterson kirska.com"
__license__ = "MIT"

from datetime import datetime
import pytz
import requests
# pylint: disable=unused-import
from Habitica_ToDoOvers.wsgi import application  # noqa: F401

from to_do_overs.models import Tasks
from to_do_overs.app_functions.cipher_functions import decrypt_text
from to_do_overs.app_functions.to_do_overs_data import ToDoOversData
from to_do_overs.app_functions.local_defines import CIPHER_FILE

TASKS = Tasks.objects.all()

for task in TASKS:
    tdo_data = ToDoOversData()

    url = 'https://habitica.com/api/v3/tasks/' + str(task.task_id)
    headers = {
        'x-api-user': str(task.owner.user_id),
        'x-api-key': decrypt_text(
            task.owner.api_key.encode('utf-8'), CIPHER_FILE
        )
    }

    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        req_json = req.json()
        if req_json['data']['completed'] and task.delay == 0:
            # Task was completed and there is no delay so recreate it
            tdo_data.hab_user_id = task.owner.user_id
            tdo_data.priority = task.priority
            tdo_data.api_token = task.owner.api_key
            tdo_data.notes = task.notes
            tdo_data.task_name = task.name
            tdo_data.task_days = task.days

            # convert tags from their DB ID to the tag UUID
            tag_list = []
            for tag in task.tags.all():
                tag_list.append(tag.tag_id)

            tdo_data.tags = tag_list

            if tdo_data.create_task(CIPHER_FILE):
                task.task_id = tdo_data.task_id
                task.save()
            else:
                print('task creation failed ' + task.task_id)
        elif req_json['data']['completed']:
            # Task was completed but has a delay
            # Get completed date and set to UTC timezone
            completed_date_naive = datetime.strptime(
                req_json['data']['dateCompleted'], '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            utc_timezone = pytz.timezone("UTC")
            completed_date_aware = utc_timezone.localize(
                completed_date_naive
            )
            # Get current UTC time
            utc_now = pytz.utc.localize(datetime.utcnow())

            # Need to round the datetimes down to get rid of partial days
            completed_date_aware = completed_date_aware.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            utc_now = utc_now.replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            # TESTING - add days to current date
            # utc_now = utc_now + timedelta(days=2)

            elapsed_time = utc_now - completed_date_aware

            # The delay we want is 1 + delay value
            if elapsed_time.days > task.delay:
                # Task was completed and the delay has passed
                tdo_data.hab_user_id = task.owner.user_id
                tdo_data.priority = task.priority
                tdo_data.api_token = task.owner.api_key
                tdo_data.notes = task.notes
                tdo_data.task_name = task.name
                tdo_data.task_days = task.days

                # convert tags from their DB ID to the tag UUID
                tag_list = []
                for tag in task.tags.all():
                    tag_list.append(tag.tag_id)

                tdo_data.tags = tag_list

                if tdo_data.create_task(CIPHER_FILE):
                    task.task_id = tdo_data.task_id
                    task.save()
                else:
                    print('task creation failed ' + task.task_id)
        else:
            print(
                'task ' + task.task_id + ' not completed or delay not met'
            )
    else:
        print('\n' + str(req.status_code))
        print(req.text)
        print('task name ' + task.name)
        print('task id ' + task.task_id)
        print('task delay ' + str(task.delay) + '\n')
