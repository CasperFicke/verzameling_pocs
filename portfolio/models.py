# portfolio/models.py

from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

# Create your models here.

# Skill model
class Skill(models.Model):
  class Meta:
    verbose_name_plural = 'Skills'
    verbose_name        = 'Skill'
  
  name         = models.CharField(max_length=20, blank=True, null=True)
  score        = models.IntegerField(default=80, blank=True, null=True)
  image        = models.FileField(blank=True, null=True, upload_to="skills")
  is_key_skill = models.BooleanField(default=False)
    
  def __str__(self):
    return self.name

# Userprofile model
class UserProfileP(models.Model):
  class Meta:
    verbose_name_plural = 'User Profiles'
    verbose_name        = 'User Profile'
    
  avatar = models.ImageField(blank=True, null=True, upload_to="avatar")
  title  = models.CharField(max_length=200, blank=True, null=True)
  bio    = models.TextField(blank=True, null=True)
  cv     = models.FileField(blank=True, null=True, upload_to="cv")
  # relaties
  user   = models.OneToOneField(User, on_delete=models.CASCADE)
  skills = models.ManyToManyField(Skill, blank=True)

  def __str__(self):
    return f'{self.user.first_name} {self.user.last_name}'

# ContactProfile model
class ContactProfile(models.Model):
  class Meta:
    verbose_name_plural = 'Contact Profiles'
    verbose_name        = 'Contact Profile'
    ordering            = ["timestamp"]

  name      = models.CharField(verbose_name="Name",max_length=100)
  email     = models.EmailField(verbose_name="Email")
  message   = models.TextField(verbose_name="Message")
  # secundair
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.name}'

# Testimonial model
class Testimonial(models.Model):
  class Meta:
    verbose_name_plural = 'Testimonials'
    verbose_name        = 'Testimonial'
    ordering            = ["name"]

  name      = models.CharField(max_length=200, blank=True, null=True)
  role      = models.CharField(max_length=200, blank=True, null=True)
  thumbnail = models.ImageField(blank=True, null=True, upload_to="testimonials")
  quote     = models.CharField(max_length=500, blank=True, null=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.name

# Media model
class Media(models.Model):
  class Meta:
    verbose_name_plural = 'Media Files'
    verbose_name        = 'Media'
    ordering            = ["name"]
	
  name     = models.CharField(max_length=200, blank=True, null=True)
  url      = models.URLField(blank=True, null=True)
  image    = models.ImageField(blank=True, null=True, upload_to="media")
  is_image = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if self.url:
      self.is_image = False
    super(Media, self).save(*args, **kwargs)
  def __str__(self):
    return self.name

# Portfolio model
class Portfolio(models.Model):
  class Meta:
    verbose_name_plural = 'Portfolio Profiles'
    verbose_name        = 'Portfolio'
    ordering            = ["name"]

  name        = models.CharField(max_length=200, blank=True, null=True)
  description = models.CharField(max_length=500, blank=True, null=True)
  body        = RichTextField(blank=True, null=True)
  image       = models.ImageField(blank=True, null=True, upload_to="portfolio")
  date        = models.DateTimeField(blank=True, null=True)
  slug        = models.SlugField(null=True, blank=True)
  is_active   = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if not self.id:
      self.slug = slugify(self.name)
    super(Portfolio, self).save(*args, **kwargs)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f"/portfolio/{self.slug}"

# Blog model
class Blog(models.Model):
  class Meta:
    verbose_name_plural = 'Blog Profiles'
    verbose_name        = 'Blog'
    ordering            = ["timestamp"]

  name        = models.CharField(max_length=200, blank=True, null=True)
  description = models.CharField(max_length=500, blank=True, null=True)
  body        = RichTextField(blank=True, null=True)
  image       = models.ImageField(blank=True, null=True, upload_to="blog")
  author      = models.CharField(max_length=200, blank=True, null=True)
  timestamp   = models.DateTimeField(auto_now_add=True)
  slug        = models.SlugField(null=True, blank=True)
  is_active   = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if not self.id:
      self.slug = slugify(self.name)
    super(Blog, self).save(*args, **kwargs)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f"/blog/{self.slug}"

# Certificate model
class Certificate(models.Model):
  class Meta:
    verbose_name_plural = 'Certificates'
    verbose_name        = 'Certificate'

  name        = models.CharField(max_length=50, blank=True, null=True)
  description = models.CharField(max_length=500, blank=True, null=True)
  title       = models.CharField(max_length=200, blank=True, null=True)
  date        = models.DateTimeField(blank=True, null=True)
  is_active   = models.BooleanField(default=True)

  def __str__(self):
    return self.name