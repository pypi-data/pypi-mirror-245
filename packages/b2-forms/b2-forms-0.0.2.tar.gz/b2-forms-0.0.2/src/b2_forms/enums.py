from django.db import models
from django.utils.translation import gettext_lazy as _


class Type(models.TextChoices):
    TEXT = "TEXT", _("Text")
    NUMBER = "NUMBER", _("Number")
    DATE = "DATE", _("Date")
    BOOLEAN = "BOOLEAN", _("Boolean")
    DATETIME = "DATETIME", _("Datetime")
    CHECKBOX = "CHECKBOX", _("Checkbox")
    RADIO = "RADIO", _("Radio")
    SLIDER = "SLIDER", _("Slider")
    PHOTOGRAPH = "PHOTOGRAPH", _("Photograph")
    FILE = "FILE", _("File")
    LINK = "LINK", _("Link")
    DOCUMENT = "DOCUMENT", _("Document")
    CPF = "CPF", _("CPF")
    CNPJ = "CNPJ", _("CNPJ")
    MONEY = "MONEY", _("Money")
