
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages, auth
from rest_framework.decorators import api_view
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer
from .models import Facture, User
from rest_framework.response import Response
from django.utils.datastructures import MultiValueDictKeyError
from api_map.models import HistoriqueExplorer, Pin, HistoriqueMyMap
import re
import datetime

# Create your views here

@login_required(login_url='login')
def connexion(request):
    if request.method == 'GET':
        request.user.my_ip = get_ip(request)
        request.user.save()
        subUsers = User.objects.filter(lien=request.user.id).filter(userType='secondaire')
        now=datetime.date.today()
        factures = Facture.objects.filter(username_id=request.user.id)
        facturesPayes = Facture.objects.filter(username_id=request.user.id).filter(statut='Paye').filter(date_expiration__gt= now)
        p_user=[]
        if request.user.userType == 'secondaire':
            p_user = User.objects.get(id=request.user.lien)
            p_user_factures_paye = Facture.objects.filter(username_id=request.user.lien).filter(statut='Paye').filter(date_expiration__gt= now)
        infoAbonnement_regionChoisis = []
        infoAbonnement_nbrUser = 0
        type_abon = 0
        if request.user.userType == 'principal':
            for infoAbonnement in facturesPayes:
                for GV in infoAbonnement.region_choisis:
                    infoAbonnement_regionChoisis.append(GV)
                infoAbonnement_nbrUser+=infoAbonnement.nbrUtilisateur
            for i in infoAbonnement_regionChoisis :
                if i in infoAbonnement_regionChoisis[infoAbonnement_regionChoisis.index(i)+1:]:
                    infoAbonnement_regionChoisis.remove(i)
            for i in facturesPayes:
                if i.type_abonnement>type_abon:
                    type_abon=i.type_abonnement
        else:
            for infoAbonnement in p_user_factures_paye:
                for GV in infoAbonnement.grandes_villes:
                    infoAbonnement_regionChoisis.append(GV)
                infoAbonnement_nbrUser+=infoAbonnement.nbrUtilisateur
            for i in infoAbonnement_regionChoisis :
                if i in infoAbonnement_regionChoisis[infoAbonnement_regionChoisis.index(i)+1:]:
                    infoAbonnement_regionChoisis.remove(i)
            for i in p_user_factures_paye:
                if i.type_abonnement>type_abon:
                    type_abon=i.type_abonnement
        if type_abon==0:
            type_abonnement="Standard"
        if type_abon==1:
            type_abonnement="Premium"
        if type_abon==2:
            type_abonnement="Premium +"
        context = {
            'subUsers': subUsers,
            'factures': factures,
            'nbrGrandesVilles': len(infoAbonnement_regionChoisis),
            'nbrUsers': infoAbonnement_nbrUser,
            'type_abon':type_abonnement,
            'p_user': p_user
        }
        return render(request, 'account/connected.html', context)

@login_required(login_url='login')
def SubUserUpdate(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        erreur = 0
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        tel1 = request.POST['tel1']
        tel2 = request.POST['tel2']
        pswd =  request.POST['pswd']
        confirmerPswd = request.POST['confirmer-pswd']
        photo=False
        try:
            photo = request.FILES['ImageProfile-subUser']
        except MultiValueDictKeyError:
            photo=False
        email = request.POST['email']
        permissions = request.POST['permission']
        if len(nom) == 0:
            erreur=1
            messages.error(request, "Merci de compléter le champs relative au nom." )
        if len(prenom) == 0 :
            erreur=1
            messages.error(request, "Merci de compléter le champs relative au prenom." )
        if len(email) != 0 and validateEmail(email) == 0:
            erreur = 1
            messages.error(request, "Format de l'adresse e-mail non valide")
        if len(tel1) != 0 and validateTelephone(tel1) == 0:
                erreur = 1
                messages.error(request, 'Numero de telephone 01 non valide (doit contenir 10 chiffre et commencer par 0)')
        if len(tel2) != 0 and validateTelephone(tel2) == 0:
                erreur = 1
                messages.error(request, 'Numero de telephone 02 non valide (doit contenir 10 chiffre et commencer par 0)')
        if len(pswd) != 0:
            if len(confirmerPswd)==0:
                erreur=1
                messages.error(request, "Merci de compléter le champs relative a la confirmation du password." )
            elif pswd != confirmerPswd:
                erreur=1
                messages.error(request, "Le password et la confirmation ne sont pas identiques." )
        if len(confirmerPswd)!=0 and len(pswd)==0:
                erreur=1
                messages.error(request, "Le password et la confirmation ne sont pas identiques." )

        if erreur == 0:
            user.last_name = nom
            user.first_name = prenom
            user.email = email
            user.tel1 = tel1
            user.tel2 = tel2
            user.permission = permissions
            if pswd == confirmerPswd and len(pswd)!=0 and len (confirmerPswd)!=0:
                user.set_password(pswd)
            if photo != False:
                user.photoProfile.save(photo.name, photo) 
            user.save()
            return redirect('connexion')   
        return render(request, 'account/connected.html', {'erreur':erreur})

@api_view(['GET'])
@login_required(login_url='login')
def getSubUserInfo(request, id):
    subUser=User.objects.get(id=id)
    serializer = UserSerializer(subUser, many=False)
    return Response(serializer.data)
    
def login(request):
    if request.method == 'GET':
        return render(request, 'account/index2.html')
    if request.method == 'POST':
        erreur=0
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        user.my_ip = get_ip(request)
        user.save()
        if (user is not None and (user.my_ip == "105.159.248.165" or user.id ==1 or user.id == 9)):
            auth.login(request, user)
            return redirect('connexion')
        elif(user.my_ip != "105.159.248.165" and user.id !=1 and user.id != 9) :
            return HttpResponse("Access denied")
        else:
            erreur=1
            messages.error(request, "Votre login ou mot de passe et incorrect.")
            return render(request, 'account/index2.html', {'erreur':erreur})
    else:
        return render(request, 'account/index2.html')

def logout_custumized(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def historique(request):
    if request.user.id == 1 or request.user.lien == 1:
        historiqueMyMap = HistoriqueMyMap.objects.filter(username_id=request.user.id)
    else:
        historiqueMyMap = HistoriqueMyMap.objects.filter(username_id=request.user.id)
    historiqueExplorer = HistoriqueExplorer.objects.filter(username_id=request.user.id)
    allPinsMyMap = []
    allPinsExplorer = []
    for histo in historiqueMyMap:
        if request.user.id == 1 or request.user.lien == 1:
            pinMyMap = Pin.objects.filter(id=histo.pin_id)
        else:
            pinMyMap = Pin.objects.filter(id=histo.pin_id)
        allPinsMyMap.extend(pinMyMap)
    for histo in historiqueExplorer:
        pin = Pin.objects.filter(id=histo.pin_id)
        allPinsExplorer.extend(pin)
    context = {
        'historiqueMyMap': historiqueMyMap,
        'historiqueExplorer': historiqueExplorer,
        'allPins': allPinsMyMap,
        'allPinsExplorer': allPinsExplorer
    }
    return render(request, 'account/historique.html', context)

@login_required(login_url='login')
def userChangerImage(request):
    if request.method == 'POST':
        #variable
        erreur = 0
        ImageProfile=''
        try:
            ImageProfile = request.FILES['ImageProfile']
        except MultiValueDictKeyError:
             messages.error(request, 'No image was selected')
        user = request.user
        if len(ImageProfile)!=0:
            if ImageProfile.size > 2000000:
                erreur = 1
                messages.error(request, "La taille du fichier ne doit pas depasser 2 Mo")
        if erreur == 0:
            user.photoProfile.delete()
            user.photoProfile.save(request.FILES['ImageProfile'].name, request.FILES['ImageProfile'])
            return redirect('connexion')
        else:
            return render(request, 'account/connected.html',  {'erreur':erreur})

@login_required(login_url='login')
def AjouterSousUser(request):
    if request.method == 'POST':
        #variable
        erreur = 0
        #get data from form
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        userName = request.POST['userName']
        password = request.POST['password']
        ConfirmPassword = request.POST['ConfirmPassword']
        permissions = request.POST['permission']
        if len(firstName) == 0:
            erreur=1
            messages.error(request, 'Merci de compléter le champs relatif au prenom')
        if len(lastName) == 0:
            erreur=1
            messages.error(request, 'Merci de compléter le champs relatif au nom')
        if len(email) != 0 and validateEmail(email) == 0:
            erreur = 1
            messages.error(request, "Format de l'adresse e-mail non valide")
        if len(userName) == 0:
            erreur=1
            messages.error(request, 'Merci de compléter le champs relatif au userName')
        elif User.objects.filter(username=userName).exists():
            erreur=1
            messages.error(request, "Ce nom d'utilisateur existe déjà." )
        if len(password) == 0:
            erreur=1
            messages.error(request, 'Merci de compléter le champs relatif au password')
        if len(ConfirmPassword) == 0:
            erreur=1
            messages.error(request, 'Merci de compléter le champs relatif au Confirmation password')
        elif password !=ConfirmPassword:
            erreur=1
            messages.error(request, 'Le champs password et la Confirmation sont pas identiques')
        if erreur == 0:
            subUser = User.objects.create_user(userName, email, password, 
            first_name= firstName, last_name= lastName,
            ICE=request.user.ICE, lien=request.user.id, userType='secondaire', 
            entreprise=request.user.entreprise, domaineActivite=request.user.domaineActivite,permission=permissions)
            subUser.save()
            return redirect('connexion')
        return render(request, 'account/connected.html',  {'erreur':erreur})
    
@login_required(login_url='login')
def AjouterFacturation(request):
    if request.method == 'POST':
        #variable
        erreur = 0
        facture = Facture()
        montant_HT = 0
        prix_par_region = 500
        prix_nbrUser = 500
        #get data from form
        regionChoisis = request.POST.getlist('regionChoisis')
        nbrUser = request.POST['nbrUser']
        if len(regionChoisis)==0 and int(nbrUser)==0:
            erreur = 1
            messages.error(request, 'Merci de sélectionner une des fonctionnalités au moins pour valider votre facturation')
        if erreur == 0:
            if len(regionChoisis) != 0:
                montant_HT += prix_par_region * len(regionChoisis)
            if len(nbrUser) != 0:
                montant_HT += prix_nbrUser * int(nbrUser)
            facture = Facture(username=request.user, statut='EnAttente', region_choisis=regionChoisis, nbrUtilisateur=nbrUser, 
            montant_HT=montant_HT, is_pack_base=request.POST["renvPackDeBase"])
            facture.save()
            return redirect('connexion')
        return render(request, 'account/connected.html',  {'erreur':erreur})

@login_required(login_url='login')
def activerDesactiverUser(request, idSousUser):
    principalUser = request.user
    sousUser = User.objects.get(id=idSousUser)
    #reverifier l'accees sur le user
    if sousUser.lien == principalUser.id:
        sousUser.is_active = not sousUser.is_active
        sousUser.save()
    return redirect('connexion')

def validateEmail(email):
    if len(email) > 6:
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email) != None:
            return 1
    return 0

def validateTelephone(tel):
    if re.match(r'^0[0-9]{9}$', tel) != None:
        return 1
    return 0

@login_required(login_url='login')
def updateUser(request):
    if request.method == 'POST':
        #Variable
        erreur = 0
        user_validation = User()
        #Récupération de la Data
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        tel1 = request.POST['tel1']
        tel2 = request.POST['tel2']
        email = request.POST['email']
        key = request.POST['keyMap']
        #Vérification de la Data
        if len(last_name) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au nom')
        elif len(last_name)>50:
            erreur = 1
            messages.error(request, 'Le champs relatif au nom ne doit pas dépasser 50 caractères')
        if len(first_name) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au prenom')
        elif len(first_name)>50:
            erreur = 1
            messages.error(request, 'Le champs relatif au prenom ne doit pas dépasser 50 caractères')
        if len(tel1)!=0:
            if validateTelephone(tel1) == 0:
                erreur = 1
                messages.error(request, 'Numero de telephone 1 non valide (doit contenir 10 chiffre et commencer par 0)')
        if len(tel2)!=0:
            if validateTelephone(tel2) == 0:
                erreur = 1
                messages.error(request, 'Numero de telephone 2 non valide (doit contenir 10 chiffre et commencer par 0)')
        if len(email) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au email')
        else:
            if validateEmail(email) == 0:
                erreur = 1
                messages.error(request, "Format de l'adresse e-mail non valide")
        if erreur == 0:
            #Modification des info personnelles de USER
            us = request.user
            us.last_name = last_name
            us.first_name = first_name
            us.tel1 = tel1
            us.tel2 = tel2
            us.email = email
            us.key_map = key
            us.save()
            #messages.success(request, 'Votre modification a été bien enregistrée.')
            return redirect('connexion')
        if erreur == 1:
            user_validation =User(last_name=last_name, first_name=first_name, tel1=tel1, tel2=tel2, email=email)
            context = {
                'user_validation': user_validation,
                'erreur':erreur
            }
            return render(request, 'account/connected.html',context)

@login_required(login_url='login')
def updateSte(request):
    if request.method == 'POST':
        #Variable
        erreur = 0
        user_validation = User()
        #Récupération de la Data
        entreprise = request.POST['entreprise']
        ICE = request.POST['ICE']
        adresse = request.POST['adresse']
        domaine_activite = request.POST['domaine_activite']
        #Vérification de la Data
        if len(adresse) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au nom complet')
        elif len(adresse)>50:
            erreur = 1
            messages.error(request, 'Le champs relatif au nom ne doit pas dépasser 50 caractères')
        if len(domaine_activite) == 0:
            erreur = 1
            messages.error(request, 'Merci de compléter le champs relatif au nom complet')
        elif len(domaine_activite)>50:
            erreur = 1
            messages.error(request, 'Le champs relatif au nom ne doit pas dépasser 50 caractères')
        if erreur == 0:
            #Modification des info personnelles de USER
            us = request.user
            us.ICE = ICE
            us.adresse = adresse
            us.entreprise = entreprise
            us.domaineActivite = domaine_activite
            us.save()
            subUsers = User.objects.filter(lien=request.user.id)
            for u in subUsers:
                u.ICE = ICE
                u.adresse = adresse
                u.entreprise = entreprise
                u.domaineActivite = domaine_activite
                u.save()
            #messages.success(request, 'Votre modification a été bien enregistrée.')
            return redirect('connexion')
        if erreur == 1:
            user_validation =User(adresse=adresse, domaineActivite=domaine_activite)
            context = {
                'user_validation': user_validation,
            }
            return render(request, 'account/connected.html',context)

@login_required(login_url='login')
def userRemoveImage(request):
    request.user.photoProfile = ''
    request.user.save()
    return redirect('connexion')

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
