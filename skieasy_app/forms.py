from skieasy_app.models import Profile, Equipment
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'user',
        )
        labels = {
            'height': 'Height (ft):',
            'bootSize': 'Boot Size (US):',
            'userType': 'User Type:',
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = (
            'profileId',
        )
