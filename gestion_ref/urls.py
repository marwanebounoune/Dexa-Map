from django.urls import path
from . import views


urlpatterns = [
    path('pins-list-2/', views.pinlist, name='api-list-2'),
    path('create_my_pin/', views.create_my_pin, name='create_my_pin'),
    path('pins-detail-2/<str:pk>/', views.pinDetail, name='api-detail-2'),#Update pins (y'a pas la decrementation des pins)
    path('delete_my_pin/<str:id>/', views.pinDelete, name='delete_my_pin'),
    path('update_my_pin/', views.update_my_pin, name='update_my_pin'),
    path('list-pin-non-valider/', views.pinlist_nonValide, name='list-pin-non-valider'),
    path('list-pin-non-valider-mobile/', views.pinlist_nonValide_mobile, name='list-pin-non-valider-mobile'),
    path('list-pin-valider/', views.pinlist_Valide, name='list-pin-valider'),
    path('validate_my_pin/<pin_id>', views.validate_my_pin, name='validate_my_pin'),
    path('ajout_actualisation/', views.ajout_actualisation, name='ajout_actualisation'),
    path('delete_actu/<pk>/<id>/', views.delete_actu, name='delete_actu'),
]