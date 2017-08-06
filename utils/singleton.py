
class SingletonInstane(type):

    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance

        except AttributeError:
            cls.__instance = super(SingletonInstane).__call__(*args, **kwargs)
            return cls.__instance