### URLS.PY WEBSITE APP ###

# Django
from django.urls import path, include

# local
from . import views

urlpatterns = [
  # HOME
  path('', views.index, name="index"),

  # DENTO
  path('book_appointment/', views.book_appointment, name="book_appointment"),
  path('contact/'         , views.contact, name="contact"),
  path('about/'           , views.about, name="about"),
  path('blog/'            , views.blog, name="blog"),
  path('blog-details/'    , views.blog_details, name="blog-details"),
  path('pricing/'         , views.pricing, name="pricing"),
  path('service/'         , views.service, name="service")
]
