from urllib import request

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer, UserModelSerializer, EventModelSerializer
from ..models import Event
from users.models import User
from .permissions import IsSuperUserOrRegister
from datetime import datetime
from rest_framework.response import Response


class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()\
    .filter(meeting_time__gte=datetime.now())\
    .order_by("meeting_time")


class UserCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperUserOrRegister]


class OneEventSubscriptionAPIView(generics.CreateAPIView):
    serializer_class = EventModelSerializer
    queryset = Event.objects.all()
    lookup_url_kwarg = "events_id"
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        self.check_object_permissions(request, event)
        event.users.add(request.user)
        serializer = self.get_serializer_class()(event)
        return Response(serializer.data)

class EventMyListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user) \
            .filter(meeting_time__gte=datetime.now()) \
            .order_by("meeting_time")