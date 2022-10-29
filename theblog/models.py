# theblog/models.py

# django
from django.conf import settings
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.urls import reverse
from django.utils.html import mark_safe
from django.core.validators import MinLengthValidator

from ckeditor.fields import RichTextField

# python
from datetime import datetime, date

# Tag model
class Tag(models.Model):
  caption     = models.CharField(max_length=40, unique=True)
  description = models.TextField(max_length=200, null=True, blank=True)

  # functie om object in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.caption

# Blogpost model
class BlogPost(models.Model):
  title        = models.CharField(max_length=200)
  title_tag    = models.CharField(max_length=200, default='title')
  header_image = models.ImageField(null=True, blank=True, upload_to="images/blogheader/")
  snippet      = models.CharField(max_length=255)
  #body        = models.TextField(validators=[MinLengthValidator(10)])
  body         = RichTextField(blank=True, null=True)
  slug         = models.SlugField(blank=True, db_index=True)
  post_date    = models.DateField(auto_now_add=True, help_text='Date when the Blogpost was first created')
  # relaties
  author       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blogposts')
  tag          = models.ManyToManyField(Tag, blank=True, related_name='blogposts')
  likes        = models.ManyToManyField(User, blank=True, related_name='blog_posts')
   
  # functie om aantal likes te bepalen
  def total_comments(self):
    return self.comments.count()

  # functie om aantal likes te bepalen
  def total_likes(self):
    return self.likes.count()
  
  # functie om object in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.title + ' | ' + str(self.author)
  # functie om image in de admin web-pagina te kunnen presenteren
  def head_image(self):
    if self.header_image != '':
      return mark_safe('<img src="%s%s" width="100" height="100" />' % (f'{settings.MEDIA_URL}', self.header_image))
  
  # functie om redirect url te bepalen
  def get_absolute_url(self):
    return reverse('all-blogposts')
    # return reverse('show_blogpost', args=(str(self.id)))

# Comment Model
class Comment (models.Model):
  title      = models.CharField(max_length=255)
  body       = models.TextField(max_length=300)
  date_added = models.DateTimeField(auto_now_add=True)
  # relaties
  blogpost   = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
  author     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')

  # functie om in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.blogpost.title} - {self.title}' 
