from django.contrib import admin
from .models import Facture, User
from django.contrib.auth.admin import UserAdmin as origin

#enregistrement du model User
class UserAdmin(origin):
    #les champs à afficher sur la page de liste des utilisateurs pour modification de l’interface d’administration
    list_display =  ('id', 'username', 'tel1','tel2','ICE','adresse','domaineActivite','userType', 'lien')
    #définir les champs qui seront affichés sur la page de création d'utilisateur.
    add_fieldsets = origin.add_fieldsets + ((None, {'fields': ('tel1','tel2','ICE','adresse','domaineActivite','userType', 'lien', 'credit_journalier', 'credit_monsuel', 'photoProfile')}),)

#enregistrement du model Facture 
class FactureAdmin(admin.ModelAdmin):
    #les champs à afficher sur la page de liste des factures pour modification de l’interface d’administration
    list_display =  ('id', 'username','statut')

admin.site.register(User, UserAdmin)
admin.site.register(Facture, FactureAdmin)
