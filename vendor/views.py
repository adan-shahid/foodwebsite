from django.shortcuts import render, get_object_or_404
from .forms import vendorRegistrationForm
from accounts.forms import userProfileForm
from accounts.models import UserProfile
from .models import Vendor

# Create your views here.
def vProfile(request):
  profile = get_object_or_404(UserProfile, user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)

#BY PASSING THE INSTANCE, WE ARE GETTING THE PREVIUOSLY STORED DATA IN THESE FORMS.
  profile_form = userProfileForm(instance=profile)
  vendor_form = vendorRegistrationForm(instance=vendor)
  context = {
    'profile_form':profile_form,
    'vendor_form':vendor_form,
  }
  return render(request, 'vendor/vProfile.html', context)

