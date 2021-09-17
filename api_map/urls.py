from django.urls import path
from . import views


urlpatterns = [

    
    path('', views.myMap, name='myMap'),
    path('getUser/<idUser>', views.getUser, name='getUser'),
    path('getVilles/<idRegion>', views.getVilles, name='getVilles'),
    path('update-type-map-2/', views.updateTypeKey, name='update-type-map-2'),
]