import pytest
import types
import typing
import annotate

@pytest.fixture
def func() -> types.FunctionType:
    def foo():
        pass

    return foo

@pytest.fixture
def cls() -> type:
    class Foo:
        pass

    return Foo

@pytest.fixture
def annotation() -> annotate.Annotation:
    return annotate.Annotation('key', 'value')

@pytest.fixture
def annotations() -> typing.List[annotate.Annotation]:
    return [
        annotate.Annotation('key-a', 'value-a'),
        annotate.Annotation('key-b', 'value-b'),
        annotate.Annotation('key-c', 'value-c'),
    ]