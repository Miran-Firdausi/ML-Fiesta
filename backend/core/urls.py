from django.urls import path
from . import views

urlpatterns = [
    path("tts/", views.get_tts),
    path("answer/", views.get_answer),
]
