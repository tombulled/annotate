import dataclasses
from typing import Any, Hashable, MutableMapping, Sequence

from . import attributes
from .models import Annotation

__all__: Sequence[str] = (
    "get_raw_annotations",
    "has_annotations",
    "set_annotations",
    "del_annotations",
    "setdefault_annotations",
    "get_annotations",
    "has_annotation",
    "get_annotation",
    "set_annotation",
    "del_annotation",
)

get_raw_annotations = attributes.annotations.get
has_annotations = attributes.annotations.has
set_annotations = attributes.annotations.set
del_annotations = attributes.annotations.delete
setdefault_annotations = attributes.annotations.setdefault


def get_annotations(obj: Any) -> MutableMapping[Hashable, Any]:
    return {
        annotation.key: annotation.value
        for annotation in get_raw_annotations(obj).values()
    }


def has_annotation(obj: Any, key: Hashable, /) -> bool:
    return key in get_annotations(obj)


def get_annotation(obj: Any, key: Hashable, default: Any = None, /) -> Any:
    return get_annotations(obj).get(key, default)


def set_annotation(obj: Any, key: Hashable, value: Any, /) -> None:
    annotations: MutableMapping[Hashable, Annotation] = get_annotations(obj)

    if key in annotations:
        annotations[key] = dataclasses.replace(annotations[key], value=value)
    else:
        annotations[key] = Annotation(key=key, value=value)


def del_annotation(obj: Any, key: Hashable, /) -> None:
    del get_annotations(obj)[key]
