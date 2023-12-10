class UnsupportedConfigItemError(Exception):
    """
    Unsupported config item error.

    The manifest and configuration specified an item which the SDK is incapable of handling yet.
    """

    pass
