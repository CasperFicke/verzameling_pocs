# photos/views.py

# Django
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse

from django.core.paginator import Page, Paginator

# local
from .models import Photo
from .forms import PhotoForm

# All Photos
def all_photos(request):
  title      = 'fotos'
  photo_list  = Photo.objects.all().order_by("name")
  photo_count = photo_list.count()

  # Set up pagination
  paginator     = Paginator(photo_list, 10)
  page_number   = request.GET.get('page')
  photos_page   = paginator.get_page(page_number)
  page_count    = "a" * photos_page.paginator.num_pages
  is_paginated  = photos_page.has_other_pages
  context = {
    'title'       : title,
    'photo_list'  : photo_list,
    'aantal'      : photo_count,
    'page_obj'    : photos_page,
    'is_paginated': is_paginated,
    'page_count'  : page_count
  }
  return render(request, 'photos/all_photos.html', context)

# show photo classbased
class show_photoView(DetailView):
  template_name = 'photos/show_photo.html'
  model = Photo

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'foto: ' + self.object.name
    loaded_photo = self.object
    request      = self.request
    favoriet_id  = request.session.get('favoriet_photo')
    context['is_favoriet'] = favoriet_id == str(loaded_photo.id)
    return context

# favoriet photo view
class AddFavorietPhotoView(View):
  def post(self, request):
    photo_id = request.POST['photo_id']
    # fav_photo = Photo.objects.get(pk=photo_id)
    request.session['favoriet_photo'] = photo_id
    return HttpResponseRedirect('/photos/' + photo_id)

# add Photo
@login_required
def add_photo(request):
  title = 'add foto'
  form = PhotoForm(request.POST or None, request.FILES or None)
  data = {}
  if form.is_valid():
    form.save()
    data['name'] = form.cleaned_data.get('name')
    data['status'] = 'ok'
    return JsonResponse(data)
  context = {
    'title' : title,
    'form'  : form,
  }
  return render(request, 'photos/add_photo.html', context)