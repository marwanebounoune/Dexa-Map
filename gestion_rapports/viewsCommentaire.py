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
        notes = Commentaire.objects.filter(rapport_id=pk).order_by('id')
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

@api_view(['POST'])
@login_required(login_url='login')  
def rep_Comment(request, pk):
    try:
        data = request.data
        note_content = data['repComment_content']
        user = request.user
        rapport_id = data['rapport_id_repCommentaire']

        rapport = Rapport.objects.get(id=rapport_id)
        today = date.today()
        commentaire = Commentaire(note=note_content, date=today, username=user, rapport=rapport, reponse_pour=pk)
        serializer = CommentaireSerializer(commentaire, many=False)
        commentaire.save()
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['GET'])
@login_required(login_url='login')
def delete_Comment(request, pk):
    try:
        note = Commentaire.objects.get(id=pk)
        if request.user.userType == 'principal' and (note.username == request.user.id or note.username == request.user.lien) or request.user.id == 1:
            note.delete()
            serializer = CommentaireSerializer(note, many=False)
            return Response(serializer.data)
        else:
            content = {'message': "Droit non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['POST'])
@login_required(login_url='login')  
def updateComment(request):
    try:
        data = request.data
        note_content = data['NewContentComment']
        note_id=data['CommentId']
        note= Commentaire.objects.get(id=note_id)

        if request.user == note.rapport.username or request.user.userType == 'principal':
            note.note = note_content
            note.save()
            serializer = CommentaireSerializer(note, many=False)
            return Response(serializer.data) 
        else:
            content = {'message': "permission non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

@api_view(['GET'])
@login_required(login_url='login') 
def getComment(request, pk):
    try:
        notes = Commentaire.objects.get(id=pk)
        serializer = CommentaireSerializer(notes, many=False)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass