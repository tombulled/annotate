from typing import Any
import annotate
import dataclasses

@dataclasses.dataclass
class Route:
    path: str
    method: str

class Annotation:
    key: Any

    def __init__(self, key: Any):
        self.key = key

    def __call__(self, *args, **kwargs):
        def decorate(obj):
            value = self.hook(*args, **kwargs)

            annotate.init(obj)

            annotations = annotate.get(obj)

            if self.key in annotations:
                value = self.replace(annotations[self.key], value)

            annotations[self.key] = value

            return obj

        return decorate

    @staticmethod
    def hook(x):
        return x

    @staticmethod
    def resolve(old, new):
        return new

class Marker(Annotation):
    def __call__(self, obj):
        return super().__call__(None)(obj)

class RouteAnnotation(Annotation):
    @staticmethod
    def hook(*paths: str, **kwargs):
        return [
            Route(path, **kwargs)
            for path in paths
        ]

    @staticmethod
    def resolve(old, new):
        return old + new

route = Annotation('route')
deprecated = Marker('deprecated')

@route('/foo')
@deprecated
def foo():
    ...