from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import PIL

# Create your models here.
class Client(models.Model):
  nom = models.CharField(max_length=50, null=True, blank=True)
  prenom = models.CharField(max_length=50, null=True, blank=True)
  email = models.CharField(max_length=50, null=True, blank=True)
  tel = models.CharField(max_length=10, null=True, blank=True)
  cin = models.CharField(max_length=10, unique=True, null=True, blank=True)
  pass
  class Meta:
    db_table = "rapport_client"
  def __str__(self):
    return str(self.nom)
 
class SituationJuridique(models.Model):
    class Meta:
        db_table = "rapport_situation_juridique"
 
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
  class Meta:
      db_table = "rapport_photographie"