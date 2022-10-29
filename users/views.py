# users/views.py

# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import send_mail

# Local
from .forms  import LoginForm, SignUpForm, EditUsersettingsForm, ProfileForm, EditProfileForm
from .models import UserProfile

# Login view
def login_user(request):
  title = 'Login'
  form  = LoginForm(request.POST or None)
  context = {
    'title': title,
    'form' : form
  }
  if form.is_valid():
    # print(form.cleaned_data)
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, ('Succesfully logged in'))
      return_url = 'index'
      if request.GET.get('next') is not None:
        return_url = request.GET.get('next')
      # Redirect to a success page.
      context['form']  = LoginForm()
      context['title'] = title
      return redirect(return_url)
    else:
      messages.success(request, ('Error logging in. Please try again..'))
      return redirect('login')
  else:
    return render(request, 'users/login.html', context)
 
# Logout view
def logout_user(request):
  logout(request)
  messages.success(request, ('Succesfully logged out'))
  # Redirect to a success page.
  return redirect('index')

# Register view
def register_user(request):
  title = 'Register'
  if request.method == 'POST':
    #do something
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(request, username=username, password=password)
      login(request, user)
      messages.success(request, ("You're Registered"))
      return redirect('index')
  else:
    form = SignUpForm()
  context = {
    'title': title,
    'form': form
  }
  return render(request, 'users/register.html', context)

# edit usersettings view
def edit_usersettings(request):
  if request.method == "POST":
    form = EditUsersettingsForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, ("You successfully updated your usersettings"))
      return redirect('index')
  else:
    form = EditUsersettingsForm(instance=request.user)
  context = {'form': form}
  return render(request, 'users/edit_usersettings.html', context)

# change password view
def change_password(request):
  if request.method == "POST":
    form = PasswordChangeForm(data=request.POST, user=request.user)
    if form.is_valid():
      form.save()
      update_session_auth_hash(request, form.user)
      messages.success(request, ("You successfully changed your password"))
      return redirect('index')
  else:
    form = PasswordChangeForm(user=request.user)
  context = {'form': form}
  return render(request, 'users/change_password.html', context)

### USERPROFILE ###

# Create profile
class CreateProfileView(CreateView):
  model         = UserProfile
  form_class    = ProfileForm
  template_name = 'users/create_profile.html'
  # fields        = '__all__'
  # success_url   = reverse_lazy('home')
  # function to get userid of loggendin user and use it to save profilepage
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

# Show profile
class ShowProfileView(DetailView):
  model         = UserProfile
  template_name = 'users/show_profile.html'
  # function to make data usable in html
  def get_context_data(self, *args, **kwargs):
    # users = UserProfile.objects.all()
    context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
    page_user = get_object_or_404(UserProfile, id=self.kwargs['pk'])
    context["page_user"] = page_user
    return context

# Edit profile
class EditProfileView(generic.UpdateView):
  model         = UserProfile
  form_class    = EditProfileForm
  template_name = 'users/edit_profile.html'
  # fields      = ['bio', 'profile_pic', 'website_url', 'twitter_url', 'facebook_url']
  success_url   = reverse_lazy ('index')
