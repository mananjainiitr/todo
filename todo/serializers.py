# use of serializer is to convert my table data into Json data
from typing import List
from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from todo import models 
from  .models import  cardOfList, project ,User , listOfProject
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class projectserializer(serializers.ModelSerializer):
    # tracks = userdataserializer(many = True)
    # emails = dataserializer(many=True,read_only=True)
    # creator_pkk = creator_pk
    # creator_pk = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), source='creator'
    # )
    member_pk2 = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='member',many = True
    )

    class Meta:
        model = project
        fields = ["id",'projtitle','wiki','creator','member_pk2','member']
        depth = 1;
        
class listserializer(serializers.ModelSerializer):
    class Meta:
        model = listOfProject
        fields = "__all__"
        depth = 1;
class cardserializer(serializers.ModelSerializer):
    member_pk2 = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_member',many = True
    )
    class Meta:
        model = cardOfList
        fields = "__all__"
        depth = 1
class userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","year","is_active","admin","staff"]
        read_only_fields = ['email','year']
        # fields = "__all__"
class dashcardserializer(serializers.ModelSerializer):
    class Meta:
        model = cardOfList
        fields = "__all__"
class dashprojserializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = "__all__"
class dataserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email"]
        read_only_fields = ['email']

class userdataserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","year","is_active","admin","staff","name"]
        read_only_fields = ["email","year","is_active","admin","staff","name"]
        

class ProjectValidator(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = ['projtitle']
        read_only_fields = ['projtitle']

