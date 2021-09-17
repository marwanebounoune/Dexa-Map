from django.urls import path
from . import views


urlpatterns = [
    path('ajout_note-2/', views.save_note, name='save_note'),
    path('note-pin-2/<pin_id>', views.get_notes_per_pin, name='get_notes_per_pin'),
    path('update-note-2/', views.update_note, name='update_note'),
    path('delete_note/<pk>', views.delete_note, name='delete_note'),
]