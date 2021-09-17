import logging
from api_map.serializers import PhotographieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from api_map.models import Photographie, Pin

# Create your views here.

#récuperation des photographies d'un pin 
@api_view(['GET'])
@login_required(login_url='login') 
def getPhotographiesByIdPin(request, pin_id):
    try:
        photos = Photographie.objects.filter(pin_id=pin_id)
        serializer = PhotographieSerializer(photos, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#supprimer la photos d'un pin
@api_view(['GET'])
@login_required(login_url='login')
def delete_my_photo_pin(request,id_photo):
    try:
        photo_pin = Photographie.objects.get(id=id_photo)
        if request.user.userType == 'principal'  or request.user.permission == 'validateur' or ((request.user.permission == 'elaborateur' or request.user.permission == 'visiteur') and photo_pin.pin.username == request.user):
            photo_pin.delete()
            photo_pin.pin.user_editer=request.user.id
            photo_pin.pin.save()
            serializer = PhotographieSerializer(photo_pin, many=False)
            return Response(serializer.data)
        else:
            content = {'message': "permission non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#créer une photos pour un pin
@api_view(['POST'])
@login_required(login_url='login')
def ajoutPhotographies(request, pin_id):
    try:
        pin = Pin.objects.get(id=pin_id)
        if request.user.userType == 'principal'  or request.user.permission == 'validateur' or ((request.user.permission == 'elaborateur' or request.user.permission == 'visiteur') and pin.username == request.user):
            erreur = 0
            data = request.data
            images = request.FILES.getlist('file')
            images_desc = data['descriptionImage']
            img=[]
            photos_existantes = Photographie.objects.filter(pin_id=pin_id)
            nbr_photos = len(photos_existantes)
            nbr_photos_max = 12 - nbr_photos
            #validation images
            if len(images)==0:
                if len(images_desc) != 0:
                    erreur = 1 
                    content = {'message': "Merci de compléter le champs relatif a l'image"} 
                    return Response(content)
            else:
                if len(images) > nbr_photos_max:
                    erreur = 1
                    content = {'message': "Vous pouvez inserer seulement "+ str(nbr_photos_max) +" images"}
                    return Response(content)
            
            # save images if exists
            if len(images) != 0 and erreur == 0:
                for image in images:
                    photo = Photographie(pin_id=pin_id, descriptif=images_desc)
                    photo.photo.save(image.name, image)
                    photo.save()
                    img.append(photo)
                
                pin.user_editer = request.user.id
                pin.save()
                serializer = PhotographieSerializer(img, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': "permission non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
