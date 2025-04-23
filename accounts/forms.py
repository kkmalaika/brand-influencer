# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# ----------------------------------------------------------------------
# Login
# ----------------------------------------------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )


# ----------------------------------------------------------------------
# Registration
# ----------------------------------------------------------------------
class CustomUserRegistrationForm(UserCreationForm):
    """
    Registration form that lets the visitor pick any membership type
    defined on the custom User model.

    •  The labels shown to the visitor are kept simple
       ('Brand', 'Influencer', 'Free').
    •  Each input box receives the Bootstrap 'form-control' class
       for consistent width / alignment.
    """

    # 👇—  Radio‑button options shown to visitors
    PUBLIC_MEMBERSHIP_CHOICES = [
        ("free", "Free"),
        ("brand", "Brand"),
        ("influencer", "Influencer"),
    ]

    membership_type = forms.ChoiceField(
        choices=PUBLIC_MEMBERSHIP_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="I am a",
        initial="free",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "membership_type"]

    # Make every non‑radio widget use Bootstrap styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Give username / email / password inputs the 'form-control' class
        for name, field in self.fields.items():
            if name != "membership_type":           # radios handled above
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing_classes} form-control".strip()

    # Persist the chosen membership_type on the user object
    def save(self, commit=True):
        user = super().save(commit=False)
        user.membership_type = self.cleaned_data["membership_type"]
        if commit:
            user.save()
        return user
