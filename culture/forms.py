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
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea)