from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializer import AudioFileSerializer
from .models import AudioFile
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.http import Http404
from .utils import validate_post_data
# Create your views here.

class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    def get_queryset(self):
        file_type = self.kwargs.get('file_type').lower() if self.kwargs.get('file_type') else ""
        pk = self.kwargs.get('pk')
        return AudioFile.objects.filter(id=pk, type=file_type)

class GetFileByTypeView(generics.ListAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    def get_queryset(self):
        file_type = self.kwargs.get('file_type').lower() if self.kwargs.get('file_type') else ""
        return AudioFile.objects.filter(type=file_type)

class CreateAudioFileView(generics.CreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    def save_file_by_type(self, file_type, serializer, data):
        obj = error = None
        if file_type == "song":
            obj = serializer.save()
        elif file_type == "podcast":
            host = data.get('host',"")
            if len(host):
                obj = serializer.save()
            else:
                error = {"message":"Host name is mandatory to create a Podcast !"}
        elif file_type == "audiobook":
            author = data.get('author',"")
            narrator = data.get('narrator',"")
            if len(author) and len(narrator):
                obj = serializer.save()
            else:
                error = {"message":"Author and Narrator both are mandatory to create a Audiobook !"}
        return [obj, error]


    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            file_type = data.get('type')
            duration = data.get('duration')
            name = data.get('name')
            if file_type and duration and name:                
                serializer = AudioFileSerializer(data=data)
                if serializer.is_valid():
                    data = self.save_file_by_type(file_type, serializer,data)
                    obj = data[0]
                    error = data[1]
                    serializer = AudioFileSerializer(obj)
                    if obj:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"Please provide file type and it's Metadata!"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception in create file api - {}".format(str(e)))
