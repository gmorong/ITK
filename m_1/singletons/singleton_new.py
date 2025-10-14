class Singleton:
    _instance = {}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
a = Singleton()
b = Singleton()
print (a is b)