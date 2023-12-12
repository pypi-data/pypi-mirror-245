from django.contrib.postgres.fields import ArrayField
from django.db import models

from b2_forms.enums import Type


class CustomFieldMixin(models.Model):
    BINARY_TYPES = {Type.PHOTOGRAPH, Type.FILE}

    name = models.CharField(max_length=300)
    multiple = models.BooleanField(default=False)
    input_type = models.CharField(
        max_length=11,
        choices=Type.choices,
        default=Type.TEXT,
    )
    values = ArrayField(
        models.JSONField(blank=True, null=True),
        blank=True,
        default=list,
    )
    keywords = ArrayField(
        models.CharField(max_length=200, blank=True, null=True),
        blank=True,
        default=list,
    )

    class Meta:
        abstract = True


class FormFieldMixin(models.Model):
    index = models.FloatField()
    required = models.BooleanField(default=True)
    form_field = models.BooleanField(default=True)

    class Meta:
        abstract = True
