# use of serializer is to convert my table data into Json data
from typing import List
from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers
from todo import models 
from  .models import  cardOfList, project ,User , listOfProject
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class projectserializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = '__all__'
class listserializer(serializers.ModelSerializer):
    class Meta:
        model = listOfProject
        fields = '__all__'
class cardserializer(serializers.ModelSerializer):
    class Meta:
        model = cardOfList
        fields = '__all__'



