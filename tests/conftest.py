from types import FunctionType
from pytest import fixture
from typing import List, cast
from annotate import Annotation


@fixture
def func() -> FunctionType:
    def foo() -> None:
        pass

    return cast(FunctionType, foo)


@fixture
def cls() -> type:
    class Foo:
        pass

    return Foo


@fixture
def annotation() -> Annotation[str, str]:
    return Annotation("key", "value")


@fixture
def annotations() -> List[Annotation[str, str]]:
    return [Annotation(f"key-{index}", f"value-{index}") for index in range(3)]
