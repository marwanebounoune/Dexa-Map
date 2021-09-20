from django.urls import path
from . import views


urlpatterns = [
    path('get_dgi_pin/', views.get_dgi_pin, name='get_dgi_pin'),
]