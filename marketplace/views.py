from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse
from vendor.models import Vendor
from menu.models import Category, foodItem
from django.db.models import Prefetch
from django.conf import settings
from marketplace.models import Cart
from marketplace.context_processor import get_cart_count

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

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems', 
            queryset=foodItem.objects.filter(is_availabe=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # CHECK IF THE FOODITEM EXISITS.
            try:

                fooditem = foodItem.objects.get(id=food_id)
                # CHECK IF USER HAS ALREADY ADDED THAT FOOD TO THE CART.
                try:

                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase the cart quantity
                    chkcart.quantity += 1
                    chkcart.save()
                    return JsonResponse({'status':'success', 'message':'Increased the Cart quantity.', 'cart_counter':get_cart_count(request), 'qty':chkcart.quantity})

                except:
                    chkcart = Cart.objects.create(user = request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'success', 'message':'Added the food to the Cart.' ,'cart_counter':get_cart_count(request), 'qty':chkcart.quantity})

            except:
                return JsonResponse({'status':'failed', 'message':'This food does not exists.'})
            
        else:
            return JsonResponse({'status':'failed', 'message':'Invalid Request'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please Login to continue'})
    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:

                fooditem = foodItem.objects.get(id=food_id)
                try:

                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkcart.quantity > 1:

                        chkcart.quantity -= 1
                        chkcart.save()
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0
                    return JsonResponse({'status':'success', 'message':'Decreased the Cart quantity.', 'cart_counter':get_cart_count(request), 'qty':chkcart.quantity})
                except:  

                    return JsonResponse({'status':'failed', 'message':'You donot have this item in your cart.','cart_counter':get_cart_count(request), 'qty':chkcart.quantity})

            except:
                return JsonResponse({'status':'failed', 'message':'This food does not exists.'})
            
        else:
            return JsonResponse({'status':'failed', 'message':'Invalid Request'})
        
    else:
        return JsonResponse({'status':'login_required', 'message':'Please Login to continue'})

def cart(request):
    cart_items = Cart.objects.filter(user=request.user) #request.user to get the loggedIn user.
    context = {
        'cart_items':cart_items,

    }
    return render(request, 'marketplace/cart.html', context)