from django.db import models
from users.models import ClientModel
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class UserLevelPage(models.Model):
    user = models.ForeignKey(ClientModel, on_delete=models.CASCADE, help_text="The user associated with this level/page.")
    level = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        db_index=True,
        help_text="Level must be an integer between 1 and 5."
    )
    page = models.PositiveIntegerField(help_text="The page number or identifier.")
    result = models.PositiveIntegerField(help_text="The result or score achieved by the user on this page.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'level', 'page')

    def __str__(self):
        return f"User: {self.user}, Page: {self.page}, Result: {self.result}"
    


        