# theblog/forms.py

# Django
from typing_extensions import Required
from django import forms

# Local
from .models import BlogPost, Comment, Tag

# Form to add blogpost
class PostForm(forms.ModelForm):
  class Meta:
    model   = BlogPost
    fields  = ('title', 'header_image', 'title_tag', 'tag', 'body', 'snippet')
    widgets = {
      'title'    : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'insert title here'}),
      'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
      #'author'   : forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'authorfield', 'type':'hidden'}),
      'tag'      : forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'tag'}),
      'body'     : forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
      'snippet'  : forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    }

# form to edit blogpost
class EditBlogpostForm(forms.ModelForm):
  class Meta:
    model   = BlogPost
    fields  = ('title', 'header_image', 'title_tag', 'body', 'snippet', 'tag')
    widgets = {
      'title'    : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'insert title here'}),
      'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
      'tag'      : forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'tag'}),
      'body'     : forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
      'snippet'  : forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    }

# Form to add tag
class TagForm(forms.ModelForm):
  class Meta:
    model   = Tag
    fields  = ('caption', 'description')
    widgets = {
      'caption'     : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tag caption here'}),
      'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'tag description here', 'rows': 4}),
    }

# Form to add comment
class CommentForm(forms.ModelForm):
  class Meta:
    model   = Comment
    fields  = ('title', 'body')
    widgets = {
      'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'comment title here'}),
      'body'  : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'comment tekst here', 'rows': 4}),
    }
