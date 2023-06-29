import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Poster.settings")

django.setup()
# _______________________________________________________________

from event_app.api.serializers import EventSerializer
from event_app.models import Event

eve = Event.objects.first()
ser = EventSerializer(eve)
print(ser.data)
