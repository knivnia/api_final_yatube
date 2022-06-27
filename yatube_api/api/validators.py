from rest_framework import serializers


class SelfFollowValidator:
    """Class-based validator for unique model fields."""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, attrs):
        attrs_list = set()
        for field in self.fields:
            attrs_list.add(attrs.get(field))
        if len(self.fields) != len(attrs_list):
            raise serializers.ValidationError("Not unique data!")
