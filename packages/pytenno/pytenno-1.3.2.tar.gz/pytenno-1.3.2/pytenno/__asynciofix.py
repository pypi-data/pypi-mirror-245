from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps


def silence(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError:
            pass

    return wrap


_ProactorBasePipeTransport.__del__ = silence(_ProactorBasePipeTransport.__del__)
