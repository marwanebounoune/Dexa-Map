from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

#La classe représentant les devis
class table_devis(models.Model):
    # les choix de domaines d'activités des entreprises
    SECTEUR_CHOICES = (
        ('Autre', 'Autre'),
        ('SG_AM', 'Société de gestion / Asset management'),
        ('B_L', 'Banque / Leasing'),
        ('P_D', 'Promoteur / Développeur'),
        ('TI','Transaction en immobilier'),
        ('C_EI','Conseil / Expertise en immobilier')
    )
    # les status qu'un devis peut avoir
    STATUT_CHOICES = (
        (u'V', 'validé'),
        (u'NV', 'en cours de traitement')
    )
    nom = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True)
    telephone = models.CharField(max_length=10, null=True)
    societe = models.CharField(max_length=200, null=True)
    secteur = models.CharField(max_length=5, null=True, choices=SECTEUR_CHOICES)
    message = models.TextField(null=True)
    date_creation = models.DateTimeField(default=timezone.now)
    fichier_pdf = models.FileField(upload_to='devis/%Y/%m/%d/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    montant_HT = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=2, default='NV', choices=STATUT_CHOICES)
def __str__(self):
    return self.nom

