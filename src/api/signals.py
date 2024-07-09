from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Account, User


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == Account.Role.User:
        User.objects.create(account=instance)


@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == Account.Role.User:
        instance.user.save()
