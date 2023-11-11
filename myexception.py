"""custom exceptions"""
class LogicException (Exception):
    """invalid logic (e.g. state of the object called)"""
    def __init__(self, message: str):
        pass
