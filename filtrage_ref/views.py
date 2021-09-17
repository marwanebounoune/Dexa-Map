import logging
from api_map.views import list_contains, user_pinlist
from api_map.serializers import PinSerializerLeger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import Facture
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from api_map.models import Note
import datetime


# Create your views here.


#récuperation des pins selon un filtrage
@api_view(['POST'])
@login_required(login_url='login')
def pinlistFilters(request):
    try:
        if request.user.my_ip == "105.159.248.165" or request.user.id == 1 or request.user.id == 9:
            pins = user_pinlist(request.user)
            user = request.user
            now=datetime.date.today()
            facturesPayes = Facture.objects.filter(username_id=user.id).filter(statut='Paye').filter(date_expiration__gt= now)
            pins_filtre_region=[]
            pins_filtre_typeDebien=[]
            pins_filtre_note=[]
            #recuperation data
            data=request.data
            typeDeBien = data['type_de_bien']
            region = data['region']
            tags = data['tags']
            
            try:
                type_validation_ok = data['type_validation_ok']
                if type_validation_ok=="1":
                    pins_filtre_type_valide_ok = [d for d in pins if d.is_validate_by_user == True]
            except MultiValueDictKeyError:
                type_validation_ok = "Null"
                pins_filtre_type_valide_ok = []

            try:
                type_validation_non = data['type_validation_non']
                if type_validation_non=="2":
                    pins_filtre_type_valide_non = [d for d in pins if (d.is_validate_by_user == False and d.from_mobile == False)]
            except MultiValueDictKeyError:
                type_validation_non = "Null"
                pins_filtre_type_valide_non = []

            try:
                type_validation_mobile = data['type_validation_mobile']
                if type_validation_mobile=="3":
                    pins_filtre_type_valide_non_from_mobile = [d for d in pins if (d.is_validate_by_user == False and d.from_mobile == True)]
            except MultiValueDictKeyError:
                type_validation_mobile = "Null"
                pins_filtre_type_valide_non_from_mobile = []

            if (type_validation_ok == "Null" and type_validation_non == "Null" and type_validation_mobile == "Null"):
                pins_filtre_type_valide = [d for d in pins if d.is_validate_by_user == True]
            else:
                pins_filtre_type_valide = []
                
            try:
                typeDeReferenceLocation = data["type_reference_location"]
                if len(typeDeReferenceLocation)!=0:
                    typeDeReferenceLocation=int(typeDeReferenceLocation)
                    pins_filtre_typeReference_location = [d for d in pins if d.type_de_reference == typeDeReferenceLocation]
            except MultiValueDictKeyError:
                typeDeReferenceLocation = "Null"
                pins_filtre_typeReference_location = []
            try:
                typeDeReferenceVente = data["type_reference_vente"]
                if len(typeDeReferenceVente)!=0:
                    typeDeReferenceVente=int(typeDeReferenceVente)
                    pins_filtre_typeReference_vente = [d for d in pins if d.type_de_reference == typeDeReferenceVente]
            except MultiValueDictKeyError:
                typeDeReferenceVente = "Null"
                pins_filtre_typeReference_vente = []
            try:
                typeDeReferenceRapport = data["type_reference_rapport"]
                if len(typeDeReferenceRapport)!=0:
                    typeDeReferenceRapport =int(typeDeReferenceRapport)
                    pins_filtre_typeReference_rapport = [d for d in pins if d.type_de_reference == typeDeReferenceRapport]
            except MultiValueDictKeyError:
                typeDeReferenceRapport = "Null"
                pins_filtre_typeReference_rapport = []
            note = data['note']
            
            #filtrage
            if len(region) != 0:
                pins_filtre_region = [d for d in pins if d.region_id == int(region)]
                
            if len(typeDeBien) != 0:
                typeDeBien=int(typeDeBien)
                if typeDeBien == 2:
                    pins_filtre_typeDebien = [d for d in pins if d.type_de_bien == 2 or d.type_de_bien == 7]
                elif typeDeBien == 6:
                    pins_filtre_typeDebien = [d for d in pins if d.type_de_bien == 6 or d.type_de_bien == 8]
                else:
                    pins_filtre_typeDebien = [d for d in pins if d.type_de_bien == typeDeBien]
            #intersection des resultats sans considerer la note
            pins =  (set(pins_filtre_typeReference_location) | set(pins_filtre_typeReference_vente) | set(pins_filtre_typeReference_rapport)) & (set(pins_filtre_type_valide_ok) | set(pins_filtre_type_valide_non) | set(pins_filtre_type_valide_non_from_mobile) | set(pins_filtre_type_valide)) & set(pins_filtre_typeDebien) & set(pins_filtre_region)
            if len(note) != 0:
                notes = Note.objects.all()
                #__icontains pour une recherche indépendante de la casse
                notes = notes.filter(note__icontains=note).filter(editer_par=user)
                if len(notes) != 0:
                    for note in notes:
                        pins_filtre_note.append(note.pin)
                    pins = set(pins) & set(pins_filtre_note)
                else:
                    content = {'message': "aucun resultat trouve avec la note mentionner"}
                    return Response(content)
            if len(tags) != 0:
                tags = tags.lower().replace(' ,', ',').split(',')
                pins_filtre_tags = [d for d in pins if list_contains(tags, d.tags.lower().replace(' ,', ',').split(','))]
                pins = set(pins) & set(pins_filtre_tags)
                if len(pins_filtre_tags)==0:
                    content = {'message': "aucun resultat trouve avec le tag mentionner"}
                    return Response(content)
        serializer = PinSerializerLeger(pins, many=True)
        return Response(serializer.data)

    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
