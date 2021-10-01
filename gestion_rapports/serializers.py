from rest_framework import serializers
from .models import Commentaire, DocumentsRapport, PhotographieRapport, Rapport
from account.serializers import UserSerializer



class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = ('id', 'lat', 'lng', 'prix_unit_estime', 'is_locked', 'username', 'dgi_zone', 'client', 'type_de_bien', 'descreptif', 'from_table','score','descriptif_age_imm', 
        'descriptif_nbr_niv','descriptif_niv', 'descriptif_nbr_appt_etage', 'descriptif_ascenceur', 'descriptif_stationnement', 'descriptif_exploitation_etage', 
        'descriptif_exploitation_rdc', 'descriptif_securiteAccInterphone', 'descriptif_securiteRes', 'descriptif_acces_mob_reduite', 'descriptif_composistion_cuisine', 
        'descriptif_composistion_sdb', 'descriptif_composistion_salon', 'descriptif_composistion_chambre', 'descriptif_donne_sur', 'descriptif_orientation','descriptif_chambr_sol', 
        'descriptif_chambr_mur', 'descriptif_chambr_plafon', 'descriptif_cuisine_sol', 'descriptif_cuisine_mur', 'descriptif_cuisine_plafon', 'descriptif_wc_sol', 'descriptif_wc_mur', 
        'descriptif_wc_plafon', 'descriptif_hall_salon_sol', 'descriptif_hall_salon_mur', 'descriptif_hall_salon_plafon', 'descriptif_climatiseur','descriptif_sdb', 'descriptif_cuisine_equip', 
        'titre_foncier', 'date_cp', 'surface_titree', 'conservation', 'fraction', 'hypotheque', 'ref_dossier_interne', 'montant_demande', 'asking_price', 'comment', 'descriptif_fenetres', 
        'descriptif_type_aluminum', 'descriptif_fenetres_manuel_electrique', 'descriptif_portes')
        #pour la représentation imbriquée avec le model Ville, User, Region
        depth = 1

class DocumentsRapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsRapport
        username = UserSerializer()
        pin = RapportSerializer()
        fields = ('id', 'rapport', 'username','type_file','fichier')
        #pour la représentation imbriquée avec le model Pin & User
        depth = 1

class PhotographieRapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotographieRapport
        pin = RapportSerializer()
        fields = ('id', 'rapport', 'photo', 'descriptif')
        #pour la représentation imbriquée avec le model Pin
        depth = 1

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        editer_par = UserSerializer()
        pin = RapportSerializer()
        fields = ('id', 'note','date','username','rapport', 'reponse_pour')
        #pour la représentation imbriquée avec le model Pin & User
        depth = 1