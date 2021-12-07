from datetime import datetime, timezone

from ariadne import convert_kwargs_to_snake_case
from pytodotxt import TodoTxt

from exceptions import TodoTxtBaseError
from utils import (get_todotxt_modified_at, get_todotxt_path_with_assertions,
                   task_to_dict)

# TODO:
# Handle only returning some of the requested inputs
# I'm having a hard time finding documentation
# Best I've found is finding the info here from a simple query fetching all:
#     info.field_nodes[0].selection_set.selections[0].selection_set.selections[0].name.value
#     'id'


@convert_kwargs_to_snake_case
def get_modified_at_resolver(obj, info):
    try:
        user_data = info.context['user_data']
        modified_at = get_todotxt_modified_at(user_data)

        payload = {
            "success": True,
            "modified_at": modified_at,
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def listTasks_resolver(obj, info, assertions):
    try:
        user_data = info.context['user_data']
        todotxt_path = get_todotxt_path_with_assertions(user_data, assertions, require_modified_at=False)

        todotxt = TodoTxt(todotxt_path)
        todotxt.parse()

        tasks = [task_to_dict(task) for task in todotxt.tasks]
            # tasks = [task_to_dict(todotxt.tasks[1])]
        payload = {
            "modified_at": datetime.fromtimestamp(todotxt_path.stat().st_mtime, timezone.utc),
            "success": True,
            "tasks": tasks
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def getTask_resolver(obj, info, id, assertions):
    try:
        user_data = info.context['user_data']
        todotxt_path = get_todotxt_path_with_assertions(user_data, assertions, require_modified_at=False)

        todotxt = TodoTxt(todotxt_path)
        todotxt.parse()

        lineNumber = int(id)
        task = todotxt.tasks[lineNumber]
        task = task_to_dict(task)
        payload = {
            "success": True,
            "modified_at": datetime.fromtimestamp(todotxt_path.stat().st_mtime, timezone.utc),
            "task": task
        }
    except TodoTxtBaseError as error:  # todo not found
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
