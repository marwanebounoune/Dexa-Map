from django.contrib.gis import geos
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gestion_dgi.serializers import DGISerializer
from gestion_dgi.models import dgi_appt_casa
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

# Create your views here.
@api_view(['GET'])
@login_required(login_url='login')
def get_dgi_pin(request):
    latitude = request.GET.get('lat')
    longitude =  request.GET.get('lng')
    serializer = DGISerializer(get_dgi_zone(latitude,longitude), many=False)
    if serializer:
        return Response(serializer.data)
    content = {'message': "dgi non reconnu"}
    return Response(content)

def get_dgi(lat, lng):
    serializer = DGISerializer(get_dgi_zone(lat,lng), many=False)
    if serializer:
        return (serializer.data)
    return (None)

def check_point_inside_polygon(lat, lng, poly):
    point = Point(lng,lat)#lat and lng doit etre des float
    return point.within(poly)

def get_dgi_zone(lat, lng):
    polys = dgi_appt_casa.objects.all()
    for poly in polys:
        if check_point_inside_polygon(float(lat), float(lng), poly.poly):
            return poly
    return None