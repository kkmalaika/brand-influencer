from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    InfluencerProfileViewSet,
    BrandProfileViewSet,
    home,
    influencer_list,
    brand_list,
    MatchInfluencersView
)

# Register API viewsets
router = DefaultRouter()
router.register(r'influencers', InfluencerProfileViewSet)
router.register(r'brands', BrandProfileViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include(router.urls)),
    path('api/match/', MatchInfluencersView.as_view(), name='match-influencers'),
    path('influencers/', influencer_list, name='influencer-list'),
    path('brands/', brand_list, name='brand-list'),

    # Auth & app routes
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),  # ✅ Only include once
]
