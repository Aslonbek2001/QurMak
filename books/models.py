import os
from django.db import models
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    max_size = 10 * 1024 * 1024  # Maksimal hajm 10 MB

    if filesize > max_size:
        raise ValidationError("Fayl hajmi 10 MB dan oshmasligi kerak!")
    return value

class BaseBook(models.Model):
    number = models.PositiveIntegerField(db_index=True)  # Har ikkala model uchun umumiy maydon
    page = models.ImageField(upload_to="book_pages/", validators=[validate_file_size])  # Har ikkala model uchun umumiy maydon

    class Meta:
        abstract = True  # Bu modelni faqat asosiy model sifatida ishlatish uchun

    def delete(self, *args, **kwargs):
        if self.page:
            if os.path.isfile(self.page.path):
                os.remove(self.page.path)  # Rasmni tizimdan o‘chirish
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.number}-page"

class BookOne(BaseBook):
    class Meta:
        db_table = "book_one"  # Modelning bazadagi nomi
        verbose_name = "Book One"
        verbose_name_plural = "Book Ones"

class BookTwo(BaseBook):
    class Meta:
        db_table = "book_two"
        verbose_name = "Book Two"
        verbose_name_plural = "Book Twos"
