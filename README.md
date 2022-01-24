# annotate
Annotate objects

## Installation
```console
pip install git+https://github.com/tombulled/annotate@main
```

## Usage

### Marker Annotation
An annotation that has no value
```python
import annotate

deprecated = annotate.marker('deprecated')

@deprecated
def foo():
    pass
```

```python
>>> foo._annotations_
{'deprecated': None}
```

### Single-Value Annotation
An annotation that has a single value
```python
import annotate

priority = annotate.annotation('priority')

@priority(3)
def foo():
    pass
```

```python
>>> foo._annotations_
{'priority': 3}
```

### Multi-Value Annotation
An annotation that has multiple values
```python
import annotate

metadata = annotate.annotation('metadata', hook=dict)

@metadata(author='sam', version='1.0.1')
def foo():
    pass
```

```python
>>> foo._annotations_
{'metadata': {'author': 'sam', 'version': '1.0.1'}}
```

### Advanced Annotating
```python
import annotate
import dataclasses
import operator

@dataclasses.dataclass
class Route:
    path: str
    method: str

route = annotate.annotation(
    'route',
    hook = lambda *paths, **kwargs: [
        Route(path, **kwargs)
        for path in paths
    ],
    replace = operator.add
)

@route('/foo', '/bar', method='GET')
@route('/cat', '/dog', method='POST')
def foo():
    pass
```

```python
>>> foo._annotations_
{'route': [Route(path='/cat', method='POST'), Route(path='/dog', method='POST'), Route(path='/foo', method='GET'), Route(path='/bar', method='GET')]}
```
