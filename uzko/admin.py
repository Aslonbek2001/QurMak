from django.contrib import admin

from .models import VocabModel

class VocabModelAdmin(admin.ModelAdmin):
    list_display = ["id", "korean", "uzb", "krill"]
    search_fields = ["id","korean","korean", "krill"]
    list_filter = ["id"]

admin.site.register(VocabModel, VocabModelAdmin)

