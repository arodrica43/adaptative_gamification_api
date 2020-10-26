from rest_framework import serializers
import json

class EnumField(serializers.ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        kwargs['choices'] = [(e.name, e.name) for e in enum]
        super(EnumField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return obj.name

    def to_internal_value(self, data):
        try:
            return self.enum[data]
        except KeyError:
            self.fail('invalid_choice', input=data)

class JSONSerializerField(serializers.JSONField):
    class json_dict(dict):
        def __str__(self):
            return json.dumps(self)
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        #print("data", data)
        if data:
            res = json.loads(data)
            return res
        else: return None
    def to_representation(self, value):
        #print("value",json.loads(json.dumps(value)))
        return self.json_dict(value)