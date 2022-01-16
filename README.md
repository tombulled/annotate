# label
Label objects

## Installation
```console
pip install git+https://github.com/tombulled/label@main
```

## Usage

### Marker Labels
A label that has no value
```python
import label

deprecated = label.marker('deprecated')

@deprecated
def foo():
    pass
```

```python
>>> foo.__labels__
{'deprecated': None}
```

### Single-Value Labels
A label that has a single value
```python
import label

priority = label.label('priority')

@priority(3)
def foo():
    pass
```

```python
>>> foo.__labels__
{'priority': 3}
```

### Multi-Value Labels
A label that has multiple values
```python
import label

metadata = label.label('metadata', hook=dict)

@metadata(author='sam', version='1.0.1')
def foo():
    pass
```

```python
>>> foo.__labels__
{'metadata': {'author': 'sam', 'version': '1.0.1'}}
```

### Advanced Labelling
```python
import label
import dataclasses

@dataclasses.dataclass
class Route:
    path: str
    method: str

route = label.label('routes', hook=Route, multi=True)

@route('/foo', method = 'GET')
@route('/bar', method = 'GET')
@route('/baz', method = 'GET')
def foo():
    pass
```

```python
>>> foo.__labels__
{'routes': [Route(path='/baz', method='GET'), Route(path='/bar', method='GET'), Route(path='/foo', method='GET')]}
```
