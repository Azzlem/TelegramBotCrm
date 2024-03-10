from enum import Enum


class Status(Enum):
    ACCEPTED = 0
    APPOINTED = 1
    IN_WORK = 2
    DEVICE_IN_SERVICE = 3
    PAID = 4
    ISSUED_TO_CUSTOMER = 5
    CLOSED = 6

