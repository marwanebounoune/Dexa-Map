from gestion_dgi.models import dgi_appt_casa
from rest_framework import serializers

#le serializer de la classe Tags
class DGISerializer(serializers.ModelSerializer):
    class Meta:
        model = dgi_appt_casa
        fields = '__all__'