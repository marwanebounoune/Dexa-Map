from api_map.serializers import PinSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User
from django.contrib.auth.decorators import login_required
from api_map.models import Pin, HistoriqueExplorer
import datetime
import logging
# Create your views here.

@api_view(['GET'])
@login_required(login_url='login') 
def getPinWithId(request, id):
    try:
        user = User.objects.get(id=request.user.id)
        system = User.objects.get(id=1)
        if user==system or (user.credit_journalier > 0 and user.credit_monsuel >0) :
            historiques = HistoriqueExplorer.objects.all()
            histo = historiques.filter(username=request.user.id).filter(pin=id).filter(date_consultation=datetime.datetime.today())
            pin = Pin.objects.get(id=id)
            if len(histo)==0:
                historique = HistoriqueExplorer(username_id= user.id, pin_id = id, date_consultation = datetime.datetime.today())
                historique.save()
                #decrementer le credit si l'utilisateur est un elaborateur ou bien le pin est un pin du systeme
                if user.permission == 'elaborateur' or pin.username == system and user.id != 1 and (user.userType == 'principal' or user.permission == 'validateur' and user.lien != 1):
                    user.credit_journalier -= 1
                    user.credit_monsuel -= 1
                    user.save()
            serializer = PinSerializer(pin, many=False)
            return Response(serializer.data)
        else:
            if user.credit_journalier == 0 and user.credit_monsuel > 0:
                content = {'message': "votre credit journalier est épuisé."}
                return Response(content)
            if user.credit_monsuel == 0:
                content = {'message': "votre credit monsuel est épuisé."}
                return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").errorcreditMonsuel(repr(e))
        pass
