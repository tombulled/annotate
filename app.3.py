import annotate
import dataclasses

@dataclasses.dataclass
class Route:
    path: str
    method: str

def description(description: str) -> annotate.Annotation:
    return annotate.Annotation('description', description, inherited=False, repeatable=True)

@description('awesome!')
@description('cool!')
class Foo:
    def __init_subclass__(cls) -> None:
        print('orgin init subclass called')
        return cls

    def some_method(self): ...

class Bar(Foo):...
class Baz(Bar):...

print(Foo._annotations_)
print(Bar._annotations_)
print(Baz._annotations_)

def route(*paths: str, **kwargs):
    routes = [
        Route(path, **kwargs)
        for path in paths
    ]

    annotations = [
        annotate.Annotation('route', route, repeatable=True)
        for route in routes
    ]

    def wrapper(obj):
        for annotation in annotations:
            annotate.annotate(obj, annotation)

        return obj

    return wrapper

@route('/foo', '/bar', method='GET')
@route('/baz', '/bat', method='POST')
def foo():
    ...

print(foo._annotations_)

@annotate.annotation('my_annotation', inherited=True)
def my_annotation(this: str, that: str) -> str:
    return f'<{this=}, {that=}>'

@my_annotation('foo', 'bar')
def fn(x: int) -> int:
    return x * 10

print(fn._annotations_)