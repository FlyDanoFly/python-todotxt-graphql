from datetime import date, datetime, timezone
import shutil

from ariadne import convert_kwargs_to_snake_case
from pytodotxt import TodoTxt, Task

from exceptions import TodoTxtBaseError
from utils import get_todotxt_path_with_assertions, task_to_dict


@convert_kwargs_to_snake_case
def commit_all_tasks_resolver(obj, info, lines, assertions):
    try:
        user_data = info.context['user_data']
        todo_path = get_todotxt_path_with_assertions(user_data, assertions)

        if user_data.get('paranoid', True):
            source = todo_path
            destination = source.parent / f'_{source.stem}_{datetime.now(timezone.utc).isoformat()}{source.suffix}'
            shutil.copy(source, destination)

        todotxt = TodoTxt(todo_path)

        tasks = [Task(line, linenr) for linenr, line in enumerate(lines)]
        print(f'Writing {len(tasks)} tasks')
        return_tasks = [task_to_dict(task) for task in tasks]
        todotxt.tasks = tasks
        todotxt.save()
        payload = {
            "modified_at": datetime.fromtimestamp(todo_path.stat().st_mtime, timezone.utc),
            "success": True,
            "tasks": return_tasks
        }
    except TodoTxtBaseError as error:  # date format errors
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

#
# Everything following is really old and not tested, I really should delete them
#

@convert_kwargs_to_snake_case
def create_task_resolver(obj, info, title, description):
    try:
        today = date.today()
        print('-'*80)
        task = {
                'id': 4,
                'title': 'mutate hello world!',
                'description': 'mutate blah blah description',
                'created_at': today
            }
        print(f'Creating new ')
        print(f'{task["title"]}')
        print(f'{task["description"]}')
        print(f'{task["created_at"].strftime("%b-%d-%Y")}')
        print('done!')
        # task = Task(  
        #     title=title, description=description, created_at=today.strftime("%b-%d-%Y")
        # )
        # db.session.add(task)
        # db.session.commit()
        payload = {
            "success": True,
            "task": task
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    return payload


@convert_kwargs_to_snake_case
def update_task_resolver(obj, info, id, title, description):
    try:
        today = date.today()
        print('-'*80)
        task = {
                'id': 4,
                'title': 'mutate hello world!',
                'description': 'mutate blah blah description',
                'created_at': today
            }
        print(f'Creating new ')
        print(f'{task["title"]}')
        print(f'{task["description"]}')
        print(f'{task["created_at"].strftime("%b-%d-%Y")}')
        print('done!')

        # task = Task.query.get(id)
        # if task:
        #     task.title = title
        #     task.description = description
        # db.session.add(task)
        # db.session.commit()
        payload = {
            "success": True,
            "task": task
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload


@convert_kwargs_to_snake_case
def delete_task_resolver(obj, info, id):
    try:
        today = date.today()
        print('-'*80)
        task = {
                'id': 4,
                'title': 'delete hello world!',
                'description': 'delete blah blah description',
                'created_at': today
            }
        print(f'Creating new ')
        print(f'{task["title"]}')
        print(f'{task["description"]}')
        print(f'{task["created_at"].strftime("%b-%d-%Y")}')
        print('done!')

        # task = Task.query.get(id)
        # db.session.delete(task)
        # db.session.commit()
        payload = {"success": True, "task": task}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload
