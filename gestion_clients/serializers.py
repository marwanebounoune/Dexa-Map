from rest_framework import serializers
from .models import ClientPhysique

class ClientPhysiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPhysique
        fields = ('id', 'nom', 'prenom', 'tel', 'email', 'cin', 'ville', 'adresse', 'denomination', 'raison_sociale','gsm')
        #pour la représentation imbriquée avec le model Ville, User, Region
        depth = 1