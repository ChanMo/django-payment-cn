from django.urls import path

from .views import *

urlpatterns = [
    path('pay/', PayView.as_view()),
    path('notify/<slug:platform>/', notify_view),
]
