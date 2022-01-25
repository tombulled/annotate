import dataclasses
import typing
import annotate

from typing import Any

'''
Marker:
    needs: key (overwrites)

Single Value:
    needs: key, value (overwrites)

Multi Value:
    needs: key, value/hook, resolver

Marker -> (key, value)
    value = None

Annotation
    value = hook(*args, **kwargs)

set(key, value)

Interfaces:
@annotate('description', 'foo')
@description('value')
'''

@dataclasses.dataclass
class Route:
    path: str
    method: str

# def marker(key):
#     return annotation(key, None)

def annotation(key, value=None):
    def wrapper(obj):
        annotate.set(obj, key, value)

        return obj

    return wrapper

# def hooked_annotation(key, hook):
#     def wrapper(*args, **kwargs):
#         return annotation(key, hook(*args, **kwargs))

#     return wrapper

def from_hook(hook):
    def decorate(key):
        def wrapper(*args, **kwargs):
            return annotation(key, hook(*args, **kwargs))

        return wrapper
    return decorate

# @dataclasses.dataclass
# class Entry:
#     key: Any
#     value: Any

@dataclasses.dataclass
class Marker:
    key: str
    value: Any = None

    def __call__(self, obj):
        annotate.init(obj)

        annotations = annotate.get(obj)

        value = self.value

        if self.key in annotations:
            value = self.resolve(annotations[self.key])

        annotations[self.key] = value

        return obj

    def resolve(self, current_value):
        return self.value

def identity(x):
    return x

# @dataclasses.dataclass
class Annotation:
    key: typing.Any
    # hook: typing.Callable = identity
    # replace: typing.Callable = lambda old, new: new

    def __init__(self, key: typing.Any, /, *, hook: typing.Optional[typing.Callable] = None) -> None:
        self.key = key

        if hook is not None:
            self.hook = hook

    @staticmethod
    def hook(x):
        return x

    def __call__(self, *args, **kwargs):
        return Marker(self.key, self.hook(*args, **kwargs))

# @dataclasses.dataclass
# class Depends(Annotation):
#     key: str = 'depends'
#     hook: typing.Callable = lambda ticket: [ticket]

    # def resolve(self, current_value):
    #     return current_value + self.value

# route = from_hook(Route)('route')
# disabled = annotation('disabled', True)
# deprecated = annotation('deprecated')
# awesome = Marker('category', 'awesome')
# depends = Annotation('depends', hook = lambda x: [x], replace=lambda a,b: a+b)

# @disabled
# @deprecated
# @route('/bar', method='GET')
# @awesome
# @depends('abc-1')
# @depends('abc-2')
# def foo():
#     ...

# depends = Depends()
depends = Annotation('depends', hook=lambda x: [x])

@depends('abc-1')
@depends('abc-2')
def bar(): ...