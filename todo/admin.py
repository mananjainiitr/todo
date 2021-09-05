from django.contrib import admin
# Register your models here.
from .models import User, project ,list , card
from todo import models

admin.site.register(User)
admin.site.register(project)
admin.site.register(list)
admin.site.register(card)