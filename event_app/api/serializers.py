from rest_framework import serializers
from event_app.models import Event
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# from users.models import User


class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    meeting_time = serializers.DateTimeField()
    users = serializers.ListSerializer(child=serializers.CharField(max_length=100))
    description = serializers.CharField(max_length=256)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)


class EventModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Event
        fields = ['name', 'meeting_time', 'users', 'description']
        read_only_fields = ['users']


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']
        read_only_fields = ['last_login',
                            'is_superuser',
                            'first_name',
                            'last_name',
                            'is_staff',
                            'is_active',
                            'data_joined',
                            'phone']

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class OneEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'meeting_time', 'users', 'description']
        read_only_fields = ['name', 'meeting_time', 'description']