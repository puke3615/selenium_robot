class NotFoundException(Exception):
    pass


class TooManyElementsException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(*args, **kwargs)


class IllegalArgumentException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(*args, **kwargs)
