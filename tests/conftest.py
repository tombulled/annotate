import pytest
import types
import typing
import annotate


@pytest.fixture
def func() -> types.FunctionType:
    def foo():
        ...

    return foo


@pytest.fixture
def cls() -> type:
    class Foo:
        ...

    return Foo


@pytest.fixture
def annotation() -> annotate.Annotation:
    return annotate.Annotation("key", "value")


@pytest.fixture
def annotations() -> typing.List[annotate.Annotation]:
    return [annotate.Annotation(f"key-{index}", f"value-{index}") for index in range(3)]
