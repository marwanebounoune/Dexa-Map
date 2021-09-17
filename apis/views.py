from django.db.models import query
from django.http.response import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import IsAuthenticated
from account.serializers import UserSerializer
from api_map.serializers import PinSerializer, PhotographieSerializer, RegionSerializer, VilleSerializer
from django.shortcuts import render
from account.models import User
from api_map.models import Photographie, Pin, Regions, Villes
from rest_framework import viewsets
# Create your views here.
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication
from . import permissions

from rest_framework.authtoken.models import Token
import datetime
import pytz
import json
from rest_framework import status

from datetime import date

class UserProfileViewSet(viewsets.ModelViewSet):
    """api for user"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,IsAuthenticated,)

class LoginViewSet(viewsets.ViewSet):
    """login tokens hundler"""
    serializer_class = AuthTokenSerializer
    def create(self, request):
        #return ObtainAuthToken().as_view()(request=request._request)
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            #token, created =  Token.objects.get_or_create(user=serializer.object['user'])
            #serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            utc_now = datetime.datetime.utcnow()
            utc_now = pytz.utc.localize(utc_now)
            if not created and token.created < utc_now - datetime.timedelta(hours=24):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = datetime.datetime.utcnow()
                token.save()

            #return Response({'token': token.key})
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PinViewsets(viewsets.ModelViewSet):
    """Pin Viewset api"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PinPermissions,IsAuthenticated,)
    serializer_class = PinSerializer

    def perform_create(self, serializer):
        try:
            try:
                region_id = self.request.data['region']
                region = Regions.objects.get(id=region_id)
            except KeyError:
                print(f"region non declaré")
                region=None
                
        except MultiValueDictKeyError:
            region=None
        try:
            try:
                ville_id = self.request.data['ville']
                ville = Villes.objects.get(id=ville_id)
            except KeyError:
                ville=None
        except MultiValueDictKeyError:
            ville=None
        
        serializer.save(username=self.request.user, region=region, ville=ville)
    def get_queryset(self):
        return Pin.objects.filter(username=self.request.user)

class PhotoViewsets(viewsets.ModelViewSet):
    """Pin Viewset api"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotographieSerializer
    queryset = Photographie.objects.all()

    def perform_create(self, serializer):
        pin_id = self.request.data['pin_id']
        pin = Pin.objects.get(id=pin_id)
        photos = Photographie.objects.filter(pin=pin)
        if len(photos) < 12:
            serializer.save(pin=pin)

class RegionViewsets(viewsets.ModelViewSet):
    """Pin Viewset api"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RegionSerializer
    queryset = Regions.objects.all()

class VilleViewsets(viewsets.ModelViewSet):
    """Pin Viewset api"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VilleSerializer
    def get_queryset(self):
        region_id = self.request.query_params.get('RegionId')
        queryset = Villes.objects.filter(region_id = region_id)
        return queryset