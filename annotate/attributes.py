from typing import Sequence

from attribute import Attribute

__all__: Sequence[str] = ("annotations",)

annotations: Attribute = Attribute("_annotations_", default_factory=dict)
