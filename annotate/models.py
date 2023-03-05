import dataclasses
from dataclasses import dataclass
from typing import Any, Generic, Hashable, Sequence, Tuple, TypeVar

from . import api

__all__: Sequence[str] = ("Annotation",)

T = TypeVar("T")


@dataclass(frozen=True)
class Annotation(Generic[T]):
    key: Hashable
    value: Any = None
    inherited: bool = False
    repeatable: bool = False
    stored: bool = True
    targets: Tuple[type, ...] = (type, object)

    def __call__(self, obj: T) -> T:
        api.annotate(obj, self)

        return obj

    def is_targetted(self, obj: Any) -> bool:
        return isinstance(obj, self.targets)

    def is_compatible(self, annotation: "Annotation") -> bool:
        return dataclasses.replace(self, value=None) == dataclasses.replace(
            annotation, value=None
        )
