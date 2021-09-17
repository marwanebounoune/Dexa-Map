from django.urls import path
from . import views


urlpatterns = [
    path('pins-import-2/', views.pinImport, name='api-import-2'),
]