import datetime
import json
import uuid

_original_encoder = json.encoder.JSONEncoder


class CommerceEncoder(_original_encoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super(CommerceEncoder, self).default(obj)

    def encode(self, obj):
        return super(CommerceEncoder, self).encode(obj)