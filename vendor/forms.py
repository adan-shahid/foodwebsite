from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator

class vendorRegistrationForm(forms.ModelForm):
    class Meta:

        vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
        model = Vendor
        fields = ['vendor_name', 'vendor_license']