from .models import ClientModel
from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=150, write_only=True) 



""" Qilingan ishlar """
"""Userni Admin tomonidan Kiritish """
"""Userni Admin tomonidan Update qilish""" """Ko'rish kera"""

"""Level uchun quiz Api"""


"""Qilinadigan ishlar"""
"""User uchun username va password update uchun api"""


class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, required=True)
    date_start = serializers.DateTimeField(required=False, allow_null=True)
    date_end = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = ClientModel
        fields = ('id', 'username', 'phone', 'date_start', 'date_end', 'password')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get("username") or self.generate_username()
        phone = validated_data['phone']
        date_start = validated_data.get('date_start', timezone.now())
        date_end = validated_data.get('date_end', timezone.now() + timedelta(days=365))
        
        user = ClientModel(
            username=username,
            phone=phone,
            date_start=date_start,
            date_end=date_end
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        
        if password:
            instance.set_password(password)
        
        instance.save()  # Yangilangan instansiyani saqlashni unutmang
        return instance

    def generate_username(self):
        last_client = ClientModel.objects.latest('id')
        last_id = last_client.id if last_client else 0
        return f'user-{last_id + 1}'

    
class ChangeUserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    old_password = serializers.CharField(required=False)

    def validate(self, data):
        user = self.context['request'].user

        # Agar username o'zgartirilmoqchi bo'lsa
        if 'username' in data:
            user.username = data['username']

        # Agar parol o'zgartirilmoqchi bo'lsa
        if 'password' in data and 'old_password' in data:
            old_password = data['old_password']
            if not user.check_password(old_password):
                raise serializers.ValidationError("Old password is not correct.")
            new_password = data['password']
            user.set_password(new_password)

        return data
    
class UserAccountSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)
    class Meta:
        model = ClientModel
        fields = ['phone']


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    pass


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields =["id", "username", "phone"]


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['id', 'username', 'password', 'phone', 'date_start', 'date_end', 'devise']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ['username', 'phone', 'date_start', 'date_end']


class MessageSerializer(serializers.Serializer):
    message = serializers.TimeField()

    
