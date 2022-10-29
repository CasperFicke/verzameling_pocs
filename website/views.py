# website/views.py

# Django
from django.shortcuts import render
from django.core.mail import send_mail

# Local
from theblog.models import BlogPost
from .forms  import ContactForm

# Index view
def index(request):
  title = 'startpagina'
  latest_posts = BlogPost.objects.all().order_by('post_date')[:3]
  context = {
    'title'       : title,
    'latest_posts': latest_posts
  }
  return render(request, 'index.html', context)

### DENTO ###
# contact view
def contact(request):
  title = 'contact'
  form = ContactForm(request.POST or None)
  context = {
    'title': title,
    'form' : form
  }
  if form.is_valid():
    print(form.cleaned_data)
    # send email
    send_mail(
      'email from website by ' + form.cleaned_data.naam, # subjext
      form.cleaned_data.get(bericht), # message
      form.cleaned_data.get(email), # from
      ['cficke@quicknet.nl'], # to
      fail_silently=False,
    )
  # present the page
  return render(request, 'website/contact.html', context)

# about view
def about(request):
  title   = 'about'
  context = {
    'title': title
  }
  return render(request, 'website/about.html', context)

# blog view
def blog(request):
  title   = 'blog'
  context = {
    'title': title
  }
  return render(request, 'website/blog.html', context)

# blog-details view
def blog_details(request):
  title   = 'blogdetails'
  context = {
    'title': title
  }
  return render(request, 'website/blog-details.html', context)

# pricing view
def pricing(request):
  return render(request, 'website/pricing.html', {})

# service view
def service(request):
  return render(request, 'website/service.html', {})

# book appointment view
def book_appointment(request):
  return render(request, 'website/book_appointment.html', {})
