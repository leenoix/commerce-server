from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)

    @classmethod
    def keys(cls):
        return tuple((x.name for x in cls))

    @classmethod
    def key_pairs(cls):
        return {x.name: x.name for x in cls}

    @classmethod
    def value_by_key(cls, key):
        if not hasattr(cls, key):
            return ''
        return getattr(cls, key).value
