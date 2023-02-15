from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Work, Status


@receiver(post_save, sender=Work)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Status.objects.create(work=instance)


@receiver(post_save, sender=Work)
def save_profile(sender, instance, **kwargs):
    instance.status.save()
