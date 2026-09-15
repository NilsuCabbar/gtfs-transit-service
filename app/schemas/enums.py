from enum import IntEnum # IntEnum olduğunda Pydantic'te tanımlı olmayan bir sayı geldiğinde hata fırlatır

class RouteType(IntEnum):
    TRAM = 0
    SUBWAY = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_TRAM = 5
    AERIAL_LIFT = 6
    FUNICULAR = 7
    TROLLEYBUS = 11
    MONORAIL = 12

class StatusType(IntEnum):
    UPLOADING = 0
    VALIDATING = 1
    COMPLETED = 2
    FAILED = 3

class WheelchairBoardingType(IntEnum):
    NO_INFO = 0
    POSSIBLE = 1
    NOT_POSSIBLE = 2

class LocationType(IntEnum):
    STOP = 0
    STATION = 1
    ENTRANCE_EXIT = 2
    GENERIC_NODE = 3
    BOARDING_AREA = 4

class DirectionType(IntEnum):
    OUTBOUND = 0
    INBOUND = 1

class PickupType(IntEnum):
    REGULAR = 0
    NO_PICKUP = 1
    MUST_PHONE = 2
    MUST_COORDINATE = 3

class DropOffType(IntEnum):
    REGULAR = 0
    NO_DROPOFF = 1
    MUST_PHONE = 2
    MUST_COORDINATE = 3