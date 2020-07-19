class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class TypeError(Error):
    def __init__(self, message):
        self.message = message

class BinTreeRootError(Error):
    def __init__(self, message):
        self.message = message

class IntersectError(Error):
    def __init__(self, message):
        self.message = message

class AssumptionError(Error):
    def __init__(self, message):
        self.message = message

class CurvatureError(Error):
    def __init__(self, message):
        self.message = message
