### FORMS.PY WEBSITE APP ###

# django
from django import forms

# contact form
class ContactForm(forms.Form):
  naam = forms.CharField(
    widget= forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'uw naam'
      }))
  email   = forms.EmailField(
    widget= forms.EmailInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'uw email'
      }))
  bericht = forms.CharField(
    widget= forms.Textarea(
      attrs={
        'class': 'form-control',
        'placeholder': 'uw bericht'
      }))

  # validation
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if not '.nl' in email:
      raise forms.ValidationError('email moet van een .nl domein zijn')
    return email
