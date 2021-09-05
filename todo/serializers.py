# use of serializer is to convert my table data into Json data
from typing import List
from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers
from todo import models 
from  .models import  card, project ,User , list
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class projectserializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = '__all__'
class listserializer(serializers.ModelSerializer):
    class Meta:
        model = list
        fields = '__all__'
class cardserializer(serializers.ModelSerializer):
    class Meta:
        model = card
        fields = '__all__'



