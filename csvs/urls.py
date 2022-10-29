### csvs/urls.py ###

# Django
from django.urls import path, include

# local
from .views import upload_fileView

urlpatterns = [
  path('csvs/', upload_fileView, name='upload-salesfile'),
]