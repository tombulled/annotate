from .annotater import Annotater

ANNOTATER = Annotater()

marker = ANNOTATER.marker
annotation = ANNOTATER.annotation
init = ANNOTATER.init
get = ANNOTATER.get

def set(obj, key, value):
    init(obj)
    get(obj)[key] = value

def has(obj) -> bool:
    return hasattr(obj, ANNOTATER.attr)