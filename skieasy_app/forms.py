from django import forms
from skieasy_app.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
        )
        labels={
            'height': 'Height (ft):',
            'bootSize': 'Boot Size:',
            'userType': 'User Type:',
        }