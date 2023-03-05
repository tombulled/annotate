# annotate
Python Annotation System

## About
Annotations are tags that store object metadata (e.g. for functions/classes)

## Installation
### From PyPI
```console
pip install tombulled-annotate
```
### From GitHub
```console
pip install git+https://github.com/tombulled/annotate@main
```

## Usage

### Marker
An annotation with a fixed value
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

### Annotation
An annotation with a configurable value
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

## Repeatable Annotation
An annotation that can be used to annotate the same object multiple times
```python
import annotate

@annotate.annotation(repeatable=True)
def tag(tag: str, /) -> str:
    return tag

@tag('awesome')
@tag('cool')
@tag('funky')
def foo():
    pass
```

```python
>>> annotate.get_annotations(foo)
{'tag': ['funky', 'cool', 'awesome']}
```

## Inherited Annotation
An annotation that gets added to subclasses of an annotated class
```python
import annotate

@annotate.annotation(inherited=True)
def identifier(identifier: str, /) -> str:
    return identifier

@identifier('abc')
class Class:
    pass

class Subclass(Class):
    pass
```

```python
>>> annotate.get_annotations(Class)
{'identifier': 'abc'}
>>> annotate.get_annotations(Subclass)
{'identifier': 'abc'}
```

## Targetted Annotation
An annotation that targets objects of specific types
```python
import annotate
import types

@annotate.annotation(targets=(types.FunctionType,))
def description(description: str, /) -> str:
    return description

@description('A really cool function')
def foo():
    pass
```

```python
>>> annotate.get_annotations(foo)
{'description': 'A really cool function'}
```

### Non-Stored Annotation
```python
import annotate

@annotate.annotation(stored=False)
def author(name: str, /) -> None:
    pass

@author('Tim')
def foo():
    pass
```

```python
>>> annotate.get_annotations(foo)
{}
```