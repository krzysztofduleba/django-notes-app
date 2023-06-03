from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from .models import Note
from .serializers import NoteSerializer


@api_view(['GET', 'POST'])
def notes(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        note = Note.objects.create(body=data['body'])
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def note(request, pk):
    if request.method == 'GET':
        try:
            note = Note.objects.get(id=pk)
            serializer = NoteSerializer(note, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NotFound('Note not found.')
    
    if request.method == 'PUT':
        try:
            data = request.data
            note = Note.objects.get(id=pk)
            serializer = NoteSerializer(instance=note, data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NotFound('Note not found.')

    if request.method == 'DELETE':
        try:
            note = Note.objects.get(id=pk)
            note.delete()
            return Response('Note was deleted!')
        except ObjectDoesNotExist:
            raise NotFound('Note not found.')
