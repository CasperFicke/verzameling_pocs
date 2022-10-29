# verwerkingen/urls.py

# Django
from django.urls import path

# local
from . import views
from .views import all_verwerkingenView, add_verwerkingView, show_verwerkingView, edit_verwerkingView

urlpatterns = [
  # Verwerkingen
  path('verwerkingen/'                         , views.all_verwerkingenView.as_view(), name='all-verwerkingen'),
  path('verwerkingen/add/'                     , views.add_verwerkingView.as_view(), name="add-verwerking"),
  path('verwerkingen/<verwerking_uuid>/'       , show_verwerkingView.as_view(), name='show-verwerking'),
  path('verwerkingen/<verwerking_uuid>/edit/'  , edit_verwerkingView.as_view(), name='edit-verwerking'),
  #path('verwerkingen/<verwerking_uuid>/delete/', views.delete_verwerkingView.as_view(), name="delete-verwerking"), classbased
  path('verwerkingen/<verwerking_uuid>/delete/', views.delete_verwerking, name="delete-verwerking"),
  ]

  