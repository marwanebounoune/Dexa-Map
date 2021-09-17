from django.urls import path
from . import views


urlpatterns = [
    path('pins-detail/<id>', views.getPinWithId, name='getPinWithId'),#Liée au crédits
]