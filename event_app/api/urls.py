"""
URL configuration for Poster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.decorators.cache import cache_page


# api/
urlpatterns = [
    path('events/', views.EventListAPIView.as_view(), name="list_event_all"),
    path('events/my', views.EventMyListAPIView.as_view(), name="my_list_event"),
    path("event/<int:events_id>", views.OneEventSubscriptionAPIView.as_view(), name="one_event_view"),
    path('users/', views.UserCreateListAPIView.as_view(), name="all_register_users"),
    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]
