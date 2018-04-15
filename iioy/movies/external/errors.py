class BaseExternalError(Exception):
    pass


class NoDataFoundError(BaseExternalError):
    pass


class HardError(BaseExternalError):
    """The api is being rate limited or something else."""
    pass


class NotFoundHardError(HardError):
    pass
