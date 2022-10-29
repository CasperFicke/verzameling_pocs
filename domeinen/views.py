# domeinen/views.py

# Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Page, Paginator
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

# local
from .models import Certificaat, Domein, Subdomein, Contact, Rol, Server, Service
from .forms import DomeinForm, ContactForm
from .filters import DomeinFilter
from .serializers import RolSerializer
from datetime import datetime, timedelta, date
import csv

# Domeinen indexpage
def domeinen_index(request):
  title = 'domeinen indexpage'
  context ={
    'title': title
  }
  return render(request, 'domeinen/domeinen_index.html', context)

# All servers
def all_servers(request):
  title        = 'servers'
  server_list  = Server.objects.all().order_by('naam')
  server_count = server_list.count()
  
  # Set up pagination
  paginator     = Paginator(server_list, 40) # Show 40 servers per page.
  page_number   = request.GET.get('page')
  servers_page  = paginator.get_page(page_number)
  page_count    = "a" * servers_page.paginator.num_pages
  is_paginated  = servers_page.has_other_pages
  context = {
    'title'       : title,
    'server_list' : server_list,
    'aantal'      : server_count,
    'page_obj'    : servers_page,
    'is_paginated': is_paginated,
    'page_count'  : page_count
  }
  return render(request, 'domeinen/all_servers.html', context)

# show server
def show_server(request, server_uuid):
  try:
    server  = Server.objects.get(uuid=server_uuid)
    title    = 'server: ' + server.naam
    context  = {
      'title'  : title,
      'server' : server,
    }
    return render(request, 'domeinen/show_server.html', context)
  except:
    raise Http404()

# All services

def all_services(request):
  title        = 'services'
  service_list  = Service.objects.all().order_by('naam')
  service_count = service_list.count()
  
  # Set up pagination
  paginator     = Paginator(service_list, 40) # Show 40 services per page.
  page_number   = request.GET.get('page')
  services_page  = paginator.get_page(page_number)
  page_count    = "a" * services_page.paginator.num_pages
  is_paginated  = services_page.has_other_pages
  context = {
    'title'       : title,
    'service_list' : service_list,
    'aantal'      : service_count,
    'page_obj'    : services_page,
    'is_paginated': is_paginated,
    'page_count'  : page_count
  }
  return render(request, 'domeinen/all_services.html', context)

# show service
def show_service(request, service_uuid):
  print(service_uuid)
  try:
    service  = Service.objects.get(uuid=service_uuid)
    print(service)
    title    = 'service: ' + service.naam
    context  = {
      'title'   : title,
      'service' : service,
    }
    return render(request, 'domeinen/show_service.html', context)
  except:
    raise Http404()

# All domeinen
def all_domeinen(request):
  title        = 'domeinen'
  domein_list  = Domein.objects.all().order_by("url")
  domein_count = domein_list.count()
  # Filtering
  domFilter = DomeinFilter(request.GET, queryset=domein_list)
  domein_list = domFilter.qs

  # Set up pagination
  paginator     = Paginator(domein_list, 25) # Show 25 domeinen per page.
  page_number   = request.GET.get('page')
  domeinen_page = paginator.get_page(page_number)
  page_count    = "a" * domeinen_page.paginator.num_pages
  is_paginated  = domeinen_page.has_other_pages
  context = {
    'title'       : title,
    'domein_list' : domein_list,
    'aantal'      : domein_count,
    'page_obj'    : domeinen_page,
    'domFilter'   : domFilter,
    'is_paginated': is_paginated,
    'page_count'  : page_count
  }
  return render(request, 'domeinen/all_domeinen.html', context)

# export domeinen to CSV
def csv_domeinen(request):
  response= HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=DomeinList_' + str(date.today()) + '.csv'
  # create CSV writer
  writer=csv.writer(response)
  # Select all domeinen to export 
  domein_list = Domein.objects.all()
  # create first row with column headings
  writer.writerow(['URL', 'Website', 'Beschrijving', 'Opmerkingen', 'DNS IPv4', 'DNS IPv6'])
  # loop thru and output
  for domein in domein_list:
    writer.writerow([domein.url, domein.website, domein.description, domein.opmerkingen, domein.dnsipv4, domein.dnsipv6])
    writer.writerow(['', 'Rol', 'Organisatie', 'Naam'])
    for betrokkene in domein.betrokkenen.all():
      writer.writerow([' ', betrokkene.rol, betrokkene.organisatie, betrokkene.name])
    writer.writerow(['', 'Naam'])
    for certificaat in domein.certificaten.all():
      writer.writerow([' ', certificaat.name])
    writer.writerow(['', 'URL'])
    for subdomein in domein.subdomeinen.all():
      writer.writerow([' ', subdomein.url])
  return response

# show domein
def show_domein(request, domein_uuid, domein_slug):
  try:
    domein   = Domein.objects.get(uuid=domein_uuid)
    title    = 'domein: ' + domein.url
    context  = {
      'title'  : title,
      'domein' : domein,
    }
    return render(request, 'domeinen/show_domein.html', context)
  except:
    raise Http404()

# add domein
@login_required
def add_domein(request):
  title = 'Add Domein'
  if request.method == "POST":
    form = DomeinForm(request.POST)
    if form.is_valid():
      domein = form.save(commit=False)
      domein.save()
      messages.success(request, ("Domein " + domein.url + " has been added!"))
      return HttpResponseRedirect('/domeinen/')
  else:
    form = DomeinForm
  context = {
    'title' : title,
    'form'  : form,
  }
  return render(request, 'domeinen/add_domein.html', context)

# Edit domein
def edit_domein(request, domein_uuid, domein_slug):
  title  = 'Edit Domein'
  domein = Domein.objects.get(uuid=domein_uuid)
  form   = DomeinForm(request.POST or None, instance = domein)
  if form.is_valid():
    form.save()
    messages.success(request, ("Domein " + domein.url + " has been updated!"))
    return redirect('all-domeinen')
  context = {
    'title' : title,
    'domein': domein, 'form': form
  }
  return render(request, 'domeinen/edit_domein.html', context)

# Delete domein
def delete_domein(request, domein_uuid, domein_slug):
  domein = Domein.objects.get(uuid=domein_uuid)
  if request.user.is_superuser:
    domein.delete()
    messages.success(request, ("Domein " + domein.url + " has been deleted!"))
    return redirect ('all-domeinen')
  else:
    messages.success(request, ("Domein " + domein.url + " is not yours to delete!"))
    return redirect ('all-domeinen')

# All subdomeinen
def all_subdomeinen(request):
  title           = 'subdomeinen'
  subdomein_list  = Subdomein.objects.all().order_by("url")
  subdomein_count = subdomein_list.count()

  # Set up pagination
  paginator        = Paginator(subdomein_list, 2) # Show 2 subdomeinen per page.
  page_number      = request.GET.get('page')
  subdomeinen_page = paginator.get_page(page_number)
  page_count       = "a" * subdomeinen_page.paginator.num_pages
  is_paginated     = subdomeinen_page.has_other_pages

  context = {
    'title'          : title,
    'subdomein_list' : subdomein_list,
    'aantal'         : subdomein_count,
    'page_obj'       : subdomeinen_page,
    'is_paginated'   : is_paginated,
    'page_count'     : page_count
  }
  return render(request, 'domeinen/all_subdomeinen.html', context)

# show subdomein
def show_subdomein(request, subdomein_uuid, subdomein_slug):
  try:
    subdomein = Subdomein.objects.get(uuid=subdomein_uuid)
    title     = 'subdomein: ' + subdomein.url
    print (subdomein.id)
    context   = {
      'title'     : title,
      'subdomein' : subdomein,
    }
    return render(request, 'domeinen/show_subdomein.html', context)
  except:
    raise Http404()

# Edit subdomein
def edit_subdomein(request, subdomein_uuid, subdomein_slug):
  title     = 'Edit Subdomein'
  subdomein = Subdomein.objects.get(uuid=subdomein_uuid)
  form      = SubdomeinForm(request.POST or None, instance=subdomein)
  if form.is_valid():
    form.save()
    messages.success(request, ("Subdomein " + subdomein.url + " has been updated!"))
    return redirect('all-subdomeinen')
  context = {
    'title'    : title,
    'subdomein': subdomein,
    'form'     : form
  }
  return render(request, 'domeinen/subdomeinen/edit_subdomein.html', context)

# Delete subdomein
def delete_subdomein(request, subdomein_uuid, subdomein_slug):
  subdomein = Subdomein.objects.get(uuid=subdomein_uuid)
  if request.user.is_superuser:
    subdomein.delete()
    messages.success(request, ("Subdomein " + subdomein.url + " has been deleted!"))
    return redirect ('all-subdomeinen')
  else:
    messages.success(request, ("Subdomein " + subdomein.url + " is not yours to delete!"))
    return redirect ('all-subdomeinen')

# All certificaten
def all_certificaten(request):
  title             = 'certificaten'
  certificaat_list  = Certificaat.objects.all().order_by("name")
  certificaat_count = certificaat_list.count()

  # Set up pagination
  paginator         = Paginator(certificaat_list, 10) # Show 10 domeinen per page.
  page_number       = request.GET.get('page')
  certificaten_page = paginator.get_page(page_number)
  page_count        = "a" * certificaten_page.paginator.num_pages
  is_paginated      = certificaten_page.has_other_pages
  context = {
    'title'            : title,
    'certificaat_list' : certificaat_list,
    'aantal'           : certificaat_count,
    'page_obj'         : certificaten_page,
    'is_paginated'     : is_paginated,
    'page_count'       : page_count
  }
  return render(request, 'domeinen/all_certificaten.html', context)

# show certificaat
def show_certificaat(request, certificaat_uuid):
  try:
    certificaat = Certificaat.objects.get(uuid=certificaat_uuid)
    title    = 'certificaat: ' + certificaat.name,
    context  = {
      'title'       : title,
      'certificaat' : certificaat
    }
    return render(request, 'domeinen/show_certificaat.html', context)
  except:
    raise Http404()

# All contacten
def all_contacten(request):
  title = 'contacten'
  if 'searched' in request.GET:
    searched     = request.GET['searched']
    # contact_list = Contact.objects.filter(name__icontains=searched).order_by('organisatie')
    multiple_q   = Q(Q(name__icontains=searched) | Q(organisatie__icontains=searched))
    contact_list = Contact.objects.filter(multiple_q).order_by('organisatie')
  else:
    contact_list = Contact.objects.all().order_by('organisatie')
  contact_count = contact_list.count()

  # Set up pagination
  paginator      = Paginator(contact_list, 10) # Show 10 contacten per page.
  page_number    = request.GET.get('page')
  contacten_page = paginator.get_page(page_number)
  page_count     = "a" * contacten_page.paginator.num_pages
  is_paginated   = contacten_page.has_other_pages
  context = {
    'title'        : title,
    'contact_list' : contact_list,
    'aantal'       : contact_count,
    'page_obj'     : contacten_page,
    'is_paginated' : is_paginated,
    'page_count'   : page_count
  }
  return render(request, 'domeinen/all_contacten.html', context)

# show contact
def show_contact(request, contact_uuid):
  try:
    contact = Contact.objects.get(uuid=contact_uuid)
    title   = 'contact: ' + contact.organisatie + contact.name
    context = {
      'title'  : title,
      'contact': contact,
    }
    return render(request, 'domeinen/show_contact.html', context)
  except:
    raise Http404()

# add contact
@login_required
def add_contact(request):
  title = 'Add Contact'
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      contact = form.save(commit=False)
      contact.save()
      messages.success(request, ("Contact " + contact.organisatie + contact.name + " has been added!"))
      return HttpResponseRedirect('/contacten/')
  else:
    form = ContactForm
  context = {
    'title': title,
    'form' : form,
  }
  return render(request, 'domeinen/add_contact.html', context)

# Edit contact
def edit_contact(request, contact_uuid):
  title   = 'Edit Contact'
  contact = Contact.objects.get(uuid=contact_uuid)
  if request.user.is_superuser:
    form = ContactForm(request.POST or None, instance=contact)
  else:
    form = ContactForm(request.POST or None, instance=contact)
  if form.is_valid():
    form.save()
    messages.success(request, ("Contact " + contact.name + " has been updated!"))
    return redirect('all-contacten')
  context = {
    'title' : title,
    'domein': contact, 'form': form
  }
  return render(request, 'domeinen/edit_contact.html', context)

# Delete contact
def delete_contact(request, contact_uuid):
  contact = Contact.objects.get(uuid=contact_uuid)
  if request.user.is_superuser:
    contact.delete()
    messages.success(request, ("Contact " + contact.name + " has been deleted!"))
    return redirect ('all-contacten')
  else:
    messages.success(request, ("Contact " + contact.name + " is not yours to delete!"))
    return redirect ('all-contacten')

# API routes rollen
@api_view(['GET'])
# alle rollen apis
def rollen_apis(request):
  api_urls = {
    'List'       : '/api/rollen/',
    'Show_rol'   : '/api/rollen/<rol_uuid>/',
    'Create_rol' : '/api/rollen/add/',
    'Update_rol' : '/api/rollen/<rol_uuid>/edit/',
    'Delete_rol' : '/api/rollen/<rol_uuid>/delete/',
  }
  return Response(api_urls)

@api_view(['GET'])
def rolList(request):
	rollen     = Rol.objects.all().order_by('rol')
	serializer = RolSerializer(rollen, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def rolDetail(request, rol_uuid):
	rol        = Rol.objects.get(uuid=rol_uuid)
	serializer = RolSerializer(rol, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def rolCreate(request):
	serializer = RolSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def rolUpdate(request, rol_uuid):
	rol        = Rol.objects.get(uuid=rol_uuid)
	serializer = RolSerializer(instance=rol, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['DELETE'])
def rolDelete(request, rol_uuid):
	rol = Rol.objects.get(uuid=rol_uuid)
	rol.delete()
	return Response('Item successfully delete!')
