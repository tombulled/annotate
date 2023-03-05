from typing import Callable, Hashable, Optional, Sequence, Tuple, TypeVar, Union

from typing_extensions import ParamSpec

from .models import Annotation

__all__: Sequence[str] = (
    "annotation",
    "marker",
)

V = TypeVar("V")
PS = ParamSpec("PS")


def annotation(
    func: Optional[Callable[PS, V]] = None,
    /,
    *,
    key: Optional[Hashable] = None,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Union[
    Callable[[Callable[PS, V]], Callable[PS, Annotation]],
    Callable[PS, Annotation],
]:
    def decorator(func: Callable[PS, V], /) -> Callable[PS, Annotation]:
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> Annotation:
            return Annotation(
                key=key if key is not None else func.__name__,
                value=func(*args, **kwargs),
                inherited=inherited,
                repeatable=repeatable,
                stored=stored,
                targets=targets,
            )

        return wrapper

    if func is None:
        return decorator

    return decorator(func)


def marker(
    func: Optional[Callable[[], V]] = None,
    /,
    *,
    key: Optional[Hashable] = None,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Union[Callable[[Callable[[], V]], Annotation], Annotation]:
    def decorator(func: Callable[[], V], /) -> Annotation:
        return Annotation(
            key=key if key is not None else func.__name__,
            value=func(),
            inherited=inherited,
            repeatable=repeatable,
            stored=stored,
            targets=targets,
        )

    if func is None:
        return decorator

    return decorator(func)
