import dataclasses
import typing

# NOTEs:
#   * Plumb in an event framework? e.g. @on(events.Annotate), @on(events.InheritAnnotations)

# errors
class TargetException(Exception): pass

# TODO: Move this implementation to `stash`
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

annotations = Attribute('_annotations_')

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

@dataclasses.dataclass
class Annotation:
    key: str
    value: typing.Any = None

    # NOTE(s):
    #   Should `inherited` apply to methods?
    #   Use a flag for `targets`(e.g. None/False) to indicate *all* targets

    inherited: bool = False
    repeatable: bool = False
    targets: typing.Tuple[type] = dataclasses.field(default_factory=lambda: (type, object))

    def __call__(self, obj):
        annotate(obj, self)

        return obj

    def is_targetted(self, obj) -> bool:
        return isinstance(obj, self.targets)

def annotate(obj, annotation):
    if not isinstance(obj, annotation.targets):
        raise TargetException('obj type not targetted by this annotation')

    if isinstance(obj, type) and not has_annotations(obj):
        orig_init_subclass = obj.__init_subclass__.__func__

        def init_subclass(cls, **kwargs):
            orig_init_subclass(cls, **kwargs)

            annotations = setdefault_annotations(cls, {})

            cls._annotations_ = {
                key: annotation
                for key, annotation in annotations.items()
                if annotation.inherited
            }
            
            return cls

        obj.__init_subclass__ = classmethod(init_subclass)

    annotations = setdefault_annotations(obj, {})

    if annotation.repeatable:
        if annotation.key not in annotations:
            annotations[annotation.key] = dataclasses.replace(annotation, value = [annotation.value])
        else:
            annotations[annotation.key].value.append(annotation.value)
    else:
        annotations[annotation.key] = annotation

def annotation(func: typing.Optional[typing.Callable] = None, /, **kwargs):
    if func is None:
        def wrapper(func):
            return annotation(func, **kwargs)

        return wrapper

    opts = {
        **dict(key=func.__name__),
        **kwargs
    }

    def wrapper(*args, **kwargs):
        return Annotation(
            **{
                **opts,
                **dict(value=func(*args, **kwargs)),
            }
        )

    return wrapper

def marker(func: typing.Optional[typing.Callable] = None, /, **kwargs):
    if func is None:
        def wrapper(func):
            return marker(func, **kwargs)

        return wrapper

    return annotation(func, **kwargs)()