from django.shortcuts import render, get_object_or_404, redirect
from .forms import vendorRegistrationForm
from accounts.forms import userProfileForm
from accounts.models import UserProfile
from .models import Vendor

from django.contrib import messages
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor

from menu.models import Category, foodItem
from menu.forms import categoryForm, foodItemForm


#HELPER FUNCTION TO GET THE VENDOR.
def get_vendor(request):
  vendor = Vendor.objects.get(user=request.user)
  return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vProfile(request):
  profile = get_object_or_404(UserProfile, user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)

  if request.method == 'POST':
  #WE ARE WRITING 'request.FILES' TO GET THE PICTURES.
    profile_form = userProfileForm(request.POST, request.FILES, instance=profile)
    vendor_form = vendorRegistrationForm(request.POST, request.FILES, instance=vendor)

    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      messages.success(request,'Restaurant profile updated!')
      return redirect('vProfile')
    else:
      print(profile_form.errors)
      print(vendor_form.errors)
  else:
    #BY PASSING THE INSTANCE, WE ARE GETTING THE PREVIUOSLY STORED DATA IN THESE FORMS FIELDS.
    profile_form = userProfileForm(instance=profile)
    vendor_form = vendorRegistrationForm(instance=vendor)
      


  context = {
    'profile_form':profile_form,
    'vendor_form':vendor_form,
    'profile':profile,
    'vendor':vendor

  }
  return render(request, 'vendor/vProfile.html', context)

#FROM HERE ONWARDS, I AM WRITING THE CODE FOR MENU 

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
  vendor = get_vendor(request) #'GET' IS USED FOR ONLY 1 QUERY OBJECT
  categories = Category.objects.filter(vendor=vendor).order_by('created_at') #'filter' IS USED FOR multiple QUERY 
  context = {
    'categories':categories,
  }
  return render(request, 'vendor/menu_builder.html',context )


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
  vendor = get_vendor(request)
  category = get_object_or_404(Category, pk=pk)
  fooditems = foodItem.objects.filter(vendor=vendor, category=category)
  context = {
    'fooditems':fooditems,
    'category':category,
  }
  return render(request,'vendor/fooditems_by_category.html', context)


#CATEGORY CRUD VIEWS.

def add_category(request):
    if request.method == 'POST':
      form = categoryForm(request.POST)
      if form.is_valid():
        category_name = form.cleaned_data['category_name']
        category = form.save(commit=False)
        category.vendor = get_vendor(request)
        category.slug = slugify(category_name)
        form.save()
        messages.success(request, "Category add successfully")
        return redirect('menu_builder')
      else:
        print(form.errors)
    else: 
      form = categoryForm()
    context = {
      'form':form,

    }
    return render(request, 'vendor/add_category.html',context)
  
def edit_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
      form = categoryForm(request.POST, instance=category)
      if form.is_valid():
        category_name = form.cleaned_data['category_name']
        category = form.save(commit=False)
        category.vendor = get_vendor(request)
        category.slug = slugify(category_name)
        form.save()
        messages.success(request, "Category updated successfully")
        return redirect('menu_builder')
      else:
        print(form.errors)
    else: 
      form = categoryForm(instance=category)
    context = {
      'form':form,
      'category':category,

    }
    return render(request, 'vendor/edit_category.html',context)
  
def delete_category(request, pk=None):
  category = get_object_or_404(Category, pk=pk)
  category.delete()
  messages.success(request, "Category deleted successfully")
  return redirect('menu_builder')
  
#FOODITEMS CRUD VIEW

def add_food(request):
  if request.method == 'POST':
      form = foodItemForm(request.POST, request.FILES)
      if form.is_valid():
        foodtitle = form.cleaned_data['food_title']
        food = form.save(commit=False)
        food.vendor = get_vendor(request)
        food.slug = slugify(foodtitle)
        form.save()
        messages.success(request, "Food add successfully")
        return redirect('fooditems_by_category', food.category.id)
      else:
        print(form.errors)
  else:
    form = foodItemForm() 
  context = {
    'form':form,
  }
  return render(request, 'vendor/add_food.html', context)

