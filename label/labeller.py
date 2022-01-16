import functools
import typing
import dataclasses
import typing


@dataclasses.dataclass
class Labeller:
    attr: str = "__labels__"

    def marker(self, key: typing.Any, /) -> typing.Callable:
        return self.label(key)(None)

    def label(
        self,
        key: typing.Any,
        /,
        *,
        hook: typing.Optional[typing.Callable] = None,
        multi: bool = False,
        overwrite: bool = True,
    ) -> typing.Callable:
        def decorate(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable:
            def wrapper(obj: typing.T, /) -> typing.T:
                value: typing.Any
                labels: dict = self.get(obj)

                if hook is not None:
                    value = hook(*args, **kwargs)
                else:
                    if len(args) != 1 or kwargs:
                        raise Exception(
                            "Multiple arguments provided without specifying a hook"
                        )

                    value = args[0]

                if overwrite or key not in labels:
                    if multi:
                        labels.setdefault(key, [])

                        labels[key].append(value)
                    else:
                        labels[key] = value

                return obj

            return wrapper

        return decorate

    def init(self, obj: typing.Any, /) -> None:
        if not hasattr(obj, self.attr):
            setattr(obj, self.attr, {})

    def get(self, obj: typing.Any, /, *, init: bool = True) -> typing.Optional[dict]:
        if init:
            self.init(obj)

        return getattr(obj, self.attr, None)
