class Interface:
    pass


def implementer(*interfaces):
    def decorator(cls):
        return cls

    return decorator


def provider(*interfaces):
    def decorator(obj):
        return obj

    return decorator
