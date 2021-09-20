from django.contrib.postgres.fields.array import ArrayField
from api_map.models import TypeBien, Villes
from django.contrib.gis.db import models

#default=['order_status_changed', 'new_signal']
#def get_sous_type_default():
#    return list(dict(constants.NOTIFICATION_SOURCE).keys())
# Create your models here.
class dgi_appt_casa(models.Model):
    poly = models.PolygonField()
    name = models.CharField(max_length=50, blank=True, null=True)
    type_de_bien =  models.ForeignKey(TypeBien, on_delete=models.CASCADE, null=True)
    ville = models.ForeignKey(Villes, on_delete=models.CASCADE, null=True)
    sous_type = models.CharField(max_length=4, blank=True, null=True,choices=(('r', 'récent'), ('r_f', 'récent et fermé'), ('a', 'ancien'),('a_f', 'ancien et fermé')), default='r',)#
    prix_unit = models.BigIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "dgi_appt_casa"