from django.urls import path
from . import views


urlpatterns = [
    path('photo-pin/<pin_id>', views.getPhotographiesByIdPin, name='getPhotographiesByIdPin'),
    path('ajoutPhotographies/<pin_id>', views.ajoutPhotographies, name='ajoutPhotographies'),
    path('delete_my_photo_pin/<id_photo>', views.delete_my_photo_pin, name='delete_my_photo_pin'),
]