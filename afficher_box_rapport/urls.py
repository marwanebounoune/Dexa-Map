from django.urls import path
from . import views


urlpatterns = [
    path('addClient/', views.AjouterClient, name='addClien'),#Liée au crédits
]