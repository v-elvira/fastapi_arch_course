class BaseException(Exception):
    detail = 'Unexpected error'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = 'Object not found'


class NoFreeRoomException(BaseException):
    detail = 'No free rooms left'
