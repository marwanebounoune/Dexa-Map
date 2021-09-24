from rest_framework import serializers
from .models import Rapport



class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = ('id', 'lat', 'lng', 'prix_unit_estime', 'is_locked', 'username', 'dgi_zone', 'client', 'type_de_bien', 'descreptif', 'from_table')
        #pour la représentation imbriquée avec le model Ville, User, Region
        depth = 1