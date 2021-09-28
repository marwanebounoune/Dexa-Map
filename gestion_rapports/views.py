from gestion_clients.models import ClientPhysique
from rest_framework import response
from gestion_dgi.models import dgi_appt_casa
import logging
from django.contrib import messages
from .serializers import DocumentsRapportSerializer, PhotographieRapportSerializer, RapportSerializer
from .models import DocumentsRapport, PhotographieRapport, Rapport
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gestion_dgi.views import check_point_inside_polygon, get_dgi, get_dgi_zone
from api_map.serializers import PinSerializerLegerPrix
from django.shortcuts import render
from math import cos, asin, sqrt, pi
from api_map.models import  Pin
import statistics
from datetime import date
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
# Create your views here.

@api_view(['POST'])
@login_required(login_url='login')
def CreerRapport(request):
    if request.method == 'POST':
        erreur = 0
        lat = request.POST['lat']
        lng = request.POST['lng']
        dgi = get_dgi(lat, lng)
        dgi_zone = dgi_appt_casa.objects.get(id=dgi['id'])
        type_de_bien = request.POST['type_de_bien']
        if (ClientPhysique.objects.filter(cin=request.POST['cin']).exists() == False):
            erreur=1
            content = {'message': "Ce client n'existe pas."}
            return Response(content)
        if erreur == 0:
            client = ClientPhysique.objects.get(cin= request.POST['cin'])
            rapport = Rapport(lat=lat, lng=lng, client=client, username=request.user, type_de_bien=type_de_bien, dgi_zone=dgi_zone)
            rapport.save()
            serializer = RapportSerializer(rapport, many=False)
            return Response(serializer.data)

@api_view(['POST'])
@login_required(login_url='login')
def situationJuridique(request, pk):
    if request.method == 'POST':
        my_rapport = Rapport.objects.get(id=pk)
        print(my_rapport)
        titre_foncier = request.POST['titre_foncier']
        date_cp = request.POST['date_cp']
        surface_titree = request.POST['surface_titree']
        conservation = request.POST['conservation']
        my_rapport.titre_foncier=titre_foncier
        my_rapport.date_cp=date_cp
        my_rapport.surface_titree=surface_titree
        my_rapport.conservation=conservation
        my_rapport.save()
        serializer = RapportSerializer(my_rapport, many=False)
        return Response(serializer.data)

@api_view(['POST'])
@login_required(login_url='login')
def editRapport(request, pk):
    if request.method == 'POST':
        my_rapport = Rapport.objects.get(id=pk)
        my_rapport.montant_demande = request.POST['montant_credit_demande']
        my_rapport.ref_dossier_interne = request.POST['ref_dossier_interne']
        my_rapport.asking_price = request.POST['asking_price']
        my_rapport.comment = request.POST['commentaire']
        my_rapport.type_de_bien = request.POST['type_de_bien_edit_rapport']
        my_rapport.save()
        serializer = RapportSerializer(my_rapport, many=False)
        return Response(serializer.data)

@api_view(['GET'])
@login_required(login_url='login')
def updateRapportClient(request):
    if request.method == 'GET':
        id_rapport = request.GET['id']
        client_id = request.GET['client_id']
        my_rapport = Rapport.objects.get(id=id_rapport)
        my_rapport.client = client_id
        my_rapport.save()
        serializer = RapportSerializer(my_rapport, many=False)
        return Response(serializer.data)

@api_view(['GET'])
@login_required(login_url='login')
def get_approxim_pins(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    pins_res=[]
    prix_array = []
    dgi = get_dgi_zone(lat,lng)
    pins= Pin.objects.filter(deleted=False).filter(type_de_reference=1)#.filter(is_validate_by_user=True)
    for pin in pins:
        lat_pin = float(pin.lat)
        lng_pin = float(pin.lng)
        d = distance(float(lat), float(lng), float(lat_pin), float(lng_pin))
        if d<1 and check_point_inside_polygon(lat_pin, lng_pin, dgi.poly):
            pins_res.append(pin)
            prix_array.append(pin.prix_unit)
    prix_array.append(dgi.prix_unit)
    moy = estimation_prix(prix_array)
    serializer = PinSerializerLegerPrix(pins_res, many=True)
    content = {'pins': serializer.data,
    'prix_estimer': int(moy)
    }
    return response.Response(content)
        
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))

def estimation_prix(array):
    moyenne = statistics.mean(array)
    return moyenne

@api_view(['GET'])
@login_required(login_url='login')
def getRapport(request, pk):
    if request.method == 'GET':
        pin = Rapport.objects.get(id=pk)
        serializer = RapportSerializer(pin, many=False)
        return Response(serializer.data)

def estimation_prix(array):
    moyenne = statistics.mean(array)
    return moyenne

@api_view(['GET'])
@login_required(login_url='login')
def preview_pdf(request):
    data = {
            #'today': datetime.date.today(), 
        'amount': 39.99,
        'customer_name': 'Cooper Mann',
        'order_id': 1233434,
    }
    return render(request,'my_map/gestion_rapports/pdf.html', data)

@api_view(['POST'])
@login_required(login_url='login')
def addFraction(request, pk):
    try:
        data = request.POST
        erreur = 0
        fraction = data['fraction']
        consistance = data['consistance']
        surface = data['surfaceFraction']
        if len(fraction)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au fraction"}
            return Response(content)
        if len(consistance)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au consistance"}
            return Response(content)
        if len(surface)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au surface"}
            return Response(content)
        if erreur == 0:
            my_rapport = Rapport.objects.get(id=pk)
            fract = []
            fract.append(str(fraction))
            print(fract)
            fract.append(str(consistance))
            fract.append(str(surface))
            print(fract)
            fract1 = []
            fract1.append(fract)
            my_rapport.fraction.append(fract)
            my_rapport.save()
            serializer = RapportSerializer(my_rapport, many=False)
            return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['POST'])
@login_required(login_url='login')
def addHypotheque(request, pk):
    try:
        data = request.POST
        erreur = 0
        montant = data['montantHypotheque']
        auProfitDe = data['au_profit_de']
        date_hypo = data['dateHypo']
        if len(montant)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au fraction"}
            return Response(content)
        if len(auProfitDe)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au consistance"}
            return Response(content)
        if len(date_hypo)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au surface"}
            return Response(content)
        if erreur == 0:
            my_rapport = Rapport.objects.get(id=pk)
            hypo = []
            hypo.append(str(montant))
            hypo.append(str(auProfitDe))
            hypo.append(str(date_hypo))
            my_rapport.hypotheque.append(hypo)
            my_rapport.save()
            serializer = RapportSerializer(my_rapport, many=False)
            return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['POST'])
@login_required(login_url='login')
def create_docs_rapport(request, pk):
    try:
        if request.method == 'POST':
            erreur = 0
            #Récupération de la Data
            data = request.data
            doc_type_1 = data['type_annexe_rapport']
            doc1=False
            try:
                doc1=request.FILES['annexe_rapport']
            except MultiValueDictKeyError:
                doc1 = False
            
            if doc1==False and len(doc_type_1)==0:
                erreur = 1 
                content = {'message': "Merci d'importer une piece jointe"} 
                return Response(content)
            if doc1!=False:
                if doc1.name.endswith('.pdf') == False:
                    erreur = 1
                    content = {'message': "le format du fichier doit etre un pdf"} 
                    return Response(content) 
                if doc1.size > 2000000:
                    erreur = 1
                    content = {'message': "la taille du fichier ne doit pas depasser 2Mo"} 
                    return Response(content)  
                if len(doc_type_1) == 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif au type la pièce jointe"} 
                    return Response(content)
            else:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a la pièce jointe"} 
                return Response(content)
            if erreur==0:
                doc_new = DocumentsRapport(rapport_id=pk, username= request.user, type_file= doc_type_1)
                doc_new.fichier.save(doc1.name, doc1)
                doc_new.save()
                serializer = DocumentsRapportSerializer(doc_new, many=False)
                return Response(serializer.data)        
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuper les pieces jointes d'un pin
@api_view(['GET'])
@login_required(login_url='login') 
def getPieceJointeByIdPin(request, pk):
    try:
        piece_jointes = DocumentsRapport.objects.filter(rapport_id=pk)
        serializer = DocumentsRapportSerializer(piece_jointes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['POST'])
@login_required(login_url='login')
def ajoutPhotographiesRapport(request, pk):
    try:
        erreur = 0
        data = request.data
        images = request.FILES.getlist('imageRapport')
        images_desc = data['descriptionImageRapport']
        img=[]
        photos_existantes = PhotographieRapport.objects.filter(rapport_id = pk)
        nbr_photos = len(photos_existantes)
        nbr_photos_max = 12 - nbr_photos
        #validation images
        if len(images)==0:
            if len(images_desc) != 0:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a l'image"} 
                return Response(content)
        else:
            if len(images) > nbr_photos_max:
                erreur = 1
                content = {'message': "Vous pouvez inserer seulement "+ str(nbr_photos_max) +" images"}
                return Response(content)
        
        # save images if exists
        if len(images) != 0 and erreur == 0:
            for image in images:
                photo = PhotographieRapport(rapport_id=pk, descriptif=images_desc)
                photo.photo.save(image.name, image)
                photo.save()
                img.append(photo)
            serializer = PhotographieRapportSerializer(img, many=True)
            return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['GET'])
@login_required(login_url='login') 
def getPhotographiesRapport(request, pk):
    try:
        photos = PhotographieRapport.objects.filter(rapport_id=pk)
        serializer = PhotographieRapportSerializer(photos, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['GET'])
@login_required(login_url='login')
def dropPhotoRapport(request,pk):
    try:
        photo_rapport = PhotographieRapport.objects.get(id=pk)
        photo_rapport.delete()
        serializer = PhotographieRapportSerializer(photo_rapport, many=False)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass