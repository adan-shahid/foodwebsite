from vendor.models import Vendor

def get_vendor(request):
  try:
    vendor = Vendor.objects.get(user=request.user) #THIS IS THAT CASE WHEN YOU'RE LOGGED IN.
  except:
    vendor = None
  return dict(vendor=vendor)
