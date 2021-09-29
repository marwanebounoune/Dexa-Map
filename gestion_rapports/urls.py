from django.urls import path
from . import views
from . import viewsCommentaire


urlpatterns = [
    path('get_approxim_pins/', views.get_approxim_pins, name='evaluer'),
    path('createRapport/', views.CreerRapport, name='createRapport'),
    path('updateRapportClient/', views.updateRapportClient, name='updateRapportClient'),
    path('rapport_detail/<str:pk>/', views.getRapport, name='rapport_detail'),
    path('preview_pdf/', views.preview_pdf, name='preview_pdf'),
    path('situationJuridique/<str:pk>/', views.situationJuridique, name='situationJuridique'),
    path('editRapport/<str:pk>/', views.editRapport, name='editRapport'),
    path('addFraction/<pk>/', views.addFraction, name='addFraction'),
    path('addHypotheque/<pk>/', views.addHypotheque, name='addHypotheque'),
    path('create_docs_rapport/<pk>', views.create_docs_rapport, name='create_docs_rapport'),
    path('getPieceJointeByIdPin/<pk>', views.getPieceJointeByIdPin, name='getPieceJointeByIdPin'),
    path('ajoutPhotographiesRapport/<pk>', views.ajoutPhotographiesRapport, name='ajoutPhotographiesRapport'),
    path('getPhotographiesRapport/<pk>', views.getPhotographiesRapport, name='getPhotographiesRapport'),
    path('dropPhotoRapport/<pk>', views.dropPhotoRapport, name='dropPhotoRapport'),
    #Commentaires
    path('addCommentRapport/', viewsCommentaire.addCommentRapport, name='addCommentRapport'),
    path('getCommentRapport/<pk>', viewsCommentaire.getCommentRapport, name='getCommentRapport'),
    path('delete_Comment/<pk>', viewsCommentaire.delete_Comment, name='delete_Comment'),
    path('getComment/<pk>', viewsCommentaire.getComment, name='getComment'),
    path('rep_Comment/<pk>', viewsCommentaire.rep_Comment, name='rep_Comment'),
    path('updateComment/', viewsCommentaire.updateComment, name='updateComment'),
]