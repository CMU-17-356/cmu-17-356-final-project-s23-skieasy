from skieasy_app.models import Profile, Equipment, EquipmentListing
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
            'firstName': 'First Name',
            'lastName': 'Last Name',
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = (
            'profileId',
        )

class EquipmentListingForm(forms.Form):
    startDate = forms.DateTimeField(label = 'Start Date', widget = forms.SelectDateWidget)
    endDate = forms.DateTimeField(label = 'End Date', widget = forms.SelectDateWidget)
