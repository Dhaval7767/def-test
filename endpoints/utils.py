from rest_framework.response import Response
from .serializer import AudioFileSerializer
from rest_framework import status


def validate_post_data(data):
    file_type = data.get('type')
    duration = data.get('duration')
    name = data.get('name')
    if file_type and duration and name:                
        serializer = AudioFileSerializer(data=data)
        if serializer.is_valid():
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
            serializer = AudioFileSerializer(obj)
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)