from django.urls import path
from .views import RetrieveUpdateDestroyAPIView, GetFileByTypeView, CreateAudioFileView

urlpatterns = [
    path('file',CreateAudioFileView.as_view()),
    path('file/<file_type>/',GetFileByTypeView.as_view()),
    path('file/<file_type>/<int:pk>',RetrieveUpdateDestroyAPIView.as_view())
]