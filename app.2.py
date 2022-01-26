import dataclasses
import typing
import annotate

from typing import Any

'''
Options:
    @repeatable (uses a list)
    @inherited (classes inherit annotations)

@repeatable
@inherited
@annotation
def route(*paths, **kwargs):
    ...

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

def identity(x):
    return x

@dataclasses.dataclass
class Route:
    path: str
    method: str

@dataclasses.dataclass
class Marker:
    key: str
    value: Any = None

    # inherited: bool = False # TODO
    repeatable: bool = False

    def __call__(self, obj):
        annotate.init(obj)

        annotations = annotate.get(obj)

        if self.repeatable:
            annotations.setdefault(self.key, [])

            annotations[self.key].append(self.value)
        else:
            annotations[self.key] = self.value

        return obj

@dataclasses.dataclass(init=False)
class Factory:
    hook: typing.Callable = identity
    marker: Marker

    def __init__(self, *args, hook: typing.Callable = identity, **kwargs):
        self.hook = hook
        self.marker = Marker(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return dataclasses.replace(self.marker, value=self.hook(*args, **kwargs))

route = Factory('route', hook=Route, repeatable=True)

@route('/a', method='GET')
@route('/b', method='GET')
def foo(): ...

print(foo._annotations_)