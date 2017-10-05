
class Singleton(type):
    _instances = None
    
    def __call__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances