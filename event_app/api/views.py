from urllib import request

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer, UserModelSerializer, OneEventSerializer
from ..models import Event
from users.models import User
from .permissions import IsSuperUserOrRegister, IsAuthenticatedOrReadOnly
from datetime import datetime


class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()\
    .filter(meeting_time__gte=datetime.now())\
    .order_by("meeting_time")


class UserCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperUserOrRegister]


class OneEventSubscriptionAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = OneEventSerializer
    queryset = Event.objects.all()
    lookup_url_kwarg = "events_id"
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly]


class EventMyListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()\
                    .order_by("meeting_time")
    permission_classes = [IsAuthenticated]
