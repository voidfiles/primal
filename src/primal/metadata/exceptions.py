
class PrimalMetadataException(Exception):
    pass


class ConditionalUpdateException(PrimalMetadataException):
    def __init__(self, cause, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.cause = cause
