# core/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BrandProfile, InfluencerProfile   # adjust to your exact model names


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profiles(sender, instance, created, **kwargs):
    """
    Automatically create a BrandProfile or InfluencerProfile row
    whenever a new user of that type is registered.
    """
    if not created:                       # only the first time the user is saved
        return

    if instance.membership_type == 'brand':
        BrandProfile.objects.create(user=instance)

    elif instance.membership_type == 'influencer':
        InfluencerProfile.objects.create(user=instance)

    # 'free' users require no extra profile
