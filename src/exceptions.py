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

class UnknownFacilityError(BaseException):
    detail = 'Unknown id in facilities_ids list'

def check_date_to_is_after_date_from(date_from: date, date_to: date):  # may be moving this to schemas would be better?
    if date_to <= date_from:
        raise HTTPException(status_code=400, detail='Date to must be later than date from')


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = 'Room not found'

class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = 'Hotel not found'

class HotelExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = 'Hotel with the same data already exists'

class FacilityExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = 'Facility already exists'

class InvalidTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = 'Invalid token'

class ExpiredTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = 'Token expired'

class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail='No access token provided'

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

class FacilityNotFoundHTTPError(BaseHTTPException):
    status_code = 404
    detail = 'Facility not found (unknown facility id)'

class FailedToDeleteHTTPException(BaseHTTPException):
    status_code = 409
    detail = 'Failed to delete'
