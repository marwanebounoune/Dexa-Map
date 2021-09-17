from django.urls import path
from . import views


urlpatterns = [

    path('', views.login, name='login'),
    path('connexion/', views.connexion, name='connexion'),
    path('SubUserUpdate/<id>', views.SubUserUpdate, name='SubUserUpdate'),
    path('getSubUserInfo/<id>', views.getSubUserInfo, name='getSubUserInfo'),
    path('logout/', views.logout_custumized, name='logout'),
    path('userChangerImage', views.userChangerImage, name='userChangerImage'),
    path('AjouterSousUser', views.AjouterSousUser, name='AjouterSousUser'),
    path('AjouterFacturation', views.AjouterFacturation, name='AjouterFacturation'),
    path('activerDesactiverUser/<idSousUser>', views.activerDesactiverUser, name='activerDesactiverUser'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('updateSte/', views.updateSte, name='updateSte'),
    path('historique/', views.historique, name='historique'),
    path('userRemoveImage/', views.userRemoveImage, name='userRemoveImage'),
]