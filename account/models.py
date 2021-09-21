from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from datetime import date

DOMAINE_CHOICES = (
    ('Autre', 'Autre'),
    ('SG_AM', 'Société de gestion / Asset management'),
    ('B_L', 'Banque / Leasing'),
    ('P_D', 'Promoteur / Développeur'),
    ('TI','Transaction en immobilier'),
    ('C_EI','Conseil / Expertise en immobilier')
)
TypeUser_CHOICES = (
    ('principal', 'principal'),
    ('secondaire', 'secondaire')
)
TypeMap_CHOICES = (
    ('Leaflet', 'Leaflet'),
    ('Google', 'Google')
)
Facture_CHOICES = (
    ('EnAttente', 'En attente'),
    ('Paye', 'Payé'),
    ('Annule', 'Annulé')
)
Abonnement_CHOICES = (
    (0, 'Standard'),
    (1, 'Premium'),
    (2, 'premium +')
)
PERMISSION_CHOICES = (
    ('elaborateur','elaborateur'),
    ('visiteur', 'visiteur'),
    ('validateur', 'validateur')
)

class User(AbstractUser):
    photoProfile = models.FileField(upload_to='images/profiles/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg','tiff'])])
    tel1 = models.CharField(max_length=10, null=True, blank=True)
    tel2 = models.CharField(max_length=10, null=True, blank=True)
    entreprise = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=500, null=True, blank=True)
    ICE = models.CharField(max_length=15, null=True, blank=True)
    domaineActivite = models.CharField(max_length=25, null=True, blank=True, choices=DOMAINE_CHOICES)
    userType = models.CharField(max_length=100, choices=TypeUser_CHOICES, default="principal")
    lien = models.IntegerField(null=True, blank=True)#qd le user est secondaire
    credit_journalier = models.IntegerField(null=True, blank=True, default=30)
    credit_monsuel = models.IntegerField(null=True, blank=True, default=300)
    type_map = models.CharField(max_length=20, blank=True, null=True, choices=TypeMap_CHOICES, default='Leaflet')
    key_map = models.CharField(max_length=50, blank=True, null=True)
    permission = models.CharField(max_length=25, null=True, blank=True, choices=PERMISSION_CHOICES)
    my_ip = models.CharField(max_length=50, null=True, blank=True, default='127.0.0.1')
    pass
    class Meta:
        db_table = "User" 
    
class Credit(models.Model):
    credit_journalier = models.IntegerField(null=True)
    credit_monsuel = models.IntegerField(null=True)
    class Meta:
        db_table = "Credit" 

class Facture(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, choices=Facture_CHOICES, blank=True)
    region_choisis = ArrayField(models.CharField(max_length=3, null=True, blank=True), null=True, blank=True)
    nbrUtilisateur = models.IntegerField(null=True, blank=True)
    montant_HT = models.FloatField(null=True, blank=True)
    date_de_facturation= models.DateField(null=True, blank=True)
    date_expiration= models.DateField(null=True, blank=True)
    fichier_pdf_genere = models.FileField(upload_to='factures/%Y/%m/%d/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    fichier_pdf_justif = models.FileField(upload_to='factures/%Y/%m/%d/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    type_abonnement = models.IntegerField(null=True, blank=True, default=0, choices=Abonnement_CHOICES)
    is_pack_base = models.BooleanField(default=False)
    class Meta:
        db_table = "Facture" 


