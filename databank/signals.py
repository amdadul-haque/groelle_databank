from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Work



@receiver(pre_save, sender=Work)
def update_storagestatus(sender, instance, **kwargs):
    if instance.renter is not None:
        instance.storagestatus = Work.StorageStatus.RNT
    elif instance.renter is None and instance.storagestatus == Work.StorageStatus.RNT:
        instance.storagestatus = Work.StorageStatus.WPT


@receiver(pre_save, sender=Work)
def update_salesstatus(sender, instance, **kwargs):
    if instance.buyer is not None and instance.salesstatus != "Geliefert":
        instance.salesstatus = Work.SalesStatus.SOLD




# @receiver(post_save, sender=Work)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Status.objects.create(work=instance)


# @receiver(post_save, sender=Work)
# def save_profile(sender, instance, **kwargs):
#     instance.status.save()
