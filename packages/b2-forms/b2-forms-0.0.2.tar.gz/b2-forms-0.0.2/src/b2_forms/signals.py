from django.db.models.signals import post_save
from django.dispatch import receiver

from b2_forms.models import Form


@receiver(post_save, sender=Form)
def create_form_sections(sender, instance, created, **kwargs):
    if created:
        instance.sections.create(name="Default")
