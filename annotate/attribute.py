import dataclasses
import typing
import stash


@dataclasses.dataclass
class Annotations(stash.DefaultedAttribute):
    name: str = "_annotations_"
    factory: typing.Callable = dict


annotations = Annotations()
