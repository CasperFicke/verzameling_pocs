# photos/urls.py

# Django
from django.urls import path

# local
from . import views

urlpatterns = [
  # Photos
  path('photos/'                 , views.all_photos, name="all-photos"),
  path('photos/add'              , views.add_photo, name="add-photo"),
  path('photos/favoriet/'        , views.AddFavorietPhotoView.as_view(), name="add-favoriet-photo"),
  path('photos/<int:pk>/delete/' , views.delete_photo, name="delete-photo"),
  path('photos/<int:pk>'         , views.show_photoView.as_view(), name="show-photo"),
]
