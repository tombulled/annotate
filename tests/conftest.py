from types import FunctionType
from typing import List, cast

from pytest import fixture

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
def annotation() -> Annotation:
    return Annotation("key", "value")


@fixture
def annotations() -> List[Annotation]:
    return [Annotation(f"key-{index}", f"value-{index}") for index in range(3)]
