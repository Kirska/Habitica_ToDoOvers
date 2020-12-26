"""Daily maintenance script - Habitica To Do Over tool

This script is run once a day to add repeats of tasks.
"""
from __future__ import print_function

from builtins import str
__author__ = "Katie Patterson kirska.com"
__license__ = "MIT"

from datetime import datetime
import time
import pytz
import requests
# pylint: disable=unused-import
from Habitica_ToDoOvers.wsgi import application  # noqa: F401

from to_do_overs.models import Tasks
from to_do_overs.app_functions.cipher_functions import decrypt_text
from to_do_overs.app_functions.to_do_overs_data import ToDoOversData
from to_do_overs.app_functions.local_defines import CIPHER_FILE


def check_recreate_task(req, task):
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

        retry = True
        delay_seconds = 0

        while retry:
            if tdo_data.create_task(CIPHER_FILE):
                task.task_id = tdo_data.task_id
                task.save()
                retry = False
                delay_seconds = 0
                print('task re-created successfully ' + task.task_id)
            else:
                print('task creation failed ' + task.task_id)
                if tdo_data.return_code == 429:
                    print('too many requests, sleeping')
                    retry = True
                    delay_seconds += 90
                    if delay_seconds > 500:
                        # stop trying
                        retry = False
                        delay_seconds = 0
                    else:
                        time.sleep(delay_seconds)
                else:
                    print('unknown failure')
                    retry = False
                    delay_seconds = 0

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

            retry = True
            delay_seconds = 0

            while retry:
                if tdo_data.create_task(CIPHER_FILE):
                    task.task_id = tdo_data.task_id
                    task.save()
                    retry = False
                    delay_seconds = 0
                    print('task re-created successfully ' + task.task_id)
                else:
                    print('task creation failed ' + task.task_id)
                    if tdo_data.return_code == 429:
                        print('too many requests, sleeping')
                        retry = True
                        delay_seconds += 90
                        if delay_seconds > 500:
                            # stop trying
                            retry = False
                            delay_seconds = 0
                        else:
                            time.sleep(delay_seconds)
                    else:
                        print('unknown failure')
                        retry = False
                        delay_seconds = 0
        else:
            print('task completed but delay not met ' + task.task_id)

    else:
        print(
            'task not completed ' + task.task_id
        )


TASKS = Tasks.objects.all()

for task_ in TASKS:
    tdo_data = ToDoOversData()

    too_many_requests_delay = True
    current_delay = 0

    while too_many_requests_delay:
        url = 'https://habitica.com/api/v3/tasks/' + str(task_.task_id)
        headers = {
            'x-api-user': str(task_.owner.user_id),
            'x-api-key': decrypt_text(
                task_.owner.api_key.encode('utf-8'), CIPHER_FILE
            )
        }

        req_ = requests.get(url, headers=headers)

        if req_.status_code == 429:
            # too many requests
            current_delay += 90
            too_many_requests_delay = True
            print("too many requests, sleeping")
            if current_delay > 500:
                # stop trying
                too_many_requests_delay = False
                current_delay = 0
            else:
                time.sleep(current_delay)
        elif req_.status_code == 200:
            check_recreate_task(req_, task_)
            too_many_requests_delay = False
        elif req_.status_code == 404:
            print("deleting task " + task_.task_id)
            Tasks.objects.filter(task_id=task_.task_id).delete()
            too_many_requests_delay = False
        else:
            print("weird return code")
            print(req_.status_code)
            too_many_requests_delay = False
