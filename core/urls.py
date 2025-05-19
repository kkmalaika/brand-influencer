from django.urls import path
from .views import influencer_dashboard, brand_dashboard, submit_campaign_brief, refresh_tiktok_stats, hashtag_search_history, add_to_watchlist
from . import views
from core import views

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
    path("scrape-tiktok/", views.scrape_tiktok_hashtag, name="scrape_tiktok"),
    path("dashboard/refresh-stats/", refresh_tiktok_stats, name="refresh_tiktok_stats"),
    path("dashboard/", views.influencer_analytics_dashboard, name="influencer_analytics_dashboard"),
    path("hashtag-history/", hashtag_search_history, name="hashtag_search_history"),
    path('hashtag-search/<int:search_id>/', views.hashtag_search_detail, name='hashtag_search_detail'),
    path("add-to-watchlist/", views.add_to_watchlist, name="add_to_watchlist"),
    path('dashboard/watchlist/', views.brand_watchlist, name='brand_watchlist'),
    path("dashboard/analytics/<int:influencer_id>/", views.influencer_analytics_detail, name="influencer_analytics_detail"),

]

