class ImpossibleScrambleException(Exception):
    """ Exception raised when encountering an impossible solve """

class ParityException(Exception):
    """ Exception raised when encountering parity """

class InvalidTurnException(Exception):
    """ Exception raised when the turn cannot be made """
