from api_map.models import Villes
from django.db import models

# Create your models here.
class ClientPhysique(models.Model):
  nom = models.CharField(max_length=50, null=True, blank=True)
  prenom = models.CharField(max_length=50, null=True, blank=True)
  email = models.CharField(max_length=50, null=True, blank=True)
  tel = models.CharField(max_length=10, null=True, blank=True)
  gsm = models.CharField(max_length=10, null=True, blank=True)
  cin = models.CharField(max_length=10, unique=True, null=True, blank=True)
  ICE = models.IntegerField(unique=True, null=True, blank=True)
  adresse= models.TextField(null=True, blank=True)
  pass
  class Meta:
    db_table = "Clients Physiques"
  def __str__(self):
    return str(self.nom)
 
class ClientMorale(models.Model):
  email = models.CharField(max_length=50, null=True, blank=True)
  tel = models.CharField(max_length=10, null=True, blank=True)
  GSM = models.CharField(max_length=10, null=True, blank=True)
  ICE = models.IntegerField(unique=True, null=True, blank=True)
  adresse= models.TextField(null=True, blank=True)
  denomination = models.CharField(max_length=250, null=True, blank=True)
  raison_sociale = models.CharField(max_length=250, null=True, blank=True)
  registre_de_commerce = models.CharField(max_length=250, null=True, blank=True)
  pass
  class Meta:
    db_table = "Clients Morale"
  def __str__(self):
    return str(self.nom)
