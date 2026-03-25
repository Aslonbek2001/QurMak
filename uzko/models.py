from django.db import models
# from UzTransliterator import UzTransliterator

class VocabModel(models.Model):
    korean = models.TextField(db_index=True, verbose_name="Qurilish atama nomi")
    uzb = models.TextField(db_index=True, verbose_name="O'zbek tilida")
    krill = models.TextField(db_index=True, verbose_name="Krill tilida", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Qurilish atamasi "
        verbose_name_plural = "Qurilish atamalar "



    # def save(self, *args, **kwargs):
    #     if self.uzb and (not self.krill):
    #         obj = UzTransliterator.UzTransliterator()
    #         self.krill = obj.transliterate(self.uzb, from_="lat", to="cyr")
    #         print(self.krill)
        
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.korean} ---- {self.uzb}" 
    


