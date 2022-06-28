from rest_framework import serializers


class UniqueFieldValidator:
    """Class-based validator for unique model fields."""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, attrs):
        attrs_set = {attrs.get(field) for field in self.fields}
        if len(self.fields) != len(attrs_set):
            raise serializers.ValidationError("Not unique fields!")
