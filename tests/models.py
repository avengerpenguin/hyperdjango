from django.core.validators import MinLengthValidator
from django.db import models
import hyperdjango


class Thing(hyperdjango.models.HyperModel):
    name = models.CharField(max_length=256, validators=[MinLengthValidator(1)])

    def __repr__(self):
        return 'Thing(pk={},name={})'.format(self.pk, self.name)
