import json
from dataclasses import is_dataclass
from datetime import datetime
from decimal import Decimal
from functools import partial


class NoSerializerMatch(Exception):
    pass


class GlobalEncoder(json.JSONEncoder):
    def __init__(self, *args, extra_serializer=None, **kwargs):
        super(GlobalEncoder, self).__init__(*args, **kwargs)

        self.extra_serializer = extra_serializer

    def default(self, o):
        if self.extra_serializer:
            try:
                return self.extra_serializer(o)
            except NoSerializerMatch:
                pass

        if isinstance(o, datetime):
            return {"_type": o.__class__.__name__, "value": o.isoformat()}
        elif isinstance(o, set):
            return {"_type": o.__class__.__name__, "value": list(o)}
        elif isinstance(o, Decimal):
            return {"_type": o.__class__.__name__, "value": str(o)}
        elif is_dataclass(o):
            return {"_type": o.__class__.__name__, "value": o.__dict__}
        else:
            raise Exception(f"Unknown `{o.__class__.__name__}` type")


def serialize(obj, indent=None, extra_serializer=None):
    return (
        GlobalEncoder(indent=indent, extra_serializer=extra_serializer)
        .encode(obj)
        .encode("utf-8")
    )


def _global_decoder(obj, extra_deserializer):
    if extra_deserializer:
        try:
            return extra_deserializer(obj)
        except NoSerializerMatch:
            pass

    if obj_type := obj.get("_type"):
        obj_value = obj["value"]

        if obj_type == "set":
            return set(obj_value)
        elif obj_type == "datetime":
            return datetime.fromisoformat(obj_value)
        elif obj_type == "Decimal":
            return Decimal(obj_value)
        else:
            raise Exception(f"Unknown `{obj_type}` type")

    return obj


def deserialize(obj, extra_deserializer=None):
    return json.loads(
        obj, object_hook=partial(_global_decoder, extra_deserializer=extra_deserializer)
    )
