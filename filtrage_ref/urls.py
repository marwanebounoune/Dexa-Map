from django.urls import path
from . import views


urlpatterns = [
    path('pins-filter/', views.pinlistFilters, name='api-filter-2'),
]