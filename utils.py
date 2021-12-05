from datetime import datetime, timezone
from pathlib import Path


def get_todotxt_path(user_data):
    return Path(user_data['todotxt_pathname'])


def get_todotxt_modified_at(user_data):
    todotxt_path = get_todotxt_path(user_data)
    return datetime.fromtimestamp(todotxt_path.stat().st_mtime, tz=timezone.utc)


def get_todotxt_path_with_assertions(user_data, assertions):
    todotxt_path = get_todotxt_path(user_data)
    modified_at = get_todotxt_modified_at(user_data)
    assertion_modified_before = assertions.get('modified_before')
    if assertion_modified_before < modified_at:
        raise ValueError('Assertion failed: file modification time is after assertion')
    return todotxt_path


def task_to_dict(task):
    return {
        'line_number': task.linenr,
        'full_text': str(task)
    }