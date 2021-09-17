from django.contrib import admin
from .models import Pin
from .models import Photographie
from .models import Note

#enregistrement du model Pin
class PinAdmin(admin.ModelAdmin):
    #les champs à afficher sur la page de liste des pins pour modification de l’interface d’administration
    list_display = ('id', 'date_ajout', 'type_de_bien', 'type_de_reference', 'is_validate_by_user', 'ville_id')
    #les champs à afficher sur la page de liste des utilisateurs pour filtrage de l’interface d’administration
    list_filter = ( 'date_ajout',  'type_de_bien', 'is_validate_by_user',  'ville_id')

#enregistrement du model Photographie
class PhotographieAdmin(admin.ModelAdmin):
    #les champs à afficher sur la page de liste des photographies des pins pour modification de l’interface d’administration
    list_display = ('id','photo')

#enregistrement du model Note
class NoteAdmin(admin.ModelAdmin):
    #les champs à afficher sur la page de liste des notes des pins pour modification de l’interface d’administration
    list_display = ('id','note')

admin.site.register(Pin, PinAdmin)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Note, NoteAdmin)