from django.shortcuts import render
from .forms import vendorRegistrationForm
from accounts.forms import userProfileForm

# Create your views here.
def vProfile(request):
  profile_form = userProfileForm()
  vendor_form = vendorRegistrationForm()
  context = {
    'profile_form':profile_form,
    'vendor_form':vendor_form,
  }
  return render(request, 'vendor/vProfile.html', context)

