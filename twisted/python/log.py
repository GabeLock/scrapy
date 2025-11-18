class PythonLoggingObserver:
    def __init__(self, name="twisted"):
        self.name = name

    def start(self):
        return None

    def stop(self):
        return None


def startLoggingWithObserver(*args, **kwargs):
    return None
