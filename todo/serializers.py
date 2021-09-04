# use of serializer is to convert my table data into Json data
from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers 
from  .models import  card, project ,User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# class projectserializer(serializers.Serializer):

#     projtitle = serializers.CharField(max_length=50)
#     wiki = serializers.CharField(max_length=500)
#     member = User.objects.get(projtitle = projtitle.text).member
#     def create(self, validated_data):
#         user = project.objects.create(
#             projtitle=validated_data['projtitle'],
#             wiki=validated_data['wiki'],
#             member = validated_data['member'],
                     
#         )
#         return user
#     class Meta:
#         model = project
#         fields = ["projtitle","wiki","member"]
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



