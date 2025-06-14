from django.shortcuts import render, HttpResponse, redirect
from .forms import userRegistrationForm
from .models import User, UserProfile
from django.contrib import messages

from vendor.forms import vendorRegistrationForm

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        print(request.POST) #request.POST, WE ARE GETTING THE DATA HERE.
        form = userRegistrationForm(request.POST)
        if form.is_valid():

            # CREATE THE USER, USING THE FORM

            # password = form.cleaned_data['password']
            # user = form.save(commit=False) #FORM IS READY TO BE SAVED, BUT NOT YET SAVED. BCZ OF COMMIT
            # user.role = User.CUSTOMER
            # user.set_password(password)
            # user.save()

            # CREATE THE USER, USING create_user METHOD.
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            #print("User is created")

            messages.success(request, "Your account has been registered successfully!")
            return redirect('registerUser')
        else:
            print("Invalid form")
            print(form.errors)
    else:
        form = userRegistrationForm()
    
    
    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.method == 'POST':
        #store the data and create a user
        form = userRegistrationForm(request.POST)
        v_form = vendorRegistrationForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "You account has been registered successfully! Please wait for admin approval.")

        else:
            print("Invalid Form")
            print(form.errors)
    else:
    
        form = userRegistrationForm()
        v_form = vendorRegistrationForm()

    context = {
        'form':form,
        'v_form':v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)
