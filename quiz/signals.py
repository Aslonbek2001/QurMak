from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from .models import QuizModel

@receiver(pre_delete, sender=QuizModel)
def delete_quiz_images(sender, instance, **kwargs):
    # Fayl mavjudligini tekshiring va o'chiring
    if instance.foto:
        instance.foto.delete(save=False)
    if instance.foto_answear:
        instance.foto_answear.delete(save=False)
    if instance.foto_one:
        instance.foto_one.delete(save=False)
    if instance.foto_two:
        instance.foto_two.delete(save=False)
    if instance.option_three:
        instance.option_three.delete(save=False)
