'''
# Serializer ; converting database to and from json
from rest_framework import serializers

from .models import Course, Stock

class CourseSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Course
    fields = ('id', 'url', 'name', 'language', 'price')


class StockSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Stock
    fields = ('id', 'url', 'ticker_name', 'ticker_description')
'''