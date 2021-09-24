from gestion_clients.models import Client
from gestion_dgi.models import dgi_appt_casa
from account.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import PIL
from datetime import date
from django.contrib.postgres.fields import ArrayField
 



class Photographie(models.Model):
  #pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True)
  photo = models.ImageField(upload_to='images/rapport/%Y/%m/%d',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg','tiff'])])
  descriptif = models.CharField(max_length=200, null=True)
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    image = Image.open(self.photo.path)
    width, height = image.size
    print("width: --",width)
    print("height: --",height)
    image=image.resize((width, height), PIL.Image.ANTIALIAS)
    image.save(self.photo.path)
    #return instance
  def __str__(self):
    return str(self.descriptif)

class Rapport(models.Model):
  lat = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  lng = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  prix_unit_estime = models.BigIntegerField(null=True, blank=True)
  is_locked = models.BooleanField(default=False, blank=True, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  dgi_zone = models.ForeignKey(dgi_appt_casa, on_delete=models.CASCADE, null=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
  type_de_bien = models.IntegerField(null=True, blank=True)
  descreptif = models.IntegerField(null=True, blank=True)
  from_table = models.CharField(max_length=1,null=True, default="R")
  score = models.IntegerField(null=True, blank=True)
  #Descriptifs des facteurs liés à l'immeuble
  descriptif_age_imm = models.IntegerField(null=True, blank=True)
  descriptif_nbr_niv = models.IntegerField(null=True, blank=True)
  descriptif_niv = models.IntegerField(null=True, blank=True)
  descriptif_nbr_appt_etage = models.IntegerField(null=True, blank=True)
  descriptif_ascenceur = models.IntegerField(null=True, blank=True)
  descriptif_stationnement = models.IntegerField(null=True, blank=True)
  descriptif_exploitation_etage = models.IntegerField(null=True, blank=True)
  descriptif_exploitation_rdc = models.IntegerField(null=True, blank=True)
  descriptif_securite = models.IntegerField(null=True, blank=True)
  descriptif_acces_mob_reduite = models.IntegerField(null=True, blank=True)
  #Descriptifs des facteurs liés à l'appartement
  descriptif_composistion = models.IntegerField(null=True, blank=True)
  descriptif_donne_sur = models.IntegerField(null=True, blank=True)
  descriptif_orientation = models.IntegerField(null=True, blank=True)
  #Descriptifs du standing
  #Descriptif des Chambres
  descriptif_chambr_sol = models.IntegerField(null=True, blank=True)
  descriptif_chambr_mur = models.IntegerField(null=True, blank=True)
  descriptif_chambr_plafon = models.IntegerField(null=True, blank=True)
  #Descriptif de la cuisine
  descriptif_cuisine_sol = models.IntegerField(null=True, blank=True)
  descriptif_cuisine_mur = models.IntegerField(null=True, blank=True)
  descriptif_cuisine_plafon = models.IntegerField(null=True, blank=True)
  #Descriptif des WCS
  descriptif_wc_sol = models.IntegerField(null=True, blank=True)
  descriptif_wc_mur = models.IntegerField(null=True, blank=True)
  descriptif_wc_plafon = models.IntegerField(null=True, blank=True)
  #Descriptif du hall salon
  descriptif_hall_salon_sol = models.IntegerField(null=True, blank=True)
  descriptif_hall_salon_mur = models.IntegerField(null=True, blank=True)
  descriptif_hall_salon_plafon = models.IntegerField(null=True, blank=True)
  #Descriptif des equipements
  descriptif_climatiseur = models.IntegerField(null=True, blank=True)
  descriptif_sdb = models.IntegerField(null=True, blank=True)
  descriptif_cuisine_equip = models.IntegerField(null=True, blank=True)
  #Situation juridique
  titre_foncier = models.CharField(max_length=9,null=True)
  date_cp = models.DateField(default=date.today, null=True)
  surface_titree = models.IntegerField(null=True, blank=True)
  conservation = models.CharField(max_length=50,null=True)
  fraction = ArrayField(ArrayField(models.CharField(max_length=25, null=True)), blank=True, null=True)
  hypotheque = ArrayField(ArrayField(models.CharField(max_length=25, null=True)), blank=True, null=True)
  def __str__(self):
    return str(self.score)

class Commentaire(models.Model):
  note = models.CharField(max_length=300, null=True)
  date = models.DateField(default=date.today, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, null=True)
  reponse_pour = models.IntegerField(null=True, blank=True)
  class Meta:
    unique_together = ('username', 'rapport')