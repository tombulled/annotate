from typing import Callable, Hashable, Tuple, TypeVar, overload

from typing_extensions import ParamSpec

from .models import Annotation

V = TypeVar("V")
PS = ParamSpec("PS")

@overload
def annotation(
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[PS, V]], Callable[PS, Annotation]]: ...
@overload
def annotation(
    *,
    key: Hashable,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[PS, V]], Callable[PS, Annotation]]: ...
@overload
def annotation(
    func: Callable[PS, V],
    /,
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[PS, Annotation]: ...
@overload
def annotation(
    func: Callable[PS, V],
    /,
    *,
    key: Hashable,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[PS, Annotation]: ...
@overload
def marker(
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[[], V]], Annotation]: ...
@overload
def marker(
    *,
    key: Hashable,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[[], V]], Annotation]: ...
@overload
def marker(
    func: Callable[[], V],
    /,
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Annotation: ...
@overload
def marker(
    func: Callable[[], V],
    /,
    *,
    key: Hashable,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Annotation: ...
