# maps/serializers.py

from rest_framework import serializers

from .models import Plaats, Metadata

#HyperlinkedModelSerializer
class PlaatsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model  = Plaats
    fields = ('pk', 'naam', 'aant_inwoners', 'latitude', 'longitude')
    extra_kwargs = {
      'latitude' : {'required': False},
      'longitude': {'required': False}
     }

# ModelSerializer
class MetadataSerializer(serializers.ModelSerializer):
  class Meta:
    model  = Metadata
    fields = '__all__'
    # extra_kwargs = {'description': {'required': False} }