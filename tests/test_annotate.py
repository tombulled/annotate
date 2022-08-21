from types import FunctionType
import pytest
import annotate
from annotate import Annotation
from typing import List, TypeVar

V = TypeVar("V")


def test_annotate_single(func: FunctionType, annotation: Annotation) -> None:
    annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {annotation.key: annotation}


def test_annotate_multiple(func: FunctionType, annotations: List[Annotation]) -> None:
    annotation: Annotation
    for annotation in annotations:
        annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {
        annotation.key: annotation for annotation in annotations
    }


def test_annotate_inherited(cls: type) -> None:
    annotation_a: Annotation[str, str] = Annotation("key-a", "value-a", inherited=False)
    annotation_b: Annotation[str, str] = Annotation("key-b", "value-b", inherited=True)

    annotate.annotate(cls, annotation_a)
    annotate.annotate(cls, annotation_b)

    subcls: type = type("subcls", (cls,), {})

    assert annotate.get_raw_annotations(subcls) == {annotation_b.key: annotation_b}


def test_annotate_repeated(func: FunctionType) -> None:
    def build_annotation(value: V, /) -> Annotation[str, V]:
        return Annotation("key", value, repeatable=True)

    annotations: List[Annotation[str, int]] = [
        build_annotation(value) for value in range(3)
    ]

    annotation: Annotation[str, int]
    for annotation in annotations:
        annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {
        annotations[0].key: build_annotation(
            [annotation.value for annotation in annotations]
        )
    }


def test_annotate_targetted(func: FunctionType) -> None:
    annotation_func: Annotation[str, str] = Annotation(
        "key-a", "value-a", targets=(FunctionType,)
    )
    annotation_type: Annotation[str, str] = Annotation(
        "key-b", "value-b", targets=(type,)
    )

    annotate.annotate(func, annotation_func)

    with pytest.raises(TypeError):
        annotate.annotate(func, annotation_type)


def test_annotate_not_stored(func: FunctionType) -> None:
    annotation: Annotation[str, str] = Annotation("key", "value", stored=False)

    annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {}
