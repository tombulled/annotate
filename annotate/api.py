import dataclasses
from types import BuiltinMethodType, MethodType
from typing import Any, Callable, Hashable, MutableMapping, Optional, Sequence, cast

from . import attributes
from .models import Annotation

__all__: Sequence[str] = ("annotate",)


def _hook(cls: type, /) -> None:
    original_init_subclass: Optional[Callable[..., type]] = None

    if not isinstance(cls.__init_subclass__, BuiltinMethodType):
        original_init_subclass = cast(MethodType, cls.__init_subclass__).__func__

    def init_subclass(subcls: type, **kwargs: Any) -> type:
        if original_init_subclass is not None:
            original_init_subclass(subcls, **kwargs)

        annotations: MutableMapping[Hashable, Any] = attributes.annotations.setdefault(
            subcls
        )

        attributes.annotations.set(
            subcls,
            {
                key: annotation
                for key, annotation in annotations.items()
                if annotation.inherited
            },
        )

        return subcls

    cls.__init_subclass__ = classmethod(init_subclass)  # type: ignore


def annotate(
    obj: Any,
    annotation: Annotation,
    /,
    *,
    force: bool = False,
    repeat: bool = True,
) -> None:
    if not annotation.is_targetted(obj) and not force:
        raise TypeError(
            f"object with type {type(obj)} not targetted by annotation {annotation!r}"
        )

    if not annotation.stored:
        return obj

    if isinstance(obj, type) and not attributes.annotations.has(obj):
        _hook(obj)

    annotations: MutableMapping[Hashable, Any] = attributes.annotations.setdefault(obj)

    if annotation.repeatable and repeat:
        if annotation.key not in annotations:
            annotation = dataclasses.replace(annotation, value=[annotation.value])
        else:
            if not annotations[annotation.key].is_compatible(annotation):
                raise ValueError(
                    "new annotation cannot merge with existing, repeatable annotation due to conflicting options"
                )

            annotation = dataclasses.replace(
                annotation, value=annotations[annotation.key].value + [annotation.value]
            )

    annotations[annotation.key] = annotation
