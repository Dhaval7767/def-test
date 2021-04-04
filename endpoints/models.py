from django.db import models
from django_seconds_field import SecondsField
from django.contrib.postgres.fields import ArrayField

# Create your models here.

AUDIO_FILE_TYPES = (('song',"Song"),
                    ('podcast',"Podcast"),
                    ('audiobook',"Audiobook"))

class BaseModel(models.Model):
    class Meta:
        abstract = True

    uploaded_time = models.DateTimeField(auto_now_add=True, help_text='audio uploaded time')
    duration = SecondsField(help_text='audio duration')

class AudioFile(BaseModel):
    type = models.CharField(max_length=10, choices=AUDIO_FILE_TYPES)
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    narrator = models.CharField(max_length=100, null=True, blank=True)
    participants = ArrayField(
                        models.CharField(max_length=100, blank=True),size=10, null=True, blank=True
                    )

    def __str__(self):
        return self.name
