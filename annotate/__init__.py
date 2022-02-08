from .api import annotate
from .attribute import annotations
from .models import Annotation
from .decorators import annotation, marker

# NOTE(s):
#   Plumb in an event framework? e.g. @on(events.Annotate), @on(events.InheritAnnotations)
#   Should `inherited` apply to methods?
#   Use a flag for `targets`(e.g. None/False) to indicate *all* targets
#   Python 3.8 or 3.9?

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
