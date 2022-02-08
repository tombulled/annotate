import annotate
import dataclasses
from annotate import marker, annotation

@dataclasses.dataclass
class Route:
    path: str
    method: str

'''
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
'''

@marker
def deprecated() -> bool:
    return True

@annotation(key='route')
def get(path: str, /) -> Route:
    return Route(
        path = path,
        method = 'GET',
    )

@annotation(key='algComplexity', inherited=False)
def algorithmic_complexity(degree: int) -> int:
    return degree ** 10

@deprecated
@get('/foo')
@algorithmic_complexity(15)
def foo(): ...

# print(foo._annotations_)

@deprecated
class Foo: pass

class Bar(Foo): pass

route_1 = annotate.Annotation('route', value='route_1', repeatable=True, inherited=False)
route_2 = annotate.Annotation('route', value='route_2', repeatable=True, inherited=True)

@route_1
@route_2
def foo(): pass

print(foo._annotations_)