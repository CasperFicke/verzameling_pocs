# events/views.py
# function based

# Django
from multiprocessing import context
#from turtle import title
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, request
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from django.core.paginator import Paginator

# pdf creation with reportlab
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

# 3th party
from xhtml2pdf import pisa

# local
from .models import Venue, Event
from .forms import VenueForm, EventFormAdmin, EventForm 
from .utils import Calendar
import calendar
from calendar import HTMLCalendar, monthrange
from datetime import datetime, timedelta, date
import csv
import qrcode

# Calendar view (class based)
class CalendarView(generic.ListView):
  model         = Event
  template_name = 'events/kalender.html'

  def get_context_data(self, **kwargs):
    title = 'Kalender'
    context = super().get_context_data(**kwargs)

    # use today's date for the calendar
    d = get_date(self.request.GET.get('month', None))

    # Instantiate calendar class with today's year and date
    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns calendar as a table
    html_cal              = cal.formatmonth(withyear=True)
    context['calendar']   = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    context['title']      = title
    return context

def get_date(req_month):
  if req_month:
    year, month = (int(x) for x in req_month.split('-'))
    return date(year, month, day=1)
  return datetime.today()

def prev_month(d):
  first = d.replace(day=1)
  prev_month = first - timedelta(days=1)
  month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
  return month

def next_month(d):
  days_in_month = calendar.monthrange(d.year, d.month)[1]
  last = d.replace(day=days_in_month)
  next_month = last + timedelta(days=1)
  month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
  return month

# event view ( used for show, add and edit)
def event(request, event_id=None):
  title    = 'Event'
  instance = Event()
  if event_id:
    instance = get_object_or_404(Event, pk=event_id)
  else:
    instance = Event()

  form = EventForm(request.POST or None, instance=instance)
  if request.POST and form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('kalender'))
  context = {
    'title': title,
    'form' : form
  }
  return render(request, 'events/event.html', context)

# all venues
def all_venues(request):
  title       = 'venues'
  venue_list  = Venue.objects.all().order_by('name')
  venue_count = venue_list.count()
 
  # Set up pagination
  paginator    = Paginator(venue_list, 2) # Show 5 venues per page.
  page_number  = request.GET.get('page')
  venues_page  = paginator.get_page(page_number)
  page_count   = "a" * venues_page.paginator.num_pages
  is_paginated = venues_page.has_other_pages

  context  = {
    'title'        : title,
    'venue_list'   : venue_list,
    'aantal'       : venue_count,
    'page_obj'     : venues_page,
    'is_paginated' : is_paginated,
    'page_count'   : page_count
  }
  return  render(request, 'events/all_venues.html', context)

# export venues to CSV
def csv_venues(request):
  response= HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=VenueList_' + str(date.today()) + '.csv'
  # create CSV writer
  writer=csv.writer(response)
  # Select all venues to export
  #venue_list = Venue.objects.filter(owner=request.user) 
  venue_list = Venue.objects.all()
  # create first row with column headings
  writer.writerow(['Naam', 'Adres', 'Postcode', 'Telefoon', 'email', 'website'])
  # loop thru and output
  for venue in venue_list:
    writer.writerow([venue.name, venue.adres, venue.postcode, venue.telefoon, venue.email, venue.website])
  return response

# export venues to TXT
def txt_venues(request):
  response=HttpResponse(content_type='text/plain')
  response['Content-Disposition'] = 'attachment; filename=VenueList_' + str(date.today()) + '.txt'
  venue_list = Venue.objects.all()
  # create empty list
  lines = []
  # loop thru and output
  for venue in venue_list:
    lines.append(f'Naam: {venue.name}\nAdres: {venue.adres}\nPostcode: {venue.postcode}\ntelefoon: {venue.telefoon}\ne-mail: {venue.email}\nWebsite: {venue.website}\n\n')
  response.writelines(lines)
  return response

# export venues to PDF
def pdf_venues(request):
  # Create a file-like buffer to receive PDF data.
  buffer = io.BytesIO()
  # Create the PDF object, using the buffer as its "file."
  p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
  # Create a textobject
  texobj = p.beginText()
  texobj.setTextOrigin(cm, cm)
  texobj.setFont("Helvetica", 14)

  venue_list = Venue.objects.all()
  # create empty list
  lines = []
  # loop thru to build contentlist
  for venue in venue_list:
    lines.append('naam: ' + venue.name)
    lines.append('Adres: ' + venue.adres)
    lines.append('Postcode: ' + venue.postcode)
    lines.append('telefoon: ' + venue.telefoon)
    lines.append('e-mail: ' + venue.email)
    lines.append('Website: ' + venue.website)
    lines.append('  ')
  # loop thru and output
  for line in lines:
    texobj.textLine(line)
  # finish pdf
  p.drawText(texobj)
  p.showPage()
  p.save()
  buffer.seek(0)
  # return pdf
  return FileResponse(buffer, as_attachment=True, filename='VenueList_' + str(date.today()) + '.pdf')

# show venue classbased ( niet actief)
class show_venueView(DetailView):
  template_name = 'events/show_venue.html'
  model = Venue

  def get_context_data(self, **kwargs):
    context       = super().get_context_data(**kwargs)
    loaded_venue  = self.get_object
    request       = self.request
    favoriet_uuid = request.session.get['favoriet_venue']
    context['is_favoriet'] = favoriet_uuid == loaded_venue.uuid
    return context

# show venue functionbased
def show_venue(request, venue_uuid):
  try:
    venue       = Venue.objects.get(uuid=venue_uuid)
    venue_owner = User.objects.get(pk=venue.owner)
    title       = 'venue: ' + venue.name
    appr_events_count  = venue.events.filter(approved=True).count()
    context = {
      'title': title,
      'appr_events_count': appr_events_count
    }
    if request.user.is_authenticated:
      context['venue']       = venue
      context['venue_owner'] = venue_owner
    return  render(request, 'events/show_venue.html', context)
  except:
    raise Http404()

# add venue
@login_required
def add_venue(request):
  title     = 'Add Venue'
  submitted = False
  if request.method == "POST":
    form = VenueForm(request.POST, request.FILES)
    if form.is_valid():
      venue = form.save(commit=False)
      venue.owner = request.user.id
      venue.save()
      return HttpResponseRedirect('/venues/add?submitted=True')
  else:
    form = VenueForm
    if 'submitted' in request.GET:
      submitted = True
  context = {
    'title'    : title,
    'form'     : form,
    'submitted': submitted
  }
  return render(request, 'events/add_venue.html', context)

# Edit venue
@login_required
def edit_venue(request, venue_uuid):
  title = 'Edit Venue'
  venue = Venue.objects.get(uuid=venue_uuid)
  form  = VenueForm(request.POST or None, request.FILES or None, instance=venue)
  if form.is_valid():
    form.save()
    messages.success(request, ("Venue " + venue.name + " has been updated!"))
    return redirect('all_venues')
  context = {
    'title': title,
    'venue': venue,
    'form' : form
  }
  return render(request, 'events/edit_venue.html', context)

# delete venue
@login_required
def delete_venue(request, venue_uuid):
  item       = Venue.objects.get(uuid=venue_uuid)
  venue_name = item.name
  item.delete()
  messages.success(request, ("Venue " + venue_name + " has been deleted!"))
  return redirect(all_venues)

# pdf venue
def pdf_venue(request, venue_uuid):
  venue      = Venue.objects.get(uuid=venue_uuid)
  venue_name = venue.name
  template_path = 'events/pdf_venue.html'
  context = {'venue': venue}
  # Create a Django response object, and specify content_type as pdf
  response = HttpResponse(content_type='application/pdf')
  content = 'attachment; filename=Venue_' + venue_name + '.pdf'
  response['Content-Disposition'] = content
  # find the template and render it.
  template = get_template(template_path)
  html = template.render(context)

  # download pdf
  pisa_status = pisa.CreatePDF(
    html, dest=response)
  # if error then show some funy view
  if pisa_status.err:
    return HttpResponse('We had some errors <pre>' + html + '</pre>')
  messages.success(request, ("pdf of venue " + venue_name + " has been created!"))
  # return redirect(show_venue, venue_uuid)
  return response

# qrcode venue
def qrcode_venue(request, venue_uuid):
  venue      = Venue.objects.get(uuid=venue_uuid)
  venue_name = venue.name
  img = qrcode.make(venue.website)
  type(img)  # qrcode.image.pil.PilImage
  img.save("some_file.png")
  return redirect(all_venues)

# search venues
def search_venues(request):
  title        = 'Search Venues'
  venue_list   = Venue.objects.all().order_by('name')
  venues_count = venue_list.count()
  if request.method == "POST":
    searched     = request.POST['searched']
    venues       = Venue.objects.filter(name__contains=searched)
    venues_found = venues.count()
    context = {
      'title'        : title,
      'searched'     : searched,
      'venues'       : venues,
      'venues_count' : venues_count,
      'venues_found' : venues_found,
    }
    return render(request, 'events/search_venues.html', context)
  else:
    # 
    venues = venue_list
    context = {
      'title'        : title,
      'venues'       : venues,
      'venues_count' : venues_count,
    }
    return render(request, 'events/search_venues.html', {})

# favoriet venue view
class AddFavorietView(View):
  def post(self, request):
    venue_uuid = request.POST['venue_uuid']
    #fav_venue  = Venue.objects.get(uuid=venue_uuid)
    request.session['favoriet_venue'] = venue_uuid
    return HttpResponseRedirect('/venues/' + venue_uuid)

# All Events view
def all_events(request):
  title = 'Events'
  event_list = Event.objects.all().order_by('-event_start')
  context = {
    'title': title,
    'event_list': event_list
  }
  return  render(request, 'events/all_events.html', context)

# add event
@login_required
def add_event(request):
  title     = 'Add Event'
  submitted = False
  if request.method == "POST":
    if request.user.is_superuser:
      form = EventFormAdmin(request.POST)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/events/add?submitted=True')
    else:
      form = EventForm(request.POST)
      if form.is_valid():
        event = form.save(commit=False)
        event.manager = request.user
        event.save()
        return HttpResponseRedirect('/events/add?submitted=True')
  else:
    # just opening the page; not submitting
    if request.user.is_superuser:
      form = EventFormAdmin(request.POST)
    else:
      form = EventForm
  if 'submitted' in request.GET:
    submitted = True
  context = {
    'title': title,
    'form':form,
    'submitted':submitted
  }
  return render(request, 'events/add_event.html', context)

# show event
def show_event(request, event_id, event_slug):
  try:
    event = Event.objects.get(id=event_id)
    title = 'event: ' + event.name
    context = {
      'title': title,
      'event': event,
    }
    return render(request, 'events/show_event.html', context)
  except:
    raise Http404()

# Edit event
@login_required
def edit_event(request, event_id, event_slug):
  title = 'Edit Event'
  event = Event.objects.get(id=event_id)
  if request.user.is_superuser:
    form = EventFormAdmin(request.POST or None, instance=event)
  else:
    form = EventForm(request.POST or None, instance=event)
  if form.is_valid():
    form.save()
    messages.success(request, ("Event " + event.name + " has been updated!"))
    return redirect('all_events')
  context = {
    'title': title,
    'event': event,
    'form' : form
  }
  return render(request, 'events/edit_event.html', context)

# Delete Event
@login_required
def delete_event(request, event_id):
  event = Event.objects.get(id=event_id)
  if request.user == event.manager or request.user.is_superuser:
    event.delete()
    messages.success(request, ("Event " + event.name + " has been deleted!"))
    return redirect ('all_events')
  else:
    messages.success(request, ("Event " + event.name + " is not yours to delete!"))
    return redirect ('all_events')

# Event approval
@login_required
def event_approval(request):
  title       = 'event approval'
  venue_list  = Venue.objects.all()
  event_list  = Event.objects.all().order_by('-event_start')
  event_count = event_list.count()
  event_approved_count = event_list.filter(approved=True).count()
  venue_count = Venue.objects.all().count()
  user_count  = User.objects.all().count()
  if request.user.is_superuser:
    if request.method == 'POST':
      id_list = request.POST.getlist('boxes')
      # uncheck all
      event_list.update(approved=False)
      # update db
      for id in id_list:
        Event.objects.filter(pk=int(id)).update(approved=True)
      messages.success(request, ("updated!!"))
      return redirect('all_events')
    else: 
      context = {
        'title'      : title,
        'event_list' : event_list,
        'event_count': event_count,
        'event_approved_count': event_approved_count,
        'venue_list' : venue_list,
        'venue_count': venue_count,
        'user_count' : user_count
      }
      return render(request,  'events/event_approval.html', context)
  else:
    messages.success(request, ("You aren't authorised"))
    return redirect('all_events')

# My events
@login_required
def my_events(request):
  title = 'My events'
  if request.user.is_authenticated:
    me = request.user.id
    events = Event.objects.filter(attendees=me).order_by('event_start')
    context = {
      'title' : title,
      'events': events,
    }
    return render (request, 'events/my_events.html', context)
  else:
    messages.success(request, ("You're not authorised to view " + title + " page!"))
    return redirect ('index')

# agenda view (/agenda/ is huidige maand, /agenda/jaar/maand/ is ingevoerde maand)
def agenda(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
  title = 'Agenda'
  # get current time
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')

  # set firstletter of month to uppercase
  month = month.capitalize()
  # convert month from name to number
  month_number = list(calendar.month_name).index(month)
  # make sure it's an integer
  month_number = int(month_number)

  # Query the event by date
  event_list = Event.objects.filter(
    event_start__year = year,
    event_start__month = month_number)

  # Create kalender
  cal = HTMLCalendar().formatmonth(
    year,
    month_number)
  context = {
    'title'       : title,
    'year'        : year,
    'month'       : month,        # text
    'month_number': month_number, # number
    'cal'         : cal,
    'current_time': current_time,
    'event_list'  : event_list 
  }
  return render(request, 'events/agenda.html', context)

# agenda view (/agenda/ is huidige maand, /agenda/jaar/maand/ is ingevoerde maand)
def agenda_by_monthnumber(request, year, monthnumber):
  year=str(datetime.now().year)
  print (monthnumber)
  # convert month from number to name
  #month = list(calendar.month_number).index(month_name)
  return HttpResponseRedirect('/events/agenda/' + year + '/november')
