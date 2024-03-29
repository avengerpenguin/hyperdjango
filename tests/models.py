from django.core.validators import MinLengthValidator
from django.db import models

from hyperdjango.models import HyperModel


class Thing(HyperModel):
    name = models.CharField(max_length=256, validators=[MinLengthValidator(1)])

    def __repr__(self):
        return f"Thing(pk={self.pk},name={self.name})"
