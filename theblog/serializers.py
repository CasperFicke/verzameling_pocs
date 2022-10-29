'''
# Serializer ; converting database to and from json
from rest_framework import serializers

from .models import BlogPost

class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = BlogPost
    fields = ('id', 'url', 'title', 'author', 'body')
'''