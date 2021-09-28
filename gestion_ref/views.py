from gestion_rapports.serializers import RapportSerializer
from gestion_rapports.models import Rapport
from api_map.views import user_pinlist, validate_LatAndLng
from api_map.serializers import PinSerializer, PinSerializerLeger
from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User
from django.contrib.auth.decorators import login_required
from decimal import Decimal, DecimalException
from django.utils.datastructures import MultiValueDictKeyError
from api_map.models import Documents, Photographie, Pin, HistoriqueMyMap, Tags
import datetime
from fold_to_ascii import fold

import re
import logging

#créer un pin
@api_view(['POST'])
@login_required(login_url='login')
def create_my_pin(request):
    try:
        if request.user.userType == "principal" or request.user.permission == 'elaborateur' or request.user.permission == 'visiteur':
            #Variable
            erreur = 0
            #Récupération de la Data
            data = request.data
            lat = data['latitude']
            lng = data['longitude']
            type_de_bien = data['type_de_bien']
            region=data['region']
            type_de_reference = data['type_de_reference']
            prix_unit = data['prix_unit']
            prix_total = data['prix_total']
            adresse = False
            contact = data['contact']
            surface = data['surface_new']
            description = data['description']
            ville = data['ville']
            tags = False
            try:
                tags = data['tag']
            except MultiValueDictKeyError:
                tags = False
            chute_fonciere = data['chute_fonciere']
            is_localized = data['localisee_nonLocalisee']
            adresseRue = data["adresseRue"]
            #images
            images = request.FILES.getlist('file')
            images_desc = data['descriptionImage']
            doc_type = data['type_piece_jointe_du_bien']
            doc_type_2 = data['type_piece_jointe_du_bien_2']
            doc_type_3 = data['type_piece_jointe_du_bien_3']
            doc_type_4 = data['type_piece_jointe_du_bien_4']
            doc_type_5 = data['type_piece_jointe_du_bien_5']
            doc_file = request.FILES.getlist('docs')
            try:
                adresse= data["adresse"]
            except MultiValueDictKeyError:
                adresse = False
            doc1=False
            doc2=False
            doc3=False
            doc4=False
            doc5=False
            if len(doc_file)>=1:
                doc1=doc_file[0]
            if len(doc_file)>=2:   
                doc2=doc_file[1]
            if len(doc_file)>=3:
                doc3=doc_file[2]
            if len(doc_file)>=4:
                doc4=doc_file[3]
            if len(doc_file)>=5:
                doc5=doc_file[4]
            if is_localized == "localisee":
                is_localized = True
            else:
                is_localized = False

            if len(lat)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif à la latitude"}
                return Response(content)
            else : 
                if validate_LatAndLng(lat) == 1: 
                    try:
                        lat = Decimal(lat.replace(',','.'))
                    except (ValueError, DecimalException):
                        erreur = 1
                        content = {'message': "Le format du champs relatif à la latitude n'est pas valide"}
                        return Response(content)
                else:
                    erreur = 1
                    content = {'message': "le champs relatif à la longitude doit etre un nombre décimal valide avec deux chiffres avant la virgule"}
                    return Response(content)

            if len(lng)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif à la longitude"}
                return Response(content)
            else :
                if validate_LatAndLng(lng) == 1:
                    try:
                        lng = Decimal(lng.replace(',','.'))
                    except (ValueError, DecimalException):
                        erreur = 1
                        content = {'message': "Le format du champs relatif à la longitude n'est pas valide"}
                        return Response(content)
                else:
                    erreur = 1
                    content = {'message': "le champs relatif à la longitude doit etre un nombre décimal valide avec deux chiffres avant la virgule"}
                    return Response(content)


            if len(region)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au region"}
                return Response(content)
            if len(ville)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif a la ville"}
                return Response(content)
            if len(type_de_reference)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au type de reference"}
                return Response(content)
            if len(type_de_bien)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au type de bien"}
                return Response(content)
            if is_localized == False and len(adresseRue) == 0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au nom de la rue"}
                return Response(content)
            
            if len(chute_fonciere) == 0:
                chute_fonciere = 0
            else :    
                try:
                    chute_fonciere = int(chute_fonciere.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif à la Quote-part terrain (éstimée) n'est pas valide, sa valeur doit être un entier"}
                    return Response(content)
            
            if len(surface) == 0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif à la surface"}  
                return Response(content)
            else :    
                try:
                    surface = int(surface.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif à la surface n'est pas valide, la valeur doit être un entier"}
                    return Response(content)
            
            if len(prix_unit)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au prix unitaire"}  
                return Response(content)
            else :    
                try:
                    prix_unit = int(prix_unit.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif àu prix unitaire n'est pas valide, sa valeur doit être un entier"}
                    return Response(content)

            if len(prix_total)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au prix total"}
                return Response(content)
            else :    
                try:
                    prix_total = int(prix_total.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif àu prix total n'est pas valide, sa valeur doit être un entier"}
                    return Response(content)
            if isinstance(prix_unit, int) == True and isinstance(surface, int) == True and isinstance(prix_unit, int) == True:
                if prix_total != prix_unit * surface:
                    erreur = 1
                    content = {'message': "la valeur du champs relatif au prix total doit être le produit de la multiplication du prix unitaire par la surface"}
                    return Response(content)

            if len(description)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif a la description"}
                return Response(content)
            #validation images
            if len(images)==0:
                if len(images_desc) != 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif a l'image"} 
                    return Response(content)
            else:
                if len(images) > 12:
                    erreur = 1
                    content = {'message': "Vous pouvez inserer seulement 12 images"}
                    return Response(content)
                    

            if len(doc_type)!=0 and doc1==False:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a la pièce jointe 1"} 
                return Response(content)
            if len(doc_type_2)!=0 and doc2==False:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a la pièce jointe 2"}
                return Response(content)
            if len(doc_type_3)!=0 and doc3==False:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a la pièce jointe 3"}
                return Response(content)
            if len(doc_type_4)!=0 and doc4==False:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a la pièce jointe 4"} 
                return Response(content)
            if len(doc_type_5)!=0 and doc5==False:
                erreur = 1 
                content = {'message': "Merci de compléter le champs relatif a la pièce jointe 5"} 
                return Response(content)


            if doc1!=False:
                if doc1.name.endswith('.pdf') == False:
                    erreur = 1
                    content = {'message': "le format du fichier 1 doit etre un pdf"} 
                    return Response(content) 
                if doc1.size > 2000000:
                    erreur = 1
                    content = {'message': "la taille du fichier 1 ne doit pas depasser 2Mo"} 
                    return Response(content)  
                if len(doc_type) == 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif au type la pièce jointe 1"} 
                    return Response(content)

            if doc2!=False and len(doc2)!=0:
                if doc2.name.endswith('.pdf') == False:
                    erreur = 1
                    content = {'message': "le format du fichier 2 doit etre un pdf "} 
                    return Response(content) 
                if doc2.size > 2000000:
                    erreur = 1
                    content = {'message': "la taille du fichier 2 ne doit pas depasser 2Mo"} 
                    return Response(content)  
                if len(doc_type_2) == 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif au type la pièce jointe 2"} 
                    return Response(content)

            if doc3!=False:
                if doc3.name.endswith('.pdf') == False:
                    erreur = 1
                    content = {'message': "le format du fichier 3 doit etre un pdf"} 
                    return Response(content) 
                if doc3.size > 2000000:
                    erreur = 1
                    content = {'message': "la taille du fichier 3 ne doit pas depasser 2Mo"} 
                    return Response(content)  
                if len(doc_type_3) == 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif au type la pièce jointe 3"} 
                    return Response(content)

            if doc4!=False:
                if doc4.name.endswith('.pdf') == False:
                    erreur = 1
                    content = {'message': "le format du fichier 4 doit etre un pdf"} 
                    return Response(content) 
                if doc4.size > 2000000:
                    erreur = 1
                    content = {'message': "la taille du fichier 4 ne doit pas depasser 2Mo"} 
                    return Response(content)  
                if len(doc_type_4) == 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif au type la pièce jointe 4"} 
                    return Response(content) 

            if doc5!=False:
                if doc5.name.endswith('.pdf') == False:
                    erreur = 1
                    content = {'message': "le format du fichier 5 doit etre un pdf"} 
                    return Response(content) 
                if doc5.size > 2000000:
                    erreur = 1
                    content = {'message': "la taille du fichier 5 ne doit pas depasser 2Mo"} 
                    return Response(content)  
                if len(doc_type_5) == 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif au type la pièce jointe 5"} 
                    return Response(content)
                

            # save new pin
            if erreur==0:
                new_pin = Pin(lat=lat, lng=lng, type_de_bien=type_de_bien, type_de_reference=type_de_reference, username=request.user, prix_unit=prix_unit, contact=contact,
                    prix_total=prix_total, descriptif=description, region_id=region, surface=surface, ville_id=ville, chute_fonciere=chute_fonciere, is_localized=is_localized, rue=adresseRue)
                if adresse != False:
                    new_pin.adresse=adresse
                if tags!=False and len(tags) != 0 and tags != 'null':
                    new_pin.tags = tags
                    tags_split = tags.split(',')
                    allTags = Tags.objects.all()
                    tags_split = fold(tags.lower().replace(' ,', ',')).split(',')
                    for tag in tags_split:
                        if not allTags.filter(label=tag).exists():
                            new_tag= Tags(label=tag)
                            new_tag.save()     
                else:
                    tags=None

                actualisation1 = []
                actualisation1.append(str(date.today()))
                actualisation1.append(str(prix_unit))
                actualisation1.append(str(prix_total))
                actualisation = []
                actualisation.append(actualisation1)
                new_pin.actualisation = actualisation
                if request.user.userType == "principal":
                    new_pin.is_validate_by_user = True
                    new_pin.user_valider = request.user.id
                else:
                    new_pin.is_validate_by_user = False
                new_pin.save()
                # save images if exists
                if len(images)!=0:
                    for image in images:
                        photo = Photographie(pin=new_pin, descriptif=images_desc)
                        photo.photo.save(image.name, image)
                        photo.save()
                #save piece jointe
                if len(doc_type) != 0 and doc1!=False:
                    doc_new_1 = Documents(pin_id=new_pin.id, username= request.user, type_file= doc_type)
                    doc_new_1.fichier.save(doc1.name, doc1)
                    doc_new_1.save()
                if len(doc_type_2) != 0 and doc2!=False:
                    doc_new_2 = Documents(pin_id=new_pin.id, username= request.user, type_file= doc_type_2)
                    doc_new_2.fichier.save(doc2.name, doc2)
                    doc_new_2.save()

                if len(doc_type_3) != 0 and doc3!=False:
                    doc_new_3 = Documents(pin_id=new_pin.id, username= request.user, type_file= doc_type_3)
                    doc_new_3.fichier.save(doc3.name, doc3)
                    doc_new_3.save()

                if len(doc_type_4) != 0 and doc4!=False:
                    doc_new_4 = Documents(pin_id=new_pin.id, username= request.user, type_file= doc_type_3)
                    doc_new_4.fichier.save(doc4.name, doc4)
                    doc_new_4.save()

                if len(doc_type_5) != 0 and doc5!=False:
                    doc_new_5 = Documents(pin_id=new_pin.id, username= request.user, type_file= doc_type_5)
                    doc_new_5.fichier.save(doc5.name, doc5)
                    doc_new_5.save()
            serializer = PinSerializer(new_pin, many=False)
            return Response(serializer.data)
        else:
            content = {'message': "permission non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation des pins
@api_view(['GET'])
@login_required(login_url='login')
def pinlist(request):
    try:
        if request.user.my_ip == "127.0.0.1" or request.user.id == 1 or request.user.id == 9:
            #l'appel de la fonction user_pinlist()
            pins = user_pinlist(request.user)
        else:
            pins = []
        serializer = PinSerializerLeger(pins, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#modifier un pin
@api_view(['POST'])
@login_required(login_url='login')
def update_my_pin(request):
    try:
        erreur = 0
        data = request.data
        my_pin = Pin.objects.get(id=data['my_pin_id'])
        if request.user.userType=="principal" or request.user.permission == 'validateur' or ((request.user.permission == 'elaborateur' or request.user.permission == 'visiteur') and my_pin.username == request.user):
            type_de_bien = data['type_de_bien']
            ville=data['ville']
            region = data['region']
            # terrain_nu_affectation = data['terrain_nu_affectation']
            type_de_reference = data['type_de_reference']
            contact = data['contact-update']
            prix_unit = data['prix_unit_update']
            prix_total = data['prix_total_update']
            surface = data['surf_update']
            description = data['description']
            tags = request.POST.getlist('tag')
            tags = ','.join(tags) #convert list item into format i1,i2
            chute_fonciere = data['chute_fonciereEdt']
            is_localized = data['localisee_nonLocalisee']
            adresseRue = data["adresseRue"]
            
            if is_localized == "localisee":
                is_localized = True
            else:
                is_localized = False
            if len(type_de_bien)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au type de bien"}
                return Response(content)
            if len(region)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif de la région"}
                return Response(content)
            if len(type_de_reference)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au type de reference"}
                return Response(content)
            if is_localized == False and len(adresseRue) == 0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au nom de la rue"}
                return Response(content)

            if len(chute_fonciere) == 0:
                chute_fonciere = 0
            else :    
                try:
                    chute_fonciere = int(chute_fonciere.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif à la Quote-part terrain (éstimée) n'est pas valide, sa valeur doit être un entier"}
                    return Response(content)
            
            if len(surface) == 0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif à la surface"}  
                return Response(content)
            else :    
                try:
                    surface = int(surface.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif à la surface n'est pas valide, la valeur doit être un entier"}
                    return Response(content)
            if len(prix_unit)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au prix unitaire"}  
                return Response(content)
            else :    
                try:
                    prix_unit = int(prix_unit.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif à la surface n'est pas valide, la valeur doit être un entier"}
                    return Response(content)
            if len(prix_total)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif au prix total"}
                return Response(content)
            else :    
                try:
                    prix_total = int(prix_total.replace(' ',''))
                except ValueError:
                    erreur = 1
                    content = {'message': "Le format du champs relatif à la surface n'est pas valide, la valeur doit être un entier"}
                    return Response(content)
            if isinstance(prix_unit, int) == True and isinstance(surface, int) == True and isinstance(prix_unit, int) == True:
                if prix_total != prix_unit * surface:
                    erreur = 1
                    content = {'message': "la valeur du champs relatif au prix total doit être le produit de la multiplication du prix unitaire par la surface"}
                    return Response(content)
            if len(description)==0:
                erreur = 1
                content = {'message': "Merci de compléter le champs relatif a la description"}
                return Response(content)
            # save new pin
            if erreur==0:
                if(my_pin.actualisation != None):
                    i = len(my_pin.actualisation)-1
                    my_pin.actualisation[i][0] = str(date.today())
                    my_pin.actualisation[i][1] = str(prix_unit)
                    my_pin.actualisation[i][2] = str(prix_total)
                else:
                    actualisation1 = []
                    actualisation1.append(str(date.today()))
                    actualisation1.append(str(prix_unit))
                    actualisation1.append(str(prix_total))
                    actualisation = []
                    actualisation.append(actualisation1)
                    my_pin.actualisation = actualisation


                #update my_pin
                my_pin.type_de_bien=type_de_bien
                my_pin.type_de_reference=type_de_reference
                my_pin.prix_unit=prix_unit
                my_pin.contact=contact
                my_pin.prix_total=prix_total
                my_pin.descriptif=description
                my_pin.ville_id=int(ville)
                my_pin.region_id = int(region)
                my_pin.surface=surface
                my_pin.chute_fonciere=chute_fonciere
                my_pin.is_localized = is_localized
                my_pin.rue = adresseRue
                #editer par
                my_pin.user_editer=request.user.id

                if len(tags) != 0 and tags != 'null':
                    my_pin.tags = tags
                    tags_split = tags.split(',')
                    allTags = Tags.objects.all()
                    tags_split = fold(tags.lower().replace(' ,', ',')).split(',')
                    for tag in tags_split:
                        if not allTags.filter(label=tag).exists():
                            new_tag= Tags(label=tag)
                            new_tag.save()
                else:
                    my_pin.tags = None

                my_pin.save()
                serializer = PinSerializer(my_pin, many=False)
                return Response(serializer.data)
        else:
            content = {'message': "permission non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#supprimer un pin
@api_view(['GET'])
@login_required(login_url='login')
def pinDelete(request,id):
    try:
        if request.user.my_ip == "127.0.0.1" or request.user.id == 1 or request.user.id == 9:
            my_pin = Pin.objects.get(id=id)
            if request.user.userType == 'principal' or ((request.user.permission == 'elaborateur' or request.user.permission == 'visiteur') and my_pin.username == request.user):
                my_pin.deleted = True
                my_pin.user_editer=request.user.id
                my_pin.save()
                serializer = PinSerializer(my_pin, many=False)
                return Response(serializer.data)
            else:
                content = {'message': "permission non accordé"}
                return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation détail des pins
@api_view(['GET'])
@login_required(login_url='login')
def pinDetail(request, pk):
    try:
        if request.user.my_ip == "127.0.0.1" or request.user.id == 1 or request.user.id == 9:
            pins = Pin.objects.get(id=pk)
            historique = HistoriqueMyMap()
            user = request.user
            historique.username_id= user.id
            historique.pin_id = pk
            historique.date_consultation = datetime.datetime.today()
            historique.save()
        else:
            pins = []
        serializer = PinSerializer(pins, many=False)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation des pins non valides
@api_view(['GET'])
@login_required(login_url='login')
def pinlist_nonValide(request):
    try:
        user_propre_pins = Pin.objects.filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=False) 
        system = User.objects.get(id=1)
        if request.user.id == 1:
            pins_systeme = Pin.objects.filter(username=system).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=False) 
            print(pins_systeme)
        else:
            pins_systeme = []
        if request.user.userType == 'principal':
            sousUsers = User.objects.filter(lien=request.user.id).filter(userType='secondaire')
            pins_sous_users = []
            for su in sousUsers:
                pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=False) 
                pins_sous_users.extend(pins_su)
            pins = set(pins_sous_users).union(set(user_propre_pins)).union(set(pins_systeme))
            serializer = PinSerializerLeger(pins, many=True)
            return Response(serializer.data)
        elif request.user.permission == 'validateur':
            pere_user = User.objects.get(id=request.user.lien)
            pere_pins = Pin.objects.filter(username=pere_user).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=False) 
            sousUsers = User.objects.filter(lien=pere_user.id).filter(userType='secondaire')
            pins_sous_users = []
            for su in sousUsers:
                pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=False) 
                pins_sous_users.extend(pins_su)
            pins = set(pins_sous_users).union(set(pere_pins)).union(pins_systeme)
            serializer = PinSerializerLeger(pins, many=True)
            return Response(serializer.data)
        elif request.user.permission == 'elaborateur':
            serializer = PinSerializerLeger(user_propre_pins, many=True)
            return Response(serializer.data)
        elif request.user.permission == 'visiteur':
            user_propre_pins = Pin.objects.filter(username=request.user.id).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=False) 
            serializer = PinSerializerLeger(user_propre_pins, many=True)
            return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation des pins non valides
@api_view(['GET'])
@login_required(login_url='login')
def pinlist_nonValide_mobile(request):
    try:
        if request.user.my_ip == "127.0.0.1" or request.user.id == 1 or request.user.id == 9:
            user_propre_pins = Pin.objects.filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=True) 
            system = User.objects.get(id=1)
            if request.user.id == 1:
                pins_systeme = Pin.objects.filter(username=system).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=True) 
            else:
                pins_systeme = []
            if request.user.userType == 'principal':
                sousUsers = User.objects.filter(lien=request.user.id).filter(userType='secondaire')
                pins_sous_users = []
                for su in sousUsers:
                    pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=True) 
                    pins_sous_users.extend(pins_su)
                pins = set(pins_sous_users).union(set(user_propre_pins)).union(set(pins_systeme))
                serializer = PinSerializerLeger(pins, many=True)
                return Response(serializer.data)
            elif request.user.permission == 'validateur':
                pere_user = User.objects.get(id=request.user.lien)
                pere_pins = Pin.objects.filter(username=pere_user).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=True) 
                sousUsers = User.objects.filter(lien=pere_user.id).filter(userType='secondaire')
                pins_sous_users = []
                for su in sousUsers:
                    pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=True) 
                    pins_sous_users.extend(pins_su)
                pins = set(pins_sous_users).union(set(pere_pins)).union(pins_systeme)
                serializer = PinSerializerLeger(pins, many=True)
                return Response(serializer.data)
            elif request.user.permission == 'elaborateur':
                serializer = PinSerializerLeger(user_propre_pins, many=True)
                return Response(serializer.data)
            elif request.user.permission == 'visiteur':
                user_propre_pins = Pin.objects.filter(username=request.user.id).filter(deleted=False).filter(is_validate_by_user=False).filter(from_mobile=True) 
                serializer = PinSerializerLeger(user_propre_pins, many=True)
                return Response(serializer.data)
        else:
            serializer = PinSerializerLeger([], many=True)
            return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation des pins non valides
@api_view(['GET'])
@login_required(login_url='login')
def pinlist_rapport(request):
    try:
        pins = Rapport.objects.filter(is_locked=False)
        serializer = RapportSerializer(pins, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperation des pins valides
@api_view(['GET'])
@login_required(login_url='login')
def pinlist_Valide(request):
    try:
        if request.user.my_ip == "127.0.0.1" or request.user.id == 1 or request.user.id == 9:
            user_propre_pins = Pin.objects.filter(username=request.user.id).filter(deleted=False).filter(is_validate_by_user=True)
            system = User.objects.get(id=1)
            if request.user.id == 1:
                pins_systeme = Pin.objects.filter(username=system).filter(deleted=False).filter(is_validate_by_user=True)
            else:
                pins_systeme = []
            if request.user.userType == 'principal':
                sousUsers = User.objects.filter(lien=request.user.id).filter(userType='secondaire')
                pins_sous_users = []
                for su in sousUsers:
                    pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False).filter(is_validate_by_user=True)
                    pins_sous_users.extend(pins_su)
                pins = set(pins_sous_users).union(set(user_propre_pins)).union(set(pins_systeme))
                serializer = PinSerializerLeger(pins, many=True)
                return Response(serializer.data)
            elif request.user.permission == 'validateur' or request.user.permission == 'elaborateur':
                pere_user = User.objects.get(id=request.user.lien)
                pere_pins = Pin.objects.filter(username=pere_user).filter(deleted=False).filter(is_validate_by_user=True)
                sousUsers = User.objects.filter(lien=pere_user.id).filter(userType='secondaire')
                pins_sous_users = []
                for su in sousUsers:
                    pins_su = Pin.objects.filter(username_id=su.id).filter(deleted=False).filter(is_validate_by_user=True)
                    pins_sous_users.extend(pins_su)
                pins = set(pins_sous_users).union(set(pere_pins))
                if request.user.permission == 'validateur':
                    pins = pins.union(pins_systeme)
                serializer = PinSerializerLeger(pins, many=True)
                return Response(serializer.data)
            elif request.user.permission == 'visiteur':
                serializer = PinSerializerLeger(user_propre_pins, many=True)
                return Response(serializer.data)
        else:
            serializer = PinSerializerLeger([], many=True)
            return Response(serializer.data)
    
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#la méthode de validation et de devalidation des pins
@api_view(['GET'])
@login_required(login_url='login')
def validate_my_pin(request, pin_id):
    try:
        if request.user.userType == 'principal' or request.user.permission == 'validateur':
                oldPin = Pin.objects.get(id=pin_id)
                oldPin.is_validate_by_user = not oldPin.is_validate_by_user
                oldPin.user_valider = request.user.id
                oldPin.save()
                serializer = PinSerializer(oldPin, many=False)
                return Response(serializer.data)
        else:
            content = {'message': "permission non acordée"}
            return Response(content)
    
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass


#créer une actualisation pour un pin
@api_view(['POST'])
@login_required(login_url='login')
def ajout_actualisation(request):
    try:
        data = request.data
        erreur = 0
        pin_id = data['pin_id_actualisation']
        prix_unit = data['prix_unit1_actualisation']
        prix_total = data['prix_tot_actualisation']
        if len(prix_unit)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au prix unitaire"}
            return Response(content)
        if len(prix_total)==0:
            erreur = 1
            content = {'message': "Merci de compléter le champs relatif au prix total"}
            return Response(content)
        if erreur == 0:
            pin = Pin.objects.get(id=pin_id)
            actualisation_x = []
            actualisation_x.append(str(date.today()))
            actualisation_x.append(str(prix_unit))
            actualisation_x.append(str(prix_total))
            pin.actualisation.append(actualisation_x)
            pin.user_editer = request.user.id
            pin.save()
            serializer = PinSerializer(pin, many=False)
            return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#supprimer une actualisation pour un pin
@api_view(['GET'])
@login_required(login_url='login')
def delete_actu(request, pk, id):
    try:
        pin = Pin.objects.get(id=pk)
        users = User.objects.filter(lien = request.user.id)
        if request.user.id == 1 or pin.is_validate_by_user == False and pin.username == request.user or pin.username.lien == request.user.id and request.user.userType == "principal":
            pin.actualisation.pop(int(id))
            pin.save()
            serializer = PinSerializer(pin, many=False)
            return Response(serializer.data)
        else:
            content = {'Message': "Droit non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
