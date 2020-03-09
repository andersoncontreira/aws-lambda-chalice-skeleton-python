from enum import Enum, IntEnum


class CustomEnum(Enum):
    @classmethod
    def get_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def get_codes(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def from_value(cls, value):
        for e in cls:
            # print(e.value, value, e.value == value)
            if isinstance(e.value, tuple):
                if e.value[0] == value:
                    return e
                elif e.value == value:
                    return e
            elif e.value == value:
                return e
        return None

    @classmethod
    def from_code(cls, code):
        for e in cls:
            if e.name == code:
                return e
        return None


class CustomIntEnum(IntEnum):
    @classmethod
    def get_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def get_codes(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def from_value(cls, value):
        for e in cls:
            # print(e.value, value, e.value == value)
            if isinstance(e.value, tuple):
                if e.value[0] == value:
                    return e
                elif e.value == value:
                    return e
            elif e.value == value:
                return e
        return None

    @classmethod
    def from_code(cls, code):
        for e in cls:
            if e.name == code:
                return e
        return None


class CustomStringEnum(CustomEnum):
    @classmethod
    def from_description(cls, description):
        for e in cls:
            if e.description == description:
                return e
        return None


