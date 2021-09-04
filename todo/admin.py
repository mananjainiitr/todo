from django.contrib import admin
# Register your models here.
from .models import User, project ,list , card

admin.site.register(User)
admin.site.register(project)
admin.site.register(list)
admin.site.register(card)


class student(admin.ModelAdmin):
    list_display = ['id','name','year','email','enrollment']