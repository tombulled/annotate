# label
Label objects

## Usage
```python
>>> import label
```

### Basic labelling
```python
@label('awesome')
def foo(): pass

@label('priority', 3)
def bar(): pass

cool = label('cool')

@cool
def baz(): pass

>>> foo.__labels__
{'awesome': None}
>>>
>>> bar.__labels__
{'priority': 3}
>>>
>>> baz.__labels__
{'cool': None}
```

### Advanced labelling
```python
import dataclasses
import sentinel
import label

@dataclasses.dataclass
class RouteModel:
    path: str
    method: str

class Test(sentinel.Sentinel): pass
class Profile(sentinel.Sentinel): pass
class Route(sentinel.Sentinel): pass

test = label(Test)
profile = label.labeller(Profile)
route = label.labeller(Route, hook = RouteModel)

@test
@profile('dev')
@route('/', method = 'GET')
def foo(): pass

>>> foo.__labels__
{Route: RouteModel(path='/', method='GET'), Profile: 'dev', Test: None}
```
