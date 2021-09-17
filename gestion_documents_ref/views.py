from api_map.serializers import DocumentsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from api_map.models import Documents, Pin
import logging

#supprimer une piece jointe pour un pin
@api_view(['GET'])
@login_required(login_url='login')
def delete_my_piece_jointe(request, fichier_id):
    try:
        pdf_pin = Documents.objects.get(id=fichier_id)
        if request.user.userType == 'principal'  or request.user.permission == 'validateur' or ((request.user.permission == 'elaborateur' or request.user.permission == 'visiteur') and pdf_pin.pin.username == request.user):
            pdf_pin.delete()
            pdf_pin.pin.user_editer=request.user.id
            pdf_pin.pin.save()
            serializer = DocumentsSerializer(pdf_pin, many=False)
            return Response(serializer.data)
        else:
            content = {'message': "droit non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#créer une piece jointe pour un pin
@api_view(['POST'])
@login_required(login_url='login')
def create_my_piece_jointe(request, pin_id):
    try:
        pin = Pin.objects.get(id=pin_id)
        if request.method == 'POST':
            if request.user.userType == 'principal'  or request.user.permission == 'validateur' or ((request.user.permission == 'elaborateur' or request.user.permission == 'visiteur') and pin.username == request.user):
                erreur = 0
                #Récupération de la Data
                data = request.data
                doc_type_1 = data['type_piece_jointe_du_bien_new']
                doc1=False
                try:
                    doc1=request.FILES['piece_jointe_new']
                except MultiValueDictKeyError:
                    doc1 = False
                
                if doc1==False and len(doc_type_1)==0:
                    erreur = 1 
                    content = {'message': "Merci d'importer une piece jointe"} 
                    return Response(content)
                if doc1!=False:
                        if doc1.name.endswith('.pdf') == False:
                            erreur = 1
                            content = {'message': "le format du fichier doit etre un pdf"} 
                            return Response(content) 
                        if doc1.size > 2000000:
                            erreur = 1
                            content = {'message': "la taille du fichier ne doit pas depasser 2Mo"} 
                            return Response(content)  
                        if len(doc_type_1) == 0:
                            erreur = 1 
                            content = {'message': "Merci de compléter le champs relatif au type la pièce jointe"} 
                            return Response(content)
                else:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif a la pièce jointe"} 
                    return Response(content)
                if erreur==0:
                    doc_new = Documents(pin_id=pin_id, username= request.user, type_file= doc_type_1)
                    doc_new.fichier.save(doc1.name, doc1)
                    doc_new.save()
                    pin.user_editer = request.user.id
                    pin.save()
                    serializer = DocumentsSerializer(doc_new, many=False)
                return Response(serializer.data)
            else:
                content = {'message': "droit non accordé"}
                return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuper les pieces jointes d'un pin
@api_view(['GET'])
@login_required(login_url='login') 
def getPieceJointeByIdPin(request, pin_id):
    try:
        piece_jointes = Documents.objects.filter(pin_id=pin_id)
        serializer = DocumentsSerializer(piece_jointes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
