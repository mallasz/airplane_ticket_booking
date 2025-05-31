# The Singleton metaclass ensures that only one instance of a class exists.
class Singleton(type):
    # Dictionary to store instances of classes using this metaclass
    _instances = {}

    # The __call__ method is invoked when a class is called to create a new instance.
    # If an instance already exists for the class, it returns the existing instance.
    # Otherwise, it creates a new one, stores it, and returns it.
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
