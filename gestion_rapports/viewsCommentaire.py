from datetime import date
import logging
from .serializers import CommentaireSerializer
from .models import Commentaire, Rapport
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
@login_required(login_url='login') 
def getCommentRapport(request, pk):
    try:
        notes = Commentaire.objects.filter(rapport_id=pk)
        serializer = CommentaireSerializer(notes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['POST'])
@login_required(login_url='login')  
def addCommentRapport(request):
    try:
        data = request.data
        note_content = data['comment_content']
        user = request.user
        rapport_id = data['rapport_id_commentaire']
        rapport = Rapport.objects.get(id=rapport_id)
        today = date.today()
        commentaire = Commentaire(note=note_content, date=today, username=user, rapport=rapport)
        serializer = CommentaireSerializer(commentaire, many=False)
        commentaire.save()
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
