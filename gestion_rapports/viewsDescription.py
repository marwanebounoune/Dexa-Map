import logging
from .serializers import RapportSerializer
from .models import Rapport
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.datastructures import MultiValueDictKeyError

@api_view(['POST'])
@login_required(login_url='login')  
def addDescription(request,pk):
    try:
        data = request.POST
        print("Data : ", data)
        #Section 1 (11)
        ageImm = data['ageImm']
        nbrNiv = data['nbrNiv']
        niv = data['niv']
        nbrApptEtg = data['nbrApptEtg']
        stationnement = data['stationnement']
        if(ageImm == ''):
            ageImm = None
        if(nbrNiv == ''):
            nbrNiv = None
        if(niv == ''):
            niv = None
        if(nbrApptEtg == ''):
            nbrApptEtg = None
        if(stationnement == ''):
            stationnement = None
        radioAscenceur = data['radioAscenceur']
        radioExpEtage = data['radioExpEtage']
        radioExpRdc = data['radioExpRdc']
        radioAccMobRed = data['radioAccMobRed']
        radioAccInterphone = data['radioAccInterphone']
        radioResidenceSecurisee = data['radioResidenceSecurisee']

        #Section 2 (10)
        nbrCuisine = data['nbrCuisine']
        nbrSDB = data['nbrSDB']
        nbrSalon = data['nbrSalon']
        nbrChambres = data['nbrChambres']
        
        if(nbrCuisine == ''):
            nbrCuisine = None
        if(nbrSDB == ''):
            nbrSDB = None
        if(nbrSalon == ''):
            nbrSalon = None
        if(nbrChambres == ''):
            nbrChambres = None
        
        try:
            checkboxDonneSurRue = data['checkboxDonneSurRue']
        except MultiValueDictKeyError:
            checkboxDonneSurRue = 0
        try:
            checkboxDonneSurCour = data['checkboxDonneSurCour']
        except MultiValueDictKeyError:
            checkboxDonneSurCour = 0
        try:
            checkboxDonneSurEspCom = data['checkboxDonneSurEspCom']
        except MultiValueDictKeyError:
            checkboxDonneSurEspCom = 0
        try:
            checkboxOrientationNord = data['checkboxOrientationNord']
        except MultiValueDictKeyError:
            checkboxOrientationNord = 0
        try:
            checkboxOrientationSud = data['checkboxOrientationSud']
        except MultiValueDictKeyError:
            checkboxOrientationSud = 0
        try:
            checkboxOrientationNeutre = data['checkboxOrientationNeutre']
        except MultiValueDictKeyError:
            checkboxOrientationNeutre = 0
        
        #Section 3 (16)
        chambre_sol = data['chambre_sol']
        chambre_mur = data['chambre_mur']
        chambre_plafond = data['chambre_plafond']

        cuisine_sol = data['cuisine_sol']
        cuisine_mur = data['cuisine_mur']
        cuisine_plafond = data['cuisine_plafond']

        wc_sol = data['wc_sol']
        wc_mur = data['wc_mur']
        wc_plafond = data['wc_plafond']

        hallSalon_sol = data['hallSalon_sol']
        hallSalon_mur = data['hallSalon_mur']
        hallSalon_plafond = data['hallSalon_plafond']

        if(chambre_sol == ''):
            chambre_sol = None
        if(chambre_mur == ''):
            chambre_mur = None
        if(chambre_plafond == ''):
            chambre_plafond = None
        
        if(cuisine_sol == ''):
            cuisine_sol = None
        if(cuisine_mur == ''):
            cuisine_mur = None
        if(cuisine_plafond == ''):
            cuisine_plafond = None
            
        if(wc_sol == ''):
            wc_sol = None
        if(wc_mur == ''):
            wc_mur = None
        if(wc_plafond == ''):
            wc_plafond = None
            
        if(hallSalon_sol == ''):
            hallSalon_sol = None
        if(hallSalon_mur == ''):
            hallSalon_mur = None
        if(hallSalon_plafond == ''):
            hallSalon_plafond = None
        
        radioFenetres = data['radioFenetres']
        radioTypeFenetres = data['radioTypeFenetres']
        ManuelElectrique = data['ManuelElectrique']

        portes = data['portes']

        if(portes == ''):
            portes = None

        #Section 4 (6)
        try:
            checkboxClimatiseurSalon = data['checkboxClimatiseurSalon']
        except MultiValueDictKeyError:
            checkboxClimatiseurSalon = 0
        try:
            checkboxClimatiseurChambre = data['checkboxClimatiseurChambre']
        except MultiValueDictKeyError:
            checkboxClimatiseurChambre = 0
        try:
            checkboxClimatiseurNeant = data['checkboxClimatiseurNeant']
        except MultiValueDictKeyError:
            checkboxClimatiseurNeant = 0
        try:
            checkboxSdbBaignoire = data['checkboxSdbBaignoire']
        except MultiValueDictKeyError:
            checkboxSdbBaignoire = 0
        try:
            checkboxSdbDouche = data['checkboxSdbDouche']
        except MultiValueDictKeyError:
            checkboxSdbDouche = 0
        radioCuisineEquip = data['radioCuisineEquip']

        rapport = Rapport.objects.get(id = pk)
        #Section 1 (11)

        rapport.descriptif_age_imm = ageImm
        print("-------------------rapport.descriptif_age_imm--------------------------- : ", rapport.descriptif_age_imm)
        rapport.descriptif_nbr_niv = nbrNiv
        rapport.descriptif_niv = niv
        rapport.descriptif_nbr_appt_etage = nbrApptEtg
        rapport.descriptif_ascenceur = radioAscenceur
        rapport.descriptif_stationnement = stationnement
        rapport.descriptif_exploitation_etage = radioExpEtage
        rapport.descriptif_exploitation_rdc = radioExpRdc
        rapport.descriptif_securiteAccInterphone = radioAccInterphone
        rapport.descriptif_securiteRes = radioResidenceSecurisee
        rapport.descriptif_acces_mob_reduite = radioAccMobRed
        
        #Section 2 (6)
        rapport.descriptif_composistion_cuisine = nbrCuisine
        rapport.descriptif_composistion_sdb = nbrSDB
        rapport.descriptif_composistion_salon = nbrSalon
        rapport.descriptif_composistion_chambre = nbrChambres
        
        descriptif_donne_sur_x = []
        descriptif_donne_sur_x.append(checkboxDonneSurRue)
        descriptif_donne_sur_x.append(checkboxDonneSurCour)
        descriptif_donne_sur_x.append(checkboxDonneSurEspCom)
        rapport.descriptif_donne_sur = descriptif_donne_sur_x

        descriptif_orientation_x = []
        descriptif_orientation_x.append(checkboxOrientationNord)
        descriptif_orientation_x.append(checkboxOrientationSud)
        descriptif_orientation_x.append(checkboxOrientationNeutre)
        rapport.descriptif_orientation = descriptif_orientation_x

        #Section 3 (16)
        #Descriptif des Chambres
        rapport.descriptif_chambr_sol = chambre_sol
        rapport.descriptif_chambr_mur = chambre_mur
        rapport.descriptif_chambr_plafon = chambre_plafond
        #Descriptif de la cuisine
        rapport.descriptif_cuisine_sol = cuisine_sol
        rapport.descriptif_cuisine_mur = cuisine_mur
        rapport.descriptif_cuisine_plafon = cuisine_plafond
        #Descriptif des WCS
        rapport.descriptif_wc_sol = wc_sol
        rapport.descriptif_wc_mur = wc_mur
        rapport.descriptif_wc_plafon = wc_plafond
        #Descriptif du hall salon
        rapport.descriptif_hall_salon_sol = hallSalon_sol
        rapport.descriptif_hall_salon_mur = hallSalon_mur
        rapport.descriptif_hall_salon_plafon = hallSalon_plafond
        #Description fenetres et portes
        rapport.descriptif_fenetres = radioFenetres
        rapport.descriptif_type_aluminum = radioTypeFenetres
        rapport.descriptif_fenetres_manuel_electrique = ManuelElectrique
        rapport.descriptif_portes = portes

        #Section 4 (6)
        descriptif_climatiseur_x = []
        descriptif_climatiseur_x.append(checkboxClimatiseurSalon)
        descriptif_climatiseur_x.append(checkboxClimatiseurChambre)
        descriptif_climatiseur_x.append(checkboxClimatiseurNeant)
        rapport.descriptif_climatiseur = descriptif_climatiseur_x
        
        descriptif_sdb_x = []
        descriptif_sdb_x.append(checkboxSdbBaignoire)
        descriptif_sdb_x.append(checkboxSdbDouche)
        rapport.descriptif_sdb = descriptif_sdb_x

        rapport.descriptif_cuisine_equip = radioCuisineEquip

        #Save rapport
        rapport.save()
        serializer = RapportSerializer(rapport, many=False)
        return Response(serializer.data)

    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass