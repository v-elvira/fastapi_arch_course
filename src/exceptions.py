from datetime import date
from fastapi import HTTPException


class BaseException(Exception):
    detail = 'Unexpected error'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = 'Object not found'

class RoomNotFoundException(ObjectNotFoundException):
    detail = 'Room not found'

class HotelNotFoundException(ObjectNotFoundException):
    detail = 'Hotel not found'

class BookingNotFoundException(ObjectNotFoundException):
    detail = 'Booking not found'

class NoFreeRoomException(BaseException):
    detail = 'No free rooms left'

class ObjectExistsException(BaseException):
    detail = 'Object already exists'

class InvalidTokenException(BaseException):
    detail = 'Invalid token'

class ExpiredTokenException(BaseException):
    detail = 'Token expired'

class WrongEmailPasswordException(BaseException):
    detail = 'Wrong email/password'

class UserExistsException(ObjectExistsException):
    detail = 'User with this email already exists'

class NotAllowedException(BaseException):
    detail = 'Action is not allowed for user'

def check_date_to_is_after_date_from(date_from: date, date_to: date):
    if date_to < date_from:
        raise HTTPException(status_code=400, detail='Date from is later than date to')


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoomNotFoundHTTPException():
    status_code = 404
    detail = 'Room not found'

class HotelNotFoundHTTPException():
    status_code = 404
    detail = 'Hotel not found'

class InvalidTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = 'Invalid token'

class ExpiredTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = 'Token expired'

class WrongEmailPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail='Wrong email/password'

class UserExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = f'User with this email already exists'

class NoFreeRoomHTTPException(BaseHTTPException):
    status_code = 409
    detail = 'No free rooms left'

class BookingNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = 'Booking not found'

class BookingEditingNotAllowedHTTPException(BaseHTTPException):
    status_code = 401
    detail = 'Current user has no right to edit this booking'
