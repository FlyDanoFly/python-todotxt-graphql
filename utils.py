from datetime import datetime, timezone
import errno
from pathlib import Path

from exceptions import TodoTxtBadAssertionError


def get_todotxt_path(user_data):
    return Path(user_data['todotxt_pathname'])


def get_todotxt_modified_at(user_data):
    todotxt_path = get_todotxt_path(user_data)
    return datetime.fromtimestamp(todotxt_path.stat().st_mtime, tz=timezone.utc)


def get_todotxt_path_with_assertions(user_data, assertions, require_modified_at=True):
    todotxt_path = get_todotxt_path(user_data)
    if not todotxt_path.exists():
        raise FileNotFoundError(errno.ENOENT, 'No file matching credentials')
        
    assertion_modified_before = assertions.get('modified_before')
    if assertion_modified_before:
        modified_at = get_todotxt_modified_at(user_data)
        if assertion_modified_before < modified_at:
            raise TodoTxtBadAssertionError('Assertion failed: file modification time is after assertion')
    elif require_modified_at:
        raise TodoTxtBadAssertionError('Assertion failed: modification time is required')
    return todotxt_path


def task_to_dict(task):
    return {
        'line_number': task.linenr,
        'full_text': str(task)
    }