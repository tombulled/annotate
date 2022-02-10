import annotate
import types

def test_marker(func: types.FunctionType) -> None:
    def marker() -> int:
        return 123

    assert annotate.marker(marker) == annotate.Annotation(
        key=marker.__name__,
        value=marker(),
    )

def test_annotation(func: types.FunctionType) -> None:
    def annotation(a: int, b: str) -> dict:
        return dict(
            a = a,
            b = b,
        )

    value: dict = dict(a = 123, b = 'abc')

    assert annotate.annotation(annotation)(**value) == annotate.Annotation(
        key=annotation.__name__,
        value=value,
    )