from django import forms
from .models import NewsletterSubscriber, BrandProfile, InfluencerProfile, CampaignBrief
from django_countries.widgets import CountrySelectWidget


# 🔔 Newsletter form
class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control',
                'required': 'required'
            })
        }


# 🏢 Brand profile editing
class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        fields = ['company_name', 'website', 'bio', 'industry', 'country']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Your company name', 'class': 'form-control', 'required': 'required'
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'https://example.com', 'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell us about your brand...', 'class': 'form-control', 'rows': 4
            }),
            'industry': forms.TextInput(attrs={
                'placeholder': 'e.g. Fitness, Beauty...', 'class': 'form-control'
            }),
            'country': CountrySelectWidget(attrs={'class': 'form-select'})
        }


# 🎯 Influencer profile editing
class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['platform', 'handle', 'followers', 'niche', 'bio']
        widgets = {
            'platform': forms.TextInput(attrs={
                'placeholder': 'e.g. Instagram, TikTok...', 'class': 'form-control', 'required': 'required'
            }),
            'handle': forms.TextInput(attrs={
                'placeholder': '@yourhandle', 'class': 'form-control', 'required': 'required'
            }),
            'followers': forms.NumberInput(attrs={
                'placeholder': 'Number of followers', 'class': 'form-control', 'required': 'required'
            }),
            'niche': forms.TextInput(attrs={
                'placeholder': 'e.g. Travel, Fashion...', 'class': 'form-control', 'required': 'required'
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Short bio...', 'class': 'form-control', 'rows': 4
            }),
        }


# 📣 Campaign Brief Form
class CampaignBriefForm(forms.ModelForm):
    class Meta:
        model = CampaignBrief
        fields = ['title', 'goals', 'niche', 'budget', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Campaign title', 'required': 'required'
            }),
            'goals': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4, 'placeholder': 'What do you hope to achieve?', 'required': 'required'
            }),
            'niche': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Target niche or audience', 'required': 'required'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Estimated budget', 'required': 'required'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date', 'required': 'required'
            }),
        }
