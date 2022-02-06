import dataclasses
import typing

ATTR: str = '_annotations_'

def get_annotations(obj):
    return getattr(obj, ATTR)

def has_annotations(obj):
    return hasattr(obj, ATTR)

def init_annotations(obj):
    setattr(obj, ATTR, {})

def identity(x):
    return x

def extract_annotations(obj):
    return {
        annotation.key: annotation.value
        for annotation in get_annotations(obj).values()
    }

def annotate(obj, annotation):
    if not isinstance(obj, annotation.targets):
        raise Exception('obj type not targetted by this annotation')

    if isinstance(obj, type) and not has_annotations(obj):
        orig_init_subclass = obj.__init_subclass__.__func__

        def init_subclass(cls, **kwargs):
            orig_init_subclass(cls, **kwargs)

            if not has_annotations(cls):
                init_annotations(cls)

            annotations = get_annotations(cls)

            cls._annotations_ = {
                key: annotation
                for key, annotation in annotations.items()
                if annotation.inherited
            }
            
            return cls

        obj.__init_subclass__ = classmethod(init_subclass)

    if not has_annotations(obj):
        init_annotations(obj)

    annotations = get_annotations(obj)

    if annotation.repeatable:
        if annotation.key not in annotations:
            annotations[annotation.key] = dataclasses.replace(annotation, value = [annotation.value])
        else:
            annotations[annotation.key].value.append(annotation.value)
    else:
        annotations[annotation.key] = annotation

def annotation(key: str, /, **opts: bool):
    def decorate(func):
        def wrapper(*args, **kwargs):
            return Annotation(
                key = key,
                value = func(*args, **kwargs),
                **opts,
            )

        return wrapper

    return decorate

@dataclasses.dataclass
class Route:
    path: str
    method: str

@dataclasses.dataclass(frozen=True)
class Annotation:
    key: str
    value: typing.Any = None

    inherited: bool = False # NOTE: Should this apply to methods?
    repeatable: bool = False

    # TODO: Use a flag (e.g. None/False) to indicate *all* targets
    targets: typing.Tuple[type] = dataclasses.field(default_factory=lambda: (type, object))

    def __call__(self, obj):
        annotate(obj, self)

        return obj

@dataclasses.dataclass
class Annotater:
    annotations: typing.List[Annotation] = dataclasses.field(default_factory=list)

def description(description: str) -> Annotation:
    return Annotation('description', description, inherited=False, repeatable=True)

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
        Annotation('route', route, repeatable=True)
        for route in routes
    ]

    def wrapper(obj):
        for annotation in annotations:
            annotate(obj, annotation)

        return obj

    return wrapper

@route('/foo', '/bar', method='GET')
@route('/baz', '/bat', method='POST')
def foo():
    ...

print(foo._annotations_)

@annotation('my_annotation', inherited=True)
def my_annotation(this: str, that: str) -> str:
    return f'<{this=}, {that=}>'

@my_annotation('foo', 'bar')
def fn(x: int) -> int:
    return x * 10

print(fn._annotations_)