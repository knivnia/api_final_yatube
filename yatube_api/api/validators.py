from rest_framework import serializers


class SelfFollowValidator:
    """CLass-based validator for self-following."""

    def __init__(self, user='user', following='following'):
        self.user = user
        self.following = following

    def __call__(self, attrs):
        if attrs[self.user] == attrs[self.following]:
            raise serializers.ValidationError("You cannot follow yourself!")
