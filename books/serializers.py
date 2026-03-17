from rest_framework import serializers
from .models import BookOne, BookTwo

class BookOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookOne
        fields = ["number", "page"]


class BookTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTwo
        fields = ["number", "page"]

    