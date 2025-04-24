from django.urls import path
from .views import influencer_dashboard, brand_dashboard, submit_campaign_brief
from . import views

urlpatterns = [
    path('edit-profile/brand/', views.edit_brand_profile, name='edit-brand-profile'),
    path('edit-profile/influencer/', views.edit_influencer_profile, name='edit-influencer-profile'),
    path('dashboard/influencer/', influencer_dashboard, name='influencer-dashboard'),
    path('dashboard/brand/', brand_dashboard, name='brand-dashboard'),
    path(
        "dashboard/match-influencers/",
        views.match_influencers,
        name="match-influencers",  # <-- keep this exact string
    ),
    path(
        "influencers/<int:pk>/",        # e.g. /core/influencers/5/
        views.influencer_detail,        # view we create next
        name="influencer-detail",       # exactly what the template expects
    ),
    path('campaign/submit/', submit_campaign_brief, name='submit-campaign-brief'),
    path('campaign/list/', views.campaign_brief_list, name='campaign-brief-list'),
    path("dashboard/analytics/", views.influencer_analytics_dashboard, name="influencer-analytics"),

]

