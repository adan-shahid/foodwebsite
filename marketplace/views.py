from django.shortcuts import render
from vendor.models import Vendor

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved = True, user__is_active =True)
    vendor_count = vendors.count() #TO COUNT THE NUMBER OF VENDORS.
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,

    }
#NOW ON THE listings.html, we have the access to vendors and vendor_count.
    return render(request, 'marketplace/listings.html',context)

