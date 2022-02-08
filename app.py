import annotate
import dataclasses

@dataclasses.dataclass
class Route:
    path: str
    method: str

def route(*paths: str, **kwargs: str):
    def wrapper(obj):
        for path in paths:
            annotate.annotate(
                obj,
                annotate.Annotation(
                    key='route',
                    value=Route(path, **kwargs),
                    repeatable=True,
                ),
            )

        return obj

    return wrapper

@route('/foo', '/bar', method='GET')
@route('/cat', '/dog', method='POST')
def foo():
    pass