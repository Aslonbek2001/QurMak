from rest_framework import serializers
from .models import UserLevelPage

# class UserLevelPageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserLevelPage
#         fields = ['id', 'user', 'level', 'page', 'result', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']

# from rest_framework import serializers
# from .models import UserLevelPage

class UserLevelPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLevelPage
        fields = ['level','page', 'result']


class ResponsePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLevelPage
        fields = ['page', 'result']


