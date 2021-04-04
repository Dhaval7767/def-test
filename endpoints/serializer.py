from rest_framework import  serializers
from .models import AudioFile

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'

    def validate_name(self, data):
        """
        Check that the start is before the stop.
        """
        # import code; code.interact(local=dict(globals(), **locals()))
        if not data :
            raise serializers.ValidationError("finish must occur after start")
        return data

    def __init__(self, *args, **kwargs):
        super(AudioFileSerializer, self).__init__(*args, **kwargs)
        # data = kwargs.get('data')
        # if not data:
        self.fields["name"].error_messages["required"] = "Pleasr enter file name! "
        self.fields["duration"].error_messages["required"] = "Pleasr enter audio file duration! "
        self.fields["type"].error_messages["required"] = "A Valid file type is required! Choices are 'song' Or 'podcast' Or 'audiobook' "
 
