from typing import Any, Dict

import annotate


def test_marker() -> None:
    def marker() -> int:
        return 123

    assert annotate.marker(marker) == annotate.Annotation(
        key=marker.__name__,
        value=marker(),
    )


def test_annotation() -> None:
    def annotation(*, a: int, b: str) -> Dict[str, Any]:
        return dict(
            a=a,
            b=b,
        )

    value: Dict[str, Any] = dict(a=123, b="abc")

    assert annotate.annotation(annotation)(**value) == annotate.Annotation(
        key=annotation.__name__,
        value=value,
    )
