import pickle


class RestrictedUnpickler(pickle.Unpickler):
    """
    This class is used more secure way to load pickle files.

    See: https://docs.python.org/3/library/pickle.html#restricting-globals
    """

    def find_class(self, module, name):
        raise pickle.UnpicklingError(
            "There is something strange in the file, do not trust it!"
        )
