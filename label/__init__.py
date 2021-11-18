import functools
import typing

import modcall

def apply_label(obj: typing.Any, /, key: typing.Any, value: typing.Any = None) -> None:
    if not hasattr(obj, '__labels__'):
        obj.__labels__: dict = {}

    obj.__labels__[key] = value

def label(key: typing.Any, value: typing.Any = None):
    def wrapper(obj):
        apply_label(obj, key, value)

        return obj

    return wrapper

def labeller(key: typing.Any, hook = lambda x: x):
    def wrapper(*args, **kwargs):
        return label(key, hook(*args, **kwargs))

    return wrapper

def get_labels(obj: typing.Any) -> dict:
    return getattr(obj, '__labels__', {})

modcall(__name__, label)
