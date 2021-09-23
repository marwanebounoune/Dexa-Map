from django.db import models

# Create your models here.
class Client(models.Model):
  nom = models.CharField(max_length=50, null=True, blank=True)
  prenom = models.CharField(max_length=50, null=True, blank=True)
  email = models.CharField(max_length=50, null=True, blank=True)
  tel = models.CharField(max_length=10, null=True, blank=True)
  cin = models.CharField(max_length=10, unique=True, null=True, blank=True)
  pass
  class Meta:
    db_table = "Clients"
  def __str__(self):
    return str(self.nom)
 
