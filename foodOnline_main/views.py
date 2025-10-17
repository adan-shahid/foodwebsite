from django.shortcuts import HttpResponse, render
from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved = True, user__is_active =True)[:8] #WE ARE GETTING 'is_active' status from User model.
    context = {
        'vendors':vendors,
    }
    return render(request, 'home.html', context)