# users/forms.py

# django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

# local
from .models import UserProfile

# Login form
class LoginForm(forms.Form):
  username = forms.CharField(
    max_length = 50,
    label   = '',
    widget  = forms.TextInput(
      attrs = {
        'class'      :'form-control',
        'placeholder': 'username'
      }),
    help_text = 'Enter your username here'
  )
  password = forms.CharField(
    widget = forms.PasswordInput(
      attrs = {
        'class'      :'form-control',
        'placeholder': 'password'
      }),
    help_text = 'Enter your password here'
  )

# Sign up form / Register
class SignUpForm(UserCreationForm):
  email = forms.EmailField(
    label  = '',
    widget = forms.EmailInput(
      attrs = {
        'class'      :'form-control',
        'placeholder': 'email'
      }),
    help_text = 'Enter your emailaddress here'
  )
  first_name = forms.CharField(
    max_length = 100,
    label  = '',
    widget = forms.TextInput(
      attrs = {
        'class'      :'form-control',
        'placeholder': 'first name'
      }),
    help_text = 'Enter your first name here'
  )
  last_name  = forms.CharField(
    max_length = 100,
    label  = '',
    widget = forms.TextInput(
      attrs = {
        'class'      :'form-control',
        'placeholder': 'last name'
      }),
    help_text = 'Enter your last name here'
  )

  class Meta:
    model = User
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      'password1',
      'password2'
    )
  
  # Opmaak django formfields
  def __init__(self, *args, **kwargs):
    super(SignUpForm, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['class'] = 'form-control'
    # self.fields['username'].label = 'hier uw gebruikersnaam'
    self.fields['username'].label = ''
    self.fields['username'].widget.attrs['placeholder'] = 'username'
    self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'

    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].label = ''
    self.fields['password1'].widget.attrs['placeholder'] = 'password'

    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].label = ''
    self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'
    self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

class EditUsersettingsForm(UserChangeForm):
  password = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'hidden'}))
  
  class Meta:
    model = User
    # exclude = ()
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      'password'
    )

  # Opmaak django formfields
  def __init__(self, *args, **kwargs):
    super(EditUsersettingsForm, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['class'] = 'form-control'
    # self.fields['username'].label = 'hier uw gebruikersnaam'
    # self.fields['username'].label = ''
    self.fields['username'].widget.attrs['placeholder'] = 'username'
    self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'

    self.fields['first_name'].widget.attrs['class'] = 'form-control'
    self.fields['first_name'].widget.attrs['placeholder'] = 'first name'

    self.fields['last_name'].widget.attrs['class'] = 'form-control'
    self.fields['last_name'].widget.attrs['placeholder'] = 'last name'

    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['placeholder'] = 'email'

# Create Profile form
class ProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = (
      'bio',
      'profile_pic',
      'website_url',
      'twitter_url',
      'facebook_url'
    )
    widgets = {
      'bio'          : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'insert bio here', 'rows': 6}),
      # 'profile_pic'  : forms.TextInput(attrs={'class': 'form-control'}),
      'website_url'  : forms.TextInput(attrs={'class': 'form-control'}),
      'twitter_url'  : forms.TextInput(attrs={'class': 'form-control'}),
      'facebook_url' : forms.TextInput(attrs={'class': 'form-control'}),
    }

# Edit Profile form
class EditProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = (
      'bio',
      'profile_pic',
      'website_url',
      'twitter_url',
      'facebook_url'
    )
    widgets = {
      'bio'          : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'insert bio here', 'rows': 6}),
      # 'profile_pic'  : forms.TextInput(attrs={'class': 'form-control'}),
      'website_url'  : forms.TextInput(attrs={'class': 'form-control'}),
      'twitter_url'  : forms.TextInput(attrs={'class': 'form-control'}),
      'facebook_url' : forms.TextInput(attrs={'class': 'form-control'}),
    }
