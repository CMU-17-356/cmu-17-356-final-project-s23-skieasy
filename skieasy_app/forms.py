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
            'boot_size': 'Boot Size (US):',
            'user_type': 'User Type:',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }


class EquipmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].required = True

    class Meta:
        model = Equipment
        exclude = (
            'profile_id',
            'content_type'
        )


class EquipmentListingForm(forms.Form):
    start_date = forms.DateTimeField(
        label='Start Date',
        widget=forms.SelectDateWidget
    )
    end_date = forms.DateTimeField(
        label='End Date',
        widget=forms.SelectDateWidget
    )
