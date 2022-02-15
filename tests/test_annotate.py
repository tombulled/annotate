import pytest
import annotate
import types
import typing


def test_annotate_single(
    func: types.FunctionType, annotation: annotate.Annotation
) -> None:
    annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {annotation.key: annotation}


def test_annotate_multiple(
    func: types.FunctionType, annotations: typing.List[annotate.Annotation]
) -> None:
    annotation: annotate.Annotation
    for annotation in annotations:
        annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {
        annotation.key: annotation for annotation in annotations
    }


def test_annotate_inherited(cls: type) -> None:
    annotation_a: annotate.Annotation = annotate.Annotation(
        "key-a", "value-a", inherited=False
    )
    annotation_b: annotate.Annotation = annotate.Annotation(
        "key-b", "value-b", inherited=True
    )

    annotate.annotate(cls, annotation_a)
    annotate.annotate(cls, annotation_b)

    class Subclass(cls):
        ...

    assert annotate.get_raw_annotations(Subclass) == {annotation_b.key: annotation_b}


def test_annotate_repeated(func: types.FunctionType) -> None:
    def build_annotation(value: int) -> annotate.Annotation:
        return annotate.Annotation("key", value, repeatable=True)

    annotations: typing.List[annotate.Annotation] = [
        build_annotation(value) for value in range(3)
    ]

    annotation: annotate.Annotation
    for annotation in annotations:
        annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {
        annotations[0].key: build_annotation(
            [annotation.value for annotation in annotations]
        )
    }


def test_annotate_targetted(func: types.FunctionType) -> None:
    annotation_func: annotate.Annotation = annotate.Annotation(
        "key-a", "value-a", targets=(types.FunctionType,)
    )
    annotation_type: annotate.Annotation = annotate.Annotation(
        "key-b", "value-b", targets=(type,)
    )

    annotate.annotate(func, annotation_func)

    with pytest.raises(TypeError):
        annotate.annotate(func, annotation_type)

def test_annotate_not_stored(func: types.FunctionType) -> None:
    annotation: annotate.Annotation = annotate.Annotation('key', 'value', stored=False)

    annotate.annotate(func, annotation)

    assert annotate.get_raw_annotations(func) == {}