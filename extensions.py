import time

# from ariadne.types import Extension
from ariadne.types import ExtensionSync as Extension
from ariadne.exceptions import HttpError

class AuthenticationError(HttpError):
     extensions = {"code": "UNAUTHENTICATED"}


class QueryExecutionTimeExtension(Extension):
    def __init__(self):
        self.start_timestamp = None
        self.end_timestamp = None
        self.is_authed = False

    def resolve(self, next_, parent, info, **kwargs):
        # raise HttpError()
        import pdb
        pdb.set_trace()
        raise AuthenticationError()
        pass

    def request_started(self, context):
        print('='*80)
        # raise RuntimeError()
        self.start_timestamp = time.perf_counter_ns()

    def request_finished(self, context):
        print('-'*80)
        self.end_timestamp = time.perf_counter_ns()

    def format(self, context):
        print('!'*80)
        if self.start_timestamp and self.end_timestamp:
            return {}
            # return {
            #     "execution": self.start_timestamp - self.end_timestamp
            # }