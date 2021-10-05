from gestion_clients.models import ClientPhysique
from gestion_dgi.models import dgi_appt_casa
from account.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import PIL
from datetime import date
from django.contrib.postgres.fields import ArrayField
 
TypeFile_CHOICES = (
  ('C_V','Contrat de vente'),
  ('C_P','Certificat de propriété'),
  ('P_C', 'Plan de cdastre')
)



class Rapport(models.Model):
  ref_dossier_interne = models.CharField(max_length=10, unique=True, null=True, blank=True)
  lat = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  lng = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  montant_demande = models.BigIntegerField(null=True, blank=True)
  prix_unit_estime = models.BigIntegerField(null=True, blank=True)
  asking_price = models.BigIntegerField(null=True, blank=True)
  is_locked = models.BooleanField(default=False, blank=True, null=True)
  comment = models.TextField(null=True, blank=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  dgi_zone = models.ForeignKey(dgi_appt_casa, on_delete=models.CASCADE, null=True)
  client = models.ForeignKey(ClientPhysique, on_delete=models.CASCADE, null=True)
  type_de_bien = models.IntegerField(null=True, blank=True)
  descreptif = models.IntegerField(null=True, blank=True)
  from_table = models.CharField(max_length=1,null=True, default="R")
  score = models.DecimalField(max_digits=10, decimal_places=9, null=True, default="0.5")
  #Descriptifs des facteurs liés à l'immeuble (11)
  descriptif_age_imm = models.IntegerField(null=True, blank=True)
  descriptif_nbr_niv = models.IntegerField(null=True, blank=True)
  descriptif_niv = models.IntegerField(null=True, blank=True)
  descriptif_nbr_appt_etage = models.IntegerField(null=True, blank=True)
  descriptif_ascenceur = models.IntegerField(null=True, blank=True)
  descriptif_stationnement = models.IntegerField(null=True, blank=True)
  descriptif_exploitation_etage = models.IntegerField(null=True, blank=True)
  descriptif_exploitation_rdc = models.IntegerField(null=True, blank=True)
  descriptif_securiteAccInterphone = models.IntegerField(null=True, blank=True)
  descriptif_securiteRes = models.IntegerField(null=True, blank=True)
  descriptif_acces_mob_reduite = models.IntegerField(null=True, blank=True)
  #Descriptifs des facteurs liés à l'appartement (6)
  descriptif_composistion_cuisine = models.IntegerField(null=True, blank=True)
  descriptif_composistion_sdb = models.IntegerField(null=True, blank=True)
  descriptif_composistion_salon = models.IntegerField(null=True, blank=True)
  descriptif_composistion_chambre = models.IntegerField(null=True, blank=True)
  descriptif_donne_sur = ArrayField(models.IntegerField(null=True, blank=True), blank=True, null=True)
  descriptif_orientation = ArrayField(models.IntegerField(null=True, blank=True), blank=True, null=True)
  #Descriptifs du standing
  #Descriptif des Chambres
  descriptif_chambr_sol = models.CharField(max_length=50, null=True, blank=True)
  descriptif_chambr_mur = models.CharField(max_length=50, null=True, blank=True)
  descriptif_chambr_plafon = models.CharField(max_length=50, null=True, blank=True)
  #Descriptif de la cuisine
  descriptif_cuisine_sol = models.CharField(max_length=50, null=True, blank=True)
  descriptif_cuisine_mur = models.CharField(max_length=50, null=True, blank=True)
  descriptif_cuisine_plafon = models.CharField(max_length=50, null=True, blank=True)
  #Descriptif des WCS
  descriptif_wc_sol = models.CharField(max_length=50, null=True, blank=True)
  descriptif_wc_mur = models.CharField(max_length=50, null=True, blank=True)
  descriptif_wc_plafon = models.CharField(max_length=50, null=True, blank=True)
  #Descriptif du hall salon
  descriptif_hall_salon_sol = models.CharField(max_length=50, null=True, blank=True)
  descriptif_hall_salon_mur = models.CharField(max_length=50, null=True, blank=True)
  descriptif_hall_salon_plafon = models.CharField(max_length=50, null=True, blank=True)
  #Description fenetres et portes
  descriptif_fenetres = models.IntegerField(null=True, blank=True)
  descriptif_type_aluminum = models.IntegerField(null=True, blank=True)
  descriptif_fenetres_manuel_electrique = models.IntegerField(null=True, blank=True)
  descriptif_portes = models.IntegerField(null=True, blank=True)
  #Descriptif des equipements
  descriptif_climatiseur = ArrayField(models.IntegerField(null=True, blank=True), blank=True, null=True)
  descriptif_sdb = ArrayField(models.IntegerField(null=True, blank=True), blank=True, null=True)
  descriptif_cuisine_equip = models.IntegerField(null=True, blank=True)
  #Situation juridique
  titre_foncier = models.CharField(max_length=9,null=True)
  date_cp = models.DateField(default=date.today, null=True)
  surface_titree = models.IntegerField(null=True, blank=True)
  conservation = models.CharField(max_length=50,null=True)
  fraction = ArrayField(ArrayField(models.CharField(max_length=25, null=True)), blank=True, null=True, default='{}')
  hypotheque = ArrayField(ArrayField(models.CharField(max_length=25, null=True)), blank=True, null=True, default='{}')
  def __str__(self):
    return str(self.score)

class Commentaire(models.Model):
  note = models.CharField(max_length=300, null=True)
  date = models.DateField(default=date.today, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, null=True)
  reponse_pour = models.IntegerField(null=True, blank=True, default='0')
  class Meta:
    db_table = "Rapport_commentaire"

class DocumentsRapport(models.Model):
  rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  type_file = models.CharField(max_length=40, null=True, choices=TypeFile_CHOICES)
  fichier = models.FileField(upload_to='doc_pins_my_map/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
  def _str_(self):
    return str(self.type_file)
  class Meta:
    db_table = "Rapport_documents"

class PhotographieRapport(models.Model):
  rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, null=True)
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