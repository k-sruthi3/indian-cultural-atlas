from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    remove_picture = forms.BooleanField(
        required=False,
        label="Remove profile picture"
    )

    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your full name"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your email"
    }))

    subject = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Subject"
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 4,
        "placeholder": "Write your message here..."
    }))

from django import forms

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Enter your registered email"
        })
    )