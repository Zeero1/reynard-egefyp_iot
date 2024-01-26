from django.urls import re_path

from . import consumers

ws_urlpatterns = [
    re_path('ws/devicewebapp/mac_add/', consumers.GraphConsumer.as_asgi()),
]