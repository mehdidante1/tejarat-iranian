from django.urls import path
from . views import *

app_name = "zarinpal"

urlpatterns = [
    path('request/', send_request, name='request'),
    path('verify/', verify , name='verify'),
]
