from django.contrib import admin
# Register your models here.
from .models import table_devis

#enregistrement du model table_devis
class table_devisAdmin(admin.ModelAdmin):
    
    #les champs à afficher sur la page de liste des devis de l’interface d’administration
    list_display = ('id', 'nom', 'email', 'telephone', 'societe', 'secteur', 'message', 'date_creation', 'status', 'montant_HT','fichier_pdf')
    #les champs à afficher sur la page de liste des devis pour filtrage de l’interface d’administration
    list_filter = ('date_creation', )
    #les champs à afficher comme des liens sur la page de liste des devis de l’interface d’administration
    list_display_links = ('id', 'nom')
    #les champs à afficher comme des champs modifiable sur la page de liste des devis de l’interface d’administration
    list_editable = ('status', 'fichier_pdf', 'montant_HT')
    #les champs à afficher comme des references de recherche sur la page de liste des devis de l’interface d’administration
    search_fields = ('nom', 'email', 'secteur', 'societe', 'status', 'telephone', 'montant_HT')
    #pagination pour l'affichage des devis de l’interface d’administration
    list_per_page = 5
admin.site.register(table_devis, table_devisAdmin )