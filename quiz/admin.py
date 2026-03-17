from django.contrib import admin
from .models import QuizModel


class QuizModelAdmin(admin.ModelAdmin):
    list_display = ["id", "level","number", "question", "sub_text"]
    search_fields = ["number","sub_text","question"]
    list_filter = ["level"]
    
    def delete_model(self, request, obj):
        # Faylni o'chirish uchun obj ni o'chirishdan oldin chaqirish
        if obj.foto:
            obj.foto.delete(save=False)
        if obj.foto_answear:
            obj.foto_answear.delete(save=False)
        if obj.foto_one:
            obj.foto_one.delete(save=False)
        if obj.foto_two:
            obj.foto_two.delete(save=False)
        if obj.foto_three:
            obj.foto_three.delete(save=False)

        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Fayllarni o'chirish uchun queryset ni o'chirishdan oldin chaqirish
        for obj in queryset:
            if obj.foto:
                obj.foto.delete(save=False)
            if obj.foto_answear:
                obj.foto_answear.delete(save=False)
            if obj.foto_one:
                obj.foto_one.delete(save=False)
            if obj.foto_two:
                obj.foto_two.delete(save=False)
            if obj.foto_three:
                obj.foto_three.delete(save=False)
        super().delete_queryset(request, queryset)

admin.site.register(QuizModel, QuizModelAdmin)