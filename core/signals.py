# core/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BrandProfile, InfluencerProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profiles(sender, instance, created, **kwargs):
    """
    Automatically create a BrandProfile or InfluencerProfile row
    whenever a new user of that type is registered.
    """
    if not created:
        return

    if instance.membership_type == 'brand':
        BrandProfile.objects.create(user=instance)

    elif instance.membership_type == 'influencer':
        InfluencerProfile.objects.create(
            user=instance,
            platform='',
            handle='',
            followers=0,  # ✅ Prevent null constraint error
            niche='',
            bio='',
        )
