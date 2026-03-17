from django.db import models

"""##############################   QuizModel    #############################"""

class QuizModel(models.Model):
    level = models.IntegerField(verbose_name="Savol Darajasi", db_index=True)
    number = models.IntegerField(verbose_name="Savol Raqami", db_index=True)
    variant_size =models.IntegerField(verbose_name="Variant foto size", default=1)
    question = models.TextField(verbose_name="Asosiy Savol matni", null=True, blank=True)
    sub_text = models.TextField(verbose_name="Sub Savol matni", null=True, blank=True)
    foto = models.ImageField(verbose_name="Savol Rasmi", upload_to="question", null=True, blank=True)
    size = models.IntegerField(verbose_name="Foto size", default=1)
    
    answer = models.TextField(verbose_name="Javob matni", null=True, blank=True)
    foto_answear = models.ImageField(verbose_name="Javob Rasmi", upload_to="question", null=True, blank=True)

    option_one = models.TextField(verbose_name="1-variant", null=True, blank=True)
    foto_one = models.ImageField(verbose_name="1-variant rasmi", upload_to="question", null=True, blank=True)

    option_two = models.TextField(verbose_name="2-variant", null=True, blank=True)
    foto_two = models.ImageField(verbose_name="2-variant rasmi", upload_to="question", null=True, blank=True)

    option_three = models.TextField(verbose_name="3-variant", null=True, blank=True)
    foto_three = models.ImageField(verbose_name="3-variant rasmi", upload_to="question", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = QuizModel.objects.get(pk=self.pk)
                if old_instance.foto and old_instance.foto != self.foto:
                    # Delete the old file from the filesystem
                    old_instance.foto.delete(save=False)
            except QuizModel.DoesNotExist:
                pass       

        super(QuizModel, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.foto:
            self.foto.delete(save=False)
        if self.foto_answear:
            self.foto_answear.delete(save=False)
        if self.foto_one:
            self.foto_one.delete(save=False)
        if self.foto_two:
            self.foto_two.delete(save=False)
        if self.foto_three:
            self.foto_three.delete(save=False)
        super(QuizModel, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.question} ----- {self.answer}"


