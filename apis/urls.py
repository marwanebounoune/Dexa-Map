from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register("profile", views.UserProfileViewSet, basename="profile")
router.register("login", views.LoginViewSet, basename="login")
router.register("pins", views.PinViewsets, basename="pins")
router.register("photos", views.PhotoViewsets, basename="photos")
router.register("regions", views.RegionViewsets, basename="regions")
router.register("villes", views.VilleViewsets, basename="villes")
urlpatterns = [
    url(r'', include(router.urls)),
]
