from rest_framework import serializers
from .models import Rapport



class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = ('id', 'lat', 'lng')
        #pour la représentation imbriquée avec le model Ville, User, Region
        depth = 1