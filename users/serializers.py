from .models import User,Person
from rest_framework import serializers
class POTSUserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['first_name','last_name', 'email', 'password']
     


class POTSPersonSerializer(serializers.ModelSerializer):
   class Meta:
      model = Person
      fields = ['name','mobile']
     
