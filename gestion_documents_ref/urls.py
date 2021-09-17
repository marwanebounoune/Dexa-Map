from django.urls import path
from . import views


urlpatterns = [
    path('list-docs-pin/<pin_id>', views.getPieceJointeByIdPin, name='list-docs-pin'),
    path('delete_my_piece_jointe/<fichier_id>', views.delete_my_piece_jointe, name='delete_my_piece_jointe'),
    path('create_my_piece_jointe/<pin_id>', views.create_my_piece_jointe, name='create_my_piece_jointe'),
]