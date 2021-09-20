from gestion_clients.models import Client
from gestion_dgi.models import dgi_appt_casa
from account.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import PIL

 
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

class Rapport(models.Model):
  lat = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  lng = models.DecimalField(max_digits=20, decimal_places=18, null=True)
  prix_unit_estime = models.BigIntegerField(null=True, blank=True)
  is_locked = models.BooleanField(default=False, blank=True, null=True)
  username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  dgi_zone = models.ForeignKey(dgi_appt_casa, on_delete=models.CASCADE, null=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return str(self.descriptif)
  class Meta:
      db_table = "rapport_generer"  
