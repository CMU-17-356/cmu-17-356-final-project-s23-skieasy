from skieasy_app.models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
        )
        labels = {
            'height': 'Height (ft):',
            'bootSize': 'Boot Size:',
            'userType': 'User Type:',
        }
