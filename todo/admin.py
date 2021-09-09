from django.contrib import admin
# Register your models here.
from .models import User, UserManager, project ,listOfProject , cardOfList
from todo import models

admin.site.register(User)
admin.site.register(project)
admin.site.register(listOfProject)
admin.site.register(cardOfList)