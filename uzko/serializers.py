from rest_framework import serializers
from .models import VocabModel



class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabModel
        fields = ['id','korean', 'uzb', 'krill']
        

class VocabSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    korean = serializers.CharField()
    uzb = serializers.CharField()
    krill = serializers.CharField()

class SearchVocabResponseSerializer(serializers.Serializer):
    results = VocabSerializer(many=True)