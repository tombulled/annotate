import dataclasses
import types
import typing

# NOTE(s):
#   Plumb in an event framework? e.g. @on(events.Annotate), @on(events.InheritAnnotations)
#   Should `inherited` apply to methods?
#   Use a flag for `targets`(e.g. None/False) to indicate *all* targets
#   Python 3.8 or 3.9?

# TODO:
#   Move `Attribute` implementation to `stash` (and add `stash` as a dependency)

@dataclasses.dataclass
class Attribute:
    attr: str

    def get(self, obj):
        return getattr(obj, self.attr)

    def delete(self, obj) -> None:
        delattr(obj, self.attr)

    def has(self, obj) -> bool:
        return hasattr(obj, self.attr)

    def set(self, obj, val) -> None:
        setattr(obj, self.attr, val)

    def setdefault(self, obj, default=None):
        if self.has(obj):
            return self.get(obj)

        self.set(obj, default)

        return default


annotations = Attribute("_annotations_")

get_raw_annotations = annotations.get
has_annotations = annotations.has
set_annotations = annotations.set
del_annotations = annotations.delete
setdefault_annotations = annotations.setdefault


def get_annotations(obj):
    return {
        annotation.key: annotation.value
        for annotation in get_raw_annotations(obj).values()
    }


@dataclasses.dataclass(frozen=True)
class Annotation:
    key: str
    value: typing.Any = None
    inherited: bool = False
    repeatable: bool = False
    targets: typing.Tuple[type] = dataclasses.field(
        default_factory=lambda: (type, object)
    )

    def __call__(self, obj):
        annotate(obj, self)

        return obj

    def is_targetted(self, obj) -> bool:
        return isinstance(obj, self.targets)

    def is_compatible(self, annotation) -> bool:
        return dataclasses.replace(self, value=None) == dataclasses.replace(
            annotation, value=None
        )


def decorate(cls: type) -> type:
    orig_init_subclass = (
        cls.__init_subclass__.__func__
        if not isinstance(cls.__init_subclass__, types.BuiltinMethodType)
        else None
    )

    @classmethod
    def init_subclass(subcls, **kwargs):
        if orig_init_subclass is not None:
            orig_init_subclass(subcls, **kwargs)

        annotations = setdefault_annotations(subcls, {})

        set_annotations(
            subcls,
            {
                key: annotation
                for key, annotation in annotations.items()
                if annotation.inherited
            },
        )

        return subcls

    cls.__init_subclass__ = init_subclass


def annotate(obj: typing.Any, annotation: Annotation, /, *, force: bool = False, repeat: bool = True) -> None:
    if not annotation.is_targetted(obj) and not force:
        raise TypeError(
            f"object with type {type(obj)} not targetted by annotation {annotation!r}"
        )

    if isinstance(obj, type) and not has_annotations(obj):
        decorate(obj)

    annotations = setdefault_annotations(obj, {})

    if annotation.repeatable and repeat:
        if annotation.key not in annotations:
            annotation = dataclasses.replace(annotation, value=[annotation.value])
        else:
            if not annotations[annotation.key].is_compatible(
                annotation
            ):
                raise ValueError("new annotation cannot merge with existing, repeatable annotation due to conflicting options")

            annotation = dataclasses.replace(
                annotation, value=annotations[annotation.key].value + [annotation.value]
            )

    annotations[annotation.key] = annotation


def annotation(func: typing.Optional[typing.Callable] = None, /, **opts: typing.Any):
    if func is None:

        def wrapper(func):
            return annotation(func, **opts)

        return wrapper

    def wrapper(*args, **kwargs):
        return Annotation(
            **(dict(key=func.__name__) | opts | dict(value=func(*args, **kwargs)))
        )

    return wrapper


def marker(func: typing.Optional[typing.Callable] = None, /, **opts: typing.Any):
    if func is None:

        def wrapper(func):
            return marker(func, **opts)

        return wrapper

    return annotation(func, **opts)()
