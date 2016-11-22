from django import forms
from gathering.models import DataTable, UserProfile
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    face = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', )
