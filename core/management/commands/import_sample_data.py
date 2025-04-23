import csv
from django.core.management.base import BaseCommand
from core.models import InfluencerProfile, BrandProfile
from accounts.models import User

class Command(BaseCommand):
    help = 'Import sample influencer and brand data from CSV files'

    def handle(self, *args, **kwargs):
        # Load Influencers
        with open('influencers_sample.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = User.objects.create_user(
                    username=row['handle'],
                    password='TestPass123!',
                    is_influencer=True
                )
                InfluencerProfile.objects.create(
                    user=user,
                    platform=row['platform'],
                    handle=row['handle'],
                    followers=int(row['followers']),
                    niche=row['niche'],
                    bio=row['bio']
                )

        # Load Brands
        with open('brands_sample_with_industry_country.csv', newline='',
                  encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = User.objects.create_user(
                    username=row['company_name'].replace(' ', '_'),
                    password='TestPass123!',
                    is_brand=True
                )
                BrandProfile.objects.create(
                    user=user,
                    company_name=row['company_name'],
                    website=row['website'],
                    bio=row['bio'],
                    industry=row['industry'],
                    country=row['country']
                )

        self.stdout.write(self.style.SUCCESS("✅ Sample data imported successfully!"))
