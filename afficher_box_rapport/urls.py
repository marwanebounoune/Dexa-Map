from django.urls import path
from . import views


urlpatterns = [
    path('get_approxim_pins/', views.get_approxim_pins, name='evaluer'),
    path('createRapport/', views.CreerRapport, name='createRapport'),#Liée au crédits
    path('updateRapportClient/', views.updateRapportClient, name='updateRapportClient'),#Liée au crédits
]