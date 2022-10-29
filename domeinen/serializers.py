# domeinen/serializers.py

from rest_framework import serializers

from .models import Rol

#HyperlinkedModelSerializer
class RolSerializer(serializers.ModelSerializer):
  class Meta:
    model  = Rol
    fields = ('uuid', 'rol', 'description')
    extra_kwargs = {'description': {'required': False} }