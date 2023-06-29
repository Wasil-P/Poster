from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from .serializers import EventSerializer, UserSerializer
from ..models import Event
from users.models import User


class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class UserCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        if request.user.is_staff is False:
            raise Exception("Не достаточно прав!")
        return queryset

    def post(self, request, *args, **kwargs):
        pass