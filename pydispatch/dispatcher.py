_listeners = {}


class Anonymous:
    pass


class Any:
    pass


def connect(receiver, signal=None, sender=None):
    _listeners.setdefault(signal, []).append(receiver)


def disconnect(receiver, signal=None, sender=None):
    receivers = _listeners.get(signal, [])
    if receiver in receivers:
        receivers.remove(receiver)


def send(signal=None, sender=None, **kwargs):
    for receiver in _listeners.get(signal, []):
        receiver(signal=signal, sender=sender, **kwargs)


def getAllReceivers(signal=None, sender=None):
    return list(_listeners.get(signal, []))


def liveReceivers(signal=None, sender=None):
    return getAllReceivers(signal, sender)
