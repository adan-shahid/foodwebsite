from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import Category

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

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor) #BCZ WE ARE ONLY GETTING THE CATEGORIES OF THAT SPECIFIC VENDOR.

    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

