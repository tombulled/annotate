def decorate(cls):
    orig_init_subclass = cls.__init_subclass__.__func__

    print(f'{orig_init_subclass=}')

    def init_subclass(subcls, **kwargs):
        orig_init_subclass(subcls, **kwargs)
        
        print(f'decorate.init_subclass({subcls=}, {kwargs=})')

    cls.__init_subclass__ = classmethod(init_subclass)

    cls._annotations_ = {'description': 'awesome cls!'}

    return cls

@decorate
class Foo:
    def __init_subclass__(cls) -> None:
        print(f'Foo.__init_subclass__({cls=})')
        
        cls._annotations_ = {}

class Bar(Foo): pass

print(Foo._annotations_)
print(Bar._annotations_)