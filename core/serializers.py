from rest_framework import serializers
from .models import InfluencerProfile, BrandProfile

class InfluencerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = '__all__'

class BrandProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandProfile
        fields = '__all__'
