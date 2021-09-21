from account.serializers import UserSerializer
from rest_framework import serializers
from .models import Note, Pin, Documents, Photographie, Regions, Villes, Tags

#le serializer de la classe Région
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ('id', 'name')
        #pour la représentation imbriquée avec le model Region
        depth = 1

#le serializer de la classe Ville
class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Villes
        Regions = RegionSerializer()
        fields = ('id', 'name','region')
        #pour la représentation imbriquée avec le model Ville
        depth = 1

#le serializer de la classe Pin avec tous les champs
class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        username = UserSerializer()
        ville = VilleSerializer()
        region = RegionSerializer()
        fields = ('id', 'lat', 'lng', 'type_de_bien', 'chute_fonciere', 'type_de_reference', 'label', 'ville', 'region', 'adresse', 'date_ajout', 'actualisation', 'username', 'user_editer', 'user_valider', 'contact', 'surface', 'prix_unit', 'prix_total', 'descriptif', 'tags', 'is_validate_by_user', 'deleted', 'rue', 'is_localized', 'from_mobile')
        #pour la représentation imbriquée avec le model Ville, User, Region
        extra_kwargs = {'username': {'read_only': True}}
        depth = 1

#le serializer de la classe Pin avec des champs ciblés pour optimiser l'affichage des pins sur les maps
class PinSerializerLeger(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ('id', 'lat', 'lng', 'label', 'type_de_reference','type_de_bien', 'is_validate_by_user', 'is_localized', 'from_table')

class PinSerializerLegerPrix(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ('id', 'lat', 'lng', 'label', 'type_de_reference','type_de_bien', 'is_validate_by_user', 'prix_unit', 'from_table')

#le serializer de la classe Photographie
class PhotographieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographie
        pin = PinSerializer()
        fields = ('id', 'pin', 'photo', 'descriptif')
        #pour la représentation imbriquée avec le model Pin
        depth = 1

#le serializer de la classe Note
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        editer_par = UserSerializer()
        pin = PinSerializer()
        fields = ('id', 'note','date','editer_par','pin')
        #pour la représentation imbriquée avec le model Pin & User
        depth = 1

#le serializer de la classe Document
class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        username = UserSerializer()
        pin = PinSerializer()
        fields = ('id', 'pin', 'username','type_file','fichier')
        #pour la représentation imbriquée avec le model Pin & User
        depth = 1

#le serializer de la classe Tags
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'