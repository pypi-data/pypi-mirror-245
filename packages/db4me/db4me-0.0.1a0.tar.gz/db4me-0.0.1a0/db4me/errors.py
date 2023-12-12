class Db4MeError(Exception):
    """Base class for exceptions in this module."""

    pass


class ConfigurationError(Db4MeError):
    """Raised when there is an error in the configuration file."""

    pass
