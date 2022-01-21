import typing
import dataclasses
import typing

from . import replacers
from . import hooks


@dataclasses.dataclass
class Annotater:
    attr: str = "_annotations_"

    def marker(self, key: typing.Any, /) -> typing.Callable:
        return self.label(key)(None)

    def label(
        self,
        key: typing.Any,
        /,
        *,
        hook: typing.Callable = hooks.identity,
        replace: typing.Callable = replacers.new,
    ) -> typing.Callable:
        def decorate(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable:
            def wrapper(obj: typing.T, /) -> typing.T:
                value: typing.Any = hook(*args, **kwargs)

                labels: dict = self.get(obj)

                if labels is None:
                    self.init(obj)

                    labels: dict = self.get(obj)

                if key in labels:
                    value = replace(labels[key], value)

                labels[key] = value

                return obj

            return wrapper

        return decorate

    def init(self, obj: typing.Any, /) -> None:
        if not hasattr(obj, self.attr):
            setattr(obj, self.attr, {})

    def get(self, obj: typing.Any, /) -> typing.Optional[dict]:
        return getattr(obj, self.attr, None)
