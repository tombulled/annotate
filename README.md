# annotate
Python Annotation System Inspired by Java Annotations

## Installation
```console
pip install git+https://github.com/tombulled/annotate@v0.1.2
```

## Usage

### Marker Annotation
An annotation that has a specific, known value
```python
import annotate

@annotate.marker
def deprecated() -> bool:
    return True

@deprecated
def foo():
    pass
```

```python
>>> annotate.get_annotations(foo)
{'deprecated': True}
```

### Single-Value Annotation
An annotation that has a single, configurable value
```python
import annotate

@annotate.annotation
def description(description: str, /) -> str:
    return description

@description('Really awesome function!')
def foo():
    pass
```

```python
>>> annotate.get_annotations(foo)
{'description': 'Really awesome function!'}
```

### Multi-Value Annotation
An annotation that has multiple, configurable values
```python
import annotate

@annotate.annotation
def metadata(*, author: str, version: str) -> dict:
    return dict(
        author = author,
        version = version,
    )

@metadata(author='sam', version='1.0.1')
def foo():
    pass
```

```python
>>> annotate.get_annotations(foo)
{'metadata': {'author': 'sam', 'version': '1.0.1'}}
```

### Advanced Annotating
```python
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
```

```python
>>> annotate.get_annotations(foo)
{'route': [Route(path='/cat', method='POST'), Route(path='/dog', method='POST'), Route(path='/foo', method='GET'), Route(path='/bar', method='GET')]}
```
