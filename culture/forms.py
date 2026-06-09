#culture/forms.py
from django import forms
from .models import Profile
from .models import Submission


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

   


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission

        fields = [
            'area_type',
            'state_name',
            'district_name',

            'capital',

            'famous_food',
            'food_image',
            'food_link',

            'famous_dance',
            'dance_image',
            'dance_link',

            'famous_folk_art',
            'folk_art_image',
            'folk_art_link',

            'famous_temple',
            'temple_image',
            'temple_link',

            'traditional_dress',
            'dress_image',
            'dress_link',

            'monuments',
            'monument_image',
            'monument_link',

            'famous_festival',
            'festival_link',

            'uniqueness',
            'uniqueness_link',

            'image',
        ]


        widgets = {
            'area_type': forms.Select(attrs={'class': 'form-control'}),
            'state_name': forms.TextInput(attrs={'class': 'form-control'}),
            'district_name': forms.TextInput(attrs={'class': 'form-control'}),

            'capital': forms.TextInput(attrs={'class': 'form-control'}),

            'famous_food': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'food_image': forms.URLInput(attrs={'class': 'form-control'}),
            'food_link': forms.URLInput(attrs={'class': 'form-control'}),

            'famous_dance': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dance_image': forms.URLInput(attrs={'class': 'form-control'}),
            'dance_link': forms.URLInput(attrs={'class': 'form-control'}),

            'famous_folk_art': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'folk_art_image': forms.URLInput(attrs={'class': 'form-control'}),
            'folk_art_link': forms.URLInput(attrs={'class': 'form-control'}),

            'famous_temple': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'temple_image': forms.URLInput(attrs={'class': 'form-control'}),
            'temple_link': forms.URLInput(attrs={'class': 'form-control'}),

            'traditional_dress': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dress_image': forms.URLInput(attrs={'class': 'form-control'}),
            'dress_link': forms.URLInput(attrs={'class': 'form-control'}),

            'monuments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'monument_image': forms.URLInput(attrs={'class': 'form-control'}),
            'monument_link': forms.URLInput(attrs={'class': 'form-control'}),

            'famous_festival': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'festival_link': forms.URLInput(attrs={'class': 'form-control'}),

            'uniqueness': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'uniqueness_link': forms.URLInput(attrs={'class': 'form-control'}),

            'image': forms.URLInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()

        area_type = cleaned_data.get('area_type')
        state_name = cleaned_data.get('state_name')
        district_name = cleaned_data.get('district_name')

        # State name must always be provided
        if not state_name:
            raise forms.ValidationError(
                "State name is required."
            )

        # District submissions must have district name
        if area_type == "district" and not district_name:
            raise forms.ValidationError(
                "District name is required when Area Type is District."
            )

        # Require at least one cultural detail
        cultural_fields = [
            cleaned_data.get('famous_food'),
            cleaned_data.get('famous_dance'),
            cleaned_data.get('famous_folk_art'),
            cleaned_data.get('famous_temple'),
            cleaned_data.get('traditional_dress'),
            cleaned_data.get('monuments'),
            cleaned_data.get('famous_festival'),
            cleaned_data.get('uniqueness'),
        ]

        if not any(cultural_fields):
            raise forms.ValidationError(
                "Please fill at least one cultural information field."
            )

        return cleaned_data