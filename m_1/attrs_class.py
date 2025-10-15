import datetime


class CreatedAtMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace["created_at"] = datetime.datetime.now()
        return super().__new__(cls, name, bases, namespace)


class MyClass(metaclass=CreatedAtMeta):
    pass


print(MyClass.created_at)
