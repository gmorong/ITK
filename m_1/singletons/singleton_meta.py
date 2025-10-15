class SingletonMeta(type):
    _instance = {}

    def call(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class SingletonClass(metaclass=SingletonMeta):
    pass


a = SingletonClass()
b = SingletonClass()
print(a is b)
