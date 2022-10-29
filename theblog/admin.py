# theblog/admin.py

# Django
from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from django.urls import reverse
from django.utils.safestring import mark_safe    

# Local
from .models import Tag, BlogPost, Tag, Comment

# settings for dedicated adminpage /blogadmin/
class BlogAdminArea(admin.AdminSite):
  site_header = 'Blog Admin Area'
  index_title = "Blog Administration"

blog_adminsite = BlogAdminArea(name = 'BlogAdmin')

# Models
class Blogadmin(admin.ModelAdmin):
  list_display = ('title', 'head_image', 'post_date', 'author', 'total_comments')
  list_filter  = ('author', 'tag', 'post_date',)
  prepopulated_fields = {'slug': ('title',)}

class Tagadmin(admin.ModelAdmin):
  list_display = ('caption', 'description',)
  ordering     = ('caption',)

class Commentadmin(admin.ModelAdmin):
  list_display = ('blogposttitle', 'title', 'author')
  ordering     = ('blogpost', 'date_added')
  # Add it to the details view:
  readonly_fields = ('blogposttitle',)
  def blogposttitle(self, obj):
    return obj.blogpost.title
  blogposttitle.short_description = 'blogpost'

# Register models with layout
# overall adminarea
admin.site.register(BlogPost, Blogadmin)
admin.site.register(Tag, Tagadmin)
admin.site.register(Comment, Commentadmin)
# dedicated admin area
blog_adminsite.register(BlogPost, Blogadmin)
blog_adminsite.register(Tag, Tagadmin)
blog_adminsite.register(Comment, Commentadmin)

# Register models without layout:
myModels = []  # iterable list
# overall adminarea
admin.site.register(myModels)
# dedicated admin area
blog_adminsite.register(myModels)
