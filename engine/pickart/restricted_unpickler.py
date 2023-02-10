import pickle


class RestrictedUnpickler(pickle.Unpickler):
    """
    This class is used for security reasons instead of pickle.load().

    See: https://docs.python.org/3/library/pickle.html#restricting-globals
    """

    def find_class(self, module, name):
        raise pickle.UnpicklingError(
            "There is something strange in the file, don't trust it!"
        )
