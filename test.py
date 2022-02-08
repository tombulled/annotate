import annotate
from annotate import marker, annotation

@marker
def deprecated() -> bool:
    return True

@deprecated
def foo(): ...

assert annotate.get_annotations(foo) == {'deprecated': True}

print('All tests passed.')