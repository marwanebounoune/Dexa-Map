from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'nom', 'prenom', 'tel', 'email', 'cin')
        #pour la représentation imbriquée avec le model Ville, User, Region
        depth = 1