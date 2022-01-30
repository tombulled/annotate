
def decorate(cls):
    cls._annotations_ = {'description': 'awesome cls!'}

    return cls

@decorate
class Foo:
    def __init_subclass__(cls) -> None:
        print(f'__init_subclass__({cls=})')
        
        cls._annotations_ = {}

class Bar(Foo): pass

print(Foo._annotations_)
print(Bar._annotations_)