from django.contrib import admin
from .models import UserLevelPage
# Register your models here.

class UserLevelPageModelAdmin(admin.ModelAdmin):
    list_display = ['level', 'page', 'result']


admin.site.register(UserLevelPage, UserLevelPageModelAdmin)