from realtysoft.logger_settings import LOGGING
from api_map.views import typeDeBien_to_id, typeDeRererence_to_id
from api_map.views import validate_LatAndLng
from api_map.serializers import PinSerializerLeger
from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from decimal import Decimal, DecimalException
from django.utils.datastructures import MultiValueDictKeyError
import pandas as pd
from api_map.models import Pin
import datetime
from fold_to_ascii import fold

#la méthode de gestion de l'importation csv
@api_view(['POST'])
@login_required(login_url='login')
def pinImport(request):
    try:
        if request.method == 'POST':
            if request.user.userType == "principal" or request.user.permission == 'elaborateur' or request.user.permission == 'visiteur':
                erreur = 0
                field_erreur = 0
                user = request.user
                csv_file = False
                new_pins = []
                #verifiv=cation du fichier
                try: 
                    csv_file = request.FILES['file_CSV']
                except MultiValueDictKeyError:
                    csv_file = False
                j=5000
                if csv_file == False:
                        erreur = 1
                        content = {'message': "Merci d'importer un fichier"}
                        return Response(content)
                if csv_file != False and len(csv_file) != 0:
                    if csv_file.name.endswith('.csv') == False:                   
                        erreur = 1
                        content = {'message': "le format du fichier doit etre un csv"} 
                        return Response(content)

                    if csv_file.size > 2000000:
                        erreur = 1
                        content = {'message': "la taille du fichier ne doit pas depasser 2 Mo"}
                        return Response(content)

                if erreur == 0:
                    data = pd.read_csv(request.FILES['file_CSV'], delimiter=";", decimal=".")
                    list =  ['date de reference','type de reference','surface','description','contact','prix unitaire','prix total','longitude','latitude','type de bien','region','ville','tags', "Quote-part terrain"]
                    extra_columns = 0
                    list_match = 1
                    regex = datetime.datetime.strptime
                    for col in data.columns: 
                        if col not in list:
                            extra_columns=1
                            content = {'message': "'"+col+"' C'est un intrus, Veuillez respecter les nomenclatures et le nombre des champs indiqué dans la discription."}
                            return Response(content)
                    if len(data.columns) < len(list):
                        list_match = 0
                        content = {'message': "Des colonnes vous manques dans votre fichier cvs, Veuillez declarer tous les champs indiqué dans la discription"}
                        return Response(content)
                    
                    if extra_columns == 0 and list_match == 1:
                        Number_cols = ["surface", "latitude", "longitude", "prix unitaire", "prix total", "region", "ville", "Quote-part terrain"]
                        String_cols = ["date de reference", "type de bien", "tags", "type de reference", "contact", "description"]
                        data.update(data[Number_cols].fillna('0'))
                        data.update(data[String_cols].fillna(''))
                        day,month,year = 1,1,1
                        nbr_ligne = 1
                        for date_ref, lat, lng, type_de_bien, type_de_reference, region, contact, surface, prix_unit, prix_unit_total, descriptif, ville, tags, chute_fonciere in zip(data["date de reference"], data["latitude"], data["longitude"], data["type de bien"], data["type de reference"], data["region"], data["contact"], data["surface"], data["prix unitaire"], data["prix total"], data["description"], data["ville"], data["tags"], data["Quote-part terrain"]):
                            nbr_ligne+=1
                            date_ref = date_ref.strip()
                            type_de_reference = type_de_reference.lower()
                            type_de_bien = fold(type_de_bien.strip().lower())
                            if lat=='0' and lng=='0' and len(type_de_bien) == 0 and len(type_de_reference) == 0 and prix_unit == '0' and prix_unit_total == '0' and surface == '0' and len(descriptif) == 0 and region=='0':
                                field_erreur = 1
                                content = {'message': "la ligne: "+str(nbr_ligne)+" contient des données manquante. merci de completer les donnees relatif à cette ligne."}
                                return Response(content)
                            if len(date_ref) != 0:
                                try:
                                    regex(date_ref, '%d/%m/%Y')
                                    day,month,year = date_ref.strip().split('/')
                                except ValueError:
                                    try:
                                        regex(date_ref, '%d-%m-%Y')
                                        day,month,year = date_ref.strip().split('-')
                                    except ValueError:
                                        field_erreur = 1
                                        content = {'message': "la date doit être sous format de dd/mm/yy ou dd-mm-yy."}
                                        return Response(content)
                                date_ref = datetime.date(int(year), int(month), int(day))
                            else:
                                field_erreur = 1
                                content = {'message': "merci de completer le champs relatif a la date de reference  en respectant le format dd/mm/yy ou dd-mm-yy."}
                                return Response(content)
                            
                            if lat!='0': 
                                if validate_LatAndLng(str(lat)) == 1: 
                                    try:
                                        lat = Decimal(str(lat).replace(',','.'))
                                    except (ValueError, DecimalException):
                                        erreur = 1
                                        content = {'message': "Le format du champs relatif à la latitude n'est pas valide"}
                                        return Response(content)
                                else:
                                    erreur = 1
                                    content = {'message': "le champs relatif à la longitude doit etre un nombre décimal valide avec deux chiffres avant la virgule"}
                                    return Response(content)

                                if lng!='0' :
                                    if validate_LatAndLng(str(lng)) == 1:
                                        try:
                                            lng = Decimal(str(lng).replace(',','.'))
                                        except (ValueError, DecimalException):
                                            erreur = 1
                                            content = {'message': "Le format du champs relatif à la longitude n'est pas valide"}
                                            return Response(content)
                                    else:
                                        erreur = 1
                                        content = {'message': "le champs relatif à la longitude doit etre un nombre décimal valide avec deux chiffres avant la virgule"}
                                        return Response(content)
                            
                            if surface != '0':
                                try:
                                    surface = int(str(surface).replace(' ',''))
                                except ValueError:
                                    erreur = 1
                                    content = {'message': "Le format du champs relatif à la surface n'est pas valide, sa valeur doit être un entier"}
                                    return Response(content)
                            if prix_unit != '0':
                                try:
                                    prix_unit = int(str(prix_unit).replace(' ',''))
                                except ValueError:
                                    erreur = 1
                                    content = {'message': "Le format du champs relatif àu prix unitaire n'est pas valide, sa valeur doit être un entier"}
                                    return Response(content)
                            if prix_unit_total != '0':
                                try:
                                    prix_unit_total = int(str(prix_unit_total).replace(' ',''))
                                except ValueError:
                                    erreur = 1
                                    content = {'message': "Le format du champs relatif àu prix total n'est pas valide, sa valeur doit être un entier"}
                                    return Response(content)
                            if chute_fonciere == '0':
                                try:
                                    chute_fonciere = int(str(chute_fonciere).replace(' ',''))
                                except ValueError:
                                    erreur = 1
                                    content = {'message': "Le format du champs relatif à la Quote-part terrain (éstimée) n'est pas valide, sa valeur doit être un entier"}
                                    return Response(content)
                            if len(type_de_reference) != 0:
                                type_de_reference = typeDeRererence_to_id(type_de_reference)
                                if type_de_reference == 0:
                                    erreur = 1
                                    content = {'message': "Le champs relatif au type de reference n'est pas valide, sa valeur doit être parmi les choix vente, location, rapport"}
                                    return Response(content)

                            if len(type_de_bien) != 0:
                                type_de_bien_Split = type_de_bien.strip().split(' ')
                                type_de_bien_abreviation=''
                                for i in range(len(type_de_bien_Split)):
                                    type_de_bien_abreviation = type_de_bien_abreviation + type_de_bien_Split[i][0]
                                type_de_bien = typeDeBien_to_id(type_de_bien_abreviation)
                                if type_de_bien == 0:
                                    erreur = 1
                                    content = {'message': "Le champs relatif au type de bien n'est pas valide, sa valeur doit être parmi les choix Residentiel, Villa, Maison, Professionnel, Commercial, Industriel, Terrain Villa, Terrain Industriel, Terrain urbain, Terrain agricole"}
                                    return Response(content)
                            
                            if ville == '0':
                                ville = None

                            new_pin = Pin(lat=lat, lng=lng, type_de_bien=type_de_bien ,type_de_reference=type_de_reference, username=user, prix_unit=prix_unit, prix_total=prix_unit_total,
                                region_id=region, descriptif=descriptif, contact=contact, surface=surface, date_ajout=date_ref, tags=tags, ville_id=ville, chute_fonciere=chute_fonciere)
                            actualisation1 = []
                            actualisation1.append(str(date.today()))
                            actualisation1.append(str(prix_unit))
                            actualisation1.append(str(prix_unit_total))
                            actualisation = []
                            actualisation.append(actualisation1)
                            new_pin.actualisation = actualisation
                            new_pins.append(new_pin)
                            if user.userType == "principal":
                                new_pin.is_validate_by_user = True
                                new_pin.user_valider = request.user.id
                        if field_erreur==0:
                            for pin in new_pins:
                                pin.save()
                            serializer = PinSerializerLeger(new_pins, many=True)
                            return Response(serializer.data)
            else:
                content = {'message': "droit non accordé"}
                return Response(content)
    except Exception as e:
        LOGGING.getLogger("error_logger").error(repr(e))
        pass
