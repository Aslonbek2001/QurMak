from django.contrib import admin
from .models import ClientModel
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta


class ClientModelAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "date_start", "date_end"]
    list_filter = ["date_start", "date_end", "created_at"]
    search_fields = ["username", "phone"]

    def save_model(self, request, obj, form, change):
        if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
            obj.password = make_password(obj.password)
        
        if not change: 
            if not obj.date_start:
                obj.date_start = timezone.now() 
            
            if not obj.date_end:
                obj.date_end = timezone.now()  + timedelta(days=365)

        super().save_model(request, obj, form, change)
    
admin.site.register(ClientModel, ClientModelAdmin)

