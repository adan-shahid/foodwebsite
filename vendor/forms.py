from django import forms
from .models import Vendor

class vendorRegistrationForm(forms.ModelForm):
    class Meta:
        vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
        model = Vendor
        fields = ['vendor_name', 'vendor_license']