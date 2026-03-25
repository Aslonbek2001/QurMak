from django.db import models
# from UzTransliterator import UzTransliterator

class VocabModel(models.Model):
    korean = models.CharField(max_length=100, db_index=True)
    uzb = models.CharField(max_length=100, db_index=True)
    krill = models.CharField(max_length=100,db_index=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    # def save(self, *args, **kwargs):
    #     if self.uzb and (not self.krill):
    #         obj = UzTransliterator.UzTransliterator()
    #         self.krill = obj.transliterate(self.uzb, from_="lat", to="cyr")
    #         print(self.krill)
        
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.korean} ---- {self.uzb}" 
    


