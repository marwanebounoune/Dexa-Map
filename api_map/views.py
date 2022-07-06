import re
from api_map.serializers import VilleSerializer
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import Facture, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.serializers import UserSerializer
from api_map.models import  Pin, Villes
from fold_to_ascii import fold
from django.shortcuts import render
import logging


# la methode de recuperation de la page map
@login_required(login_url='login') 
def myMap(request):
    try:
        if request.method == 'GET':
            type_abon = 0
            erreur =0
            villes = Villes.objects.all()
            context={
                'villes': villes
            }
            if request.user.userType == "principal":
                facturesPayes = Facture.objects.filter(username_id=request.user.id).filter(statut='Paye')
            else:
                facturesPayes = Facture.objects.filter(username_id=request.user.lien).filter(statut='Paye')
            for i in facturesPayes:
                if i.type_abonnement>type_abon:
                    type_abon=i.type_abonnement
            if type_abon == 1 or type_abon == 2 or request.user.id == 1 or request.user.lien == 1:
                return render(request, 'account/connected.html', context)
            else:
                erreur=1
                messages.error(request, 'Désolé, votre pack ne contient My Map, Veuillez demander le compte PREMIUM ou PREMIUM PLUS')
                return render(request, 'account/connected.html', {'erreur':erreur})

    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperer un user à partir un id
@api_view(['GET'])
@login_required(login_url='login')
def getUser(request, idUser):
    try:
        user = User.objects.get(id=idUser)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperer les villes selon id des régions
@api_view(['GET'])
@login_required(login_url='login')
def getVilles(request, idRegion):
    try:
        villes = Villes.objects.filter(region_id=idRegion)
        serializer = VilleSerializer(villes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#fonction pour comparer deux listes
def list_contains(List1, List2): 
    check = False
    for m in List1:
        #fold pour eliminer les accents
        m=fold(m)
        for n in List2:
            n=fold(n)
            if m == n: 
                check = True
                return check              
    return check

#méthode de modification des types de la map
@api_view(['POST'])
@login_required(login_url='login')  
def updateTypeKey(request):
    try:
        data = request.data
        key= ''
        user = User.objects.get(id=request.user.id)
        if data['type_map']=='Leaflet':
            type_map=data['type_map']
        else:
            key = data['keyMap']
            type_map=data['type_map']
        user.key_map=key
        user.type_map=type_map
        user.save()
        serializer = UserSerializer(user, many=False)
        return redirect('connexion')

    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#vérification de syntaxe pour le latitude et la longitude
def validate_LatAndLng(lat_lng):
    if re.match(r'[+-]?[0-9]{1,2}\.[0-9]+$', lat_lng) != None: #Valide return 1
        return 1
    return 0

#récuperation des pin selon les droits des utilisateurs
def user_pinlist(user):
    try:
        user_propre_pins = Pin.objects.filter(username=user).filter(deleted=False)
        if user.permission == 'visiteur':
            return set(user_propre_pins)
        if user.permission == 'elaborateur':
            pere_user = User.objects.get(id=user.lien)
            pere_pins = Pin.objects.filter(username=pere_user).filter(deleted=False)
            sousUsers = User.objects.filter(lien=pere_user.id).filter(userType='secondaire')
            pins_sous_users = []
            for su in sousUsers:
                pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False)
                pins_sous_users.extend(pins_su)
            pins = set(pins_sous_users).union(set(pere_pins))
            return set(pins)

        if user.userType == 'principal':
            sousUsers = User.objects.filter(lien=user.id).filter(userType='secondaire')
            pins_sous_users = []
            for su in sousUsers:
                pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False)
                pins_sous_users.extend(pins_su)
            pins = set(pins_sous_users).union(set(user_propre_pins))
            return set(pins)
        if user.permission == 'validateur':
            pere_user= User.objects.get(id=user.lien)
            pere_pins = Pin.objects.filter(username=pere_user).filter(deleted=False)
            sousUsers = User.objects.filter(lien=pere_user.id).filter(userType='secondaire')
            pins_sous_users = []
            for su in sousUsers:
                pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False)
                pins_sous_users.extend(pins_su)
            pins = set(pins_sous_users).union(set(pere_pins))
            return set(pins)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation du type de réference à partir de son id
def typeDeRererence_to_id(typeDeRererence):
    if typeDeRererence == "vente":
        return 1
    if typeDeRererence == "location":
        return 2
    if typeDeRererence == "rapport":
        return 3
    return 0 #retourner zero si qqch d'invalide est tapé

#récuperation du type de bien à partir de son id
def typeDeBien_to_id( typeDeBien):
    if typeDeBien == "r":#Residentiel
        return 1
    if typeDeBien == "v":#Villa
        return 2
    if typeDeBien == "m":#Maison
        return 3
    if typeDeBien == "p":#Professionnel
        return 4
    if typeDeBien == "c":#Commercial
        return 5
    if typeDeBien == "i": #Industriel
        return 6
    if typeDeBien == "tv": #Terrain Villa
        return 7
    if typeDeBien == "ti":#Terrain Industriel
        return 8
    if typeDeBien == "tu":#Terrain urbain 
        return 9
    if typeDeBien == "ta":#Terrain agricole
        return 10
    return 0 #retourner zero si qqch d'invalide est tapé


















