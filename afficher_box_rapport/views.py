from django.contrib import messages
from afficher_box_rapport.serializers import RapportSerializer
from afficher_box_rapport.models import Client, Rapport
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gestion_dgi.views import check_point_inside_polygon, get_dgi_zone
from api_map.serializers import PinSerializerLegerPrix
from django.shortcuts import render
from math import cos, asin, sqrt, pi
from api_map.models import  Pin
import statistics
# Create your views here.

@api_view(['GET'])
@login_required(login_url='login')
def CreerRapport(request):
    if request.method == 'GET':
        erreur = 0
        lat = request.GET['lat']
        lng = request.GET['lng']
        if erreur == 0:
            rapport = Rapport(lat=lat, lng=lng, username=request.user)
            rapport.save()
            serializer = RapportSerializer(rapport, many=False)
            return Response(serializer.data)



@api_view(['GET'])
@login_required(login_url='login')
def updateRapportClient(request):
    if request.method == 'GET':
        id_rapport = request.GET['id']
        client_id = request.GET['client_id']
        print(client_id)
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
    moy = estimation_prix(prix_array)
    serializer = PinSerializerLegerPrix(pins_res, many=True)
    return Response(serializer.data)
        
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))

def estimation_prix(array):
    moyenne = statistics.mean(array)
    return moyenne
