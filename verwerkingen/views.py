# verwerkingen/views.py

from django.contrib.messages.api import success
from django.db.models import fields
from django.forms.forms import Form
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator

# local
from .models import Verwerking
from .forms import VerwerkingForm

#all verwerkingen classbased
class all_verwerkingenView(ListView):
  model               = Verwerking
  template_name       = 'verwerkingen/all_verwerkingen.html'
  context_object_name = 'verwerkingen_list'
  paginate_by         = 10

  def get_context_data(self, **kwargs):
    context  = super(all_verwerkingenView, self).get_context_data(**kwargs)
    context ['title'] = 'Verwerkingen'
    verwerkingen_list = Verwerking.objects.all()
    context ['aantal']= verwerkingen_list.count()
    paginator         = Paginator(verwerkingen_list, self.paginate_by)
    page_number       = self.request.GET.get('page')
    verwerkingen_page = paginator.get_page(page_number)
    page_count        = "a" * verwerkingen_page.paginator.num_pages
    context ['page_count'] = page_count
    return  context

# show verwerking classbased
class show_verwerkingView(DetailView):
  model               = Verwerking
  template_name       = 'verwerkingen/show_verwerking.html'
  context_object_name = 'verwerking'
  def get_object(self):
    return Verwerking.objects.get(pk=self.kwargs['verwerking_uuid'])

# add verwerking classbased
class add_verwerkingView(LoginRequiredMixin, CreateView):
  model         = Verwerking
  fields        = '__all__'
  template_name = 'verwerkingen/add_verwerking.html'
  success_url   = '/verwerkingen/'

# edit verwerking classbased
class edit_verwerkingView(UpdateView):
  form_class    = VerwerkingForm
  fields        = '__all__'
  template_name = 'verwerkingen/edit_verwerking.html'
  success_url   = 'all-verwerkingen'

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)

# delete verwerking classbased
# class delete_verwerkingView(DeleteView):
#   model         = Verwerking
#   success_url = reverse_lazy('all-verwerkingen')
 
# delete verwerking functionbased
def delete_verwerking(request, verwerking_uuid):
  verwerking = Verwerking.objects.get(uuid=verwerking_uuid)
  if request.user.is_superuser:
    verwerking.delete()
    messages.success(request, ("Verwerking " + verwerking.naam + " has been deleted!"))
    return redirect ('all-verwerkingen')
  else:
    messages.success(request, ("Verwerking " + verwerking.naam + " is not yours to delete!"))
    return redirect ('all-verwerkingen')
