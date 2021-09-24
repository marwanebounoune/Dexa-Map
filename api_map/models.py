import PIL
from account.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from datetime import date
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from PIL import Image
#Les types des biens immobiliers
TypeDeBien_CHOICES = (
  ('1', 'Residentiel'),
  ('2', 'Villa'),
  ('3', 'Maison'),
  ('4', 'Professionnel'),
  ('5', 'Commercial'),
  ('6','Industriel'),
  ('7', 'Terrain Villa'),
  ('8', 'Terrain Industriel'),
  ('9', 'Terrain urbain'),
  ('10', 'Terrain agricole')
)
#Les types des réferences des biens
TypeDeReference_CHOICES = (
  ('1', 'Vente'),
  ('2', 'Location'),
  ('3', 'Rapport')
)
#Les types des pieces jointes des biens
TypeFile_CHOICES = (
  ('C_V','Contrat de vente'),
  ('C_L','Contrat de location')
)

#La classe représentant les regions du maroc
class Regions(models.Model):
  name = models.CharField(max_length=50, null=True, blank=True)
  def __str__(self):
    return str(self.name)

#La classe représentant les villes du maroc
class Villes(models.Model):
  name = models.CharField(max_length=50, null=True, blank=True)
  region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True)
  def __str__(self):
    return str(self.name)

#(classe non utilisée )
class TypeBien(models.Model):
  name = models.CharField(max_length=50, null=True, blank=True)
  def __str__(self):
    return str(self.name)

#(classe non utilisée )
class TypeRef(models.Model):
  name = models.CharField(max_length=50, null=True, blank=True)
  def __str__(self):
    return str(self.name)
  
#(classe non utilisée )
class Pin(models.Model):
  lat = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  lng = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  type_de_bien = models.IntegerField(null=True, blank=True)
  type_de_reference = models.IntegerField(null=True, blank=True)
  label = models.CharField(max_length=4, unique=True,null=True, blank=True)
  ville = models.ForeignKey(Villes, on_delete=models.CASCADE, null=True)
  region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True)
  adresse = models.TextField(null=True, blank=True)
  date_ajout = models.DateField(default=date.today, null=True)
  actualisation = ArrayField(ArrayField(models.CharField(max_length=25, null=True)), blank=True, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  user_editer = models.IntegerField(null=True, blank=True)
  user_valider = models.IntegerField(null=True, blank=True)
  contact = models.TextField(null=True, blank=True)
  surface = models.BigIntegerField(null=True, blank=True)
  prix_unit = models.BigIntegerField(null=True, blank=True)
  prix_total = models.BigIntegerField(null=True, blank=True)
  descriptif = models.TextField(null=True, blank=True)
  tags = models.CharField(max_length=500, null=True)
  is_validate_by_user = models.BooleanField(default=False, blank=True, null=True)
  deleted = models.BooleanField(default=False, blank=True, null=True)
  chute_fonciere = models.IntegerField(null=True, blank=True)#
  rue  = models.CharField(max_length=500,null=True)
  is_localized = models.BooleanField(default=True, blank=True, null=True)
  from_mobile = models.BooleanField(default=False, blank=True, null=True)
  from_table = models.CharField(max_length=1,null=True, default="D")

  class Meta:
    indexes = [models.Index(fields=['username', ]),
      models.Index(fields=['deleted', ]),
      models.Index(fields=['is_validate_by_user', ]),
      models.Index(fields=['region', ]),
      models.Index(fields=['type_de_reference', ]),
      models.Index(fields=['type_de_bien', ])]
    db_table = "Dexa_pin"

  def __str__(self):
    return self.label
  def baseN(self, num,b,numerals="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"):
    result = ((num == 0) and numerals[0]) or (self.baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
    if len(result)<4:
      limit = 4-len(result)
      while limit !=0:
        result="0"+result
        limit-=1
    return result
  #redefinir la methode save pour convertir label
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if not self.label:
      #conversion en base 62
      self.label = self.baseN(self.pk, 62)#14750000
      super().save(update_fields=['label'])


#La classe représentant les photos des biens
class Photographie(models.Model):
  pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True)
  photo = models.FileField(upload_to='images/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg','tiff'])])
  descriptif = models.CharField(max_length=40, null=True)
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    #instance = super(Photographie, self).save(*args, **kwargs)
    #image = Image.open(instance.photo.path)
    image = Image.open(self.photo.path)
    width, height = image.size
    print("width: --",width)
    print("height: --",height)
    #image.save(self.photo.path,quality=20,optimize=True)
    image=image.resize((width, height), PIL.Image.ANTIALIAS)
    image.save(self.photo.path)
    #return instance
  def __str__(self):
    return str(self.descriptif)
  class Meta:
    db_table = "Dexa_photographies"

#La classe représentant les Notes des biens
class Note(models.Model):
  note = models.CharField(max_length=300, null=True)
  date= models.DateField(default=date.today, null=True)
  editer_par = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True)
  class Meta:
    unique_together = ('editer_par', 'pin')
    db_table = "Dexa_notes"

#La classe représentant les historiques des utilisateurs
class HistoriqueExplorer(models.Model):
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True) 
  date_consultation = models.DateField(default=date.today, null=True)
  class Meta:
    db_table = "Dexa_historique_explorer"

#La classe représentant les historiques des references modifiees
class HistoriqueMyMap(models.Model):
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True)
  date_consultation = models.DateField(default=date.today, null=True)
  class Meta:
    db_table = "Dexa_historique_my_map"

#La classe représentant les documents des biens
class Documents(models.Model):
  pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  type_file = models.CharField(max_length=40, null=True, choices=TypeFile_CHOICES)
  fichier = models.FileField(upload_to='doc_pins_my_map/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
  def _str_(self):
    return str(self.type_file)
  class Meta:
    db_table = "Dexa_documents"

#La classe représentant les tags des biens
class Tags(models.Model):
  label = models.CharField(max_length=250, null=True, blank=True)
  def _str_(self):
    return str(self.label)
  class Meta:
    db_table = "Dexa_tags"
