from api_map.serializers import NoteSerializer
from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from api_map.models import Note, Pin
import logging

#sauvgarder une note pour un pin 
@api_view(['POST'])
@login_required(login_url='login')  
def save_note(request):
    try:
        data = request.data
        note_content = data['note_content']
        user = request.user
        pin_id = data['pin_id']
        pin = Pin.objects.get(id=pin_id)
        today = date.today()
        note = Note(note=note_content, date=today, editer_par=user, pin=pin)
        serializer = NoteSerializer(note, many=False)
        if note:
            note.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#récuperer les notes d'un pin
@api_view(['GET'])
@login_required(login_url='login') 
def get_notes_per_pin(request, pin_id):
    try:
        notes = Note.objects.filter(pin_id=pin_id)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#modifier une note pour un pin
@api_view(['POST'])
@login_required(login_url='login')  
def update_note(request):
    try:
        data = request.data
        note_content = data['old_note_content']
        note_id=data['note_id']
        note=Note.objects.get(id=note_id)

        if request.user == note.pin.username or request.user.userType == 'principal':
            note.note = note_content
            note.save()
            serializer = NoteSerializer(note, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        else:
            content = {'message': "permission non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass

#supprimer une note pour un pin
@api_view(['GET'])
@login_required(login_url='login')
def delete_note(request, pk):
    try:
        note = Note.objects.get(id=pk)
        if request.user.userType == 'principal' and (note.editer_par == request.user.id or note.editer_par == request.user.lien) or request.user.id == 1:
            note.delete()
            serializer = NoteSerializer(note, many=False)
            return Response(serializer.data)
        else:
            content = {'message': "Droit non accordé"}
            return Response(content)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        pass
