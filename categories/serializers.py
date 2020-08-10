from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.CharField()
    name = serializers.CharField()
    lft = serializers.IntegerField()
    rgt = serializers.IntegerField()