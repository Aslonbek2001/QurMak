from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import ClientModel


class UserForm(ModelForm):
    class Meta:
        meta = ClientModel
        fields = "__all__"
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }



