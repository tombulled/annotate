from typing import Any, Callable, Hashable, Tuple, TypeVar, overload

from typing_extensions import ParamSpec

from .models import Annotation

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
PS = ParamSpec("PS")

@overload
def annotation(
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[PS, V]], Callable[PS, Annotation[str, V]]]: ...
@overload
def annotation(
    *,
    key: K,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[PS, V]], Callable[PS, Annotation[K, V]]]: ...
@overload
def annotation(
    func: Callable[PS, V],
    /,
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[PS, Annotation[str, V]]: ...
@overload
def annotation(
    func: Callable[PS, V],
    /,
    *,
    key: K,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[PS, Annotation[K, V]]: ...
@overload
def marker(
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[[], V]], Annotation[str, V]]: ...
@overload
def marker(
    *,
    key: K,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Callable[[Callable[[], V]], Annotation[K, V]]: ...
@overload
def marker(
    func: Callable[[], V],
    /,
    *,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Annotation[Any, V]: ...
@overload
def marker(
    func: Callable[[], V],
    /,
    *,
    key: K,
    inherited: bool = False,
    repeatable: bool = False,
    stored: bool = True,
    targets: Tuple[type, ...] = (type, object),
) -> Annotation[K, V]: ...
