from django.urls import path
from . import views


urlpatterns = [
    path('getTags/', views.getTags, name='getTags'),
]